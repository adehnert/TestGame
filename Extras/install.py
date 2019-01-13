#!/usr/bin/python

"""
Install script for GameTeX addons

Also various other bonus features that care about the list of files being
installed.
"""

from __future__ import print_function, unicode_literals

# pylint: disable=locally-disabled
#
# Passes: pylint3 vgametex.py && echo flake8 && python3 -mflake8 vgametex.py

import argparse
import os.path
import shutil
import subprocess
import sys
import tarfile
import tempfile

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)  # pylint: disable=invalid-name


class F:  # pylint: disable=invalid-name
    """
    Represents a file to distribute
    """

    def __init__(self, repo, site="",  # pylint: disable=too-many-arguments
                 exclude=None, install=True, git_rel=False):
        """
        Initialize object
        """
        self.repo = repo
        self.site = site or os.path.basename(repo)
        self.exclude = exclude
        self.install = install
        self.git_rel = git_rel

    def fixup_tar_install(self, git_parent):
        """
        Move any installed file that is installed to the wrong place by tar
        """
        if self.git_rel and git_parent:
            # We want to move the whole subtree (eg, .circleci), not just the
            # single file (.circleci/config.yml), to be a direct sibling of
            # .git.  If we ever get multiple files in a git-relative directory,
            # or become concerned one of the directories might already exist
            # and have content we shouldn't move, we'll need to fix this.
            dir_name = self.repo.split('/')[0]
            shutil.move(dir_name, '..')

    def add_to_tar_install(self, tar):
        """
        Add file to installer tarfile
        """
        if self.install:
            tar.add(self.repo)

    def copy_to_site(self, site_dir):
        """
        Copy file from repo to site directory
        """
        site_path = os.path.join(site_dir, self.site)
        if self.exclude:
            cmd = ['grep', '-v', self.exclude, self.repo]
            log.info("Running %s > %s", cmd, site_path)
            with open(site_path, 'w') as fp:
                subprocess.check_call(cmd, stdout=fp)
        else:
            log.info("Copying %s -> %s", self.repo, site_path)
            shutil.copy(self.repo, site_path)


FILES = [
    F("Extras/gitlab-docs-index.html", "index.html", install=False),
    F("artifacts/greensheets/guildcamp-git.pdf", install=False),
    F("Extras/vgametex.py"),
    F("Extras/install.py"),

    # CI
    F("artifacts/greensheets/ci.pdf", install=False),
    F("Greensheets/Makefile", "Makefile-green"),
    F("Production/Makefile", "Makefile-prod"),
    F(".circleci/config.yml", "circleci-config.yml", exclude="mail_merge.py",
      git_rel=True),
    F(".gitlab-ci.yml", "gitlab-ci.yml", exclude="copy_to_site",
      git_rel=True),

    # Mail merge
    F("Extras/mail_merge.py"),
    F("Extras/README-mail-merge"),
]

TARFILE_NAME = 'addons.tar'


def parse_args():
    """
    Parse arguments
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='mode')

    install_parser = subparsers.add_parser("install")
    install_parser.add_argument("--webbase",
                                default="https://adehnert.gitlab.io/TestGame/")

    copy_to_site_parser = subparsers.add_parser("copy_to_site")
    copy_to_site_parser.add_argument("dest")

    # argparse doesn't seem to support a default subparser. This hack will
    # use install if none is specified, with the default values.
    argv = sys.argv[1:]
    if not argv:
        argv += ['install']

    args = parser.parse_args(argv)
    return args


def fetch(url, dest):
    """
    Fetch a file from <url> to <dest>
    """
    log.info("Downloading %s to %s", url, dest)
    subprocess.check_call(["curl", "-o", dest, url])


def install_from_tar(files, webbase):
    """
    Download and install addons using tar file
    """
    if not os.path.isdir('LaTeX'):
        sys.exit("Installer must be called from the top of your GameTeX "
                 "install (the directory containing LaTeX/, Production/, and "
                 "so forth")

    prefix = 'gametex-addons-'
    with tempfile.NamedTemporaryFile(prefix=prefix, suffix='.tar') as tar:
        fetch(webbase+'/'+TARFILE_NAME, tar.name)
        subprocess.check_call(['tar', '-xvf', tar.name])

    if os.path.isdir('.git'):
        git_parent = False
    elif os.path.isdir('../.git'):
        git_parent = True
    else:
        log.warning("Neither current nor parent directory contains a .git "
                    "directory. Not bothering to move .git-relative files, "
                    "such as CI configuration.")
        git_parent = None

    for file_obj in files:
        file_obj.fixup_tar_install(git_parent=git_parent)


def create_tar(files, tarname):
    """
    Create tarfile with the addon files
    """
    with tarfile.open(tarname, mode='w') as tar:
        for file_obj in files:
            file_obj.add_to_tar_install(tar)


def copy_to_site(files, site_dir):
    """
    Copy files from repo to site directory
    """
    shutil.copy(os.path.join(site_dir, "index.html"),
                os.path.join(site_dir, "index-default.html"))

    for file_obj in files:
        file_obj.copy_to_site(site_dir)
    create_tar(files, os.path.join(site_dir, TARFILE_NAME))


def main():
    """
    Main function
    """
    args = parse_args()

    if args.mode == 'install':
        install_from_tar(FILES, args.webbase)
    elif args.mode == 'copy_to_site':
        copy_to_site(FILES, args.dest)
    else:
        raise ValueError("unknown operation")


if __name__ == "__main__":
    main()

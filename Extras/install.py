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

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)  # pylint: disable=invalid-name


class F:  # pylint: disable=invalid-name,too-few-public-methods
    """
    Represents a file to distribute
    """

    def __init__(self, repo, site="", exclude=None, git_rel=False):
        """
        Initialize object
        """
        self.repo = repo
        self.site = site or os.path.basename(repo)
        self.exclude = exclude
        self.git_rel = git_rel

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
    F("Extras/gitlab-docs-index.html", "index.html"),
    F("artifacts/greensheets/guildcamp-git.pdf"),
    F("Extras/vgametex.py"),

    # CI
    F("artifacts/greensheets/ci.pdf"),
    F("Greensheets/Makefile", "Makefile-green"),
    F("Production/Makefile", "Makefile-prod"),
    F(".circleci/config.yml", "circleci-config.yml", exclude="mail_merge.py"),
    F(".gitlab-ci.yml", "gitlab-ci.yml", exclude="copy_to_site"),

    # Mail merge
    F("Extras/mail_merge.py"),
    F("Extras/README-mail-merge"),
]


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

    args = parser.parse_args()
    return args


def copy_to_site(files, site_dir):
    """
    Copy files from repo to site directory
    """
    shutil.copy(os.path.join(site_dir, "index.html"),
                os.path.join(site_dir, "index-default.html"))

    for file_obj in files:
        file_obj.copy_to_site(site_dir)


def main():
    """
    Main function
    """
    args = parse_args()

    if args.mode == 'install':
        raise ValueError("not implemented")
    elif args.mode == 'copy_to_site':
        copy_to_site(FILES, args.dest)
    else:
        raise ValueError("unknown operation")


if __name__ == "__main__":
    main()

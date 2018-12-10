#!/usr/bin/env python3

"""
virtualenv-style support for GameTeX, without needing to manipulate the
environment manually or in dotfiles. Intended to be run as a command; see
--help for details.
"""

# pylint: disable=locally-disabled,invalid-name,missing-docstring
#
# Passes: pylint3 vgametex.py && echo flake8 && python3 -mflake8 vgametex.py

import argparse
import logging
import os.path
import re
import subprocess
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def find_path():
    this = os.path.realpath(sys.argv[0])
    root = os.path.dirname(os.path.dirname(this))
    return root


def find_game_file(path, regexp):
    try:
        with open(os.path.join(*path), 'rt') as fp:
            file_re = re.compile(regexp)
            for line in fp:
                match = file_re.match(line.strip())
                if match:
                    logger.info("Found GameTeX class name in %s", path)
                    return match.group('cls')
    except FileNotFoundError:
        pass  # we expect this may not exist


def find_game(parser, root):
    ret = find_game_file((root, 'Production', 'listchar-PRINT.tex'),
                         r'^\\documentclass\[listchar\]\{(?P<cls>[A-Za-z]+)\}')
    if ret:
        return ret
    ret = find_game_file((root, 'Extras', 'gametex.pl'),
                         r'^\$gameclass = "(?P<cls>[A-Za-z]+)";$')
    if ret:
        return ret
    parser.error("Could not detect game class, and none was specified")


desc = """

virtualenv-style support for GameTeX, without needing to manipulate the
environment manually or in dotfiles.


Two modes are supported:

In eval mode, run something like "eval `%(prog)s -m eval`" to update the
variables in your current environment.

In prefix mode, you can run a specific command within an appropriate
environment:
- If you pass no arguments, %(prog)s will start a shell, using $SHELL if set or
  /bin/sh otherwise.
- If you pass arguments, %(prog)s will treat those arguments as a command and
  run them. If you need to pass options to your command (for example, pdflatex
  -halt-on-error), you should place "--" before the command so %(prog)s doesn't
  try to interpret it as a vgametex.py argument

"""


def parse_args():
    rdhf = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(description=desc, formatter_class=rdhf)
    parser.add_argument('--mode', '-m', choices=('eval', 'prefix'),
                        default='prefix')
    parser.add_argument('--game', '-g', default=None,
                        help='GameTeX class name of the game')
    parser.add_argument('--path', '-p', default=None,
                        help="Path to game's root (the directory containing " +
                        " the LaTeX, Extras, Production, etc. directories)")
    parser.add_argument('argv', nargs='*',
                        help="Command to run with GameTeX setup")
    args = parser.parse_args()
    if args.mode == 'eval' and args.argv:
        parser.error("eval mode doesn't accept arguments")
    if args.path is None:
        args.path = find_path()
    if args.game is None:
        args.game = find_game(parser, args.path)
    logger.debug(args)
    return args


def build_vars(args):
    cur_texinputs = os.environ.get("TEXINPUTS", "")
    envvars = [
        (args.game, args.path),
        ('TEXINPUTS', os.path.join(args.path, 'LaTeX') + ':' + cur_texinputs),
    ]
    if args.mode == 'eval':
        envvars.append(('PS1', '[%s] $PS1' % (args.game, )))
    logger.debug("Environment vars = %s", envvars)
    return envvars


def handle_eval(args):
    for k, v in build_vars(args):
        print('%(k)s="%(v)s"; export %(k)s;' % dict(k=k, v=v))


def handle_prefix(args):
    envvars = os.environ.copy()
    new_vars = build_vars(args)
    envvars.update(new_vars)
    if args.argv:
        cmd_args = args.argv
    else:
        cmd_args = [os.environ.get("SHELL", "/bin/sh")]
    popen = subprocess.Popen(args=cmd_args, env=envvars)
    popen.wait()
    if popen.returncode != 0:
        sys.exit(popen.returncode)


def run():
    args = parse_args()
    if args.mode == 'eval':
        handle_eval(args)
    elif args.mode == 'prefix':
        handle_prefix(args)


if __name__ == '__main__':
    run()

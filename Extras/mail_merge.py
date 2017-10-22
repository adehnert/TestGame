#!/usr/bin/env python3

# pylint: disable=locally-disabled,invalid-name,missing-docstring,fixme
#
# Passes: pylint3 vgametex.py && echo flake8 && python3 -mflake8 vgametex.py

import argparse
from email.parser import Parser
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import email.utils
import json
import logging
import os.path
import subprocess

import vgametex

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="mail merge emails to group")
    parser.add_argument('--game', '-g', default=None,
                        help='GameTeX class name of the game')
    parser.add_argument('--path', '-p', default=None,
                        help="Path to game's root (the directory containing " +
                        " the LaTeX, Extras, Production, etc. directories)")
    parser.add_argument('--class', dest='klass', default='PC',
                        help="required GameTeX class for inclusion")
    parser.add_argument('template', type=argparse.FileType('r'),
                        help="Template for email to send")
    parser.add_argument('--generate', action='store_true',
                        help="Generate character packet")
    parser.add_argument('--attach', action='store_true',
                        help="Attach character packet to emails")
    parser.add_argument('--force-rcpt', type=str,
                        help="Send only to designated address")
    parser.add_argument('--send', dest='dry_run', action='store_false')
    parser.add_argument('--limit', default=1000, type=int,
                        help="Stop after LIMIT players")
    args = parser.parse_args()
    if args.path is None:
        args.path = vgametex.find_path()
    if args.game is None:
        args.game = vgametex.find_game(parser, args.path)
    logger.debug(args)
    return args


name_cleanups = [
    (r'\unskip', ''),
    (r'\ignorespaces', ''),
    ('  ', ' '),
    ('  ', ' '),
]


def cleanup_name(name):
    for fr, to in name_cleanups:
        name = name.replace(fr, to)
    return name


def parse_recipients(msg, name):
    headers = msg.get_all(name, failobj=[])
    return email.utils.getaddresses(headers)


def send_mail_sendmail(rcpts, msg):
    args = ["/usr/sbin/sendmail", "-oi"] + rcpts
    p = subprocess.Popen(args, stdin=subprocess.PIPE)
    p.communicate(msg.as_bytes())


def send_mail(rcpts, msg):
    send_mail_sendmail(rcpts, msg)


class Character:
    def __init__(self, macro, basepath):
        self.macro = macro
        self.macro['plain_name'] = cleanup_name(macro['name'])
        self.basepath = basepath

    def get_packet_dir(self):
        return os.path.join(self.basepath, 'Production/packets')

    def generate_sheets(self):
        # TODO: for now, we always "pdfsheets" -- maybe we should support
        # just the charsheet, for example?
        # TODO: use vgametex (probably with some sort of vgametex-provided
        # check_call that does the environment?
        args = ['../../Extras/gametex.pl', 'pdfsheets', self.macro['macro']]
        subprocess.check_call(args, cwd=self.get_packet_dir())

    def attach_sheets(self, msg):
        basename = self.macro['macro']+'-sheets.pdf'
        filename = os.path.join(self.get_packet_dir(), basename)
        sheet = open(filename, 'rb').read()
        sheet_msg = MIMEApplication(sheet, _subtype='pdf', name='packet.pdf')
        msg.attach(sheet_msg)

    def merge_one(self, tmpl, dry_run, force_rcpt=None, attach=False):
        print(self.macro)

        formatted = tmpl.format(**self.macro)
        parser = Parser()
        parsed = parser.parsestr(formatted)
        assert not parsed.is_multipart()

        # Find recipients, and remove any BCC header
        parsed['To'] = self.macro['email']
        recipients = []
        recipients.extend(parse_recipients(parsed, 'To'))
        recipients.extend(parse_recipients(parsed, 'CC'))
        recipients.extend(parse_recipients(parsed, 'BCC'))
        del parsed['BCC']

        if attach:
            # Create a MIMEMultipart wrapper, and copy all the headers
            # up to it.
            msg = MIMEMultipart()
            msg.attach(parsed)
            for key, value in parsed.items():
                msg[key] = value

            # Actually attach the sheets
            self.attach_sheets(msg)
        else:
            # No attachments, so no MIMEMultipart wrapper
            msg = parsed

        mail_rcpts = [force_rcpt] if force_rcpt else [e for n, e in recipients]

        print(formatted)
        print("outer recipients=%s mail=%s" % (recipients, mail_rcpts))
        if dry_run:
            print(msg)
        else:
            send_mail(mail_rcpts, msg)


def merge_all(args):
    with open(os.path.join(args.path, 'Production/json-PRINT.json')) as fp:
        json_data = json.load(fp)
    tmpl = args.template.read()
    merged = []
    num_sent = 0
    for macro in json_data:
        if args.klass in macro['classes']:
            num_sent += 1
            if num_sent > args.limit:
                break

            char = Character(macro, args.path)
            if args.generate:
                char.generate_sheets()
            char.merge_one(tmpl, dry_run=args.dry_run,
                           force_rcpt=args.force_rcpt, attach=args.attach)
            stats = (macro['macro'], macro['email'], macro['plain_name'])
            merged.append(stats)

    print("Merged the following:")
    print("%20s\t%36s\t%s" % ("Macro", "Email", "Name"))
    for elem in merged:
        print("%20s\t%36s\t%s" % elem)


def run():
    args = parse_args()
    merge_all(args)


if __name__ == '__main__':
    run()

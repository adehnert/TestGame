Mail Merge
==========

`mail_merge.py` will allow you to send personalized emails to your players.

One major use case is to send out costuming hints (the most basic approach is
just to send the name and badge description, which works; if you add a
costuming hint and plumb it through the JSON output, that should work too).
Another is to email out packets, for games that aren't bothering with packet
handout.

The mail merge script depends on the JSON export:

    (cd Production && latex json-PRINT.tex)

To verify behavior, you'll probably want to start by doing a dry run with a
couple messages, and make sure the formatted text looks right:

    Extras/mail_merge.py --limit=2 Extras/emails/casting.txt

You can specify a new template or modify that one as desired. Formatting is
done using the Python format string mechanism
(https://docs.python.org/3/library/string.html#formatstrings), passing in the
`json-PRINT.json` dict for the macro. In short, you can include a field name
wrapped with {braces} to format that field. If you need to add a new attribute
to that dict, look for `\POSTSETS{Char}` in gametex.sty and the instances of
`\jsonkeyval` inside it, and add more similar ones.

If you want to mail out sheets, you should probably generate them and then
review them to make sure nothing undesirable is included:

    Extras/mail_merge.py --generate Extras/emails/casting.txt

If you want to review the email with the attachment in your email, you can
use `--force-rcpt` to make the emails go to you instead of the players:

    Extras/mail_merge.py --attach --force-rcpt=testing@mit.edu --limit=2 --send Extras/emails/casting.txt

Once you're happy, send out the emails:

    Extras/mail_merge.py --send Extras/emails/casting.txt

Or to attach the sheets you generated above:

    Extras/mail_merge.py --attach --send Extras/emails/casting.txt

I'd suggest generating sheets in a separate command from actually sending them out, but if you prefer to combine the steps you can:

    Extras/mail_merge.py --generate --attach --send Extras/emails/casting.txt

Note that if you don't generate all sheets (in particular, without passing
`--limit`) before or while running the script with `--attach`, it will error out.


Mail sending infrastructure
---------------------------

There's two basic ways to send mail using this script:
- `send_mail_sendmail` uses `/usr/sbin/sendmail` on the local machine. On an Athena machine, this should work fine.
- `send_mail_smtp` uses SMTP (the standard mail protocol on the internet) directly. Using `send_mail_smtp` alongside SendGrid (which requires additional setup, described below) is probably the simplest way for most people to use the script from a personal machine.

To select the mechanism, edit the script to change the order of the `send_mail = send_mail_...` lines to put the one you prefer last.

Setting up SendGrid
-------------------

1. Go to https://sendgrid.com/ and choose "start for free"
2. Once logged in, go to Settings -> Sender authentication -> Verify a single user, and verify the email address you will be sending from (e.g. game-gms@mit.edu)
3. Under API Keys, create a new API key. "Mail send" is probably the only privilege it needs (but I think I just use the defaults). Save the API key into a file
4. Make sure `send_mail` (in the script body) is using `send_mail_smtp`
5. When running the script, pass the path to the API key as the `--sendgrid-api` argument: for example, `--sendgrid-api=sendgrid.key`

SendGrid will show all the emails it has processed at https://app.sendgrid.com/email_activity?filters=%22%22&isAndOperator=true&page=1 (if you want to check that your players got the messages).

If you have bounces for some address (for example, you test with the game-gms@ list shortly after setting it up), SendGrid will remember that and not send future messages there -- you can check for this and delete these suppressions at https://app.sendgrid.com/suppressions/bounces

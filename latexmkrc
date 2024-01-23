# This file is intended to be used by Overleaf (overleaf.com). It sets
# up the Overleaf environment (using latexmk, a perl-based system that
# Overleaf happens to use) to match the necessary GameTeX environment.
#
# The game's environment variable is set up here.
# Extras/changeclass.pl can change its name here in addition to
# everywhere else. (It should match the name of the game's class, as
# per README)
#
# If you use latexmk locally, you can repurpose this file, by changing
# the path to this GameTeX installation.  If you are sharing a repo
# with someone who is using overleaf, you should probably not commit
# your local changes, in order to not break their overleaf usage.

$ENV{'game'}='/compile';
$ENV{'TEXINPUTS'}='.:/compile/LaTeX/:';

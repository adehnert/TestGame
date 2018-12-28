#!/bin/sh

set -eu

dest=$1

cp $dest/index.html $dest/index-default.html
cp Extras/gitlab-docs-index.html $dest/index.html
cp artifacts/greensheets/guildcamp-git.pdf $dest/
cp Extras/vgametex.py $dest/vgametex.py

# CI
cp artifacts/greensheets/ci.pdf $dest/
cp Greensheets/Makefile $dest/Makefile-green
cp Production/Makefile $dest/Makefile-prod
grep -v mail_merge.py .circleci/config.yml > $dest/circleci-config.yml
grep -v Extras/gitlab-copy-docs.sh .gitlab-ci.yml > $dest/gitlab-ci.yml

# Mail merge
cp Extras/mail_merge.py $dest/mail_merge.py
cp Extras/README-mail-merge $dest/README-mail-merge.txt

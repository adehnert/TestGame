#!/bin/sh

set -eu

dest=$1

cp $dest/index.html $dest/index-default.html
cp Extras/gitlab-docs-index.html $dest/index.html
cp artifacts/greensheets/guildcamp-git.pdf $dest/
cp artifacts/greensheets/ci.pdf $dest/
cp Extras/vgametex.py $dest/vgametex.py
cp Greensheets/Makefile $dest/Makefile-green
cp Production/Makefile $dest/Makefile-prod
grep -v mail_merge.py .circleci/config.yml > $dest/circleci-config.yml
grep -v Extras/gitlab-copy-docs.sh .gitlab-ci.yml > $dest/gitlab-ci.yml

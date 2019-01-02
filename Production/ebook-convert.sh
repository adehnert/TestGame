#!/bin/sh
set -euf

usage="$0 [-g game] file"

game="(unknown)"
while getopts "g:h" options; do
    case $options in
        g ) game=$OPTARG; shift;;
        h ) echo "$usage"; exit 0;;
        \? ) echo "$usage"; exit 1;;
        * ) echo "$usage"; exit 1;;
    esac
done
shift `expr $OPTIND - 1 || :`


file=$1

# TODO:
# Compile the document; also, parse off the .tex extension as needed
# Options:
# Accept -g for game name
# -l for sheet label? (default: filename)
# -t for ebook title? (default: "$game $label")
# -h for help

ebook-convert \
    "$file.html" "$file.epub" \
    --authors="$game GMs" --title="$game $file" --series="$game" --publisher="GameTeX" \
    --epub-inline-toc  --debug-pipeline="$file"

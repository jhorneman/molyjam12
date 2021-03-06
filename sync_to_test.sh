#!/bin/sh

cd ~/dev/molyjam/dev

# rsync parameters:
# a - archive mode - preserver timestamps etc.
# v - verbose
# r - recursive
# W - transfer the whole file
# --delete - delete destination files if they no longer exist at source
# --exclude-from - exclude a whole bunch of stuff listed in a text file

rsync -avW --exclude-from 'sync_exclude_list.txt' . ../test/
rsync -avrW --exclude-from 'sync_exclude_list.txt' ./static ../test/static
rsync -avrW --exclude-from 'sync_exclude_list.txt' ./templates ../test/templates

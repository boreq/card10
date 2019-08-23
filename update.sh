#!/bin/bash
set -e

mkdir -p mounted_badge
sudo mount /dev/sdb mounted_badge

sudo cp -r ~/card/state/apps/boreq/ ./mounted_badge/apps/ && sync
sudo cp -r ~/card/state/boreq.json ./mounted_badge && sync

sleep 2

sudo umount mounted_badge

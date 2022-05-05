#!/usr/bin/env bash
# https://github.com/Asocia/dotfiles/blob/master/.config/eww/bar/scripts/workspace
python3 ~/.config/eww/scripts/qtile.py $1
tail -F -n1 ~/.cache/workspaces | while read -r; do
    python3 ~/.config/eww/scripts/qtile.py $1
done
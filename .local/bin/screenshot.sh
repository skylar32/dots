#!/usr/bin/env bash

if [[ $1 == "-p" ]]; then
    filename=$(scrot -s -f -e "echo \$f")
else
    filename=$(scrot -e "echo \$f")
fi

killall xclip
xclip -selection clipboard -t image/png -i ${filename}
mv ${filename} ~/images/screenshots/${filename}
dunstify scrot "The screen has been captured, copied to clipboard, and saved to ${filename}."

exit 0

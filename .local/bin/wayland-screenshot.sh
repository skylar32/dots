#!/usr/bin/env bash

while getopts "fc" flag
do
    case "${flag}" in
        f) fullscreen=true ;;
        c) clipboard=true  ;;
    esac
done

cmd="grim"

if [[ -z ${fullscreen} ]]; then
    cmd="$cmd -g $(slurp -d)"
fi

if [[ -v clipboard ]]; then
    eval "$cmd - | wl-copy -t image/png"
    notify-send -a "grim" "Screenshot copied to clipboard."
else
    filename="$(date +%F_%H:%M:%S).png"
    eval "$cmd ~/images/screenshots/$filename"
    notify-send -a "grim" "Screenshot saved to $filename" 
fi

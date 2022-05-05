#!/usr/bin/env bash

active_output=$(pactl list sinks | awk '/Active Port/ && /analog/' | awk '{ print $3 }')
vol="$($(dirname "$0")/get-vol.sh)"
muted=$(pactl list sinks | awk '/Mute/ { print $2 }' | tail -1)

case $active_output in
    "analog-output-lineout")
        if [[ $muted == "yes" ]]; then
            echo "ﱝ"
        else
            case 1 in
                $(($vol >= 75))) echo "" ;;
                $(($vol >= 35))) echo "墳" ;;
                $(($vol >   0))) echo "奔" ;;
                            *)   echo "" ;;
            esac
        fi ;;
    "analog-output-headphones")
        if [[ $muted == "yes" ]]; then
            echo "ﳌ"
        else
            echo ""
        fi ;;
esac
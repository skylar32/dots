#!/usr/bin/env bash

sinkid=1
activeport=$(pactl list sinks | awk '/Active Port/ && /analog/' | awk '{ print $3 }')

if [ "$activeport" == "analog-output-headphones" ]; then
    pactl set-sink-port 0 analog-output-lineout
fi

if [ "$activeport" == "analog-output-lineout" ]; then
    pactl set-sink-port 0 analog-output-headphones
fi

exit 0

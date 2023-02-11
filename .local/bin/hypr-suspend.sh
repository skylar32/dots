#!/bin/bash 
swayidle -w \
    timeout 1200 "hyprctl dispatch dpms off" \
        resume "hyprctl dispatch dpms on"

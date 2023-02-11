#!/bin/bash 
swayidle -w \
    timeout 1200 "hyprctl dispatch dpms off" \
        resume "hyperctl dispatch dpms on"

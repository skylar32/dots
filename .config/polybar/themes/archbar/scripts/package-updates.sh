#!/bin/sh
# https://www.reddit.com/r/archlinux/comments/gwccb3/is_there_a_way_to_show_the_number_of_outdated/fsuquiy
format() {
    if [ "$1" -eq 0 ]; then
        echo '-'
    else
        echo "$1"
    fi
}

if ! updates_arch="$(checkupdates | wc -l)"; then
    updates_arch=0
fi

if ! updates_aur="$(yay -Qum 2>/dev/null | wc -l)"; then
    updates_aur=0
fi

updates="$((updates_arch + updates_aur))"

color=$(xrdb -query | grep *color3 | awk '{ print $2 }')
if [ "$updates" -gt 0 ]; then
    echo "%{A1:kitty -- yay -Syyu:}%{F${color}}%{F-} $(format $updates_arch) ($(format $updates_aur))  %{A}"
else
    echo
fi

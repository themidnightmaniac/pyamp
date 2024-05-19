#!/bin/bash

function notify {
    if [[ $(pstree | grep dunst) ]]; then
        killall dunst 2> /dev/null
        notify-send -u low "Now playing:" "$(mpc current)"
    else
        notify-send -u low "Now playing:" "$(mpc current)"
    fi
}

#   I use this to update my statusbar and notify me if the song changes.
case $1 in
    resumed)        pkill -RTMIN+1 dwmblocks;;
    paused)         pkill -RTMIN+1 dwmblocks;;
    stopped)        pkill -RTMIN+1 dwmblocks;;
    song_change)    pkill -RTMIN+1 dwmblocks && notify;;
esac

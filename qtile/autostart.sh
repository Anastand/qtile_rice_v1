#!/usr/bin/env bash 
# variety &

nm-applet & 

blueman-applet &

nitrogen --restore &

/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &

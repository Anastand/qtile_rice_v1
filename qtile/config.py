
import os
import re
import socket
import subprocess
from libqtile import bar, layout, widget, hook, qtile 
from typing import List
from libqtile.command import lazy
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Rule, KeyChord, hook
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
mod1 = "mod1"
mod2 = "control"
terminal = guess_terminal()


keys = [
         ##########################
         ## move focus  window   ##
         ##########################

    Key([mod1], "left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod1], "right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod1], "down", lazy.layout.down(), desc="Move focus down"),
    Key([mod1], "up", lazy.layout.up(), desc="Move focus up"),
   
         ######################
         ## Shuffle window   ##
         ######################
   
    Key([mod1, "shift"], "left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod1, "shift"], "right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod1, "shift"], "down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod1, "shift"], "up", lazy.layout.shuffle_up(), desc="Move window up"),

    # Toggle between different layouts as defined below

    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod2, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod2, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

         #####################
         ## Revise window   ##
         #####################

    Key([mod1, "control"], "left",
        lazy.layout.grow_left(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod1, "control"], "right",
        lazy.layout.grow_right(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
         #######################
         ### CUSTOM MAPPING  ###
         #######################   

    Key([mod], "Return", lazy.spawn("kitty"), desc="Launch terminal"),
    Key([mod,"shift"], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod2], "space", lazy.spawn("rofi -show drun"), desc="Spawn rofi dmenu "),
    




]



# █▀▀ █▀█ █▀█ █░█ █▀█ █▀
# █▄█ █▀▄ █▄█ █▄█ █▀▀ ▄█


groups = [Group(f"{i+1}") for i in range(6)]

for i in groups:
    keys.extend(
            [
                Key(
                    [mod],
                    i.name,
                    lazy.group[i.name].toscreen(),
                    desc="Switch to group {}".format(i.name),
                    ),
                Key(
                    [mod, "shift"],
                    i.name,
                    lazy.window.togroup(i.name, switch_group=True),
                    desc="Switch to & move focused window to group {}".format(i.name),
                    ),
                ]
            )


###𝙇𝙖𝙮𝙤𝙪𝙩###

layouts = [
    
    layout.MonadTall(),
    
    layout.Floating(),
]





widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(
                    padding = 0,
                    scale = 0.5,
                ),           
               widget.CurrentLayout(
                    font = "Noto Sans Bold",
                ),                     
                widget.GroupBox(),

                widget.Prompt(),
                widget.WindowName(),
                widget.Systray(),
                widget.TextBox(
                text="" ,
                padding=4,
                fontsize=14
                ),
                widget.Backlight(
    			backlight_name="intel_backlight",
				),
                widget.Clock(format= "%d-%m-%Y : %I:%M %p %A"),
            ],
            24,
           
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
         Match(wm_class='confirmreset'),  # gitk
         Match(wm_class='makebranch'),  # gitk
         Match(wm_class='maketag'),  # gitk
         Match(wm_class='ssh-askpass'),  # ssh-askpass
         Match(title='branchdialog'),  # gitk
         Match(title='pinentry'),  # GPG key password entry
         Match(wm_class='Arcolinux-welcome-app.py'),
         Match(wm_class='Arcolinux-calamares-tool.py'),
         Match(wm_class='confirm'),
         Match(wm_class='dialog'),
         Match(wm_class='download'),
         Match(wm_class='error'),
         Match(wm_class='file_progress'),
         Match(wm_class='notification'),
         Match(wm_class='splash'),
         Match(wm_class='toolbar'),
         Match(wm_class='Arandr'),
         Match(wm_class='feh'),
         Match(wm_class='Galculator'),
         Match(wm_class='archlinux-logout'),
         Match(wm_class='xfce4-terminal'),
 
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

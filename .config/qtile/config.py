import subprocess
import os

from libqtile import qtile, layout, hook, bar, widget
from libqtile.config import Key, Group, Match, Rule, Screen, Click, Drag
from libqtile.lazy import lazy
from libqtile.dgroups import simple_key_binder


mod = "mod4"
home = os.path.expanduser('~')

apps = {
    "terminal": "kitty",
    "browser": "firefox"
}

follow_mouse_focus = False
auto_minimize = False

##########################################################################################
# HELPER FUNCTIONS
##########################################################################################

@hook.subscribe.startup_once
def autostart():
    """https://github.com/qtile/qtile/issues/685"""
    processes = [
        f"{home}/.local/bin/set-wallpaper.sh",
        "picom --experimental-backends -b",
        f"{home}/.config/eww/launch.sh",
        f"rm {home}/.cache/workspaces"
    ]
    for process in processes:
        subprocess.Popen(process.split(' '))

@hook.subscribe.client_managed
@hook.subscribe.client_urgent_hint_changed
@hook.subscribe.client_killed
@hook.subscribe.setgroup
@hook.subscribe.group_window_add
def hook_response(*args, **kwargs):
    """https://github.com/Asocia/dotfiles/blob/master/.config/qtile/modules/hooks.py#L17"""
    with open(f"{home}/.cache/workspaces", 'a') as f:
        f.write('q\n')

##########################################################################################
# KEY BINDS
##########################################################################################

keys = [
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "e", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts")
]

# window management keybinds
keys.extend([
    # window operations
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen for focused window"),
    Key([mod], "period", lazy.window.toggle_floating(), desc="Toggle floating for focused window"),
    # move focus
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    # move windows
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),
    # toggle between split and unsplit sides of stack.
    # split = all windows displayed
    # unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    )
])

# media keys
keys.extend([
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q sset Master 5%+")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q sset Master 5%-")),
    Key([], "XF86AudioMute", lazy.spawn("amixer set Master toggle")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl --player=spotify,%any play-pause")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl --player=spotify,%any previous")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl --player=spotify,%any next"))
])

# application keybinds
keys.extend([
    Key([mod], "Return", lazy.spawn(apps['terminal']), desc="Launch terminal"),
    Key([mod], "F2", lazy.spawn(apps['browser']), desc="Launch internet browser"),
    Key([mod], "d", lazy.spawn("rofi -show drun"), "Open the application launcher"),
    Key([], "Print", lazy.spawn(f"{home}/.local/bin/screenshot.sh -p"), "Take a partial screenshot"), 
    Key([mod], "Print", lazy.spawn(f"{home}/.local/bin/screenshot.sh"), "Take a full-screen screenshot"), 
])

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

##########################################################################################
# GROUPS
##########################################################################################

groups = [
    Group(
        "www",
        label="",
        position=1,
        matches=[Match(wm_class="firefox")]
    ),
    Group(
        "spotify",
        label="阮",
        position=2,
        matches=[Match(wm_class="Spotify")],
        spawn="spotify"
    ),
    Group(
        "discord",
        label="ﭮ",
        position=3,
        matches=[Match(wm_class="Discord")],
        spawn="discord"
    ),
    Group(
        "steam",
        label="",
        position=4,
        matches=[Match(wm_class="Steam")],
        layout_opts={
            "ratio": 0.2,
            "master_match": Match(title=['Friends'])
        },
        spawn="steam-native"
    ),
    Group(
        "dev",
        label="",
        position=5,
        matches=[Match(wm_class="Code")]
    )
]
groups.extend([Group(str(i % 10), position=i) for i in range(len(groups) + 1, 11)])

dgroups_app_rules = [
    Rule(
        Match(wm_class=[
            "1Password"
        ]),
        float=True,
        intrusive=True
    )
]

dgroups_key_binder = simple_key_binder(mod)

##########################################################################################
class SpiralLeft(layout.Spiral):
    def __init__(self, **config):
        super().__init__(
            margin=15,
            border_width=0,
            new_client_position="bottom",
            ratio=0.5,
            main_pane="top"
        )

layouts = [
    layout.Spiral(
        margin=15,
        border_width=0,
        new_client_position="bottom",
        ratio=0.5
    ),
    SpiralLeft(),
    layout.Zoomy(
        margin=15,
        columnwidth=400
    ),
    layout.Max()
]

screens = [
    Screen(
        top=bar.Gap(70)
    ),
    Screen()
]

def get_layout_index(lo):
    return [l.name for l in layouts].index(lo.name)

@hook.subscribe.layout_change
def layout_changed(new_layout, group):
    if get_layout_index(new_layout) % 2 != group.screen.index:
        group.use_next_layout()

@hook.subscribe.startup
def startup():
    screens[1].group.use_layout(1)

#!/usr/bin/python
from config import *

import pickle
import time
import os
import sys
import subprocess



def run(command: str, default = None) -> str | None:
    result = subprocess.run(command.split(), capture_output=True)
    if result.returncode:
        return default
    else:
        return result.stdout.decode().strip()


def fetch_cached_notification() -> dict:
    with open(NOTIF_PATH, "rb") as in_file:
        return pickle.load(in_file)


def get_now_playing() -> str:
    if run("playerctl --player=spotify status") is None:
        return ""
    else:
        song, artist, album = (
            run(f"playerctl --player=spotify metadata {item}") for item in ("title", "artist", "album")
        )
        return f"{artist} - {song} - {album}"


def get_current_notification() -> dict:
    notification = fetch_cached_notification()
    if notification.get("app_name") != "Spotify" and time.time() - notification.get("timestamp", 0) < NOTIF_PERSIST_SECS:
        return f"[{notification['app_name']}] {notification['summary']}"
    else:
        return get_now_playing()



if __name__ == "__main__":
    print(get_current_notification())
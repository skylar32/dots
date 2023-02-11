#!/usr/bin/python
from config import NOTIF_PATH, NOTIF_PERSIST_SECS, WAYBAR_SIGNAL

import pickle
import os
import time
from pathlib import Path


def cache_notification():
    notification = {
        key.lower().removeprefix("dunst_"): value for key, value in os.environ.items() if key.startswith("DUNST_")
    }
    notification["timestamp"] = time.time()
    with open(NOTIF_PATH, "wb") as out_file:
        pickle.dump(notification, out_file)


def signal_waybar():
    r = os.system(f"pkill -SIGRTMIN+{WAYBAR_SIGNAL} waybar")


if __name__ == "__main__":
    cache_notification()
    signal_waybar()
    time.sleep(NOTIF_PERSIST_SECS)
    signal_waybar()

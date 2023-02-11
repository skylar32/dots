#!/usr/bin/env python3.10
import ujson
from libqtile.command.client import CommandClient
from sys import argv


screen = int(argv[1])
q = CommandClient()

groups_dict = []

for group_name, group in q.call('groups').items():
    groups_dict.append({
        "icon": group['label'],
        "classes": ' '.join(
            item for item in (
                'workspace',
                group_name,
                'active' if group['screen'] is not None else None,
                'current' if group['screen'] == screen else None,
                'icon' if not group['label'].isnumeric() else None,
                'occupied' if group['windows'] else None
            ) if item is not None
        ),
        "onclick": f"qtile cmd-obj -o group {group_name} -f toscreen"
    })

print(ujson.dumps(groups_dict))

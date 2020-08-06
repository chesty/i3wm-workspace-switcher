#!/bin/python3

'''
/tmp/wslock is a text file with a whitespace list of workspace names
            that are permitted to change to
            eg: `echo 3 4 5 work > /tmp/wslock`
            will allow you to change to the workspaces named 3 4 5 and work
            `> /tmp/wslock` will lock to current workspace
            `rm /tmp/wslock` will allow changing to any workspace


            i3 config
            bindsym $mod+Mod1+Left exec bin/workspace.py workspace prev
            bindsym $mod+Mod1+Right exec bin/workspace.py workspace next
            ...
            bindsym $mod+1 exec bin/workspace.py workspace $ws1
            bindsym $mod+2 exec bin/workspace.py workspace $ws2
            ...

'''

import json
import sys
import subprocess


def new_workspace(focused, workspaces, args):
    '''
        get the index of the workspace we want to switch to
    '''
    new_ws = None
    if args[1] == 'prev':
        new_ws = focused - 1
        if new_ws < 0:
            new_ws = len(workspaces) - 1
    elif args[1] == 'next':
        new_ws = focused + 1
        if new_ws > len(workspaces) - 1:
            new_ws = 0
    else:
        for i, workspace in enumerate(workspaces):
            if workspace['name'] == args[1]:
                new_ws = i
                break
    return new_ws


def workspace_focus(workspaces):
    for i, workspace in enumerate(workspaces):
        if workspace['focused']:
            return i


def workspace(args):
    # if /tmp/wslock doesn't exist or there are any errors reading it
    # allow workspace changes
    try:
        wslockfd = open('/tmp/wslock')
        wslock = wslockfd.read()
        allowed_ws = wslock.split()
    except Exception:
        subprocess.run(["i3-msg", *args])
        sys.exit(0)

    # /tmp/wslock exists but it's empty, don't allow ws changes
    if not len(allowed_ws):
        sys.exit(0)

    # read in the workspace data structure, any failures allow switching
    try:
        i3msg = subprocess.run(["i3-msg", "-t", "get_workspaces"],
                               capture_output=True)
        workspaces = json.loads(i3msg.stdout)
    except Exception:
        subprocess.run(["i3-msg", *args])
        sys.exit(0)

    # get the index of the workspaces list that has focus
    focused = workspace_focus(workspaces)
    if focused is None:
        sys.exit(0)

    # get the index of the workspace we want to switch to
    new_ws = new_workspace(focused, workspaces, args)

    # switch to non existing workspace if it's in the allowed list
    if new_ws is None:
        if args[1] in allowed_ws:
            subprocess.run(["i3-msg", *args])
        sys.exit(0)

    # switch to the existing workspace if it's in the allowed list
    if workspaces[new_ws]['name'] in allowed_ws:
        subprocess.run(["i3-msg", "workspace", workspaces[new_ws]['name']])
        sys.exit(0)

    # if next or prev, cycle through the workspaces looking for the first match
    # then switch to it
    if args[1] == 'next' or args[1] == 'prev':
        for _ in workspaces:
            new_ws = new_workspace(new_ws, workspaces, args)
            # switch to the new workspace if it's in the allowed list
            if workspaces[new_ws]['name'] in allowed_ws:
                subprocess.run(["i3-msg", "workspace",
                                workspaces[new_ws]['name']])
                sys.exit(0)

    sys.exit(0)


if len(sys.argv) == 1:
    sys.exit(0)

if sys.argv[1] == "workspace":
    workspace(sys.argv[1:])

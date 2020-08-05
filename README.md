# i3wm-workspace-switcher
A quickly written and barely tested productivity tool for i3wm to stop you temporarily from switching to certain workspaces


In your i3 config where workspace switching is configured add "exec workspace.py" before the workspace keyword. eg:

```
bindsym $mod+Mod1+Left exec bin/workspace.py workspace prev         
bindsym $mod+Mod1+Right exec bin/workspace.py workspace next        
...                                                                 
bindsym $mod+1 exec bin/workspace.py workspace $ws1                 
bindsym $mod+2 exec bin/workspace.py workspace $ws2                 
...       
```

Then to control which workspaces you allow yourself to switch to, echo them to `/tmp/wslock`

`/tmp/wslock` is a text file with a whitespace separated list of workspace names you allow youself to switch to.
If you try to switch to a workspace not allowed it will either skip over it if you use "next" or "prev", or it won't change to it if you try to switch directly to it.

eg: `echo 3 5 work > /tmp/wslock`                                 
will allow you to change to the workspaces named 3 5 and work     
"next" and "prev" will cycle through in the specified direction and skip workspaces not in the allowed list.


`> /tmp/wslock` will lock to current workspace
`rm /tmp/wslock` will allow changing to any workspace


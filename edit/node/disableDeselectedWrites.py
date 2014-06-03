import nuke

# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"

__menus__ = {
  'Tools/Edit/Node/Disable Deselected Write Nodes': {
    'cmd': 'disable_deselected_writes()',
    'hotkey': '',
    'icon': ''
  }
}


def disable_deselected_writes():
    nodes = nuke.selectedNodes()
    if len(nodes) < 1:
        print('No nodes selected')
    else :
        all_write_nodes = nuke.allNodes('Write')
        for node in all_write_nodes:
            if node not in nodes:
                node['disable'].setValue(True)
        
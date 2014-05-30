import nuke

# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"

__menus__ = {
  'Tools/Edit/Paste To Selected': {
    'cmd': 'paste_to_selected()',
    'hotkey': '#+v',
    'icon': ''
  }
}


def toggle_selection(node):
    node['selected'].setValue(not node['selected'].value())
    
def paste_to_selected():
    if not nuke.selectedNodes():
        nuke.nodePaste('%clipboard%')
        return
    selection = nuke.selectedNodes()
    for node in selection:
        toggle_selection(node)
    for node in selection:
        node['selected'].setValue(True)
        nuke.nodePaste('%clipboard%')
        node['selected'].setValue(False)
    for node in selection:
        toggle_selection(node)
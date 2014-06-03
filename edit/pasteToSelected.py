import nuke

# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"

__menus__ = {
  'Tools/Edit/Paste To Selected': {
    'cmd': 'pasteToSelected()',
    'hotkey': '#+v',
    'icon': ''
  }
}


def toggleSelection(node):
    node['selected'].setValue(not node['selected'].value())
    
def pasteToSelected():
    if not nuke.selectedNodes():
        nuke.nodePaste('%clipboard%')
        return
    selection = nuke.selectedNodes()
    for node in selection:
        toggleSelection(node)
    for node in selection:
        node['selected'].setValue(True)
        nuke.nodePaste('%clipboard%')
        node['selected'].setValue(False)
    for node in selection:
        toggleSelection(node)
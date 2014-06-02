import os, platform
import nuke
# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"


__menus__ = {
  'Tools/Edit/Node/Toggle Postage Stamps': {
    'cmd': 'toggle_postage_stamp()',
    'hotkey': '',
    'icon': ''
  }
}


def toggle_postage_stamp(nodes=[], classes=['Read', 'Write']):
  if not nodes:
    nodes = nuke.selectedNodes()
  if not nodes:
    nodes = nuke.allNodes()
  if not nodes:
    return
  for node in nodes:
    if node.Class() in classes:
      cur_value = node['postage_stamp'].value()
      node['postage_stamp'].setValue(not cur_value)
  return

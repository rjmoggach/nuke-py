import nuke

# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"

__menus__ = {
  'Tools/3D/Toggle Display Wireframe or Textured': {
    'cmd': 'toggle_wireframe()',
    'hotkey': '',
    'icon': 'toggle_wireframe.png'
  }
}


toggle_wireframe(nodes=[]):
  if not nodes:
    nodes=nuke.selectedNodes()
  if not nodes:
    nodes=nuke.allNodes()
  if nodes:
    for node in nodes:
      if node.Class() == 'ReadGeo2':
        if node['display'].value() == 'wireframe':
          node['display'].setValue('textured')
        if node['display'].value() == 'textured':
          node['display'].setValue('wireframe')
  else:
    return

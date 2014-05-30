import nuke

# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"

__menus__ = {
  'Tools/Nodes/Align/Mirror Nodes X':  {
    'cmd': 'mirror_nodes(nuke.selectedNodes())',
    'hotkey': '#+x',
    'icon': ''
  },
  'Tools/Nodes/Align/Mirror Nodes Y':  {
    'cmd': 'mirror_nodes(nuke.selectedNodes(), "y")',
    'hotkey': '#+y',
    'icon': ''
  }
}

def mirror_nodes( nodes, direction = 'x' ):
  '''
  Mirror nodes either horizontally or vertically.
  '''
  if len( nodes ) < 2:
    return
  if direction.lower() not in ('x', 'y'):
    raise ValueError, 'direction argument must be x or y'
  if direction.lower() == 'x':
    positions = [ float(node.xpos() + node.screenWidth() / 2) for node in nodes ]
  else:
    positions = [ float(node.ypos() + node.screenHeight() / 2) for node in nodes ]
  axis = sum( positions ) / len( positions )
  for node in nodes:
    if direction.lower() == 'x':
      node.setXpos( int(node.xpos() - 2 * (node.xpos() + node.screenWidth() / 2 - axis) ) )
    else:
      node.setYpos( int(node.ypos() - 2 * (node.ypos() + node.screenHeight() / 2 - axis) ) )
  return axis



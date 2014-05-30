import nuke

# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"

__menus__ = {
  'Tools/Edit/Node/Align/Align Nodes X':  {
    'cmd': 'align_nodes(nuke.selectedNodes())',
    'hotkey': '#x',
    'icon': ''
  },
  'Tools/Edit/Node/Align/Align Nodes Y':  {
    'cmd': 'align_nodes(nuke.selectedNodes(), "y")',
    'hotkey': '#y',
    'icon': ''
  }
}


def align_nodes( nodes, direction = 'x' ):
  '''
  Align nodes either horizontally or vertically.
  '''
  if len( nodes ) < 2:
    return
  if direction.lower() not in ('x', 'y'):
    raise ValueError, 'direction argument must be x or y'

  positions = [ float( n[ direction.lower()+'pos' ].value() ) for n in nodes]
  avg_position = sum( positions ) / len( positions )
  for n in nodes:
    if direction == 'x':
      for n in nodes:
        if not n.Class() == "Dot":
          n.setXpos( int(avg_position) )
        else:
          n.setXpos( int(avg_position) + 40)
    else:
      for n in nodes:
          n.setYpos( int(avg_position) )

  return avg_position



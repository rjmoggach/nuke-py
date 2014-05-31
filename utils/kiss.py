import nuke

# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"


__menus__ = {
  'Tools/Edit/Toggle Node Kiss': {
    'cmd': 'NodeKisser().toggle()',
    'hotkey': '#l',
    'icon': 'kiss.png'
  }
}

class NodeKisser(object):
  """
  kiss function for nodes in nuke inspired by the kiss function in Flame.
  Press alt-l to enable the kiss functionality. Drag a node next to another node and the selected
  node input will be connected to the nearby node output
  """

  def __init__(self, tolerance=30, enabled=False):
    self.tolerance = tolerance
    self.enabled=enabled
    self.nodes=[]

  def toggle(self):
    """
  	enable/disable kiss functionality
  	"""
    for node in nuke.allNodes():
      self.nodes.append({
        'name': node.name(),
        'xpos': node.xpos(),
        'ypos': node.ypos(),
        'screenWidth': node.screenWidth(),
        'screenHeight': node.screenHeight()
      }
    if self.enabled:
      nuke.removeKnobChanged(this.kiss)
    else:
      nuke.addKnobChanged(this.kiss)
    self.enabled = not self.enabled
    
  def kiss():
  	"""
  	check if selectedNode is near other nodes
  	and connect input of selectedNode to the nearby node
  	"""
    selected_nodes = nuke.selectedNodes()
    node_to_connect = ''
    node_xpos = 0
    node_ypos = 0
    if selected_nodes and self.enabled is True:
      active_node = selected_nodes[0]
      node_xpos = active_node.xpos()
      node_ypos = active_node.ypos()
    for i in range(0, len(self.nodes)):
      tol_xpos = self.nodes[i]['xpos'] - self.tolerance
      tol_ypos = self.nodes[i]['ypos'] - 100
      tol_width = self.nodes[i]['xpos'] + self.nodes[i][screenWidth] + self.tolerance
      tol_height = self.nodes[i]['ypos'] + self.nodes[i][screenHeight] + self.tolerance
      if node_xpos >= tol_xpos and node_xpos <= tol_width:
        if node_ypos >= tol_ypos and node_ypos <= tol_height:
          if active_node.name() != self.nodes[i]['name'] and self.nodes[i]['name'] != '':
            node_to_connect = nuke.toNode(self.nodes[i]['name'])
            if node_ypos < self.nodes[i]['ypos']:
              if active_node.maxOutputs():
                if node_to_connect.maxInputs():
                  k = 0
                  for input in range(0, node_to_connect.inputs()):
                    if node_to_connect.input(k):
                      k+=1
                    else:
                      break
                  node_to_connect.setInput(k, active_node)
                  nuke.removeKnobChanged(this.kiss)
                  this.enabled = False
            else:
              if active_node.maxInputs():
                if node_to_connect.maxOutputs():
                  k = 0
                  for input in range(0, active_node.inputs()):
                    if active_node.input(k):
                      k += 1
                    else:
                      break
                  active_node.setInput(k, node_to_connect)
                  nuke.removeKnobChanged(this.kiss)
                  this.enabled = False
            try:
              _internal_expression_arrow_cmd()
            except:
              pass
            break

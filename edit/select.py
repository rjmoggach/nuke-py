


select_classes(nodes=[], classes=['Write'], toggle=False):
  if not nodes:
    nodes = nuke.allNodes()
    for node in nodes:
      if node.Class() in classes:
        node['selected'].setValue(True)
      else:
        node['selected'].setValue(False)
    return True
  else:
    if not toggle:
      for node in nodes:
        if node.Class() in classes:
          node['selected'].setValue(True)
        else:
          node['selected'].setValue(False)
      return True
    else:
      for node in nuke.allNodes():
        if node.Class() in classes:
          node['selected'].setValue(not node['selected'])
        else:
          node['selected'].setValue(False)
      return True
      

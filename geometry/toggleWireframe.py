





toggle_wireframe(nodes=[]):
  
  for node in nodes:
    if node.Class() == 'ReadGeo2':
      node['display'].setValue('wireframe')

def textured(nodes=[], toggle=True):
  for node in nodes:
    if node.Class() == 'ReadGeo2':
      node['display'].setValue('textured')
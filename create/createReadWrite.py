import re
import os, string
import nuke
from nukescripts import panels


# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"

__menus__ = {
  'Tools/Create/Read from Write': {
    'cmd': 'createReadWrite(nuke.selectedNodes())',
    'hotkey': '#+r',
    'icon': ''
  },
  'Tools/Create/Write from Read': {
    'cmd': 'createReadWrite(nuke.selectedNodes())',
    'hotkey': '',
    'icon': ''
  }
}


def createReadWrite(nodes=[], y_offset=80):
  '''
  function to:
    create a read node from a write node
    or
    create a write node from a read node
  
  works on single or multiple selections
  '''
  # if no nodes are defined look for selected nodes
  if not nodes:
    nodes = nuke.selectedNodes()
  
  # if nodes is still empty, nothing is selected
  if nodes == ():
    nuke.message('ERROR: No node(s) selected.')
    return
  
  for node in nodes:
    _class = node.Class()
    if _class in ['Write', 'Read']:
      file = node.knob('file').getValue()
      proxy = node.knob('proxy').getValue()
      first = nuke.toNode('root').knob('first_frame').getValue()
      last = nuke.toNode('root').knob('last_frame').getValue()
      colorspace = node.knob('colorspace').getValue()
      xpos = node.knob('xpos').getValue()
      ypos = int(node.knob('ypos').getValue()) + y_offset
      knobs = []
      fields = ('file','proxy','first','last','colorspace','xpos','ypos')
      for entry in fields:
        if eval(entry) != '':
          knobs.append(entry)
          knobs.append(str(eval(entry)))
      if _class == 'Write':
        nuke.createNode('Read', string.join(knobs))
      else:
        nuke.createNode('Write', string.join(knobs))
  return



# OLDER VERSIONS
def createReadFromWrite(nodes=[]):
	'''
	function to create a read node
	from a selected write node
	'''

	# if no nodes are defined look for selected nodes
	if not nodes:
		nodes = nuke.selectedNodes()
	
	# if nodes is still empty, nothing is selected
	if nodes == ():
		nuke.message('ERROR: No node(s) selected.')
		return
	
	#work around to select single node as an object
	node = nodes[0]
	_class = node.Class()
	if _class == "Write":
		file = node.knob('file').getValue()
		proxy = node.knob('proxy').getValue()
		first = nuke.toNode('root').knob('first_frame').getValue()
		last = nuke.toNode('root').knob('last_frame').getValue()
		xpos = node.knob('xpos').getValue()
		ypos = int(node.knob('ypos').getValue()) + 40
		knobs = []
		fields = ('file','proxy','first','last','xpos','ypos')
		for entry in fields:
			if eval(entry) != '':
				knobs.append(entry)
				knobs.append(str(eval(entry)))
		nuke.createNode('Read', string.join(knobs))	
	return




def createWriteFromRead(nodes=[]):
  '''
  function to create a write node
  from a selected read node
  '''

  # if no nodes are defined look for selected nodes
  if not nodes:
    nodes = nuke.selectedNodes()
  
  # if nodes is still empty, nothing is selected
  if not nodes:
    nuke.message('ERROR: No node(s) selected.')
    return
  
  for node in nodes:
    _class = node.Class()
    if _class == "Read":
      file = node.knob('file').getValue()
      proxy = node.knob('proxy').getValue()
      first = nuke.toNode('root').knob('first_frame').getValue()
      last = nuke.toNode('root').knob('last_frame').getValue()
      xpos = node.knob('xpos').getValue()
      ypos = int(node.knob('ypos').getValue()) + 40
      knobs = []
      fields = ('file','proxy','first','last','xpos','ypos')
      for entry in fields:
        if eval(entry) != '':
          knobs.append(entry)
          #knobs.append(str(eval(entry)))
      nuke.createNode('Write', string.join(knobs))  
  return



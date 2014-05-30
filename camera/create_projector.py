import nuke

# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"


__menus__ = {
  'Tools/Camera/Create Projector from Camera':  {
    'cmd': 'create_projector(nuke.selectedNodes())',
    'hotkey': '',
    'icon': ''
  }
}

def clipboard():
  return "%clipboard%"


def deselect_all_nodes():
  for node in nuke.allNodes():
    node['selected'].setValue(False)


def copy_paste():
  nuke.nodeCopy(clipboard())
  deselect_all_nodes()
  nuke.nodePaste(clipboard())


def create_projector(nodes=[]):
  if not nodes:
    nuke.message('ERROR: No node(s) selected.')
    return

  for node in nodes:
    deselect_all_nodes()
    if node.Class() in [ "Camera2", "Camera"]:
      node_name = node.name()
      frame = nuke.getInput("Frame to Project for {0}?".format(node_name))
      try:
        int(frame)
      except ValueError:
        nuke.message("You must enter a frame number!")
        return 0
      node['selected'].setValue(True)
      copy_paste()
      new_camera = nuke.selectedNode()
      new_camera.addKnob(nuke.Int_Knob('ref_frame', 'Reference Frame'))
      new_camera['ref_frame'].setValue(int(frame))
      new_camera['label'].setValue("Projection at frame: [value ref_frame]")
      new_camera['tile_color'].setValue(123863)
      new_camera['gl_color'].setValue(123863)
  
      for knob in new_camera.knobs().values():
        if knob.hasExpression():
          if knob.arraySize() ==1:
            chan_name = "{0}.{1}".format(new_camera.name(), knob.name())
            first = "{0}".format(nuke.root().firstFrame())
            last = "{0}".format(nuke.root().lastFrame())
            knob_name = "{0}".format(knob.name())
            nuke.animation( chan_name, "generate", (first, last, "1", "y", knob_name))
          else:
            i = knob.arraySize() - 1
            while i > -1:
              chan_name = "{0}.{1}.{2}".format(new_camera.name(), knob.name(), i)
              first = "{0}".format(nuke.root().firstFrame())
              last = "{0}".format(nuke.root().lastFrame())
              knob_name = "{0}".format(knob.name())
              nuke.animation( chan_name, "generate", first, last, "1", "y", knob_name))
              i-=1
  
      for knob in new_camera.knobs().values():
         if knob.isAnimated():
           knob.setExpression('curve(ref_frame)')
  
  

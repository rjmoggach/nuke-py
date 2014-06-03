import os, platform
import nuke
# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"


__menus__ = {
  'Tools/Create/Create Write Dirs': {
    'cmd': 'createWriteDirs(nuke.selectedNodes())',
    'hotkey': '#+w',
    'icon': 'createWriteDirs.png'
  }
}


def createWriteDirs(nodes=[]):
  '''
  create write directories for selected write nodes
  supports stereo view notation with %v or %V
  '''
  # if no nodes are specified then look for selected nodes
  if not nodes:
    nodes = nuke.selectedNodes()

  # if nodes is still empty no nodes are selected
  if not nodes:
    nuke.message('ERROR: No node(s) selected.')
    return

  EXISTING = []

  for entry in nodes:
    _class = entry.Class()
    if _class == "Write":
      path = nuke.filename(entry)
      output_paths = []
      if path is None:
        continue
      all_views = curnode.knob('views').value() # look for views in the write node
      all_views = all_views.split() # split them out
      for view in all_views:
        if '%v' in path:
          output_paths.append(path.replace('%v',view[:1]))
        if '%V' in path:
          output_paths.append(path.replace('%V',view))
        if not len(output_paths):
          output_paths.append(path)
        for output_path in output_paths:
          root_path = os.path.dirname(output_path)
          if os.path.exists(root_path) == True:
            nuke.tprint('Path Exists: {0}'.format(root_path))
            return
          try:
            os.mkdir(root_path)
            os.chmod(root_path,0775)
          except:
            if nuke.ask('Create Path? \n{0}'.format(root_path)):
              os.makedirs(root_path)
              os.chmod(root_path,0775)
            else:
              return
  return

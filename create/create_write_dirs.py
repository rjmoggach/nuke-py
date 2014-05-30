import os, platform
import nuke
# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"


__menus__ = {
  'Tools/Create/Create Write Dirs': {
    'cmd': 'create_write_dirs(nuke.selectedNodes())',
    'hotkey': '#+w',
    'icon': ''
  }
}


def create_write_dirs(nodes=[]):
  '''
  Makes directories for selected write nodes
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
      if path is None:
        continue
      root_path = os.path.dirname(path)

      if os.path.exists(root_path) == True:
        nuke.tprint('Path Exists: {0}'.format(root_path))
        return
      try:
        os.mkdir(root_path)
        os.chmod(root_path,0775)
      except:
        if nuke.ask('Create Path: {0}'.format(root_path)):
          os.makedirs(root_path)
          os.chmod(root_path,0775)
        else:
          return
  return

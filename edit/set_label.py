import nuke

# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"

__menus__ = {
  'Tools/Edit/Set or Append Label(s)': {
    'cmd': 'set_label()',
    'hotkey': 'F9',
    'icon': 'set_label.png'
  }
}

def set_label(nodes=nuke.selectedNodes()):
    '''
    Quickly edit the label for a selected node
    or append a label to all selected nodes
    '''
    if not nodes:
      nuke.message('ERROR: No node(s) selected.')
      return
    elif len(nodes) == 1:
      node = nuke.selectedNodes()[-1]
      node_label = node['label'].value()
      node_name = node.name()
      panel = nuke.Panel('Edit Label')
      panel.setTitle('Edit Label for: {0}'.format(node_name))
      panel.setWidth(350)
      panel.addNotepad('Label', node_label)
      result = panel.show()
      if result:
        label = panel.value('Label')
        try:
          node['label'].setValue(label)
        except:
          return
      else:
        return
    else:
      panel = nuke.Panel('Append Label')
      panel.setTitle('Append to Labels')
      panel.setWidth(350)
      panel.addNotepad('Label', '')
      result = panel.show()
      if result:
        label = panel.value('Label')
        for node in nodes:
          try:
            node_label = node['label'].value()
            new_label = '{0}\n{1}'.format(node_label, label)
            node['label'].setValue(new_label)
          except:
            return
      return

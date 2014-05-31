import nuke

__menus__ = {
  'Tools/Time/Append Clips':  {
    'cmd': 'append_clips()',
    'hotkey': '',
    'icon': ''
  }
}

def append_clips():
  append_clip_node = nuke.nodes.AppendClip()
  all_read_nodes = [node for node in nuke.allNodes() if node.Class() == "Read"] 
  num_nodes = len(all_read_nodes)
  print num_nodes
  x=0
  while x != num_nodes:
    append_clip_node.setInput(x,all_read_nodes[x])
    x+=1
 

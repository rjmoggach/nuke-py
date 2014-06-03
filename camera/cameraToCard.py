import nuke

# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"

__menus__ = {
  'Tools/Camera/Camera to Card':  {
    'cmd': 'cameraToCard()',
    'hotkey': '',
    'icon': 'cameraToCard.png'
  },
  'Tools/Camera/Card to Camera':  {
    'cmd': 'cardToCamera()',
    'hotkey': '',
    'icon': 'cardToCamera.png'
  }
}

def cameraToCard():
  trans_geo_str = ' '.join([
    'inputs {2}',
    'name {cameraToCard}',
    'translate {0 0 "-this.distance"}',
    'scaling {this.hapt this.vapt}',
    'uniform_scale {this.distance}',
    'addUserKnob {20 Distance}',
    'addUserKnob {7 hapt}',
    'hapt {{"1/([value input1.focal]/[value input1.haperture])" }}',
    'addUserKnob {7 vapt}',
    'vapt {{"1/([value input1.focal]/[value input1.haperture])"}}',
    'addUserKnob {7 distance R 0 1000}',
    'distance 1'
  ])
  trans_geo_node = nuke.createNode('TransformGeo', trans_geo_str)
  trans_geo_node_translate = "{0}.translate".format(trans_geo_node.name())
  trans_geo_node_distance = "{0}.distance".format(trans_geo_node.name())
  axis_node = nuke.createNode('Axis')
  camera_node = nuke.createNode('Camera2', 'translate {{0 0 {0}}} pivot {{{1} {1} {1}}}'.format(trans_geo_node_distance, trans_geo_node_translate))
  trans_geo_node.setInput(1, camera_node)
  camera_node.setInput(1, axis_node)

def cardToCamera():
  trans_geo_str = ' '.join([
    'name {cardToCamera}',
    'translate {0 0 "-this.distance"}',
    'scaling {this.hapt this.vapt}',
    'uniform_scale {this.distance}',
    'addUserKnob {20 Distance}',
    'addUserKnob {7 hapt}',
    'hapt {{"1/([value input1.focal]/[value input1.haperture])" }}',
    'addUserKnob {7 vapt}',
    'vapt {{"1/([value input1.focal]/[value input1.haperture])" }}',
    'addUserKnob {7 distance R 0 1000}',
    'distance 1'
  ])
  transform_geo_node = nuke.createNode('TransformGeo', trans_geo_str)
  camera_node = nuke.createNode('Camera2')
  transform_geo_node.setInput(1, camera_node)

import math
import nuke

# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"


__menus__ = {
  'Tools/Camera/Create Camera from V-Ray Metadata':  {
    'cmd': 'create_vray_camera(nuke.selectedNodes())',
    'hotkey': '',
    'icon': ''
  }
}



def create_vray_camera( node ):
  '''
  create camera with vray exr metadata
  looks at metadata in current pipe and creates
  camera node accordingly
  '''
  node_data = node.metadata()
  required_fields = ['exr/camera%s' % i for i in ('FocalLength', 'Aperture', 'Transform')]
  if not set(required_fields).issubset( node_data ):
    nuke.message('ERROR: No relevant camera metadata found.')
    return
  
  first_frame = node.firstFrame()
  last_frame = node.lastFrame()
  ret = nuke.getFramesAndViews( 'Create Camera from Metadata', '%s-%s' %( first_frame, last_frame )  )
  frame_range = nuke.FrameRange( ret[0] )
  
  cam = nuke.createNode( 'Camera2' )
  cam['useMatrix'].setValue( False )
  
  for camera_attr in ( 'focal', 'haperture', 'translate', 'rotate'):
    cam[camera_attr].setAnimated()

  for current_task, frame in enumerate( frame_range ):
    horiz_aperture = node.metadata( 'exr/cameraAperture', frame)
    fov = node.metadata( 'exr/cameraFov', frame) # get camera FOV
    focal = horiz_aperture / ( 2 * math.tan(math.radians(fov) / 2.0))
    cam['focal'].setValueAt(float(focal),frame)
    cam['haperture'].setValueAt(float(horiz_aperture),frame)
    matrix_camera = node.metadata( 'exr/cameraTransform', frame) # get camera transform data
    matrix_created = nuke.math.Matrix4()
    for key,val in enumerate(matrix_camera):
      matrixCreated[key] = val
    # this is needed for VRay.  It's a counter clockwise rotation      
    matrix_created.rotateX(math.radians(-90))
    # Get a vector that represents the camera translation
    translate = matrix_created.transform(nuke.math.Vector3(0,0,0))
    # give us xyz rotations from cam matrix (must be converted to degrees)
    rotate = matrix_created.rotationsZXY()
    # set camera translate & rotate
    cam['translate'].setValueAt(float(translate.x), frame, 0)
    cam['translate'].setValueAt(float(translate.y), frame, 1)
    cam['translate'].setValueAt(float(translate.z), frame, 2)
    cam['rotate'].setValueAt(float(math.degrees(rotate[0])), frame, 0)
    cam['rotate'].setValueAt(float(math.degrees(rotate[1])), frame, 1) 
    cam['rotate'].setValueAt(float(math.degrees(rotate[2])), frame, 2) 



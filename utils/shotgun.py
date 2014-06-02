# shotgun.py
#
# this is a collection of useful shotgun related functions
# for getting data in and out of shotgun
#
# most require the shotgun object which is created
# via the shotgun api
#
# usually goes like this:
# 
# from shotgun_api3 import Shotgun
# shotgun = Shotgun('https://' + 'studio shotgun url', 'myGreatShotgunTool', 'API Key')
#
# then call the function with the shotgun object
#

import re

def get_fields_for_entity(shotgun, entity):
  """
  get fields for a shotgun type/entity
  """
  all_fields = []
  fields = shotgun.schema_field_read(entity)
  for field in fields:
    all_fields.append(field)
  return all_fields  


def frame_pad(input_path):
  pattern = re.compile(r'%[0-9]+d')
  frame_pad_data = pattern.findall(input_path)
  if frame_pad_data:
    out = frame_pad_data[0]
    out_format = out
  if not frame_pad_data:
    pattern = re.compile(r'#')
    frame_pad_data = pattern.findall(input_path)
    out = ''
    for n in range(len(frame_pad_data)):
      out = out + frame_pad_data[n]
    out_format = '%' + '0%0dd' % (len(frame_pad_data))
  return out, out_format

def get_project(shotgun, project_name):
  """
  get shotgun project by name
  """
  return_fields = get_fields_for_entity(shotgun, 'Project')
  project = project.replace('_', ' ')
  shotgun_query = [
    ['name', 'is', project_name],
  ]
  return shotgun.find_one('Project', shotgun_query, return_fields)


def get_sequence(shotgun, project, sequence_code):
  """
  get sequence for project
  Parameters : (shotgun, project, sequence)
  """
  return_fields = get_fields_for_entity(shotgun, 'Sequence')
  shotgun_query = [
    ['code', 'is', sequence_code],
    ['project','is', project]
  ]
  sequence = shotgun.find_one('Sequence', shotgun_query, return_fields)
  return sequence


def get_shot(shotgun, project, shot_code):
  """
  get shot for project
  Parameters : (shotgun, project, shot_code)
  """    
  return_fields = get_fields_for_entity(shotgun, 'Shot')
  shotgun_query = [
    ['code', 'is', shot_code],
    ['project', 'is', project]
  ]
  shot = shotgun.find_one('Shot', shotgun_query, return_fields)
  return shot


def create_project(shotgun, project_name):
  """
  create project in shotgun
  Parameters : (shotgun, project_name)
  """
  return_fields = ['layout_project', 'id']
  shotgun_query = [['name', 'is', 'a']]
  template = shotgun.find_one('Project', shotgun_query, return_fields)
  data = {
    'name': project_name,
    'layout_project': template
  }
  return shotgun.create('Project', data)


def create_sequence(shotgun, project, sequence_code):
  """
  create sequence for project
  Parameters : (shotgun, project, sequence_code)
  """
  data = {
    'project': {
      "type": "Project", "id": project['id']
    },
    'code': sequence_code
  }
  return shotgun.create('Sequence', data)


def create_shot(shotgun, project, shot, seq='', task_template_name=''):
  """
  create shot for given project/sequence
  Parameters : (shotgun, project, shot, seq='', task_template_name='Basic shot template'
  """
  shotgun_query = [['code', 'is', task_template_name ]]
  template = shotgun.find_one('TaskTemplate', shotgun_query)
  data = {
    'project': {
      "type": "Project", "id": project['id']
    },
    'code': shot,
    'task_template' : template,
    'description': '',
    'self.sg_sequence': seq,
    'self.sg_status_list': 'wtg'
  }
  return shotgun.create('Shot', data)


def get_shot_notes(shotgun, shot_id):
  """
  get notes for shot
  Parameters : (shotgun, shot_id)
  Output : Note data :
  ['tasks', 'attachments', 'updated_at', 'replies', 'id', 'subject', 'playlist', '
  addressings_to', 'created_by', 'content', 'sg_status_list', 'reply_content', 
  'updated_by', 'addressings_cc', 'read_by_current_user', 'user', 'note_links', 
  'created_at', 'sg_note_from', 'project', 'sg_note_type', 'tag_list']    
  """
  return_fields = ['subject', 'content', 'created_at']
  shotgun_query = [['note_links','is', shot_id]]
  shotgun_sorting = [{'field_name':'created_at','direction':'desc'}]
  return shotgun.find('Note', shotgun_query, return_fields, shotgun_sorting)


def get_latest_note_for_shot(shotgun, shot_id):
  """
  get latest note for shot only
  Parameters : (shotgun, shot_id)
  """
  return get_shot_notes(shotgun, shot_id)[0]


def create_note_for_shot(shotgun, project, shot_id, subject, content):
  """
  create note for shot
  Parameters : (shotgun, project, shot_id, subject, content)
  Output : noteID
  """
  data = {
    'subject': subject,
    'content': content,
    'note_links': [shot_id],
    'project': project
  }
  # create the note
  return shotgun.create('Note', data)


def create_version(shotgun, project, shot, version_code, description, frame_path, first_frame, last_frame, client_name=None, source_file=None, task=None, user=None, final=False, make_thumbnail=False, make_shot_thumbnail=False):
  """
  create a version
  Parameters : (shotgun, project, shot_id, version_code, description, frame_path, first_frame, last_frame, client_name=None, source_file=None, task=None)
  Output : version_id
  """
  data = {
    'project': project,
    'code': version_code,
    'description': description,
    'sg_path_to_frames': frame_path,
    'sg_first_frame' : int(first_frame),
    'sg_last_frame' : int(last_frame),
    'sg_status_list': 'rev',
    'entity': shot
  }
  if task != None:
    filters = [['content', 'is', task], ['entity', 'is', shot]]
    task_id = shotgun.find_one('Task', filters)
    data['sg_task']=task_id
  version_fields = shotgun.schema_field_read('Version')
  if 'sg_client_name' not in version_fields and client_name != None:
    field_type = 'text'
    field_name = 'Client Name'
    new_field = shotgun.schema_field_create('Version', field_type, field_name)
  if client_name != None:
    data['sg_client_name'] = client_name
  if 'sg_source_file' not in version_fields and source_file != None:
    field_type = 'text'
    field_name = 'Source File'
    new_field = shotgun.schema_field_create('Version', field_type, field_name)
  if source_file != None:
    data['sg_source_file'] = source_file
  version = shotgun.create('Version', data)
  middle_frame = (int(first_frame) + int(last_frame)) / 2
  padding, pad_str = frame_pad(frame_path)
  padded_frame = pad_str % (middle_frame)
  if make_thumbnail == True:
    thumb_data = shotgun.upload_thumbnail('Version', version['id'], frame_path.replace(padding, padded_frame))
  if make_shot_thumbnail == True:
    thumb_data = shotgun.upload_thumbnail('Shot', shot['id'], frame_path.replace(padding, padded_frame))   
  return version    

 
def get_version(shotgun, version_id):
  """
  get version
  Parameters : (shotgun, version_id)
  Output : Version data:
  ['sg_version_type', 'open_notes_count', 'code', 'playlists', 'sg_task', 'image',
  'updated_at', 'sg_output', 'sg_path_to_frames', 'tasks', 'frame_range', 'id', 
  'description', 'sg_uploaded_movie_webm', 'open_notes', 'tank_published_file', 
  'task_template', 'created_by', 'sg_movie_type', 'sg_status_list', 'notes', 
  'sg_client_name', 'sg_uploaded_movie_mp4', 'updated_by', 'sg_send_for_final', 
  'user', 'sg_uploaded_movie_frame_rate', 'entity', 'step_0', 'sg_client_version', 
  'sg_uploaded_movie_transcoding_status', 'created_at', 'sg_qt', 'project', 
  'filmstrip_image', 'tag_list', 'frame_count', 'flagged']    
  """
  return_fields = get_fields_for_entity(shotgun, 'Version')
  shotgun_query = [['id', 'is', version_id]]
  shotgun_sorting = [{'field_name':'created_at','direction':'desc'}]
  return shotgun.find('Version',shotgun_query, return_fields, shotgun_sorting)[0]


# look for versions in a shot:
def get_versions_for_shot(shotgun, shot_id):
  """
  Find all versions in a shot with most recent first
  Parameters : (shotgun, shot_id)
  Output : Version data:
  ['sg_version_type', 'open_notes_count', 'code', 'playlists', 'sg_task', 'image',
  'updated_at', 'sg_output', 'sg_path_to_frames', 'tasks', 'frame_range', 'id', 
  'description', 'sg_uploaded_movie_webm', 'open_notes', 'tank_published_file', 
  'task_template', 'created_by', 'sg_movie_type', 'sg_status_list', 'notes', 
  'sg_client_name', 'sg_uploaded_movie_mp4', 'updated_by', 'sg_send_for_final', 
  'user', 'sg_uploaded_movie_frame_rate', 'entity', 'step_0', 'sg_client_version', 
  'sg_uploaded_movie_transcoding_status', 'created_at', 'sg_qt', 'project', 
  'filmstrip_image', 'tag_list', 'frame_count', 'flagged']    
  """
  return_fields = get_fields_for_entity(shotgun, 'Version')
  shotgun_query = [['entity','is',shot_id]]
  shotgun_sorting = [{'field_name':'created_at','direction':'desc'}]
  return shotgun.find('Version', shotgun_query, return_fields, shotgun_sorting)


def get_latest_version(shotgun, shot_id):
  """
  Find only the most recent version
  Parameters : (shotgun, shot_id)
  Output : Version data:
  ['sg_version_type', 'open_notes_count', 'code', 'playlists', 'sg_task', 'image',
  'updated_at', 'sg_output', 'sg_path_to_frames', 'tasks', 'frame_range', 'id',
  'description', 'sg_uploaded_movie_webm', 'open_notes', 'tank_published_file',
  'task_template', 'created_by', 'sg_movie_type', 'sg_status_list', 'notes', 
  'sg_client_name', 'sg_uploaded_movie_mp4', 'updated_by', 'sg_send_for_final',
  'user', 'sg_uploaded_movie_frame_rate', 'entity', 'step_0', 'sg_client_version',
  'sg_uploaded_movie_transcoding_status', 'created_at', 'sg_qt', 'project', 
  'filmstrip_image', 'tag_list', 'frame_count', 'flagged']     
  """
  return_fields = get_fields_for_entity(shotgun, 'Version')
  shotgun_query = [['entity','is',shot_id]]
  shotgun_sorting = [{'field_name':'created_at','direction':'desc'}]
  return shotgun.find_one('Version', shotgun_query, return_fields, shotgun_sorting)


def get_latest_version_for_task(shotgun, shot_id, task):
  """
  get latest version for shot task
  Parameters: (shotgun, shot_id, task)
  """
  return_fields = get_fields_for_entity(shotgun, 'Version')
  filters = [['content','is',task],['entity','is',shot_id]]
  task_id = shotgun.find_one('Task', filters)
  # then look for the latest
  #version using the task ID.  note that we need to use the [0] or else we're sending the array versus the hash
  shotgun_query = [['entity','is',shot_id],['self.sg_task','is',task_id]]
  shotgun_sorting = [{'field_name':'created_at','direction':'desc'}]
  return shotgun.find_one('Version', shotgun_query, return_fields, shotgun_sorting)


## The following requires a field called "client_version" be added to shotgun
def update_client_version(shotgun, shot_id, version, client_version_name ='Client Version'):
  """
  This takes the shot_id and version (int) and updates the shot with this client version number
  Sometimes the client wants to see different version numbers versus the internal ones.  This option allows for it.
  You will need to create a field.  Client Version is what I have used but you can specify what you want here.
  Parameters: (shotgun, shot_id, version, client_version_name ='Client Version')
  Output : Version data
  """
  shotgun_field_name = 'sg_' + client_version_name.lower().replace(' ','_')
  data = { shotgun_field_name: version}
  try:
    result = shotgun.update('Shot', shot_id['id'], data)
  except:
    new_field = shotgun.schema_field_create('Shot', 'number', client_version_name)
    result = shotgun.update('Shot', shot_id['id'], data)
  return result


def upload_qt(shotgun, entity_type, item, path):
  """
  upload a movie to shotgun
  Parameters: (shotgun, entity, item, path)
  Eg: upload_qt(shotgun, 'Version', version_data, '/my/file.mov')
  """
  entity = entity_type.capitalize()
  if entity.lower() == 'shot':
    try:
      result = shotgun.upload(entity, item['id'], path, 'sg_qt')
    except:
      new_field = shotgun.schema_field_create('Shot', 'url', 'QT')
      result = shotgun.upload(entity, item['id'], path, 'sg_qt')
  elif entity.lower() == 'version':
    result = shotgun.upload(entity, item['id'], path, 'sg_uploaded_movie')
  return result

 
def get_client_version(shotgun, shot_id, client_version_name='Client Version'):
  """
  Get latest client version number
  Parameters : (shotgun, hotID, client_version_name='Client Version')
  Output : Version data
  """
    
  shotgun_field_name = 'sg_' + client_version_name.lower().replace(' ','_')
  try :
    current_version = shot_id[shotgun_field_name]
  except :
    current_version = 0
  if current_version == None:
    return 0
  return current_version


def get_playlist(shotgun, project, playlist_code):
  """
  get playlist for project by name
  Parameters : (shotgun, project, playlist_code)
  Output : playlist data:
  ['code', 'description', 'versions', 'created_at', 'sg_cinesync_session_url', 
  'updated_at', 'created_by', 'project', 'filmstrip_image', 'notes', 'image', 
  'updated_by', 'sg_cinesync_session_key', 'sg_status', 'tag_list', 'id', 
  'sg_date_and_time']    
  """
    
  return_fields = get_fields_for_entity(shotgun, 'Playlist')
  shotgun_query = [['code','is',playlist_code],['project','is',project]]
  return shotgun.find_one('Playlist', shotgun_query, return_fields)


def create_playlist(shotgun, project, playlist_code, playlist_desc=''):
  """
  create a playlist
  Parameters : (shotgun, project, playlist_code, playlist_desc='')
  Output : playlist data
  """
  data = {
    'project': project,
    'code': playlist_code,
    'description':playlist_desc
  }
  return shotgun.create('Playlist', data)


def create_playlist_version(shotgun, project, playlist_code, version):
  """
  create a playlist version
  Parameters: (shotgun, project, playlist_code, version)
  Output: dict of the playlist
  """
  return_fields = ['versions']
  shotgun_query = [['code','is',playlist_code],['project','is',project]]
  playlist_list = shotgun.find_one('Playlist', shotgun_query, return_fields)
  if len(playlist_list):
    version_list = playlist_list['versions'];
    version_list.append({'type':'Version','name':version['code'],'id':version['id']})
    return shotgun.update('Playlist', playlist_list['id'], {'versions' : version_list})


def get_playlist_info(shotgun, project, playlist_code):
  """
  get playlist info
  Parameters : (shotgun, project, playlist_code)
  Output : version data
  """
  data = []
  version_data = []
  return_fields = get_fields_for_entity(shotgun, 'Version')
  shotgun_query = [['code','is',playlist_code],['project','is',project]]
  playlist = shotgun.find_one('Playlist', shotgun_query, ['versions'])
  for version in playlist['versions']:
    shotgun_query = [['id','is',version['id']]]
    data.append(shotgun.find_one('Version', shotgun_query, return_fields))
  return data    


def get_time_for_shot(shotgun, shot):
  """
  Given shot (as dict) return total time on shot as [0] and other times for each task on shot
  """

  output_data = []
  return_fields = ['content', 'time_logs_sum']
  total_time = 0
  for current_task in shot['tasks']:
    shotgun_query = [['id','is',current_task['id']]]
    task_data = shotgun.find_one('Task', shotgun_query, return_fields)
    total_time += task_data['time_logs_sum']
    output_data.append({'name': task_data['content'], 'time': task_data['time_logs_sum']})
  output_data.insert(0,{'name': shot['code'], 'time': total_time})
  return output_data


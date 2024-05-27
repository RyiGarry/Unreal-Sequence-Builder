import unreal, json, sequencer_key_examples

# To do before running:
# Change cam_names, cam_tc_start, and cam_tc_end (lines 10-12) to match yours. cam_names must match level sequence names.
# Add location and name of master sequence in your project at line 13.

#Add all cams here with names and start timecodes (where you want them to be placed in the master edit) in 24fps timecode.
cam_names = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110]
cam_tc_start = [0, 101, 201, 301, 401, 501, 601, 701, 801, 901, 1001]
cam_tc_end = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100]

master_seq_str = "/Game/SequenceMaster"
master_sequence = unreal.load_asset(master_seq_str)
shotsTrack = master_sequence.add_master_track(unreal.MovieSceneCinematicShotTrack)

def float_key_example(sequencer_asset_path, offset_time):
	sequence = unreal.load_asset(sequencer_asset_path, unreal.LevelSequence)
	
	all_tracks = sequence.get_master_tracks()
	all_float_keys = []
	
	for object_binding in sequence.get_bindings():
		all_tracks.extend(object_binding.get_tracks())
		
	for track in all_tracks:
		for section in track.get_sections():
			for channel in section.find_channels_by_type(unreal.MovieSceneScriptingFloatChannel):
				keys = channel.get_keys()
				print('Added {0} keys from channel: {1} on section: {2}'.format(len(keys), channel.get_name(), section.get_name()))
				all_float_keys.extend(keys)
	
	print("Writing float key properties:")
	for key in all_float_keys:
		print('Time: {0: 6d}:{1:4.3f} Value: {2: 6.2f} InterpMode: {3} TangentMode: {4} TangentWeightMode: {5} ArriveTangent: {6:+11.8f} ArriveTangentWeight: {7:+9.4f}  LeaveTangent: {8:+11.8f} LeaveTangentWeight: {9:+9.4f}'.format(
		key.get_time().frame_number.value, key.get_time().sub_frame, key.get_value(), key.get_interpolation_mode(), key.get_tangent_mode(), key.get_tangent_weight_mode(), key.get_arrive_tangent(), key.get_arrive_tangent_weight(), key.get_leave_tangent(), key.get_leave_tangent_weight())
		)

	add_time_to_keys(sequence, all_float_keys, offset_time)

	return

def add_time_to_keys(sequence, key_array, time):
	print('Adding {0} frames (time) to {1} keys in array...'.format(time, len(key_array)))
	
	time_as_frame_time = unreal.FrameTime(unreal.FrameNumber(time))
	time_as_tick = unreal.TimeManagementLibrary.transform_time(time_as_frame_time, sequence.get_display_rate(), sequence.get_tick_resolution())

	for key in key_array:
		print('CurrentTime: {0} NewTime: {1}'.format(key.get_time().frame_number, key.get_time().frame_number + time))
		key.set_time(key.get_time().frame_number + time, 0.0, unreal.SequenceTimeUnit.DISPLAY_RATE)
	
	print('Finished!')
	return

x = 0
for i in cam_names:
	#Access level sequence of specified camera.
	level_needed = cam_names[x]
	level_sequence_str = f"/Game/{level_needed}"

	level_sequence = unreal.load_asset(level_sequence_str)
	unreal.LevelSequenceEditorBlueprintLibrary.open_level_sequence(level_sequence)

#Offset camera to specified frame number.
	tc_start = cam_tc_start[x]
	float_key_example(level_sequence_str, tc_start)

#Set level sequence start and end points to match time of camera within the level sequences, NOT the master sequence.
	tc_start2 = cam_tc_start[x]
	tc_end = cam_tc_end[x]
	level_sequence.set_playback_start(tc_start2)
	level_sequence.set_playback_end(tc_end)
	unreal.LevelSequenceEditorBlueprintLibrary.refresh_current_level_sequence()

	cam_name = cam_names[x]
	#Add cam with name matching sequence from main level into the active sequence.
	camera = unreal.load_object(None, f"/Game/Map.Map:PersistentLevel.{cam_name}")
	subsequence = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()

	# add a camera cut track
	camera_cut_track = subsequence.add_master_track(unreal.MovieSceneCameraCutTrack)
	camera_cut_section = camera_cut_track.add_section()
	tc_start_seconds = tc_start//24 - 30
	tc_end_seconds = tc_end//24 + 30
	camera_cut_section.set_start_frame_seconds(tc_start_seconds)
	camera_cut_section.set_end_frame_seconds(tc_end_seconds)

	# add a binding for the camera
	camera_binding = subsequence.add_possessable(camera)
	# transform_track = camera_binding.add_track(unreal.MovieScene3DTransformTrack)
	# transform_section = transform_track.add_section()
	# transform_section.set_start_frame_bounded(0)
	# transform_section.set_end_frame_bounded(0)

	# add the binding for the camera cut section
	camera_binding_id = subsequence.make_binding_id(camera_binding, unreal.MovieSceneObjectBindingSpace.LOCAL)
	camera_cut_section.set_camera_binding_id(camera_binding_id)

	#add attach track from newly created camera to existing cam in sequencer.

	#camera = unreal.load_object(None, f"/Game/Map.Map:PersistentLevel.{cam_name}")
	#camera_binding = subsequence.add_possessable(camera)
	#camera_binding_id = subsequence.make_binding_id(camera_binding, unreal.MovieSceneObjectBindingSpace.LOCAL)
	#camera_cut_section.set_camera_binding_id(camera_binding_id)

	#attach_binding_id = sequence.make_binding_id(guid_of_cube_1, unreal.MovieSceneObjectBindingSpace.LOCAL)
	#attach_settings.set_constraint_binding_id(attach_binding_id)

	#adding empty sequences at the correct TC
	unreal.LevelSequenceEditorBlueprintLibrary.open_level_sequence(master_sequence)

	# add MovieSceneCinematicShotTrack track to your master_sequence
	# add a section to the track
	section = shotsTrack.add_section()
	master_tc_start = cam_tc_start[x]
	master_tc_end = cam_tc_end[x]
	section.set_end_frame(master_tc_end)
	section.set_start_frame(master_tc_start)

	#add your shot sequence to the section
	sequence_insert_str = f"/Game/{cam_name}"
	print(sequence_insert_str)
	shot = unreal.load_asset(sequence_insert_str)
	section.set_editor_property('sub_sequence', shot)

	#level_sequence.set_playback_start(tc_start2 - 32)
	#level_sequence.set_playback_end(tc_end + 32)

	x = x + 1
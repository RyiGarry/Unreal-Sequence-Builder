# Unreal-Sequence-Builder

This is a Pythonesque way to create a master sequence made up of imported individual cameras in Unreal Engine - for instance if you have 3D tracks for real-world cameras that you want to assemble into a single sequence. The script places a load of individual level sequences into a master sequence, and also adjusts the keys of the level sequences to match their position in the master sequence.

See here for a quick example of how it works: https://youtu.be/552k8l18VUA

I've also included the sample project (pre-Python) to show how the cams and level sequences should be set up. This is just a sample with 10 cameras, but the true value of it is if you have a lot (100s) of tracked cameras imported that you need assembled into a master sequence.

Tested on Unreal 4.27, make sure to enable Sequencer Scripting plugin.

This is for a 24fps sequence, but this can be changed on lines 158 and 159 (change //24 to your chosen frame rate).

-----

One issue is that the camera cut tracks in the indiviual level sequences are replaced with an empty track (rather than being bound to the existing camera in the sequence). This is because originally the script was built to take a posessable camera that existed in the scene and create an attach track to attach it to a spawnable camera in the level sequence. The spawnable camera would've been assigned the camera cut track, but as that's not happening here (just using the existing camera in the sequencer) it creates an empty camera cut track.

The issue is on line 77 - [camera = unreal.load_object(None, f"/Game/Map.Map:PersistentLevel.{cam_name}")] - this needs to load the CineCameraActor in the level sequence (probably referencing the level_sequence_str). Will try and look at it when I can for that sake of completeness. I've left that code section in though as it creates a camera cut section over the level sequence that illustrates what'd happen.

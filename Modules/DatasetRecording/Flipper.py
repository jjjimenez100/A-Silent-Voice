import Modules.DatasetRecording.ImageFlipper as imgfli


DIRECTORY = "D:\moreframs/frames"
FRAME_START = 1201

iflipper = imgfli.FlipImages(DIRECTORY, FRAME_START)
iflipper.start()
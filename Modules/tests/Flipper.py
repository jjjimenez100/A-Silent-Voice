import Modules.tests.ImageFlipper as imgfli


DIRECTORY = ""
FRAME_START = 0

iflipper = imgfli.FlipImages(DIRECTORY, FRAME_START)
iflipper.start()
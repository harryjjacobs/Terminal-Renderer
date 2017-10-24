"""
Harry Jacobs

Some useful resources that helped me:
https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#cursor-navigation

This script has been tested on linux only. It will not run in the windows
command prompt unless you are using ANSICON or other similar programs or a
very old version of windows. See more here:
https://stackoverflow.com/questions/16755142/how-to-make-win32-console-recognize-ansi-vt100-escape-sequences

---
Usage:

When run without arguments the script will look for the apple.jpg in 
the current directory.

If an alternative file is provided, it will try to render that. If a
directory is provided, the program will loop forever through each 
file, creating an animation. The frame rate can be set in the code 
below (fps). I have noticed when running with python2 the animation
lags considerably more than when using python 3.

The file can be imported as a module as well.
---
"""

import os
import sys
import time
from PIL import Image

UP = u'\u001b[{n}A'
DOWN = u'\u001b[{n}B'
CLEAR_LINE = u"\u001b[1000D"
BLOCK = u'\u2588'
BEGIN_COLOR = u'\u001b[38;2;{r};{g};{b}m' # 38 means foreground, 2 specifies 24 bit color
END_COLOR = u'\u001b[0m'
NEWLINE = '\n'

class TerminalRenderer():
	"""
	A class is used so that it can be used to render
	new images over the top of existing ones.
	In order to do this the cursor must be moved back
	to the top at the start of each render.
	There are 'try: excepts' everywhere so we can clean
	up properly on exit.
	"""
	write = sys.stdout.write

	def __init__(self):
		self.current_height = -1

	def render(self, path):
		im = Image.open(path)
		rgb_im = im.convert('RGB')
		width, height = rgb_im.size
		# jump to top if height set
		self.write(UP.format(n=self.current_height))
		# store image height for resetting/overwrite
		self.current_height = height

		try:
			for y in range(height):
				try:
					self.write(CLEAR_LINE) # clear previous row by shifting 1000 places
					for x in range(width):
						self.write_block(rgb_im.getpixel((x, y)))
					self.new_line()
				except:
					self.reset()
					quit()
		except:
			self.reset()
			quit()

	def new_line(self):
		try:
			self.write(NEWLINE)
		except:
			self.reset()
			quit()

	def write_block(self, rgb):
		try:
			# draw block
			self.write(BEGIN_COLOR.format(r=rgb[0], g=rgb[1], b=rgb[2]) + BLOCK + END_COLOR)
		except:
			self.reset()
			quit()

	def reset(self):
		# used to jump down so that when control is 
		# returned to the console we are not on top
		# of the image
		self.write(DOWN.format(n=self.current_height))
		self.write(CLEAR_LINE)


if __name__ == "__main__":
	fps = 8
	tr = TerminalRenderer()

	file = "apple.jpg"
	files = []
	if len(sys.argv) >= 2:
		if os.path.isdir(sys.argv[1]):
			for frame in os.listdir(sys.argv[1]):
				files.append(os.path.join(sys.argv[1], frame))
		else:
			tr.render(sys.argv[1])
			quit()
	else:
		tr.render(file)
		quit()

	while True:
		for file in files:
			tr.render(file)
			try:
				time.sleep(1/fps)
			except:
				tr.reset()
				quit()
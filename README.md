# Uni task to make a program render an image using the console.

Note:
This script has been tested on linux only. It will not run in the windows
command prompt unless you are using ANSICON or another similar program or
an old version of windows. See more here:
https://stackoverflow.com/questions/16755142/how-to-make-win32-console-recognize-ansi-vt100-escape-sequences

Usage:

When run without arguments the script will look for the apple.jpg in 
the current directory.

If an alternative file is provided, it will try to render that. If a
directory is provided, the program will loop forever through each 
file, creating an animation. The frame rate can be set in the code 
below (fps). I have noticed when running with python2 the animation
lags considerably more than when using python 3.

The file can be imported as a module as well.
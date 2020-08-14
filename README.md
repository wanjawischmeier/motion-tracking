# motion-tracking
 
My attempt on creating a simple motion-tracking 'framework' for unity using python.

It should track both hands via a simple opencv-python color detection algorithym, and then write the position to a mmf (memory-mapped-file).
A simple C# class can read the bytes from that file and set them as variables, which can then be easily acessed via another script created by the user.
The whole reading-process of course works async and not on the ui-thread.

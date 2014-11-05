import sys
import time
import re
from Tkinter import *
from dxfwrite import DXFEngine as dxf;

###################################################
## Tree Generation
###################################################

`

def tree_gen_wrapper(max_depth):
    tree_gen(max_depth,0)

# DXF Generation
class Point: 
	def __init__(self, in_x, in_Y, isDown):
		self.x = in_x
		self.y = in_y
		self.penDown = isDown

 

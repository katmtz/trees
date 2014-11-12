import sys
import time
import re
import math
import random
import getopt
from Tkinter import *
from dxfwrite import DXFEngine as dxf

###################################################
## Global Declarations
###################################################
(x,y) = (400,600)
(startx,starty) = (400,600)
theta = 90
master = Tk()
canvas = Canvas(master,width=800,height=800)
coords = []

##################################################
# DXF Generation
##################################################
class Point: 
    def __init__(self, in_x, in_y):
        self.x = in_x
        self.y = in_y

def dxf_gen():
    drawing = dxf.drawing(sys.argv[2] + ".dxf")
    drawing.header['$LUNITS'] = 4
    drawing.add_layer('LINES')

    for i in xrange(len(coords)):
       drawing.add(dxf.line((coords[i-1].x, coords[i-1].y),
                                  (coords[i].x,coords[i].y),
                                  color=1,
                                  layer='LINES'))

    drawing.save()

############################################################
# Tree Generation
############################################################

def forward(dist,color='red'):
    global x,y
    newx = x - dist * math.cos(math.radians(theta))
    newy = y - dist * math.sin(math.radians(theta))
    canvas.create_line(int(x),int(y),int(newx),int(newy), fill=color)
    (x,y) = (newx,newy)
    coords.append(Point(x,y))

def left(dist, color='red'):
    global x,y
    newx = x - dist
    canvas.create_line(x,y, newx, y, fill=color)
    (x,y) = (newx,y)
    coords.append(Point(x,y))

def right(dist, color='red'):
    global x,y
    newx = x + dist
    canvas.create_line(x,y,newx,y,fill=color)
    (x,y) = (newx,y)
    coords.append(Point(x,y))

def down(dist, color='red'):
    global x,y
    newy = y + dist
    canvas.create_line(x,y,x,newy,fill=color)
    (x,y) = (x,newy)
    coords.append(Point(x,y))

def turn(angle):
    global theta
    theta = theta + angle

def square():
    turn(-45)
    for i in range(3):
        forward(10)
        turn(90)
    forward(6)
    turn(90+45)

def hexagon():
    turn(-60)
    for i in range(5):
        forward(10)
        turn(60)
    forward(4)
    turn(60+60)

def tree_gen():
    choices = [square, hexagon, hexagon,tree_gen, tree_gen,tree_gen]
    branch_angle = 30
    turn(-branch_angle)
    forward(30)
    random.choice(choices)()
    forward(-30)
    turn(2*branch_angle)
    forward(30)
    random.choice(choices)()
    forward(-30)
    turn(-branch_angle)

def drawbase(standtype):
    print "Draw base ", standtype
    if standtype == "A":
        forward(40, 'blue')
    else:
        forward(50, 'blue')

def finishbase(standtype):
    print "Finish base", standtype
    down(35,'blue')
    if standtype == "A":
        right(10, 'blue')
        down(10, 'blue')
        right(4,'blue')
        forward(10, 'blue')
        right(10, 'blue')
        down(starty-y, 'blue')
        left(x-startx, 'blue')
        
    else:
        right(25, 'blue')
        down(starty-y,'blue')
        left(10,'blue')
        forward(10,'blue')
        left(4, 'blue')
        down(10, 'blue')
        left(x-startx, 'blue')
        
#################################################################
# MAIN
#################################################################

def main(argv):
    standtype = "A"
    try:
        opts, args = getopt.getopt(argv, "hs:",["standtype="])
    except getopt.GetoptError:
        print 'Usage: trees.py -s [A|B]'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: trees.py -s [A|B]'
            sys.exit()
        elif opt in ("--standtype"):
            if arg == "A" or arg == "B":
                standtype = arg
            else: 
                print 'Standtype must be A or B'
                sys.exit(2)

    print "Drawing a tree with stand type", standtype

    canvas.pack()
    drawbase(standtype)
    tree_gen()
    finishbase(standtype)

    dxf_gen()

if __name__ == "__main__":
    main(sys.argv[1:])
    mainloop()

import math
import numpy
import yaml


configs = yaml.load( file('../local/config.yaml') )
window_size_h = configs['options']['resolution'][0]
window_size_v = configs['options']['resolution'][1]


def translate(x,y,z):
    """ Return a translation matrix. """
    return [
        [1.0,0,0,x],
        [0,1.0,0,y],
        [0,0,1.0,z],
        [0,0,0,1.0]
    ]

def rotate(x,y):
    """ Return a rotation matrix. It rotates around the x- and y- axes. """

    rot_x = [
        [1.0,0,0,0],
        [0,math.cos(x),-math.sin(x),0],
        [0,math.sin(x),math.cos(x),0],
        [0,0,0,1.0]
    ]
    rot_y = [
        [math.cos(y),0,math.sin(y),0],
        [0,1.0,0,0],
        [-math.sin(y),0,math.cos(y),0],
        [0,0,0,1.0]
    ]
    return numpy.dot(rot_x, rot_y)

def scale(x, y, z):
    """ Return a scaling matrix. """
    return [
        [x,0,0,0],
        [0,y,0,0],
        [0,0,z,0],
        [0,0,0,1.0]
    ]


# Numbers needed for depth perception
fzNear = 10.0
fzFar = 510.0
#frustumScale = 2.7 # Gots to be just enough to englobe the whole field
frustumScale = 1.0 # Gots to be just enough to englobe the whole field

# Numbers about "camera"
length_of_field = 500
width_of_field = 200
elevation_of_camera = 100
push_back_of_camera_from_field = 100
push_back_of_camera = length_of_field/2.0 + push_back_of_camera_from_field
angle_of_camera = math.atan( float(elevation_of_camera)/float(push_back_of_camera))

perspectiveMatrix = [
    [frustumScale/(1440.0/900.0),  0,              0,                                  0],
    [0,             frustumScale,   0,                                  0],
    [0,             0,              (fzFar + fzNear) / (fzNear-fzFar),  (2*fzFar * fzNear) / (fzNear - fzFar)],
    [0,             0,              -1.0,                               0.0]
]

# Our transformations applied by doing dot products.
translation_of_camera =  translate(0.0, -elevation_of_camera, -push_back_of_camera)
rotation_of_camera = rotate(angle_of_camera, 0.0)
camera_matrix = numpy.dot(rotation_of_camera, translation_of_camera)
camera_matrix = numpy.dot(scale(1.0,-1.0,1.0), camera_matrix)
camera_matrix = numpy.dot(perspectiveMatrix, camera_matrix)

inverse_camera_matrix = numpy.linalg.inv(perspectiveMatrix)
inverse_camera_matrix = numpy.dot(numpy.linalg.inv(scale(1.0,-1.0,1.0)), inverse_camera_matrix)
inverse_camera_matrix = numpy.dot(numpy.linalg.inv(rotation_of_camera), inverse_camera_matrix)
inverse_camera_matrix = numpy.dot(numpy.linalg.inv(translation_of_camera), inverse_camera_matrix)

c = rotate(math.pi/2.0-angle_of_camera, 0.0)
#c = numpy.dot(translate(), c)


def distance_squared(position1, position2):
	return (position1[0]-position2[0])**2 + (position1[1]-position2[1])**2 + (position1[2]-position2[2])**2

def pos_to_2d(position):
    """ Transform the current <x,y,z> point to a <x,y> point that will appear
        on the screen. That means we apply transformations to the point. """

    out = numpy.dot(camera_matrix, position+[1] )
    for i in range(len(out)):
        out[i] /= out[3]
    out[0] *= window_size_h
    out[1] *= window_size_v
    out[0] += window_size_h/2.0
    out[1] += window_size_v/2.0
    out2 = ( int(out[0]), int(out[1]) )
    return out2

def point_to_pos(position):
    """ Transform the current <x,y> point to a <x,y,z> point that will be used
    in game. That means we need to do the reverse from what pos_to_2d is doing. """
    out = position
    out[0] -= window_size_h/2.0
    out[1] -= window_size_v/2.0
    out[0] /= window_size_h
    out[1] /= window_size_v
    out = numpy.dot(inverse_camera_matrix, list(position)+[-1,1])
    for i in range(len(out)):
        out[i] /= out[3]
    return tuple(out[0:3])

import copy

# Method 1: more precise
p = list(point_to_pos( [730, 20] ))+[1]
print p

cam_pos = [0, elevation_of_camera, push_back_of_camera]

direction = [cam_pos[0]-p[0], cam_pos[1]-p[1], cam_pos[2]-p[2]]
diff = [0, -elevation_of_camera, -push_back_of_camera]
dist = numpy.dot(diff, [0,1,0]) / numpy.dot(direction, [0,1,0])
pos = cam_pos+numpy.dot(dist, direction)

print "dist:", dist
print ">>>", pos
print "pos_to_2d:", pos_to_2d(list(pos))

p = list(point_to_pos( [730, 20] ))+[1]

# Method 2: less precise, uses matrices...
print p
res = numpy.dot(translate(0.0, -elevation_of_camera, -push_back_of_camera), p)
print res
res = numpy.dot(rotate(angle_of_camera-math.pi/2.0, 0), res)
res[1] += 10
res[0] *= 361.821/3.2
res[2] *= 431.481/2.0
print res



__author__ = 'binroot'

import bpy
from mathutils import Vector
from mathutils.geometry import intersect_ray_tri
import random
from scipy.spatial import cKDTree as KDTree
import numpy as np
import csv
import sys

HANG_POINT_SAMPLES = 300
NUM_NEIGHBORS = 15
HANG_SIZE = 4

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print("argv: " + str(sys.argv))
if len(sys.argv) < 4 or len(sys.argv) > 5:
    print(bcolors.FAIL + "[ ✘ ] Usage: blender --background  --python gen_points.py <file>.3ds" + bcolors.ENDC)
    sys.exit(0)

if not sys.argv[-1].endswith(".3ds"):
    print(bcolors.FAIL + "[ ✘ ] Usage: blender --background  --python gen_points.py <file>.3ds" + bcolors.ENDC)
    sys.exit(0)

CLOTH_FILE = sys.argv[-1]

C = bpy.context
D = bpy.data
O = bpy.ops

def init():
    O.object.mode_set(mode='OBJECT')
    O.object.delete()

def import_obj(filename):
    # Import the cloth
    print(bcolors.OKBLUE + 'Importing ' + filename + bcolors.ENDC)
    O.import_scene.autodesk_3ds('EXEC_DEFAULT', filepath=filename)
    obj = D.objects[2]
    C.scene.objects.active = obj
    O.transform.rotate(1, axis=(1, 0, 0))
    return obj

def pick_indices(obj, indices):
    # Set the paint brush size
    D.scenes['Scene'].tool_settings.unified_paint_settings.size = HANG_SIZE

    # Mark vertex to hang
    obj.vertex_groups.new('Group')
    obj.vertex_groups['Group'].add(indices, 1.0, 'REPLACE')

def reset():
    init()
    return import_obj(CLOTH_FILE)

obj = reset()

# get all candidate hang points
vertices = obj.data.vertices
v_data = []
for v in vertices:
    v_data.append((list(v.co), v.index))


sampled_vertices = []
indices = []
with open('points.csv', 'w', newline='', encoding='utf8') as csvfile:
    writer = csv.writer(csvfile)
    while (len(sampled_vertices) < HANG_POINT_SAMPLES) and len(v_data) > 0:
        # build kd tree
        arrayOfPoints = np.array(list(zip(*v_data))[0]) # [ [1,2,3], [4,5,6] ]
        kdTreeOfPoints = KDTree(arrayOfPoints)

        # sample a point
        rand_idx = random.randint(0, len(v_data)-1)
        sampled_vertices.append(v_data[rand_idx])
        # print("v_data size: " + str(len(v_data)))
        # print("arrayOfPoints size: " + str(len(arrayOfPoints)))
        # print("rand_idx: " + str(rand_idx))
        hang_point = v_data[rand_idx][0]
        hang_index = v_data[rand_idx][1]

        # write [hang_index, x, y, z]
        indices.append(hang_index)
        row = [hang_index] + list(hang_point);
        writer.writerow(row)
        print(str(row))

        # remove some of its neighbors
        #print("rand_idx " + str(rand_idx))
        #print("size of ArrayOfPoints: " + str(len(ArrayOfPoints)))
        dists,idxs = kdTreeOfPoints.query(hang_point, NUM_NEIGHBORS)
        # print("query at " + str(hang_point))
        #print("idxs: " + str(idxs))
        neighbors_to_remove = []
        removeAll = False
        for n_idx in idxs:
            # print("n_idx: " + str(n_idx))
            # print("v_data size: " + str(len(v_data)))
            if n_idx < len(v_data):
                neighbor = v_data[n_idx]
                #print("neighbor: " + str(neighbor))
                neighbors_to_remove.append(neighbor)
            else:
                removeAll = True

        for neighbor in neighbors_to_remove:
            #print("removing " + str(neighbor))
            v_data.remove(neighbor)
        if removeAll:
            v_data.clear()

    pick_indices(obj, indices)
    # print(sampled_vertices)
print(bcolors.OKGREEN + "[ ✓ ] Saved points.csv" + bcolors.ENDC)
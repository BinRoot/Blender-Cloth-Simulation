__author__ = 'robot'

import bpy
import sys
import os

HANG_SIZE = 8   # the weight paintbrush size
SIMULATION_END_FRAME = 300

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
if len(sys.argv) < 5 or len(sys.argv) > 6:
    print(bcolors.FAIL + "[ ✘ ] Usage: blender --background --python simulate.py <file>.3ds <index>" + bcolors.ENDC)
    sys.exit(0)

if not sys.argv[-2].endswith('.3ds'):
    print(bcolors.FAIL + "[ ✘ ] Usage: blender --background --python simulate.py <file>.3ds <index>" + bcolors.ENDC)
    sys.exit(0)

OUTPUT_DIR = 'output/'
CLOTH_FILE = sys.argv[-2]
INDEX = int(sys.argv[-1])

C = bpy.context
D = bpy.data
O = bpy.ops

def init():
    O.object.mode_set(mode='OBJECT')

    # Delete the initial cube
    O.object.delete()

def import_obj(filename):
    #O.object.mode_set(mode='OBJECT')

    # Import the cloth
    print('Importing ' + filename)
    O.import_scene.autodesk_3ds('EXEC_DEFAULT', filepath=filename)
    obj = D.objects[2]
    C.scene.objects.active = obj
    O.transform.rotate(1, axis=(1, 0, 0))
    return obj

def set_up_cloth_for_simulation(obj, index):
    O.object.mode_set(mode='WEIGHT_PAINT')

    # Set the paint brush size
    D.scenes['Scene'].tool_settings.unified_paint_settings.size = HANG_SIZE

    # Mark vertex to hang
    obj.vertex_groups.new('Group')
    obj.vertex_groups['Group'].add([index], 1.0, 'REPLACE')

    O.object.mode_set(mode='OBJECT')

    # Add cloth modifier
    print("Adding cloth modifier");
    O.object.modifier_add(type='CLOTH')

    # Add solidify modifier
    print("Adding solidify modifier")
    O.object.modifier_add(type='SOLIDIFY')

    # Add subsurf modifier, and change levels to 2
    print("Adding subsurf modifier, and changing levels to 2")
    O.object.modifier_add(type='SUBSURF')
    obj.modifiers['Subsurf'].levels = 2

    O.object.shade_smooth()

    # Set cloth presets
    print("Setting cloth type to cotton, and increasing steps")
    obj.modifiers['Cloth'].settings.quality = 10
    obj.modifiers['Cloth'].settings.use_pin_cloth = True
    obj.modifiers['Cloth'].settings.vertex_group_mass = 'Group'
    obj.modifiers['Cloth'].collision_settings.use_self_collision = True

def run_simulation():
    for frame in range(0, SIMULATION_END_FRAME):
        print("rendering frame " + str(frame))
        C.scene.frame_set(frame)
        C.active_object.keyframe_insert("location") # optional?
    print("finished rendering")

def export_obj(filename):
    O.object.modifier_apply(modifier='Cloth')
    O.export_scene.obj(filepath=filename)

def simulate_cloth_hanging(obj, index):
    print("simulating cloth hang at index " + str(index))
    set_up_cloth_for_simulation(obj, index)
    run_simulation()
    cloth_name = os.path.basename(CLOTH_FILE).split('.')[0]
    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    export_obj(OUTPUT_DIR + cloth_name + '_' + str(index) + ".obj")

def reset():
    init()
    return import_obj(CLOTH_FILE)

obj = reset()
simulate_cloth_hanging(obj, INDEX)
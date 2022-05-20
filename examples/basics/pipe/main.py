import blenderproc as bproc
import numpy as np
import bpy

scene_path = "examples/basics/pipe/test.obj"
blend_path = "examples/basics/pipe/pipa_hijau.blend"

bproc.init()

# load the objects into the scene
objs = bproc.loader.load_blend(blend_path)

# define a light and set its location and energy level
light = bproc.types.Light()
light.set_type("POINT")
light.set_location([5, -5, 5])
light.set_energy(1000)

light = bproc.types.Light()
light.set_type("POINT")
light.set_location([-2, -1, 2.5])
light.set_energy(1000)

bpy.context.view_layer.objects.active = bpy.data.objects['Plane']
bpy.context.object.modifiers["Screw"].screw_offset = 2.2

# define the camera resolution
bproc.camera.set_resolution(512, 512)

with open("examples/resources/camera_positions", "r") as f:
    for line in f.readlines():
        line = [float(x) for x in line.split()]
        position, euler_rotation = line[:3], line[3:6]
        matrix_world = bproc.math.build_transformation_mat(position, euler_rotation)
        bproc.camera.add_camera_pose(matrix_world)
        break


# activate normal and depth rendering
bproc.renderer.enable_normals_output()
bproc.renderer.enable_depth_output(activate_antialiasing=False)

data = bproc.renderer.render()

# Render segmentation masks (per class and per instance)
data.update(bproc.renderer.render_segmap(map_by=["class", "instance", "name"]))

# write the data to a .hdf5 container
bproc.writer.write_hdf5("examples/basics/pipe/output", data)
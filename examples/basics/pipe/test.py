import blenderproc as bproc
import numpy as np
import bpy

blend_path = "examples/basics/pipe/pipe.blend"

bproc.init()

# load the objects into the scene
objs = bproc.loader.load_blend(blend_path)

# define a light and set its location and energy level
light1 = bproc.types.Light()
light1.set_type("POINT")
light1.set_location([0.0648, -5.10561, 5.54109])
light1.set_energy(1000)

light2 = bproc.types.Light()
light2.set_type("POINT")
light2.set_location([5, -4.83221, 5])
light2.set_energy(1000)

light3 = bproc.types.Light()
light3.set_type("POINT")
light3.set_location([2.58102, -2.18806, 5])
light3.set_energy(10.6)
light3.set_color([255,0,0])



# define the camera resolution
bproc.camera.set_resolution(512, 512)
bproc.camera.set_intrinsics_from_blender_params(lens=0.10)

line = [0, -16.671, 4.0742,  1.57, 0, 0]
position, euler_rotation = line[:3], line[3:6]
matrix_world = bproc.math.build_transformation_mat(position, euler_rotation)
bproc.camera.add_camera_pose(matrix_world)



# activate normal and depth rendering
bproc.renderer.enable_normals_output()
bproc.renderer.enable_depth_output(activate_antialiasing=False)

data = bproc.renderer.render()

# Render segmentation masks (per class and per instance)
data.update(bproc.renderer.render_segmap(map_by=["class", "instance", "name"]))

# write the data to a .hdf5 container
bproc.writer.write_hdf5("examples/basics/pipe/output", data)
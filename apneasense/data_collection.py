from pyrender import Mesh, Scene, Viewer
import trimesh

watch_file_path = "\smartwatch\smartwatch_3d.glb"

watch = trimesh.load(watch_file_path, file_type='glb')

watch_meshes = []
for geometry in watch.geometry.values():
    mesh = Mesh.from_trimesh(geometry)
    watch_meshes.append(mesh)

scene = Scene()
for mesh in watch_meshes:
    scene.add(mesh)

viewer = Viewer(scene,use_raymond_lighting=True)

while not viewer.is_done():
    viewer.render()
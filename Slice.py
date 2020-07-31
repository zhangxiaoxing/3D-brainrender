import brainrender
from brainrender.Utils import actors_funcs as af
brainrender.SHADER_STYLE = 'cartoon'  # plastic
brainrender.ROOT_COLOR = 'transparent'
brainrender.ROOT_ALPHA = .1
from brainrender.scene import Scene

scene = Scene()
root = scene.actors['root']
th = scene.add_brain_regions(['STR', 'TH'], alpha=3)  #solid wireframe,这两个参数默认为False

pos1 = [4000, 3849, 5688.5]
sx, sy = 15000, 15000              # 设置平面大小
norm1 = [-1, 0, 0]                   # 设置平面方向（目测是法向量）,根据法向量的正负可以操纵切面的方向
plane1 = scene.atlas.get_plane_at_point(pos1, norm1, sx, sy, color='lightblue')
scene.cut_actors_with_plane(plane1, close_actors=True, showplane=False)

pos2 = [3990, 3849, 5688.5]
sx, sy = 15000, 15000              # 设置平面大小
norm2 = [1, 0, 0]                   # 设置平面方向（目测是法向量）,根据法向量的正负可以操纵切面的方向
plane2 = scene.atlas.get_plane_at_point(pos2, norm2, sx, sy, color='lightblue')  #color='lightblue'
scene.cut_actors_with_plane(plane2, close_actors=True, showplane=False)   #close_actor=True可以使得截面变薄，但是无法使截面颜色均匀

scene.render(camera='coronal', zoom=0.8)







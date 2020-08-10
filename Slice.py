import brainrender

brainrender.SHADER_STYLE = 'ambient'  # plastic
brainrender.DEFAULT_STRUCTURE_ALPHA = 1
brainrender.DISPLAY_ROOT=True

brainrender.ROOT_COLOR = 'transparent'
brainrender.ROOT_ALPHA = 0.1
from ZXScene import ZXScene

scene = ZXScene()
root = scene.actors['root']
th = scene.add_brain_regions(['STR','TH'])  # solid wireframe,这两个参数默认为False

pos1 = [4000, 3849, 5688.5]
sx, sy = 15000, 15000  # 设置平面大小
norm1 = [-1, 0, 0]  # 设置平面方向（目测是法向量）,根据法向量的正负可以操纵切面的方向
plane1 = scene.atlas.get_plane_at_point(pos1, norm1, sx, sy, color='lightblue')
scene.cut_actors_with_plane(plane1, close_actors=True, showplane=False)  # close_actor=True可以使得截面变薄，但是无法使截面颜色均匀

pos2 = [3990, 3849, 5688.5]
norm2 = [1, 0, 0]  # 设置平面方向（目测是法向量）,根据法向量的正负可以操纵切面的方向
plane2 = scene.atlas.get_plane_at_point(pos2, norm2, sx, sy, color='lightblue')  # color='lightblue'
scene.cut_actors_with_plane(plane2, close_actors=True, showplane=False)  # close_actor=True可以使得截面变薄，但是无法使截面颜色均匀

pos3 = [4010, 3849, 5688.5]
sx, sy = 15000, 15000  # 设置平面大小
norm1 = [-1, 0, 0]  # 设置平面方向（目测是法向量）,根据法向量的正负可以操纵切面的方向
plane3 = scene.atlas.get_plane_at_point(pos3, norm1, sx, sy, color='lightblue')
scene.cut_root_with_plane(plane1, close_actors=True, showplane=False)  # close_actor=True可以使得截面变薄，但是无法使截面颜色均匀

pos4 = [3980, 3849, 5688.5]
norm2 = [1, 0, 0]  # 设置平面方向（目测是法向量）,根据法向量的正负可以操纵切面的方向
plane4 = scene.atlas.get_plane_at_point(pos4, norm2, sx, sy, color='lightblue')  # color='lightblue'
scene.cut_root_with_plane(plane4, close_actors=True, showplane=False)  # close_actor=True可以使得截面变薄，但是无法使截面颜色均匀

scene.render(camera='coronal', zoom=0.8)


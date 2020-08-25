import brainrender
from scipy.io import loadmat
from ZXScene import ZXScene
brainrender.SHADER_STYLE = 'ambient'  # plastic
brainrender.DEFAULT_STRUCTURE_ALPHA = 1
brainrender.DISPLAY_ROOT = True
brainrender.ROOT_COLOR = 'gray'
brainrender.ROOT_ALPHA = 1
brainrender.DISPLAY_INSET = False
from matplotlib import cm
import os
import numpy as np
data = loadmat(r'C:\Users\Fish\Desktop\BrainRender-master\opgenstats.mat')
sums = []
dist = []
for i in range(len(data['opgenStats'][0][0][0])):
    reg = data['opgenStats'][0][0][1][i][0][0]
    tran = data['opgenStats'][0][0][0][i][0]
    sums.append([reg, tran])
    dist.append(tran)

dmin = np.floor(-0.7 * 100).astype(np.int)#np.floor(np.min(dist) * 100).astype(np.int)
dmax = np.floor(0.7 * 100).astype(np.int)#np.floor(np.max(dist) * 100).astype(np.int)

jmap = cm.get_cmap('jet', dmax - dmin + 1)
jetmap = jmap(range(dmax - dmin + 1))
scene = ZXScene(display_inset=False, base_dir=r'D:\figure_0817\figure6')

deep = 9193
thick = 10
pos1 = [deep, 3849, 5688.5]
sx, sy = 15000, 15000  # 设置平面大小
norm1 = [-1, 0, 0]  # 设置平面方向（目测是法向量）,根据法向量的正负可以操纵切面的方向
plane1 = scene.atlas.get_plane_at_point(pos1, norm1, sx, sy, color='lightblue')
pos2 = [deep-thick, 3849, 5688.5]
norm2 = [1, 0, 0]  # 设置平面方向（目测是法向量）,根据法向量的正负可以操纵切面的方向
plane2 = scene.atlas.get_plane_at_point(pos2, norm2, sx, sy, color='lightblue')  # color='lightblue'

for s in sums:
    cmIdx = np.floor(s[1] * 100).astype(np.int) - dmin
    scene.add_brain_regions([s[0]], colors=jetmap[cmIdx][:3], use_original_color=False, alpha=1, add_labels=False) # alpha值设置透明度，越小越透明
    scene.cut_actors_with_plane(plane1, close_actors=True, showplane=False)  # close_actor=True可以使得截面变薄，但是无法使截面颜色均匀
    scene.cut_actors_with_plane(plane2, close_actors=True, showplane=False)  # close_actor=True可以使得截面变薄，但是无法使截面颜色均匀
    pos1[0] = pos1[0]+.1
    pos2[0] = pos2[0]-.1
    plane1 = scene.atlas.get_plane_at_point(pos1, norm1, sx, sy, color='lightblue')
    plane2 = scene.atlas.get_plane_at_point(pos2, norm2, sx, sy, color='lightblue')  # color='lightblue'

pos3 = [deep, 3849, 5688.5]  #deep+thick
plane3 = scene.atlas.get_plane_at_point(pos3, norm1, sx, sy, color='lightblue')  # color='lightblue'
scene.cut_root_with_plane(plane3, close_actors=True, showplane=False)  # close_actor=True可以使得截面变薄，但是无法使截面颜色均匀

pos4 = [deep-thick, 3849, 5688.5]  #deep-2*thick
plane4 = scene.atlas.get_plane_at_point(pos4, norm2, sx, sy, color='lightblue')  # color='lightblue'
scene.cut_root_with_plane(plane4, close_actors=False, showplane=False)  # close_actor=True可以使得截面变薄，但是无法使截面颜色均匀

scene.screenshots_folder = r'D:\figure_0817\figure6\no_name_new'
if not os.path.exists(scene.screenshots_folder):
    os.makedirs(scene.screenshots_folder)
scene.screenshots_name = 'cut_Deep=' + str(deep)

scene.render(camera='coronal', zoom=0.8, interactive=False)
scene.take_screenshot()

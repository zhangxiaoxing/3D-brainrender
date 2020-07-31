# ENTI换脑区名字为ENT
from scipy.io import loadmat
import numpy as np
from matplotlib import cm
import brainrender
from brainrender.scene import Scene
import h5py
import vtkmodules as vtk
import os
import pandas as pd
brainrender.SHADER_STYLE = 'cartoon'
brainrender.WHOLE_SCREEN = True
brainrender.DISPLAY_INSET = False
brainrender.WHOLE_SCREEN = True
data = loadmat(r'C:\Users\Fish\Desktop\BrainRender-master\opgenstats.mat')
# data.keys()
#data['opgenStats'][0][0][1]
sums = []
dist = []
for i in range(len(data['opgenStats'][0][0][0])):
    reg = data['opgenStats'][0][0][1][i][0][0]
    tran = data['opgenStats'][0][0][0][i][0]
    sums.append([reg, tran])
    dist.append(tran)

dmin = np.floor(np.min(dist) * 100).astype(np.int)
dmax = np.floor(np.max(dist) * 100).astype(np.int)

jmap = cm.get_cmap('jet', dmax - dmin + 1)
jetmap = jmap(range(dmax - dmin + 1))
scene = Scene(display_inset=False, base_dir=r'D:\PyCharmProject\brain3Dtest\result')
Actors = []
name = []
color = []
for s in sums:
    cmIdx = np.floor(s[1] * 100).astype(np.int) - dmin
    Actors.append(scene.add_brain_regions([s[0]], colors=jetmap[cmIdx][:3], use_original_color=False, alpha=1,
                                              add_labels=False))  # alpha值设置透明度，越小越透明
    name.append(s[0])
    color.append(cmIdx)


thick = 10
for deep in range(9183, 9383 - thick, 200):
    pos1 = [deep, 3849, 5688.5]
    sx, sy = 15000, 15000  # 设置平面大小
    norm1 = [1, 0, 0]  # 设置平面方向（目测是法向量）,根据法向量的正负可以操纵切面的方向
    plane1 = scene.atlas.get_plane_at_point(pos1, norm1, sx, sy, color='white')  # color='lightblue'

    pos2 = [deep+thick, 3849, 5688.5]
    sx, sy = 15000, 15000  # 设置平面大小
    norm2 = [-1, 0, 0]  # 设置平面方向（目测是法向量）,根据法向量的正负可以操纵切面的方向 -1
    plane2 = scene.atlas.get_plane_at_point(pos2, norm2, sx, sy, color='white', alpha=1)  # color='lightblue'
    scene.cut_actors_with_plane(plane1, close_actors=True, showplane=False)  # , returncut=True
    scene.cut_actors_with_plane(plane2, close_actors=True, showplane=False)
    scene.screenshots_folder = r'D:\screenshot_0728\no_name'
    if not os.path.exists(scene.screenshots_folder):
        os.makedirs(scene.screenshots_folder)

    scene.screenshots_name = 'cut_Deep=' + str(deep) + '~' + str(deep + thick)
    scene.screenshots_extension = 'png'
    scene.render(camera='coronal', zoom=1, interactive=False)  # zoom的大小决定了后边截图的大小
    scene.take_screenshot()



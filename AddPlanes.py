import brainrender

brainrender.SHADER_STYLE = 'cartoon'
brainrender.WHOLE_SCREEN = True
brainrender.DISPLAY_INSET = False
#brainrender.SHOW_AXES = True      # 可以显示坐标轴
brainrender.ROOT_ALPHA = .5  # 设置非渲染部分的透明度
from brainrender.scene import Scene
from matplotlib import cm
import h5py
import numpy as np
from ZXScene import ZXScene
import os
import vtkmodules as vtk
import os


# 读取数据内容(transient.h5py文件)
with h5py.File("transient_6.hdf5", "r") as ffr:
    sus_trans = np.array(ffr["sus_trans"], dtype="int8")
    reg = [x.decode() for x in ffr["reg"]]

reg_set = list(set(reg))
sums = []
for one_reg in reg_set:
    reg_sel = [x == one_reg for x in reg]
    count = np.sum(reg_sel)
    trans = np.sum(np.logical_and(reg_sel, sus_trans[1, :]))
    sums.append([one_reg, count, trans, trans / count])

dist = [x[3] for x in sums if x[1] >= 100]
dmin = np.floor(np.min(dist) * 100).astype(np.int)
dmax = np.floor(np.max(dist) * 100).astype(np.int)

scene = ZXScene(base_dir=r'result')  # 绘制3D旋转视频时camera="sagittal", SCREENSHOT_TRANSPARENT_BACKGROUND=False设置非透明背景，但是好像效果不明显

jmap = cm.get_cmap('jet', dmax - dmin + 1)
jetmap = jmap(range(dmax - dmin + 1))
# Add the whole thalamus in gray
Actors = []
for s in sums:
    if s[1] >= 100 and s[0] != 'Unlabeled' and s[0] != 'root':
        cmIdx = np.floor(s[3] * 100).astype(np.int) - dmin
        # Actors[s[0]] = scene.add_brain_regions([s[0]], colors=jetmap[cmIdx][:3], use_original_color=False, alpha=0.8,
        #                                       add_labels=False)  # alpha值设置透明度，越小越透明
        Actors.append(scene.add_brain_regions([s[0]], colors=jetmap[cmIdx][:3], use_original_color=False, alpha=0.25,
                                              add_labels=False))  # alpha值设置透明度，越小越透明

# 修改此处可以在3D途中的指定位置添加截面
pos1 = [2183, 3849, 5688.5]    #pos = [4000, 3849, 5688.5]  # scene.atlas._root_midpoint   # 设置平面的原点  (单位不知道诶，就很烦，拿100)
sx, sy = 15000, 8000  # 设置平面大小
norm = [1, 0, 0]  # 设置平面方向（目测是法向量）
plane1 = scene.atlas.get_plane_at_point(pos1, norm, sx, sy, color='blue', alpha=.5)

pos2 = [3183, 3849, 5688.5]
plane2 = scene.atlas.get_plane_at_point(pos2, norm, sx, sy, color='blue', alpha=.5)

pos3 = [4183, 3849, 5688.5]
plane3 = scene.atlas.get_plane_at_point(pos3, norm, sx, sy, color='blue', alpha=.5)

pos4 = [5183, 3849, 5688.5]
plane4 = scene.atlas.get_plane_at_point(pos4, norm, sx, sy, color='blue', alpha=.5)

pos5 = [6183, 3849, 5688.5]
plane5 = scene.atlas.get_plane_at_point(pos5, norm, sx, sy, color='blue', alpha=.5)

pos6 = [7183, 3849, 5688.5]
plane6 = scene.atlas.get_plane_at_point(pos6, norm, sx, sy, color='blue', alpha=.5)

pos7 = [8183, 3849, 5688.5]
plane7 = scene.atlas.get_plane_at_point(pos7, norm, sx, sy, color='blue', alpha=.5)

pos8 = [9183, 3849, 5688.5]
plane8 = scene.atlas.get_plane_at_point(pos8, norm, sx, sy, color='blue', alpha=.5)

plane = [plane1, plane2, plane3, plane4, plane5, plane6, plane7, plane8]
scene.add_plane(plane)


# scene.render(camera='sagittal', zoom=1, interactive=False)  # sagittal
scene.render(camera='top', zoom=1, interactive=False)  # top
scene.take_screenshot()
# scene.render(interactive=False)

# scene.export_for_web(filepath=r'D:\savetest\brexport.html')  很生气，这一步报错。

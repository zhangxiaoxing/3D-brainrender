import brainrender
from brainrender.scene import Scene
from matplotlib import cm
import h5py
import numpy as np
import vtkmodules as vtk
import os
brainrender.WHOLE_SCREEN = True
brainrender.ROOT_ALPHA = 1  # 设置非渲染部分的透明度
brainrender.ROOT_COLOR = 'white'  # transparent
brainrender.DISPLAY_INSET = 'True'

# 设置全局变量
brainrender.SHADER_STYLE = 'cartoon'
brainrender.WHOLE_SCREEN = True

# 读取数据内容(transient.h5py文件)
with h5py.File(os.path.join(r"D:\PyCharmProject\brain3Dtest", "transient_6.hdf5"), "r") as ffr:
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

jmap = cm.get_cmap('jet', dmax - dmin + 1)
jetmap = jmap(range(dmax - dmin + 1))
scene = Scene(display_inset=False, base_dir=r'D:\PyCharmProject\brain3Dtest\result')
Actors = []
name = []
color = []
for s in sums:
    if s[1] >= 100 and s[0] != 'Unlabeled' and s[0] != 'root':
        cmIdx = np.floor(s[3] * 100).astype(np.int) - dmin
        Actors.append(scene.add_brain_regions([s[0]], colors=jetmap[cmIdx][:3], use_original_color=False, alpha=1,
                                              add_labels=False))  # alpha值设置透明度，越小越透明
        name.append(s[0])
        color.append(cmIdx)
#scene.render()
thick = 10
for deep in range(8183, 8383 - thick, 200):
    sx, sy = 15000, 15000  # 设置平面大小
    pos = [deep, 3849, 5688.5]
    norm = [1, 0, 0]  # 设置平面方向（目测是法向量）
    plane = scene.atlas.get_plane_at_point(pos, norm, sx, sy, color='lightblue')
    scene1 = Scene(display_inset=False, base_dir=r'D:\PyCharmProject\brain3Dtest\20200727')
    Actors1 = []
    for i in range(len(Actors)):
        if vtk.vtkRenderingCore.vtkActor.GetBounds(Actors[i])[1] < deep or \
                vtk.vtkRenderingCore.vtkActor.GetBounds(Actors[i])[0] > deep + thick:
            continue
        else:
            Actors1.append(scene1.add_brain_regions(name[i], colors=jetmap[color[i]][:3], use_original_color=False,
                                                    alpha=1, add_labels=False))
            scene1.add_actor_label(Actors1[-1], name[i], size=200, color='blackboard', xoffset=-100)
    #scene1.render()
    scene1.cut_actors_with_plane(plane, close_actors=False, showplane=False, add_labels=False)
    scene1.render(camera='coronal', zoom=1, interactive=True)
    #scene.take_screenshot()

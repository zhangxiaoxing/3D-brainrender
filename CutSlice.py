# 跑循环有BUG
import brainrender

brainrender.SHADER_STYLE = 'cartoon'
brainrender.WHOLE_SCREEN = True
brainrender.DISPLAY_INSET = False
import ReadRawDataHDF5 as rr
import vtkmodules as vtk
import brainrender
#brainrender.SHADER_STYLE = 'cartoon'
brainrender.WHOLE_SCREEN = True
# brainrender.SHOW_AXES = True      # 可以显示坐标轴
# brainrender.ROOT_ALPHA = .01  # 设置非渲染部分的透明度
import h5py
import numpy as np
import shutil
import os
import gc

# 此处可更改，用于放置缓存文件，是传递给scene中参数base_dir的
path = r'D:\Render'
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

thick = 10 # 切片厚度，单位不明（可能是微米级）
j = 0
for deep in range(9183, 9383 - thick, 200):  # 13193
    j += 1
    scene, Actors, name = rr.ReadRawData(dmax, dmin, sums, path)
    sx, sy = 15000, 15000  # 设置平面大小
    pos1 = [deep, 3849, 5688.5]
    norm1 = [1, 0, 0]  # 设置平面方向（目测是法向量）
    plane1 = scene.atlas.get_plane_at_point(pos1, norm1, sx, sy, color='lightblue')
    pos2 = [deep + thick, 3849, 5688.5]
    norm2 = [-1, 0, 0]
    plane2 = scene.atlas.get_plane_at_point(pos2, norm2, sx, sy, color='lightblue')
    scene.cut_actors_with_plane(plane1, close_actors=True, showplane=False,
                                add_labels=False)  # scene.actors['root']这一步可以完整显示出我们渲染的部分
    scene.cut_actors_with_plane(plane2, close_actors=True, showplane=False, add_labels=False)

    scene.screenshots_folder = r'D:\screenshot_0727\no_name'
    if not os.path.exists(scene.screenshots_folder):
        os.makedirs(scene.screenshots_folder)

    scene.screenshots_name = 'cut_Deep=' + str(deep) + '~' + str(deep + thick)
    scene.screenshots_extension = 'png'
    scene.render(camera='coronal', zoom=1, interactive=False)  # zoom的大小决定了后边截图的大小
    scene.take_screenshot()
    scene.close()
    del scene, Actors, name
    if j == 15:
        j = 0
        shutil.rmtree(path)
        path = r'D:\Render'
    gc.collect()

j = 0
for deep in range(9183, 9383 - thick, 200):  # -17__13193
    j += 1
    scene, Actors, name = rr.ReadRawData(dmax, dmin, sums, path)
    sx, sy = 15000, 15000  # 设置平面大小
    pos1 = [deep, 3849, 5688.5]
    norm1 = [1, 0, 0]  # 设置平面方向（目测是法向量）
    plane1 = scene.atlas.get_plane_at_point(pos1, norm1, sx, sy, color='lightblue')
    pos2 = [deep + thick, 3849, 5688.5]
    norm2 = [-1, 0, 0]
    plane2 = scene.atlas.get_plane_at_point(pos2, norm2, sx, sy, color='lightblue')
    scene.cut_actors_with_plane(plane1, close_actors=True, showplane=False,
                                add_labels=False)  # scene.actors['root']这一步可以完整显示出我们渲染的部分
    scene.cut_actors_with_plane(plane2, close_actors=True, showplane=False, add_labels=False)
    for i in range(len(Actors)):
        if vtk.vtkRenderingCore.vtkActor.GetBounds(Actors[i])[1] < deep or vtk.vtkRenderingCore.vtkActor.GetBounds(Actors[i])[0] > deep + thick:
            continue
        else:
            scene.add_actor_label(Actors[i], name[i], size=200,
                                  color='blackboard')  # , xoffset=250， 还可以设置 solid wireframe, 可以置为True
    scene.screenshots_folder = r'D:\screenshot_0727\name'
    if not os.path.exists(scene.screenshots_folder):
        os.makedirs(scene.screenshots_folder)

    scene.screenshots_name = 'cut_Deep=' + str(deep) + '~' + str(deep + thick)
    scene.screenshots_extension = 'png'
    scene.render(camera='coronal', zoom=1, interactive=False)  # zoom的大小决定了后边截图的大小
    scene.take_screenshot()
    scene.close()
    del scene, Actors, name
    if j == 15:
        j = 0
        shutil.rmtree(path)
        path = r'D:\Render'
    gc.collect()

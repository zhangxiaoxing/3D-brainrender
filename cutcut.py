"""此代码中是为了画脑区的界面图，根据不同深度，沿x轴（坐标第一维）方向进行迭代切割"""
# 导入各种库
import brainrender

from xxCode import screenshot_params

brainrender.SHADER_STYLE = 'cartoon'
brainrender.WHOLE_SCREEN = True
from brainrender.scene import Scene
from matplotlib import cm
import h5py
import numpy as np
import vtkmodules as vtk
import os


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
"""
screenshot_params = dict(
    folder=r'D:\screenshotsTest\0723',
    name='br0',  # 修改保存的图片的名字， 代码后边会给你加生成时间，精确到日期和秒
    scale=3,  # scale越大分辨率越高，通常大于1
    #    type='.jpg'   # svg图片保存不了？只能保存png和jpg格式,默认为png
)


# Create a scene
scene = Scene(screenshot_kwargs=screenshot_params,
              base_dir=r'D:\PyCharmProject\brain3Dtest\result')  # 绘制3D旋转视频时camera="sagittal", SCREENSHOT_TRANSPARENT_BACKGROUND=False设置非透明背景，但是好像效果不明显
"""
scene = Scene(base_dir=r'D:\PyCharmProject\brain3Dtest\result')  # 绘制3D旋转视频时camera="sagittal", SCREENSHOT_TRANSPARENT_BACKGROUND=False设置非透明背景，但是好像效果不明显

jmap = cm.get_cmap('jet', dmax - dmin + 1)
jetmap = jmap(range(dmax - dmin + 1))
# Add the whole thalamus in gray
Actors = []
for s in sums:
    if s[1] >= 100 and s[0] != 'Unlabeled' and s[0] != 'root':
        cmIdx = np.floor(s[3] * 100).astype(np.int) - dmin
        # Actors[s[0]] = scene.add_brain_regions([s[0]], colors=jetmap[cmIdx][:3], use_original_color=False, alpha=0.8,
        #                                       add_labels=False)  # alpha值设置透明度，越小越透明
        Actors.append(scene.add_brain_regions([s[0]], colors=jetmap[cmIdx][:3], use_original_color=False, alpha=1,
                                              add_labels=False))  # alpha值设置透明度，越小越透明

# Specify position, size and orientation of the plane
for deep in range(-17, 13193, 200):    #13193
    pos = [deep, 3849, 5688.5]
    #pos = [4000, 3849, 5688.5]  # scene.atlas._root_midpoint   # 设置平面的原点  (单位不知道诶，就很烦，拿100)
    sx, sy = 15000, 15000  # 设置平面大小
    norm = [1, 0, 0]  # 设置平面方向（目测是法向量）
    plane = scene.atlas.get_plane_at_point(pos, norm, sx, sy, color='lightblue')

    scene.cut_actors_with_plane(plane, close_actors=False,  # set close_actors to True close the holes left by cutting
                                showplane=True, alpha=1)  # scene.actors['root']这一步可以完整显示出我们渲染的部分


    scene.screenshots_folder = r'D:\screenshot_0726\no_name'
    if not os.path.exists(scene.screenshots_folder):
        os.makedirs(scene.screenshots_folder)

    scene.screenshots_name = 'cut_Deep=' + str(deep)
    scene.screenshots_extension = 'png'
    scene.render(camera='coronal', zoom=0.8, interactive=False)  # zoom的大小决定了后边截图的大小
    scene.take_screenshot()


scene = Scene(base_dir=r'D:\PyCharmProject\brain3Dtest\result')  # 绘制3D旋转视频时camera="sagittal", SCREENSHOT_TRANSPARENT_BACKGROUND=False设置非透明背景，但是好像效果不明显

jmap = cm.get_cmap('jet', dmax - dmin + 1)
jetmap = jmap(range(dmax - dmin + 1))
# Add the whole thalamus in gray
Actors = []
for s in sums:
    if s[1] >= 100 and s[0] != 'Unlabeled' and s[0] != 'root':
        cmIdx = np.floor(s[3] * 100).astype(np.int) - dmin
        # Actors[s[0]] = scene.add_brain_regions([s[0]], colors=jetmap[cmIdx][:3], use_original_color=False, alpha=0.8,
        #                                       add_labels=False)  # alpha值设置透明度，越小越透明
        Actors.append(scene.add_brain_regions([s[0]], colors=jetmap[cmIdx][:3], use_original_color=False, alpha=1,
                                              add_labels=False))  # alpha值设置透明度，越小越透明

for deep in range(-17, 13193, 200):
    pos = [deep, 3849, 5688.5]
    # pos = [4000, 3849, 5688.5]  # scene.atlas._root_midpoint   # 设置平面的原点  (单位不知道诶，就很烦，拿100)
    sx, sy = 15000, 15000  # 设置平面大小
    norm = [1, 0, 0]  # 设置平面方向（目测是法向量）
    plane = scene.atlas.get_plane_at_point(pos, norm, sx, sy, color='lightblue', alpha=1)
    scene.cut_actors_with_plane(plane, close_actors=False, showplane=False) # 注意close_actor的时候，所标的名字里面的圈圈也会被填满
                                 # set close_actors to True close the holes left by cutting
                                 # scene.actors['root']这一步可以完整显示出我们渲染的部分
    # 这个地方需要改一下，当切到3000往上的时候，有些坐标不在里边，这些是标不上去的
    for i in range(len(Actors)):
        if vtk.vtkRenderingCore.vtkActor.GetBounds(Actors[i])[1] < deep:
            break
        else:
            scene.add_actor_label(Actors[i], sums[i], size=100, color='blackboard')  # , xoffset=250， 还可以设置 solid wireframe, 可以置为True

    #screenshot_params['folder']=r'D:\screenshot_0726\name'
    #screenshot_params['name']='cut_'+str(deep)
    scene.screenshots_folder = r'D:\screenshot_0726\name'
    scene.screenshots_name = 'cut_Deep=' + str(deep)
    if not os.path.exists(scene.screenshots_folder):
        os.makedirs(scene.screenshots_folder)

    scene.screenshots_name = 'cut_Deep=' + str(deep)
    scene.screenshots_extension = 'png'
    scene.render(camera='coronal', zoom=0.8, interactive=False)  # zoom的大小决定了后边截图的大小
    scene.take_screenshot()





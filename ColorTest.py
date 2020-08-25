#敲定图1用0.1-0.4的colorbar
import brainrender

brainrender.SHADER_STYLE = 'ambient'  # plastic
brainrender.DEFAULT_STRUCTURE_ALPHA = .8
brainrender.DISPLAY_ROOT = True
brainrender.ROOT_COLOR = 'gray'
brainrender.ROOT_ALPHA = .2
brainrender.DISPLAY_INSET = False
import h5py
import numpy as np
import os
from matplotlib import cm
from ZXScene import ZXScene

# root = scene.actors['root']
# th = scene.add_brain_regions(['STR', 'TH'])  # solid wireframe,这两个参数默认为False
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
dmin = np.floor(0.1 * 100).astype(np.int)#np.floor(np.min(dist) * 100).astype(np.int)
dmax = np.floor(0.4 * 100).astype(np.int)#np.floor(np.max(dist) * 100).astype(np.int)
scene = ZXScene(base_dir=r'D:\figure_0817\figure1')
jmap = cm.get_cmap('jet', dmax - dmin + 1)
jetmap = jmap(range(dmax - dmin + 1))


for s in sums:
    if s[1] >= 100 and s[0] != 'Unlabeled' and s[0] != 'root':
        cmIdx = np.floor(s[3] * 100).astype(np.int) - dmin
        scene.add_brain_regions([s[0]], colors=jetmap[cmIdx][:3], use_original_color=False, alpha=1, add_labels=False)


pos1 = [2183, 3849, 5688.5]    #pos = [4000, 3849, 5688.5]  # scene.atlas._root_midpoint   # 设置平面的原点  (单位不知道诶，就很烦，拿100)
sx, sy = 15000, 15000  # 设置平面大小
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
scene.screenshots_folder = r'D:\figure_0817\figure1\no_name_new'
scene.screenshots_name = 'top'
scene.render(camera='top', zoom=1, interactive=False)
scene.take_screenshot()
#scene.take_screenshot()
scene.screenshots_folder = r'D:\figure_0817\figure1\no_name_new'
scene.screenshots_name = 'sagittal'
scene.render(camera='sagittal', zoom=1, interactive=False)
scene.take_screenshot()


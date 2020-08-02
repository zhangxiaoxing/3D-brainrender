import brainrender
brainrender.SHADER_STYLE = 'cartoon'
brainrender.WHOLE_SCREEN = True
from brainrender.scene import Scene
from matplotlib import cm
import numpy as np
from brainrender.animation.video import BasicVideoMaker
import vtkmodules as vtk
from scipy.io import loadmat
data = loadmat(r'C:\Users\Fish\Desktop\BrainRender-master\opgenstats.mat')

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
scene = Scene(display_inset=True, base_dir=r'D:\brain3Dtest\result')
Actors = []
name = []
color = []
for s in sums:
    cmIdx = np.floor(s[1] * 100).astype(np.int) - dmin
    scene.add_brain_regions([s[0]], colors=jetmap[cmIdx][:3], use_original_color=False, alpha=.25, add_labels=False) # alpha值设置透明度，越小越透明

vmkr = BasicVideoMaker(scene)
vmkr.make_video(azimuth=1, niters=360, duration=18, save_name="figure6Vedio_noname")

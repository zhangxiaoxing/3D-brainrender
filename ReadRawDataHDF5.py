def ReadRawData(dmax, dmin, sums, path):
    import brainrender
    brainrender.SHADER_STYLE = 'cartoon'
    brainrender.WHOLE_SCREEN = True
    # brainrender.SHOW_AXES = True      # 可以显示坐标轴
    # brainrender.ROOT_ALPHA = .01  # 设置非渲染部分的透明度
    from brainrender.scene import Scene
    from matplotlib import cm
    import numpy as np
    import random
    import os

    # dir = [r'D:\Render\test1', r'D:\Render\test2', r'D:\Render\test3', r'D:\Render\test4']
    # base_dir0 = random.choice(dir)
    base_dir0 = path
    if not os.path.exists(base_dir0):
        os.makedirs(base_dir0)
    scene = Scene(
        base_dir=base_dir0)  # 绘制3D旋转视频时camera="sagittal", SCREENSHOT_TRANSPARENT_BACKGROUND=False设置非透明背景，但是好像效果不明显
    jmap = cm.get_cmap('jet', dmax - dmin + 1)
    jetmap = jmap(range(dmax - dmin + 1))
    # Add the whole thalamus in gray
    Actors = []
    name = []
    for s in sums:
        if s[1] >= 100 and s[0] != 'Unlabeled' and s[0] != 'root':
            cmIdx = np.floor(s[3] * 100).astype(np.int) - dmin
            Actors.append(scene.add_brain_regions([s[0]], colors=jetmap[cmIdx][:3], use_original_color=False, alpha=1,
                                                  add_labels=False))  # alpha值设置透明度，越小越透明
            name.append(s[0])
    return scene, Actors, name

cutcut.py中是迭代切割显示冠状面，并添加brain region label；
slice.py是可以直接运行切片示例文件，主要问题在于切片截面封闭不均，和scene.cut_actors_with_plane(plane2, close_actors=True, showplane=False)中close_actors有关。
debug ing

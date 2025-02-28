#%%
import skgmsh as sg

%reload_ext autoreload
%autoreload 2


# shell = [(0, 0, 0), (0, 10, 0), (10, 10, 0), (10, 0, 0), (0, 0, 0)]
# holes = [[(2, 2, 0), (2, 4, 0), (4, 4, 0), (4, 2, 0), (2, 2, 0)]]
# alg = sg.Delaunay2D(shell=shell, holes=holes)
# alg.cell_size = 0.5
# alg.mesh.plot(show_edges=True, cpos="xy")

try:
    a = 1 / 0

finally:
    print("prout")
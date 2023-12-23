import pvgmsh
import pyvista
import numpy as np


# Gmsh Python tutorial 1
# https://gitlab.onelab.info/gmsh/gmsh/blob/gmsh_4_10_5/tutorials/python/t1.py

vertices = np.array([[0, 0, 0], [0.1, 0, 0], [0.1, 0.3, 0], [0, 0.3, 0]])
faces = np.hstack([[4, 0, 1, 2, 3]])
surf = pyvista.PolyData(vertices, faces)

# pvgmsh does not support PhysicalGroup; group configuration can be easily done with PyVista.

mesh = pvgmsh.generate_mesh(surf)

plotter = pyvista.Plotter(shape=(1, 2))
plotter.subplot(0, 0)
plotter.add_mesh(surf, color="tan", show_edges=True)
plotter.subplot(0, 1)
plotter.add_mesh(mesh, color="tan", show_edges=True)
plotter.show(cpos="xy")

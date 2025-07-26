r"""
Constrain edge size for Delaunay2D
-----------------------------------

Constrain edge size for Delaunay2D.

"""

from __future__ import annotations

import pyvista as pv
import shapely

import skgmsh as sg

# Set global theme to allow empty meshes
pv.global_theme.allow_empty_mesh = True

edge_source = pv.Polygon(n_sides=16, radius=16)
# Convert points to shapely polygon (remove z-coordinate)
points_2d = edge_source.points[:, :2]
shell = shapely.Polygon(points_2d)

try:
    mesh = sg.Delaunay2D(shell=shell).mesh
except (ValueError, RuntimeError) as e:
    print(f"Mesh generation failed: {e}")
    mesh = pv.PolyData()  # Create empty mesh for plotting

p = pv.Plotter()
p.add_mesh(mesh, show_edges=True)
p.add_mesh(pv.PolyData(edge_source.points), render_points_as_spheres=True, color="red", point_size=10)
p.view_xy()
p.show()

# %%
# With option `constrain_edge_size=True`, the edge size is constrained.

try:
    mesh = sg.Delaunay2D(shell=shell, constrain_edge_size=True).mesh
    if mesh.n_points > 0:
        mesh.plot(show_edges=True, color="white", cpos="xy")
    else:
        print("Warning: Empty mesh generated")
except (ValueError, RuntimeError) as e:
    print(f"Mesh generation with constrained edge size failed: {e}")

# %%
# Works with holes too!

hole1 = pv.Polygon(n_sides=6, radius=4).translate([-4.0, -4.0, 0.0])
hole2 = pv.Polygon(n_sides=8, radius=2).translate([4.0, 4.0, 0.0])

# Convert holes to shapely polygons
hole1_2d = shapely.Polygon(hole1.points[:, :2])
hole2_2d = shapely.Polygon(hole2.points[:, :2])

try:
    mesh = sg.Delaunay2D(shell=shell, holes=[hole1_2d, hole2_2d], constrain_edge_size=True).mesh
    if mesh.n_points > 0:
        mesh.plot(show_edges=True, color="white", cpos="xy")
    else:
        print("Warning: Empty mesh with holes generated")
except (ValueError, RuntimeError) as e:
    print(f"Mesh generation with holes failed: {e}")

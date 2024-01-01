"""Test script."""
import gmsh
import pyvista as pv
from pygmsh.helpers import extract_to_meshio
from pyvista.core.utilities import fileio

edge_source = pv.Cube()
points = edge_source.points
faces = edge_source.regular_faces

gmsh.initialize()

for i, point in enumerate(points):
    _ = gmsh.model.geo.add_point(point[0], point[1], point[2], 1.0, i + 1)

surface_loop = []
for i, face in enumerate(faces):
    _ = gmsh.model.geo.add_line(face[0] + 1, face[1] + 1, i * 4 + 0)
    _ = gmsh.model.geo.add_line(face[1] + 1, face[2] + 1, i * 4 + 1)
    _ = gmsh.model.geo.add_line(face[2] + 1, face[3] + 1, i * 4 + 2)
    _ = gmsh.model.geo.add_line(face[3] + 1, face[0] + 1, i * 4 + 3)
    _ = gmsh.model.geo.add_curve_loop([i * 4 + 0, i * 4 + 1, i * 4 + 2, i * 4 + 3], i + 1)
    _ = gmsh.model.geo.add_plane_surface([i + 1], i + 1)
    gmsh.model.geo.remove_all_duplicates()
    gmsh.model.geo.synchronize()
    surface_loop.append(i + 1)

_ = gmsh.model.geo.add_surface_loop(surface_loop, 1)
_ = gmsh.model.geo.add_volume([1], 1)
gmsh.model.geo.synchronize()
gmsh.model.mesh.generate(3)
mesh = extract_to_meshio()
gmsh.clear()
gmsh.finalize()

output = fileio.from_meshio(mesh)

plotter = pv.Plotter(shape=(1, 2))
plotter.link_views()
plotter.add_mesh(edge_source, show_edges=True)
plotter.add_point_labels(edge_source.points, labels=range(1, 9))
plotter.add_point_labels(edge_source.cell_centers().points, labels=range(1, 6 + 1))
plotter.subplot(0, 1)
plotter.add_mesh(output, show_edges=True)
plotter.add_point_labels(output.points, labels=range(1, 15))
plotter.show()

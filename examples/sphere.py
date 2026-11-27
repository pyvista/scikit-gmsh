"""
Example of creating and visualizing a 3D sphere mesh using Gmsh and PyVista.

This example demonstrates how to create a 3D sphere mesh using Gmsh and visualize it
using PyVista. The mesh is saved in both .msh format and as PNG images from different
viewing angles.
"""

from __future__ import annotations

from typing import Literal

import gmsh
import numpy as np
import pyvista as pv

# Set PyVista plotting backend
pv.set_plot_theme("document")
pv.global_theme.window_size = [800, 600]
pv.global_theme.background = "white"
pv.OFF_SCREEN = True  # Enable off-screen rendering

# Initialize Gmsh
gmsh.initialize()

# Create a new model
model = gmsh.model
model.add("sphere")

# Create a sphere
sphere = model.occ.addSphere(0, 0, 0, 1.0)

# Synchronize the CAD kernel with the Gmsh model
model.occ.synchronize()

# Generate the mesh
model.mesh.generate(3)

# Get the mesh data
nodes = model.mesh.getNodes()
elements = model.mesh.getElements()

# Print some basic information
print(f"Number of nodes: {len(nodes[1]) // 3}")
print(f"Number of elements: {len(elements[2])}")

# Write the mesh to a file
gmsh.write("sphere.msh")

# Finalize Gmsh
gmsh.finalize()

# Create PyVista mesh for visualization
# Convert nodes to numpy array and reshape
node_coords = np.array(nodes[1]).reshape(-1, 3)
print(f"Node coordinates shape: {node_coords.shape}")

# Get tetrahedral elements and convert to 0-based indexing
tet_elements = np.array(elements[2][1]).reshape(-1, 4) - 1  # Use elements[2][1] for connectivity
print(f"Tetrahedra connectivity shape: {tet_elements.shape}")

# Create PyVista UnstructuredGrid
grid = pv.UnstructuredGrid({pv.CellType.TETRA: tet_elements}, node_coords)
print("Grid information:")
print(grid)

# Extract surface
surface = grid.extract_surface()
print("Surface information:")
print(surface)


def save_view(view_name: str, camera_pos: Literal["xy", "xz", "yz"]) -> None:
    """
    Save a view of the mesh from a specified camera position.

    Args:
        view_name: Name of the view (used in the output filename)
        camera_pos: Camera position ("xy", "xz", or "yz")

    """
    plotter = pv.Plotter(off_screen=True)
    plotter.add_mesh(surface, show_edges=True, color="lightblue", edge_color="black", opacity=0.7)
    plotter.camera_position = camera_pos
    plotter.camera.zoom(1.5)
    plotter.show_axes()
    plotter.show(screenshot=f"sphere_{view_name}.png")


# Save views from different angles
save_view("xy", "xy")  # Top view
save_view("xz", "xz")  # Front view
save_view("yz", "yz")  # Side view

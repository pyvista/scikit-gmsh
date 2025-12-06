r"""
I-beam shell model example
--------------------------

Generate a shell model of an I-beam using Gmsh Python API.
This example demonstrates how to create 2D shell elements for structural analysis,
similar to the approach used in FEniCSx tutorials for shell structures.

Based on: https://bleyerj.github.io/comet-fenicsx/tours/shells/I_beam_gmsh/I_beam_gmsh.html
"""

# sphinx_gallery_thumbnail_number = 3  # noqa:ERA001

from __future__ import annotations

import numpy as np
import pyvista as pv

import skgmsh as sg


def create_i_beam_cross_section(
    height: float = 0.3,
    width: float = 0.15,
    web_thickness: float = 0.01,
    flange_thickness: float = 0.02,
) -> list[tuple[float, float, float]]:
    """
    Create an I-beam cross-section profile.

    Parameters
    ----------
    height : float, default: 0.3
        Total height of the I-beam.
    width : float, default: 0.15
        Width of the flanges.
    web_thickness : float, default: 0.01
        Thickness of the web.
    flange_thickness : float, default: 0.02
        Thickness of the flanges.

    Returns
    -------
    list[tuple[float, float, float]]
        List of (x, y, z) coordinates defining the I-beam profile.

    """
    # Define the I-beam profile starting from bottom-left, going counter-clockwise
    return [
        # Bottom flange (left to right)
        (-width / 2, -height / 2, 0),
        (width / 2, -height / 2, 0),
        (width / 2, -height / 2 + flange_thickness, 0),
        # Right side of web
        (web_thickness / 2, -height / 2 + flange_thickness, 0),
        (web_thickness / 2, height / 2 - flange_thickness, 0),
        # Top flange (right side)
        (width / 2, height / 2 - flange_thickness, 0),
        (width / 2, height / 2, 0),
        # Top flange (right to left)
        (-width / 2, height / 2, 0),
        (-width / 2, height / 2 - flange_thickness, 0),
        # Left side of web
        (-web_thickness / 2, height / 2 - flange_thickness, 0),
        (-web_thickness / 2, -height / 2 + flange_thickness, 0),
        # Back to start
        (-width / 2, -height / 2 + flange_thickness, 0),
        (-width / 2, -height / 2, 0),
    ]


# %%
# Create I-beam cross-section profile.

i_beam_profile = create_i_beam_cross_section()

# %%
# Generate shell mesh using Delaunay2D.

delaunay_2d = sg.Delaunay2D(shell=i_beam_profile, cell_size=0.02)
mesh = delaunay_2d.mesh

# %%
# Plot the I-beam cross-section shell mesh.

mesh.plot(show_edges=True, color="white", line_width=2, cpos="xy")

# %%
# Create a curved I-beam shell by extruding along a curved path.
# This demonstrates how to create more complex shell structures
# suitable for structural analysis (e.g., with FEniCSx).

# Create points along a curved path (arc)
n_points = 20
theta = np.linspace(0, np.pi / 2, n_points)  # Quarter circle
radius = 2.0

# Create meshes at different positions along the curve
meshes = []
for _i, t in enumerate(theta):
    # Calculate position and rotation
    x = radius * np.sin(t)
    z = radius * (1 - np.cos(t))

    # Create a rotated copy of the mesh
    mesh_copy = mesh.copy()
    # Rotate and translate
    mesh_copy.rotate_z(np.degrees(t), point=(0, 0, 0))
    mesh_copy.translate([x, 0, z])

    meshes.append(mesh_copy)

# Combine all meshes
curved_beam = meshes[0]
for mesh_part in meshes[1:]:
    curved_beam = curved_beam.merge(mesh_part)

# %%
# Plot the curved I-beam shell.

curved_beam.plot(show_edges=True, color="lightgray", line_width=1)

# %%
# Highlight boundary regions.
# Different boundaries can be tagged for applying boundary conditions
# in finite element analysis.

p = pv.Plotter()
p.add_mesh(curved_beam, show_edges=True, color="lightgray", opacity=0.8)
p.add_mesh(meshes[0], color="blue", label="Start boundary")
p.add_mesh(meshes[-1], color="red", label="End boundary")
p.add_legend()
p.show()

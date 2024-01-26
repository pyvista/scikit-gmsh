"""PvGmsh package for 3D mesh generation test."""
import numpy as np
import pyvista as pv

import pvgmsh as pm


def test_frontal_delaunay_2d() -> None:
    """Frontal-Delaunay 2D mesh algorithm test code."""
    edge_source = pv.Polygon(n_sides=4, radius=8, fill=False)
    mesh = pm.frontal_delaunay_2d(edge_source, target_size=2.0)
    assert mesh.number_of_points > edge_source.number_of_points
    assert mesh.number_of_cells > edge_source.number_of_cells
    assert np.allclose(mesh.volume, edge_source.volume)
    # TODO @tkoyama010: Compare cell type.
    # https://github.com/pyvista/pvgmsh/pull/125


def test_delaunay_3d() -> None:
    """Delaunay 3D mesh algorithm test code."""
    edge_source = pv.Cube()
    mesh = pm.delaunay_3d(edge_source, target_size=0.5)
    assert mesh.number_of_points > edge_source.number_of_points
    assert mesh.number_of_cells > edge_source.number_of_cells
    assert np.allclose(mesh.volume, edge_source.volume)
    # TODO @tkoyama010: Compare cell type.
    # https://github.com/pyvista/pvgmsh/pull/125

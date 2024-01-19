"""PvGmsh package for 3D mesh generation test."""
import numpy as np
import pyvista as pv

import pvgmsh as pm


def test_frontal_delaunay_2d() -> None:
    """Frontal-Delaunay 2D mesh algorithm test code."""
    edge_source = pv.Polygon(n_sides=4, radius=8, fill=False)
    mesh = pm.frontal_delaunay_2d(edge_source, target_size=2.0)
    assert np.allclose(mesh.bounds, edge_source.bounds)


def test_delaunay_3d() -> None:
    """Delaunay 3D mesh algorithm test code."""
    edge_source = pv.Cube()
    mesh = pm.delaunay_3d(edge_source, target_size=0.5)
    assert np.allclose(mesh.bounds, edge_source.bounds)

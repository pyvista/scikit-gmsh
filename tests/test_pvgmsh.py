"""PvGmsh package for 3D mesh generation test."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

import numpy as np
import pytest
import pyvista as pv

import pvgmsh as pm

EDGE_SOURCES = [
    pv.Polygon(n_sides=4, radius=8, fill=False),
    pv.Circle().extract_feature_edges(),
]


@pytest.mark.parametrize(
    "edge_source",
    EDGE_SOURCES,
)
@pytest.mark.parametrize("target_sizes", [2.0, [1.0, 2.0, 3.0, 4.0], None])
def test_frontal_delaunay_2d(
    edge_source: pv.PolyData, target_sizes: float | Sequence[float] | None
) -> None:
    """Frontal-Delaunay 2D mesh algorithm test code."""
    edge_source = pv.Polygon(n_sides=4, radius=8, fill=False)
    mesh = pm.frontal_delaunay_2d(edge_source, target_sizes=target_sizes)
    assert mesh.number_of_points > edge_source.number_of_points
    assert mesh.number_of_cells > edge_source.number_of_cells
    assert np.allclose(mesh.volume, edge_source.volume)
    # TODO @tkoyama010: Compare cell type. # noqa: FIX002
    # https://github.com/pyvista/pvgmsh/pull/125


@pytest.mark.parametrize(
    "target_sizes", [0.5, [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], None]
)
def test_delaunay_3d(target_sizes: float | Sequence[float] | None) -> None:
    """Delaunay 3D mesh algorithm test code."""
    edge_source = pv.Cube()
    mesh = pm.delaunay_3d(edge_source, target_sizes=target_sizes)
    assert mesh.number_of_points > edge_source.number_of_points
    assert mesh.number_of_cells > edge_source.number_of_cells
    assert np.allclose(mesh.volume, edge_source.volume)
    # TODO @tkoyama010: Compare cell type. # noqa: FIX002
    # https://github.com/pyvista/pvgmsh/pull/125

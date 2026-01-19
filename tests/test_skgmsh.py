"""scikit-gmsh package for 3D mesh generation test."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

import numpy as np
import pytest
import pyvista as pv

import skgmsh as sg

EDGE_SOURCES = [
    pv.Polygon(n_sides=4, radius=8),
]


def create_i_beam_cross_section(
    height: float = 0.3,
    width: float = 0.15,
    web_thickness: float = 0.01,
    flange_thickness: float = 0.02,
) -> list[tuple[float, float, float]]:
    """Create an I-beam cross-section profile."""
    return [
        (-width / 2, -height / 2, 0),
        (width / 2, -height / 2, 0),
        (width / 2, -height / 2 + flange_thickness, 0),
        (web_thickness / 2, -height / 2 + flange_thickness, 0),
        (web_thickness / 2, height / 2 - flange_thickness, 0),
        (width / 2, height / 2 - flange_thickness, 0),
        (width / 2, height / 2, 0),
        (-width / 2, height / 2, 0),
        (-width / 2, height / 2 - flange_thickness, 0),
        (-web_thickness / 2, height / 2 - flange_thickness, 0),
        (-web_thickness / 2, -height / 2 + flange_thickness, 0),
        (-width / 2, -height / 2 + flange_thickness, 0),
    ]


def test_frontal_delaunay_2d_default() -> None:
    """Frontal-Delaunay 2D mesh algorithm test code."""
    edge_source = pv.Polygon(n_sides=4, radius=8)
    mesh = sg.frontal_delaunay_2d(edge_source)
    assert mesh.number_of_points == edge_source.number_of_points
    assert np.allclose(mesh.volume, edge_source.volume)
    # TODO @tkoyama010: Compare cell type. # noqa: FIX002
    # https://github.com/pyvista/scikit-gmsh/pull/125
    frontal_delaunay_2d = sg.Delaunay2D(edge_source=edge_source)
    mesh = frontal_delaunay_2d.mesh
    assert mesh.number_of_points == edge_source.number_of_points
    assert np.allclose(mesh.volume, edge_source.volume)


def test_frontal_delaunay_2d_recombine() -> None:
    """Frontal-Delaunay 2D mesh algorithm test code."""
    edge_source = pv.Polygon(n_sides=4, radius=8)
    mesh = sg.frontal_delaunay_2d(edge_source, recombine=True)
    assert mesh.number_of_points == edge_source.number_of_points
    assert mesh.number_of_cells == 1
    assert np.allclose(mesh.volume, edge_source.volume)
    for cell in mesh.cell:
        assert cell.type == pv.CellType.QUAD


@pytest.mark.parametrize("edge_source", EDGE_SOURCES)
@pytest.mark.parametrize("target_sizes", [2.0, [1.0, 2.0, 3.0, 4.0]])
def test_frontal_delaunay_2d(edge_source: pv.Polygon, target_sizes: float | Sequence[float]) -> None:
    """Frontal-Delaunay 2D mesh algorithm test code."""
    mesh = sg.frontal_delaunay_2d(edge_source, target_sizes=target_sizes)
    assert mesh.number_of_points > edge_source.number_of_points
    assert mesh.number_of_cells > edge_source.number_of_cells
    assert np.allclose(mesh.volume, edge_source.volume)
    # TODO @tkoyama010: Compare cell type. # noqa: FIX002
    # https://github.com/pyvista/scikit-gmsh/pull/125


@pytest.mark.parametrize("target_sizes", [0.5, [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]])
def test_delaunay_3d(target_sizes: float | Sequence[float]) -> None:
    """Delaunay 3D mesh algorithm test code."""
    edge_source = pv.Cube()
    mesh = sg.delaunay_3d(edge_source, target_sizes=target_sizes)
    assert mesh.number_of_points > edge_source.number_of_points
    assert mesh.number_of_cells > edge_source.number_of_cells
    assert np.allclose(mesh.volume, edge_source.volume)
    # TODO @tkoyama010: Compare cell type. # noqa: FIX002
    # https://github.com/pyvista/scikit-gmsh/pull/125


@pytest.mark.parametrize("edge_source", [pv.Cube(), pv.Cylinder()])
def test_delaunay_3d_default(edge_source: pv.PolyData) -> None:
    """Delaunay 3D mesh algorithm test code."""
    edge_source.merge(pv.PolyData(edge_source.points), merge_points=True, inplace=True)
    delaunay_3d = sg.Delaunay3D(edge_source)
    mesh = delaunay_3d.mesh
    assert np.allclose(mesh.volume, edge_source.volume)


def test_shell_model_i_beam() -> None:
    """Test shell model generation for I-beam cross-section."""
    i_beam_profile = create_i_beam_cross_section()
    delaunay_2d = sg.Delaunay2D(shell=i_beam_profile, cell_size=0.02)
    mesh = delaunay_2d.mesh

    assert mesh.number_of_points > 0
    assert mesh.number_of_cells > 0
    # Verify all cells are 2D (triangles or quads)
    for cell in mesh.cell:
        assert cell.type in [pv.CellType.TRIANGLE, pv.CellType.QUAD]

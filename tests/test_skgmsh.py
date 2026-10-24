# Copyright (c) 2024 scikit-gmsh contributors
"""scikit-gmsh package for 3D mesh generation test."""

from __future__ import annotations

import gc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

import gmsh
import numpy as np
import pytest
import pyvista as pv

import skgmsh as sg

EDGE_SOURCES = [
    pv.Polygon(n_sides=4, radius=8),
]


def test_delaunay_classes_share_single_gmsh_session() -> None:
    """Multiple class-based meshers share one session; the last release ends it."""
    shell = [(0, 0), (1, 0), (0, 1)]
    mesher_2d = sg.Delaunay2D(shell=shell)
    edge_source = pv.Cube()
    edge_source.merge(pv.PolyData(edge_source.points), merge_points=True, inplace=True)
    mesher_3d = sg.Delaunay3D(edge_source)
    assert gmsh.is_initialized()

    with pytest.raises(RuntimeError, match="is active"):
        sg.frontal_delaunay_2d(pv.Polygon(n_sides=3))

    mesh_2d = mesher_2d.mesh
    mesh_3d = mesher_3d.mesh
    assert mesh_2d.number_of_points == len(shell)
    assert mesh_2d.number_of_cells == 1
    assert np.allclose(mesh_3d.volume, edge_source.volume)

    mesher_3d.finalize()
    assert gmsh.is_initialized()  # mesher_2d still holds the session
    with pytest.raises(RuntimeError, match="has been finalized"):
        _ = mesher_3d.mesh

    mesher_2d.finalize()
    assert not gmsh.is_initialized()
    with pytest.raises(RuntimeError, match="has been finalized"):
        _ = mesher_2d.mesh


def test_four_delaunay_classes_share_single_gmsh_session() -> None:
    """Two Delaunay2D and two Delaunay3D meshers share one session."""
    shell = [(0, 0), (1, 0), (0, 1)]
    shell_b = [(5, 5), (6, 5), (5, 6)]
    mesher_2d_a = sg.Delaunay2D(shell=shell)
    mesher_2d_b = sg.Delaunay2D(shell=shell_b)
    edge_source = pv.Cube()
    edge_source.merge(pv.PolyData(edge_source.points), merge_points=True, inplace=True)
    mesher_3d_a = sg.Delaunay3D(edge_source)
    mesher_3d_b = sg.Delaunay3D(edge_source)
    assert gmsh.is_initialized()

    for mesher_2d in (mesher_2d_a, mesher_2d_b):
        mesh_2d = mesher_2d.mesh
        assert mesh_2d.number_of_points == len(shell)
        assert mesh_2d.number_of_cells == 1
    for mesher_3d in (mesher_3d_a, mesher_3d_b):
        assert np.allclose(mesher_3d.mesh.volume, edge_source.volume)

    mesher_2d_a.finalize()
    assert gmsh.is_initialized()  # three meshers still hold the session
    for mesher in (mesher_2d_b, mesher_3d_a, mesher_3d_b):
        assert mesher.mesh is not None
    mesher_2d_b.finalize()
    mesher_3d_a.finalize()
    assert gmsh.is_initialized()  # mesher_3d_b holds the last lease
    mesher_3d_b.finalize()
    assert not gmsh.is_initialized()


def test_concurrent_meshing_matches_single_run() -> None:
    """Concurrent meshers produce meshes identical to single-run meshers."""

    def cube_source() -> pv.PolyData:
        edge_source = pv.Cube()
        edge_source.merge(pv.PolyData(edge_source.points), merge_points=True, inplace=True)
        return edge_source

    shell = [(0, 0), (1, 0), (0, 1)]
    assert not gmsh.is_initialized()

    # Single runs: one mesher owns the session end to end.
    # ``Delaunay2D(...)/Delaunay3D(...)`` initialize Gmsh in ``__init__``.
    baseline_2d_mesher = sg.Delaunay2D(shell=shell)
    assert gmsh.is_initialized()  # initialize: implicit in __init__
    baseline_2d = baseline_2d_mesher.mesh
    baseline_2d_mesher.finalize()
    assert not gmsh.is_initialized()  # finalize: explicit call, session closed

    baseline_3d_mesher = sg.Delaunay3D(cube_source())
    assert gmsh.is_initialized()  # initialize: implicit in __init__
    baseline_3d = baseline_3d_mesher.mesh
    baseline_3d_mesher.finalize()
    assert not gmsh.is_initialized()  # finalize: explicit call, session closed

    assert not gmsh.is_initialized()

    # Concurrent runs: all four meshers share one session.
    # Each __init__ merely keeps the shared session alive (leased); only the
    # last explicit finalize() closes it.
    mesher_2d_a = sg.Delaunay2D(shell=shell)
    mesher_2d_b = sg.Delaunay2D(shell=shell)
    mesher_3d_a = sg.Delaunay3D(cube_source())
    mesher_3d_b = sg.Delaunay3D(cube_source())
    assert gmsh.is_initialized()  # all four share one session

    concurrent_2d_a = mesher_2d_a.mesh
    concurrent_2d_b = mesher_2d_b.mesh
    concurrent_3d_a = mesher_3d_a.mesh
    concurrent_3d_b = mesher_3d_b.mesh

    for concurrent_2d in (concurrent_2d_a, concurrent_2d_b):
        assert np.array_equal(concurrent_2d.points, baseline_2d.points)
        assert np.array_equal(concurrent_2d.faces, baseline_2d.faces)
    for concurrent_3d in (concurrent_3d_a, concurrent_3d_b):
        assert np.array_equal(concurrent_3d.points, baseline_3d.points)
        assert np.array_equal(concurrent_3d.cells, baseline_3d.cells)

    # finalize: explicit, one per mesher; only the last one closes Gmsh
    mesher_2d_a.finalize()
    assert gmsh.is_initialized()  # three leases remain
    mesher_2d_b.finalize()
    assert gmsh.is_initialized()  # two leases remain
    mesher_3d_a.finalize()
    assert gmsh.is_initialized()  # one lease remains
    mesher_3d_b.finalize()
    assert not gmsh.is_initialized()  # last finalize closes the shared session


def test_deleting_delaunay_class_finalizes_gmsh() -> None:
    """Deleting the active mesher releases Gmsh and permits a replacement."""
    mesher = sg.Delaunay2D(shell=[(0, 0), (1, 0), (0, 1)])  # noqa: S604
    assert gmsh.is_initialized()

    del mesher
    gc.collect()

    assert not gmsh.is_initialized()
    replacement = sg.Delaunay2D(shell=[(0, 0), (1, 0), (0, 1)])  # noqa: S604
    replacement.finalize()


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

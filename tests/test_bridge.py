"""Tests for the ``skgmsh.bridge`` PyVista ↔ gmsh helpers."""

from __future__ import annotations

import gmsh
import pytest
import pyvista as pv

import skgmsh


@pytest.fixture
def gmsh_session() -> None:
    """Bracket each test with ``gmsh.initialize`` / ``gmsh.finalize``."""
    gmsh.initialize()
    yield
    gmsh.finalize()


def test_from_gmsh_empty_model(gmsh_session: None) -> None:  # noqa: ARG001
    """An empty model returns an empty grid."""
    gmsh.model.add("empty")
    gmsh.model.setCurrent("empty")
    grid = skgmsh.from_gmsh("empty")
    assert grid.n_points == 0
    assert grid.n_cells == 0


def test_to_then_from_gmsh_roundtrip(gmsh_session: None) -> None:  # noqa: ARG001
    """A PolyData round-trips through gmsh as a tagged grid."""
    src = pv.Sphere()
    skgmsh.to_gmsh(src, model_name="named")
    grid = skgmsh.from_gmsh("named")
    assert grid.n_cells > 0
    assert str(grid.field_data["cad.source_format"][0]) == "gmsh"


def test_from_gmsh_after_meshing(gmsh_session: None) -> None:  # noqa: ARG001
    """A meshed rectangle yields a populated grid."""
    gmsh.option.setNumber("General.Terminal", 0)
    gmsh.model.add("rect")
    gmsh.model.setCurrent("rect")
    gmsh.model.occ.addRectangle(0, 0, 0, 1, 1)
    gmsh.model.occ.synchronize()
    gmsh.model.mesh.generate(2)
    grid = skgmsh.from_gmsh()
    assert grid.n_cells > 0

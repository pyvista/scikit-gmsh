"""
Bridges between :mod:`gmsh` and :mod:`pyvista`.

gmsh is a global-state mesh generator, so these helpers consult the
currently-initialized gmsh model. The caller is responsible for
``gmsh.initialize()`` / ``gmsh.finalize()`` bracketing.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

import gmsh
import numpy as np
import pyvista as pv

if TYPE_CHECKING:
    from collections.abc import Iterator

_TRIANGLE_VERTEX_COUNT = 3

_GMSH_TO_VTK: dict[int, tuple[int, int]] = {
    1: (3, 2),
    2: (5, 3),
    3: (9, 4),
    4: (10, 4),
    5: (12, 8),
    6: (13, 6),
    7: (14, 5),
    15: (1, 1),
}


def from_gmsh(model_name: str | None = None) -> pv.UnstructuredGrid:
    """
    Pull the current gmsh model into a :class:`pyvista.UnstructuredGrid`.

    Parameters
    ----------
    model_name : str, optional
        Name of the gmsh model to read. When omitted, the current
        model is used.

    Returns
    -------
    pyvista.UnstructuredGrid
        Mesh from gmsh, with one cell per gmsh element. Element types
        outside the supported map are skipped.

    Examples
    --------
    >>> import gmsh
    >>> from skgmsh.bridge import from_gmsh
    >>> gmsh.initialize()
    >>> gmsh.option.setNumber("General.Terminal", 0)
    >>> _ = gmsh.model.add("demo")
    >>> _ = gmsh.model.occ.addRectangle(0, 0, 0, 1, 1)
    >>> gmsh.model.occ.synchronize()
    >>> gmsh.model.mesh.generate(2)
    >>> grid = from_gmsh()
    >>> type(grid).__name__
    'UnstructuredGrid'
    >>> grid.n_cells > 0
    True
    >>> gmsh.finalize()

    """
    if model_name is not None:
        gmsh.model.setCurrent(model_name)

    node_tags, coords, _ = gmsh.model.mesh.getNodes()
    coords = np.asarray(coords, dtype=float).reshape(-1, 3)
    tag_to_idx = {int(t): i for i, t in enumerate(node_tags)}

    cells: list[int] = []
    cell_types: list[int] = []
    elem_types, _elem_tags, elem_nodes = gmsh.model.mesh.getElements()
    for etype, nodes in zip(elem_types, elem_nodes, strict=True):
        if int(etype) not in _GMSH_TO_VTK:
            continue
        vtk_type, n_nodes = _GMSH_TO_VTK[int(etype)]
        flat = np.asarray(nodes, dtype=np.int64).reshape(-1, n_nodes)
        for row in flat:
            cells.append(n_nodes)
            cells.extend(tag_to_idx[int(t)] for t in row)
            cell_types.append(vtk_type)

    if not cells:
        grid = pv.UnstructuredGrid()
        if coords.size:
            grid.points = coords
        return grid

    cells_arr = np.asarray(cells, dtype=np.int64)
    types_arr = np.asarray(cell_types, dtype=np.uint8)
    grid = pv.UnstructuredGrid(cells_arr, types_arr, coords)
    grid.field_data["cad.source_format"] = np.array(["gmsh"])
    return grid


def to_gmsh(
    mesh: pv.UnstructuredGrid | pv.PolyData,
    *,
    model_name: str = "skgmsh",
) -> None:
    """
    Install a PyVista mesh as the current gmsh model (in place).

    Parameters
    ----------
    mesh : pyvista.UnstructuredGrid or pyvista.PolyData
        Mesh to register.
    model_name : str, default: ``"skgmsh"``
        Name of the gmsh model to create.

    Examples
    --------
    >>> import gmsh
    >>> import pyvista as pv
    >>> from skgmsh.bridge import to_gmsh
    >>> gmsh.initialize()
    >>> gmsh.option.setNumber("General.Terminal", 0)
    >>> to_gmsh(pv.Sphere())
    >>> gmsh.model.getCurrent()
    'skgmsh'
    >>> gmsh.finalize()

    """
    gmsh.model.add(model_name)
    gmsh.model.setCurrent(model_name)
    surface_tag = gmsh.model.addDiscreteEntity(2)

    points = np.asarray(mesh.points, dtype=float).reshape(-1)
    node_tags = list(range(1, len(mesh.points) + 1))
    gmsh.model.mesh.addNodes(2, surface_tag, node_tags, points.tolist())

    triangles: list[int] = []
    for tri in _iter_triangles(mesh):
        triangles.extend(int(i) + 1 for i in tri)
    if triangles:
        elem_tags = list(range(1, 1 + len(triangles) // 3))
        gmsh.model.mesh.addElementsByType(surface_tag, 2, elem_tags, triangles)


def _iter_triangles(mesh: pv.UnstructuredGrid | pv.PolyData) -> Iterator[Any]:
    """Yield triangle index triplets from a surface mesh."""
    if isinstance(mesh, pv.PolyData):
        tri = mesh.triangulate()
        faces = tri.faces.reshape(-1, 4)
        for row in faces:
            if int(row[0]) == _TRIANGLE_VERTEX_COUNT:
                yield row[1:4]
        return
    surf = mesh.extract_surface(algorithm="dataset_surface").triangulate()
    faces = surf.faces.reshape(-1, 4)
    for row in faces:
        if int(row[0]) == _TRIANGLE_VERTEX_COUNT:
            yield row[1:4]

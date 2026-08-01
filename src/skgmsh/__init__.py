# Copyright (c) 2024 scikit-gmsh contributors
"""scikit-gmsh package for 3D mesh generation."""

from __future__ import annotations

from contextlib import suppress
import datetime
from typing import TYPE_CHECKING
from typing import Self
import weakref

import gmsh
import numpy as np
import pyvista as pv
import scooby
import shapely

from skgmsh.bridge import from_gmsh as from_gmsh
from skgmsh.bridge import to_gmsh as to_gmsh

if TYPE_CHECKING:
    from collections.abc import Sequence

    from numpy.typing import ArrayLike

INITIAL_MESH_ONLY_2D = 3
FRONTAL_DELAUNAY_2D = 6
DELAUNAY_3D = 1
INITIAL_MESH_ONLY_3D = 3

SILENT = 0
SIMPLE = 0

TRUE = 1
FALSE = 0

now = datetime.datetime.now(tz=datetime.UTC)

# major, minor, patch
version_info = 0, 4, 0

# Nice string for the version
__version__ = ".".join(map(str, version_info))


class Report(scooby.Report):  # type: ignore[misc]
    """
    Generate an environment package and hardware report.

    Parameters
    ----------
    ncol : int, default: 3
        Number of package-columns in html table; only has effect if
        ``mode='HTML'`` or ``mode='html'``.

    text_width : int, default: 80
        The text width for non-HTML display modes.

    """

    def __init__(self: Report, ncol: int = 3, text_width: int = 80) -> None:  # numpydoc ignore=PR01
        """Generate a :class:`scooby.Report` instance."""
        # mandatory packages
        core: list[str] = [
            "matplotlib",
            "numpy",
            "pooch",
            "pyvista",
            "scooby",
            "vtk",
            "gmsh",
            "meshio",
            "pygmsh",
            "pyvista",
        ]

        # optional packages
        optional: list[str] = [
            "imageio",
            "pyvistaqt",
            "PyQt5",
            "IPython",
            "colorcet",
            "cmocean",
            "ipywidgets",
            "scipy",
            "tqdm",
            "jupyterlab",
            "pytest_pyvista",
            "trame",
            "trame_client",
            "trame_server",
            "trame_vtk",
            "trame_vuetify",
            "jupyter_server_proxy",
            "nest_asyncio",
        ]

        extra_meta = [
            ("GPU Details", "None"),
        ]

        super().__init__(
            core=core,
            optional=optional,
            ncol=ncol,
            text_width=text_width,
            extra_meta=extra_meta,
        )


def delaunay_3d(
    edge_source: pv.PolyData,
    target_sizes: float | Sequence[float] | None = None,
    *,
    _manage_gmsh: bool = True,
) -> pv.UnstructuredGrid | None:
    """
    Delaunay 3D mesh algorithm.

    Parameters
    ----------
    edge_source : pyvista.PolyData
        Specify the source object used to specify constrained
        edges and loops. If set, and lines/polygons are defined, a
        constrained triangulation is created. The lines/polygons
        are assumed to reference points in the input point set
        (i.e. point ids are identical in the input and
        source).

    target_sizes : float | Sequence[float]
        Target mesh size close to the points.

    Returns
    -------
    pyvista.UnstructuredGrid
        Mesh from the 3D delaunay generation.

    Notes
    -----
    .. versionadded:: 0.2.0

    """
    points = edge_source.points
    faces = edge_source.irregular_faces

    if _manage_gmsh:
        _ensure_no_active_mesher()
        gmsh.initialize()
    if target_sizes is None:
        gmsh.option.set_number("Mesh.Algorithm", INITIAL_MESH_ONLY_3D)
        gmsh.option.set_number("Mesh.MeshSizeExtendFromBoundary", 0)
        gmsh.option.set_number("Mesh.MeshSizeFromPoints", 0)
        gmsh.option.set_number("Mesh.MeshSizeFromCurvature", 0)
    else:
        gmsh.option.set_number("Mesh.Algorithm3D", DELAUNAY_3D)
    gmsh.option.set_number("General.Verbosity", SILENT)
    gmsh.option.set_number("Mesh.AlgorithmSwitchOnFailure", FALSE)
    gmsh.option.set_number("Mesh.RecombinationAlgorithm", SIMPLE)
    gmsh.option.set_number("Mesh.RecombineNodeRepositioning", FALSE)

    if target_sizes is None:
        target_sizes = 0.0

    if isinstance(target_sizes, float):
        target_sizes = [target_sizes] * edge_source.number_of_points

    for i, (point, target_size) in enumerate(zip(points, target_sizes, strict=False)):
        id_ = i + 1
        gmsh.model.geo.add_point(point[0], point[1], point[2], target_size, id_)

    surface_loop = []
    for i, face in enumerate(faces):
        curve_tags = []
        for j, _ in enumerate(face):
            start_tag = face[j - 1] + 1
            end_tag = face[j] + 1
            curve_tag = gmsh.model.geo.add_line(start_tag, end_tag)
            curve_tags.append(curve_tag)
        gmsh.model.geo.add_curve_loop(curve_tags, i + 1)
        gmsh.model.geo.add_plane_surface([i + 1], i + 1)
        surface_loop.append(i + 1)

    gmsh.model.geo.remove_all_duplicates()
    gmsh.model.geo.synchronize()

    gmsh.model.geo.add_surface_loop(surface_loop, 1)
    gmsh.model.geo.add_volume([1], 1)

    gmsh.model.geo.synchronize()
    mesh = generate_mesh(3, finalize=_manage_gmsh)

    ind = []
    for i, cell in enumerate(mesh.cell):
        if cell.type != pv.CellType.TETRA:
            ind.append(i)
    mesh = mesh.remove_cells(ind)
    mesh.clear_data()

    return mesh


def frontal_delaunay_2d(  # noqa: C901, PLR0912
    edge_source: pv.PolyData | shapely.geometry.Polygon,
    target_sizes: float | ArrayLike | None = None,
    recombine: bool = False,  # noqa: FBT001, FBT002
    *,
    _manage_gmsh: bool = True,
) -> pv.UnstructuredGrid | None:
    """
    Frontal-Delaunay 2D mesh algorithm.

    Parameters
    ----------
    edge_source : pyvista.PolyData | shapely.geometry.Polygon
        Specify the source object used to specify constrained
        edges and loops. If set, and lines/polygons are defined, a
        constrained triangulation is created. The lines/polygons
        are assumed to reference points in the input point set
        (i.e. point ids are identical in the input and
        source).

    target_sizes : float | ArrayLike
        Target mesh size close to the points.
        Default max size of edge_source in each direction.

    recombine : bool
        Recombine the generated mesh into quadrangles.

    Returns
    -------
    pyvista.UnstructuredGrid
        Mesh from the 2D delaunay generation.

    Notes
    -----
    .. versionadded:: 0.2.0

    """
    if _manage_gmsh:
        _ensure_no_active_mesher()
        gmsh.initialize()
    if target_sizes is None:
        gmsh.option.set_number("Mesh.Algorithm", INITIAL_MESH_ONLY_2D)
        gmsh.option.set_number("Mesh.MeshSizeExtendFromBoundary", 0)
        gmsh.option.set_number("Mesh.MeshSizeFromPoints", 0)
        gmsh.option.set_number("Mesh.MeshSizeFromCurvature", 0)
    else:
        gmsh.option.set_number("Mesh.Algorithm", FRONTAL_DELAUNAY_2D)
    gmsh.option.set_number("General.Verbosity", SILENT)

    if target_sizes is None:
        target_sizes = 0.0

    if isinstance(edge_source, shapely.geometry.Polygon):
        wire_tags = []

        if isinstance(target_sizes, float):
            target_sizes = [target_sizes] * (len(edge_source.interiors) + 1)

        for target_size, linearring in zip(target_sizes, [edge_source.exterior, *list(edge_source.interiors)], strict=False):
            sizes = [target_size] * (len(linearring.coords) - 1) if isinstance(target_size, float) else target_size
            coords = linearring.coords[:-1].copy()
            tags = []
            for size, coord in zip(sizes, coords, strict=False):
                x, y, z = coord
                tags.append(gmsh.model.geo.add_point(x, y, z, size))
            curve_tags = []
            for i, _ in enumerate(tags):
                start_tag = tags[i - 1]
                end_tag = tags[i]
                curve_tags.append(gmsh.model.geo.add_line(start_tag, end_tag))
            wire_tags.append(gmsh.model.geo.add_curve_loop(curve_tags))
        gmsh.model.geo.add_plane_surface(wire_tags)
        gmsh.model.geo.synchronize()
    else:
        points = edge_source.points
        lines = edge_source.lines

        if isinstance(target_sizes, float):
            target_sizes = [target_sizes] * edge_source.number_of_points

        embedded_points = []
        for target_size, point in zip(target_sizes, points, strict=False):
            embedded_points.append(gmsh.model.geo.add_point(point[0], point[1], point[2], target_size))

        for i in range(lines[0] - 1):
            id_ = i + 1
            gmsh.model.geo.add_line(lines[i + 1] + 1, lines[i + 2] + 1, id_)

        gmsh.model.geo.add_curve_loop(range(1, lines[0]), 1)
        gmsh.model.geo.add_plane_surface([1], 1)
        gmsh.model.geo.synchronize()
        gmsh.model.mesh.embed(0, embedded_points, 2, 1)

    if recombine:
        gmsh.model.mesh.set_recombine(2, 1)

    mesh = generate_mesh(2, finalize=_manage_gmsh)

    ind = []
    for index, cell in enumerate(mesh.cell):
        if cell.type in [pv.CellType.VERTEX, pv.CellType.LINE]:
            ind.append(index)

    return mesh.remove_cells(ind)


def generate_mesh(dim: int, *, finalize: bool = True) -> pv.UnstructuredGrid:
    """
    Generate a mesh of the current model.

    Parameters
    ----------
    dim : int
        Mesh dimension.

    finalize : bool, default: True
        Finalize Gmsh after generating the mesh. Class-based meshers disable
        this because they own the Gmsh session until ``finalize()`` is called.

    Returns
    -------
    pyvista.UnstructuredGrid
        Generated mesh.

    """
    gmsh_to_pyvista_type = {
        1: pv.CellType.LINE,
        2: pv.CellType.TRIANGLE,
        3: pv.CellType.QUAD,
        4: pv.CellType.TETRA,
        5: pv.CellType.HEXAHEDRON,
        6: pv.CellType.WEDGE,
        7: pv.CellType.PYRAMID,
        15: pv.CellType.VERTEX,
    }

    try:
        gmsh.model.mesh.generate(dim)
        node_tags, coord, _ = gmsh.model.mesh.getNodes()
        element_types, element_tags, element_node_tags = gmsh.model.mesh.getElements()

        # Points
        assert (np.diff(node_tags) > 0).all()  # noqa: S101
        points = np.reshape(coord, (-1, 3))

        # Cells
        cells = {}

        for type_, tags, node_tags in zip(element_types, element_tags, element_node_tags, strict=False):
            assert (np.diff(tags) > 0).all()  # noqa: S101

            celltype = gmsh_to_pyvista_type[type_]
            num_nodes = gmsh.model.mesh.getElementProperties(type_)[3]
            cells[celltype] = np.reshape(node_tags, (-1, num_nodes)) - 1

        mesh = pv.UnstructuredGrid(cells, points)

    finally:
        gmsh.clear()
        if finalize:
            gmsh.finalize()

    return mesh


class _GmshMesher:
    """Manage the process-global Gmsh session used by class-based meshers."""

    _instance: weakref.ReferenceType[_GmshMesher] | None = None

    def __new__(cls, *_args: object, **_kwargs: object) -> Self:
        active = _GmshMesher.active()
        if active is not None:
            msg = f"Cannot create {cls.__name__} while {type(active).__name__} is active. Call finalize() or delete the active mesher first."
            raise RuntimeError(msg)

        instance = super().__new__(cls)
        instance._initialized = False
        _GmshMesher._instance = weakref.ref(instance)
        return instance

    @classmethod
    def active(cls) -> _GmshMesher | None:
        """Return the class-based mesher that currently owns Gmsh."""
        return cls._instance() if cls._instance is not None else None

    def _initialize_gmsh(self) -> None:
        """Initialize the Gmsh session owned by this mesher."""
        if gmsh.is_initialized():
            msg = "Gmsh is already initialized outside this mesher. Finalize that session before creating a Delaunay class."
            raise RuntimeError(msg)
        gmsh.initialize()
        self._initialized = True

    def _require_initialized(self) -> None:
        """Raise when this mesher no longer owns an active Gmsh session."""
        if not self._initialized:
            msg = f"This {type(self).__name__} has been finalized"
            raise RuntimeError(msg)

    def finalize(self) -> None:
        """Finalize Gmsh and release the active mesher slot."""
        try:
            if self._initialized and gmsh.is_initialized():
                gmsh.clear()
                gmsh.finalize()
        finally:
            self._initialized = False
            active = _GmshMesher.active()
            if active is self:
                _GmshMesher._instance = None

    def __del__(self) -> None:
        """Release Gmsh when the owning mesher is garbage-collected."""
        with suppress(Exception):
            self.finalize()


def _ensure_no_active_mesher() -> None:
    """Prevent standalone functions from clobbering a class-owned session."""
    active = _GmshMesher.active()
    if active is not None:
        msg = f"Cannot use a standalone meshing function while {type(active).__name__} is active. Call finalize() first."
        raise RuntimeError(msg)


class Delaunay2D(_GmshMesher):
    """
    Delaunay 2D mesh algorithm.

    Parameters
    ----------
    edge_source : pyvista.PolyData | shapely.Polygon
        Specify the source object used to specify constrained
        edges and loops. If set, and lines/polygons are defined, a
        constrained triangulation is created. The lines/polygons
        are assumed to reference points in the input point set
        (i.e. point ids are identical in the input and
        source).

    shell : sequence
        A sequence of (x, y [,z]) numeric coordinate pairs or triples, or
        an array-like with shape (N, 2) or (N, 3).
        Also can be a sequence of Point objects.

    holes : sequence
        A sequence of objects which satisfy the same requirements as the
        shell parameters above.

    cell_size : float | ArrayLike
       Meshing constraint at point.

    constrain_edge_size : bool
        If True, cell size at points are set to their maximum edge length.

    Notes
    -----
    .. versionadded:: 0.2.0

    Gmsh uses process-global state, so only one ``Delaunay2D`` or
    ``Delaunay3D`` instance may be active at a time. Call ``finalize()`` or
    delete the active instance before creating another class-based mesher.

    """

    def __init__(
        self: Delaunay2D,
        *,
        edge_source: pv.PolyData | shapely.Polygon | None = None,
        shell: Sequence[tuple[int]] | None = None,
        holes: Sequence[tuple[int]] | None = None,
        cell_size: float | ArrayLike | None = None,
        constrain_edge_size: bool = False,
    ) -> None:
        """Initialize the Delaunay2D class."""
        if edge_source is not None:
            self._edge_source = edge_source
        else:
            self._edge_source = shapely.Polygon(shell, holes)

        if constrain_edge_size:
            if isinstance(self.edge_source, shapely.Polygon):
                cell_size = [self._compute_cell_size_from_points(self.edge_source.exterior.coords)]
                cell_size += [self._compute_cell_size_from_points(hole.coords) for hole in self.edge_source.interiors]

            else:
                # Only the first line is processed
                lines = edge_source.lines
                line = lines[1 : lines[0] + 1]
                edge_points = edge_source.points[line]
                cell_size = self._compute_cell_size_from_points(edge_points)

        self._cell_size = cell_size
        self._recombine = False
        self._initialize_gmsh()

    @staticmethod
    def _compute_cell_size_from_points(points: ArrayLike) -> ArrayLike:
        """Compute cell size from points array."""
        lengths = np.linalg.norm(np.diff(points, axis=0), axis=-1)
        lengths = np.insert(lengths, 0, lengths[-1])

        return np.maximum(lengths[:-1], lengths[1:])

    @property
    def edge_source(self: Delaunay2D) -> pv.PolyData | shapely.geometry.Polygon:
        """Get the edge source."""
        return self._edge_source

    @property
    def mesh(self: Delaunay2D) -> pv.PolyData:
        """Get the mesh."""
        self._require_initialized()
        mesh = frontal_delaunay_2d(
            self._edge_source,
            target_sizes=self._cell_size,
            recombine=self._recombine,
            _manage_gmsh=False,
        )
        return pv.PolyData(mesh.points, mesh.cells)

    @property
    def cell_size(self: Delaunay2D) -> float | ArrayLike | None:
        """Get the cell_size of the mesh."""
        return self._cell_size

    @cell_size.setter
    def cell_size(self: Delaunay2D, size: float | ArrayLike | None) -> None:
        """Set the cell_size of the mesh."""
        self._cell_size = size

    def enable_recombine(self: Delaunay2D) -> None:
        """Enable recombination of the mesh."""
        self._recombine = True

    def disable_recombine(self: Delaunay2D) -> None:
        """Disable recombination of the mesh."""
        self._recombine = False


class Delaunay3D(_GmshMesher):
    """
    Delaunay 3D mesh algorithm.

    Parameters
    ----------
    edge_source : pyvista.PolyData
        Specify the source object used to specify constrained
        edges and loops. If set, and lines/polygons are defined, a
        constrained triangulation is created. The lines/polygons
        are assumed to reference points in the input point set
        (i.e. point ids are identical in the input and
        source).

    Notes
    -----
    .. versionadded:: 0.2.0

    Gmsh uses process-global state, so only one ``Delaunay2D`` or
    ``Delaunay3D`` instance may be active at a time. Call ``finalize()`` or
    delete the active instance before creating another class-based mesher.

    """

    def __init__(
        self: Delaunay3D,
        edge_source: pv.PolyData,
        cell_size: float | None = None,
    ) -> None:
        """Initialize the Delaunay3D class."""
        self._edge_source = edge_source
        self._cell_size = cell_size
        self._initialize_gmsh()

    @property
    def edge_source(self: Delaunay3D) -> pv.PolyData:
        """Get the edge source."""
        return self._edge_source

    @property
    def mesh(self: Delaunay3D) -> pv.UnstructuredGrid:
        """Get the mesh."""
        self._require_initialized()
        self._mesh = delaunay_3d(self.edge_source, target_sizes=self.cell_size, _manage_gmsh=False)
        return self._mesh

    @property
    def cell_size(self: Delaunay3D) -> float | None:
        """Get the cell_size of the mesh."""
        return self._cell_size

    @cell_size.setter
    def cell_size(self: Delaunay3D, size: int) -> None:
        """Set the cell_size of the mesh."""
        self._cell_size = size

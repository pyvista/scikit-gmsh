"""PvGmsh package for 3D mesh generation."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import gmsh
import numpy as np
import pyvista as pv
import scooby
from pygmsh.helpers import extract_to_meshio

if TYPE_CHECKING:
    from collections.abc import Sequence

FRONTAL_DELAUNAY_2D = 6
DELAUNAY_3D = 1

now = datetime.datetime.now(tz=datetime.timezone.utc)

# major, minor, patch
version_info = 0, 2, "dev0"

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

    def __init__(
        self: Report, ncol: int = 3, text_width: int = 80
    ) -> None:  # numpydoc ignore=PR01
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


class PlotterBase:
    """
    Base class with common behaviour for a gmsh aware plotter.

    See :class:`pyvista.Plotter`.

    Parameters
    ----------
    *args :
        See :class:`pyvista.Plotter` for further details.

    **kwargs : dict, optional
        See :class:`pyvista.Plotter` for further details.

    Notes
    -----
    .. versionadded:: 0.1.0

    """

    def __init__(self: PlotterBase, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]  # noqa: ANN002, ANN003
        """
        Create gmsh aware plotter.

        Parameters
        ----------
        *args :
            See :class:`pyvista.Plotter` for further details.

        **kwargs : dict, optional
            See :class:`pyvista.Plotter` for further details.

        Notes
        -----
        .. versionadded:: 0.1.0

        """
        super().__init__(*args, **kwargs)


class Plotter(PlotterBase, pv.Plotter):  # type: ignore[misc]
    """Plotting object to display vtk meshes or numpy arrays."""


class Cube:
    """Create a cube."""

    def __init__(self: Cube) -> None:
        """
        Create a cube.

        Examples
        --------
        Create a cube.

        >>> import skgmsh as sg
        >>> cube = sg.Cube()

        """
        self.cube_data: pv.Cube = pv.Cube()

    def delaunay_3d(
        self: Cube,
        edge_source: Cube,
        *,
        target_sizes: float | Sequence[float] | None = None,
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

        target_sizes : float | Sequence[float], optional
            Target mesh size close to the points.

        Returns
        -------
        pyvista.UnstructuredGrid
            Mesh from the 3D delaunay generation.

        """
        points = edge_source.cube_data.points
        faces = edge_source.cube_data.regular_faces
        bounds = edge_source.cube_data.bounds

        gmsh.initialize()
        gmsh.option.set_number("Mesh.Algorithm3D", DELAUNAY_3D)

        if target_sizes is None:
            target_sizes = np.max(
                [
                    np.abs(bounds[1] - bounds[0]),
                    np.abs(bounds[3] - bounds[2]),
                    np.abs(bounds[5] - bounds[4]),
                ]
            )

        if isinstance(target_sizes, float):
            target_sizes = [target_sizes] * edge_source.number_of_points

        for i, (point, target_size) in enumerate(zip(points, target_sizes)):
            id_ = i + 1
            gmsh.model.geo.add_point(point[0], point[1], point[2], target_size, id_)

        surface_loop = []
        for i, face in enumerate(faces):
            gmsh.model.geo.add_line(face[0] + 1, face[1] + 1, i * 4 + 0)
            gmsh.model.geo.add_line(face[1] + 1, face[2] + 1, i * 4 + 1)
            gmsh.model.geo.add_line(face[2] + 1, face[3] + 1, i * 4 + 2)
            gmsh.model.geo.add_line(face[3] + 1, face[0] + 1, i * 4 + 3)
            gmsh.model.geo.add_curve_loop(
                [i * 4 + 0, i * 4 + 1, i * 4 + 2, i * 4 + 3], i + 1
            )
            gmsh.model.geo.add_plane_surface([i + 1], i + 1)
            gmsh.model.geo.remove_all_duplicates()
            gmsh.model.geo.synchronize()
            surface_loop.append(i + 1)

        gmsh.model.geo.add_surface_loop(surface_loop, 1)
        gmsh.model.geo.add_volume([1], 1)

        gmsh.model.geo.synchronize()
        gmsh.model.mesh.generate(3)

        mesh = pv.wrap(extract_to_meshio())
        gmsh.clear()
        gmsh.finalize()

        ind = []
        for i, cell in enumerate(mesh.cell):
            if cell.type != pv.CellType.TETRA:
                ind.append(i)
        mesh = mesh.remove_cells(ind)
        mesh.clear_data()

        return mesh

    @property
    def number_of_points(self: Cube) -> int:
        """Return the number of points in the cube."""
        number_of_points: int = self.cube_data.number_of_points
        return number_of_points

    @property
    def number_of_cells(self: Cube) -> int:
        """Return the number of cells in the cube."""
        number_of_cells: int = self.cube_data.number_of_cells
        return number_of_cells

    @property
    def volume(self: Cube) -> float:
        """Return the volume of the cube."""
        volume: float = self.cube_data.volume
        return volume


class Polygon:
    """Create a polygon."""

    def __init__(self: Polygon, n_sides: int, radius: float) -> None:
        """
        Create a polygon.

        Parameters
        ----------
        n_sides : int
            Number of sides for the polygon.

        radius : float
            Radius of the polygon.

        Examples
        --------
        Create a polygon.

        >>> import skgmsh as sg
        >>> polygon = sg.Polygon(n_sides=4, radius=8)

        """
        self.poly_data: pv.Polygon = pv.Polygon(
            n_sides=n_sides, radius=radius, fill=False
        )

    def frontal_delaunay_2d(
        self: Polygon,
        edge_source: Polygon,
        *,
        target_sizes: float | Sequence[float] | None = None,
    ) -> pv.PolyData | None:
        """
        Frontal-Delaunay 2D mesh algorithm.

        Parameters
        ----------
        edge_source : pyvista.PolyData
            Specify the source object used to specify constrained
            edges and loops. If set, and lines/polygons are defined, a
            constrained triangulation is created. The lines/polygons
            are assumed to reference points in the input point set
            (i.e. point ids are identical in the input and
            source).

        target_sizes : float | Sequence[float], optional
            Target mesh size close to the points.
            Default max size of edge_source in each direction.

        Returns
        -------
        pyvista.PolyData
            Mesh from the 2D delaunay generation.

        """
        points = self.poly_data.points
        lines = edge_source.poly_data.lines
        bounds = edge_source.poly_data.bounds

        gmsh.initialize()
        gmsh.option.set_number("Mesh.Algorithm", FRONTAL_DELAUNAY_2D)

        if target_sizes is None:
            target_sizes = np.max(
                [
                    np.abs(bounds[1] - bounds[0]),
                    np.abs(bounds[3] - bounds[2]),
                    np.abs(bounds[5] - bounds[4]),
                ]
            )

        if isinstance(target_sizes, float):
            target_sizes = [target_sizes] * edge_source.number_of_points

        for i, (target_size, point) in enumerate(zip(target_sizes, points)):
            id_ = i + 1
            gmsh.model.geo.add_point(point[0], point[1], point[2], target_size, id_)

        for i in range(lines[0] - 1):
            id_ = i + 1
            gmsh.model.geo.add_line(lines[i + 1] + 1, lines[i + 2] + 1, id_)

        gmsh.model.geo.add_curve_loop(range(1, lines[0]), 1)
        gmsh.model.geo.add_plane_surface([1], 1)
        gmsh.model.geo.synchronize()
        gmsh.model.mesh.generate(2)
        mesh = extract_to_meshio()
        gmsh.clear()
        gmsh.finalize()

        for cell in mesh.cells:
            if cell.type == "triangle":
                return pv.PolyData.from_regular_faces(mesh.points, cell.data)
        return None

    @property
    def number_of_points(self: Polygon) -> int:
        """Return the number of points in the polygon."""
        number_of_points: int = self.poly_data.number_of_points
        return number_of_points

    @property
    def number_of_cells(self: Polygon) -> int:
        """Return the number of cells in the polygon."""
        number_of_cells: int = self.poly_data.number_of_cells
        return number_of_cells

    @property
    def volume(self: Polygon) -> float:
        """Return the volume of the polygon."""
        volume: float = self.poly_data.volume
        return volume

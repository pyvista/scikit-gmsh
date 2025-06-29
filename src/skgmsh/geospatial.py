"""
Geospatial mesh generation module for scikit-gmsh.

This module provides functionality to generate meshes from geospatial vector data,
similar to pandamesh. It supports conversion of geopandas GeoDataFrames to meshes.
"""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Any

import numpy as np

try:
    from shapely.geometry import MultiPolygon, Polygon
    from shapely.ops import unary_union

    HAS_GEOPANDAS = True
except ImportError:
    HAS_GEOPANDAS = False
    msg = "geopandas is not installed. Geospatial mesh generation will not be available. Install with: pip install geopandas"
    warnings.warn(msg, stacklevel=2)

import pyvista as pv

from . import Delaunay2D

if TYPE_CHECKING:
    import geopandas as gpd


class GeoMesher:
    """
    Generate meshes from geospatial vector data.

    This class provides functionality similar to pandamesh, allowing conversion
    of geopandas GeoDataFrames to unstructured meshes using scikit-gmsh's
    Delaunay triangulation.

    Parameters
    ----------
    geodataframe : geopandas.GeoDataFrame
        The input geodataframe containing polygon geometries and optional
        cellsize information.
    cellsize_column : str, optional
        Name of the column containing cell size values. Default is "cellsize".
    default_cellsize : float, optional
        Default cell size to use if cellsize_column is not found or has missing values.
        If None, uses 1/50th of the maximum extent.

    Examples
    --------
    >>> import geopandas as gpd
    >>> from shapely.geometry import Polygon
    >>> from skgmsh.geospatial import GeoMesher
    >>> # Create a simple GeoDataFrame
    >>> polygon = Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])
    >>> gdf = gpd.GeoDataFrame({"geometry": [polygon], "cellsize": [0.5]})
    >>> # Generate mesh
    >>> mesher = GeoMesher(gdf)
    >>> vertices, faces = mesher.generate()

    """

    def __init__(self, geodataframe: gpd.GeoDataFrame, cellsize_column: str = "cellsize", default_cellsize: float | None = None) -> None:
        """Initialize the GeoMesher."""
        if not HAS_GEOPANDAS:
            msg = "geopandas is required for geospatial mesh generation. Install with: pip install geopandas"
            raise ImportError(msg)

        self.gdf = geodataframe.copy()
        self.cellsize_column = cellsize_column
        self.default_cellsize = default_cellsize

        # Ensure we have polygon geometries
        if not all(self.gdf.geometry.type.isin(["Polygon", "MultiPolygon"])):
            msg = "GeoDataFrame must contain only Polygon or MultiPolygon geometries"
            raise ValueError(msg)

        # Calculate default cellsize if not provided
        if self.default_cellsize is None:
            bounds = self.gdf.total_bounds
            extent = max(bounds[2] - bounds[0], bounds[3] - bounds[1])
            self.default_cellsize = extent / 50.0

    def _prepare_geometry(self) -> tuple[list[tuple[float, float, float]], np.ndarray]:
        """
        Prepare geometry for meshing.

        Returns
        -------
        shell : list
            List of (x, y, z) tuples representing the outer boundary.
        cell_sizes : numpy.ndarray
            Array of cell sizes at each vertex.

        """
        # Combine all geometries
        combined_geom = unary_union(self.gdf.geometry.values)

        # Extract exterior coordinates
        if isinstance(combined_geom, Polygon):
            exterior_coords = np.array(combined_geom.exterior.coords)  # Keep duplicate last point for closure
        elif isinstance(combined_geom, MultiPolygon):
            # For MultiPolygon, use the convex hull as the shell
            combined_geom = combined_geom.convex_hull
            exterior_coords = np.array(combined_geom.exterior.coords)
        else:
            msg = f"Unsupported geometry type: {type(combined_geom)}"
            raise TypeError(msg)

        # Convert to list of (x, y, z) tuples
        shell = [(x, y, 0) for x, y in exterior_coords]

        # Prepare cell sizes
        if self.cellsize_column in self.gdf.columns:
            # For now, use the minimum cell size from the dataframe
            cell_sizes = self.gdf[self.cellsize_column].fillna(self.default_cellsize).min()
        else:
            cell_sizes = self.default_cellsize

        # Create cell size array
        cell_size_array = np.array([cell_sizes])

        return shell, cell_size_array

    def _extract_holes(self) -> list[list[tuple[float, float, float]]]:
        """
        Extract holes from polygons.

        Returns
        -------
        holes : list of pyvista.PolyData
            List of PolyData objects representing holes.

        """
        holes = []

        for geom in self.gdf.geometry:
            if isinstance(geom, Polygon) and geom.interiors:
                for interior in geom.interiors:
                    hole_coords = [(x, y, 0) for x, y in interior.coords]
                    holes.append(hole_coords)
            elif isinstance(geom, MultiPolygon):
                for poly in geom.geoms:
                    if poly.interiors:
                        for interior in poly.interiors:
                            hole_coords = [(x, y, 0) for x, y in interior.coords]
                            holes.append(hole_coords)

        return holes

    def generate(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Generate the mesh.

        Returns
        -------
        vertices : numpy.ndarray
            Array of vertex coordinates with shape (n_vertices, 2).
        faces : numpy.ndarray
            Array of face connectivity with shape (n_faces, 3).

        """
        # Prepare geometry
        shell, cell_sizes = self._prepare_geometry()
        holes = self._extract_holes()

        # Create mesh using scikit-gmsh
        mesher = Delaunay2D(
            shell=shell,  # type: ignore[arg-type]
            holes=holes,  # type: ignore[arg-type]
            cell_size=cell_sizes[0],  # Use uniform cell size for now
        )

        mesh = mesher.mesh

        # Extract vertices and faces
        vertices = mesh.points[:, :2]  # Only keep x, y coordinates
        # For PolyData, faces are stored differently
        if hasattr(mesh, "faces"):
            faces = mesh.faces.reshape(-1, 4)[:, 1:]  # Skip the cell size (first value)
        else:
            # Extract triangles from cells
            cells = mesh.cells
            faces = []
            i = 0
            while i < len(cells):
                n_points = cells[i]
                if n_points == 3:  # Triangle  # noqa: PLR2004
                    faces.append(cells[i + 1 : i + 4])
                i += n_points + 1
            faces = np.array(faces)

        return vertices, faces

    def generate_mesh(self) -> pv.UnstructuredGrid:
        """
        Generate the mesh as a PyVista UnstructuredGrid.

        Returns
        -------
        mesh : pyvista.UnstructuredGrid
            The generated mesh.

        """
        shell, cell_sizes = self._prepare_geometry()
        holes = self._extract_holes()

        mesher = Delaunay2D(shell=shell, holes=holes, cell_size=cell_sizes[0])  # type: ignore[arg-type]

        return mesher.mesh

"""
Example of geospatial mesh generation with scikit-gmsh.

This example demonstrates how to generate meshes from geospatial vector data,
similar to the pandamesh library. It creates a mesh from polygon geometries
defined in a GeoDataFrame.
"""

from __future__ import annotations

import sys

import numpy as np
import pyvista as pv

try:
    import geopandas as gpd
    from shapely.geometry import Polygon
except ImportError:
    print("This example requires geopandas. Install with: pip install geopandas")
    sys.exit(1)

from skgmsh import GeoMesher


def create_sample_geodata() -> gpd.GeoDataFrame:
    """Create a sample GeoDataFrame with some interesting polygons."""
    # Create a main polygon (like a simplified country boundary)
    main_coords = [(0, 0), (10, 0), (12, 3), (15, 5), (15, 10), (12, 12), (10, 15), (5, 15), (3, 12), (0, 10)]
    # main_polygon = Polygon(main_coords)  # Not used directly

    # Create a lake (hole) inside the main polygon
    lake_coords = [(8, 8), (11, 8), (11, 11), (8, 11)]
    polygon_with_hole = Polygon(main_coords, [lake_coords])

    # Create an island polygon
    island_coords = [(3, 3), (6, 3), (6, 6), (3, 6)]
    island = Polygon(island_coords)

    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(
        {
            "name": ["mainland", "island"],
            "geometry": [polygon_with_hole, island],
            "cellsize": [0.5, 0.3],  # Different cell sizes for different features
        }
    )

    return gdf  # noqa: RET504


def main() -> None:
    """Run the geospatial mesh generation example."""
    # Create sample geodata
    print("Creating sample geospatial data...")
    gdf = create_sample_geodata()

    print(f"GeoDataFrame contains {len(gdf)} features:")
    print(gdf[["name", "cellsize"]])

    # Generate mesh using GeoMesher
    print("\nGenerating mesh...")
    mesher = GeoMesher(gdf, cellsize_column="cellsize")

    # Get vertices and faces (pandamesh-style output)
    vertices, faces = mesher.generate()
    print(f"Generated mesh with {len(vertices)} vertices and {len(faces)} faces")

    # Also get as PyVista mesh for visualization
    mesh = mesher.generate_mesh()

    # Add some scalar data for visualization
    mesh["elevation"] = np.sin(mesh.points[:, 0] * 0.5) * np.cos(mesh.points[:, 1] * 0.5)

    # Visualize the result
    print("\nVisualizing mesh...")
    plotter = pv.Plotter()
    plotter.add_mesh(mesh, scalars="elevation", show_edges=True, edge_color="black", line_width=0.5, cmap="terrain")

    # Add the original polygon boundaries for reference
    for _idx, row in gdf.iterrows():
        geom = row.geometry
        if hasattr(geom, "exterior"):
            # Extract exterior coordinates
            coords = np.array(geom.exterior.coords)
            coords_3d = np.column_stack([coords, np.zeros(len(coords))])
            polyline = pv.PolyData(coords_3d)
            n_points = len(coords_3d) - 1
            lines = np.column_stack([np.arange(n_points), np.arange(1, n_points + 1)])
            lines = np.column_stack([np.full(n_points, 2), lines]).ravel()
            polyline.lines = lines
            plotter.add_mesh(polyline, color="red", line_width=3, label=f"{row['name']} boundary")

            # Add interior rings (holes)
            for interior in geom.interiors:
                hole_coords = np.array(interior.coords)
                hole_coords_3d = np.column_stack([hole_coords, np.zeros(len(hole_coords))])
                hole_polyline = pv.PolyData(hole_coords_3d)
                n_points = len(hole_coords_3d) - 1
                lines = np.column_stack([np.arange(n_points), np.arange(1, n_points + 1)])
                lines = np.column_stack([np.full(n_points, 2), lines]).ravel()
                hole_polyline.lines = lines
                plotter.add_mesh(hole_polyline, color="blue", line_width=3, label="hole")

    plotter.add_legend()
    plotter.show_axes()
    plotter.view_xy()
    plotter.show()

    # Print some statistics
    print("\nMesh statistics:")
    print(f"  Total area: {mesh.area:.2f}")
    print(f"  Average cell area: {mesh.area / len(faces):.4f}")
    print(f"  Min cell area: {min(mesh.compute_cell_sizes()['Area']):.4f}")
    print(f"  Max cell area: {max(mesh.compute_cell_sizes()['Area']):.4f}")


if __name__ == "__main__":
    main()

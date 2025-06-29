"""
Simple example of geospatial mesh generation, mimicking pandamesh README example.

This example closely follows the pandamesh README example, showing how to
generate a mesh from a simple polygon with scikit-gmsh's GeoMesher.
"""

from __future__ import annotations

import sys

from matplotlib import tri
import matplotlib.pyplot as plt

try:
    import geopandas as gpd
    from shapely.geometry import Polygon
except ImportError:
    print("This example requires geopandas. Install with: pip install geopandas")
    sys.exit(1)

from skgmsh import GeoMesher


def main() -> None:
    """Run the simple geospatial mesh generation example."""
    # Create a simple polygon (similar to pandamesh's south america example)
    # This is a simplified shape that resembles a geographic region
    coords = [(0, 0), (5, 0), (7, 2), (8, 5), (7, 8), (5, 10), (2, 10), (0, 8), (-1, 5), (0, 2)]
    polygon = Polygon(coords)

    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(
        {
            "geometry": [polygon],
            "cellsize": [0.5],  # Set mesh cell size
        }
    )

    print("Created GeoDataFrame with polygon")
    print(f"Polygon area: {polygon.area:.2f}")
    print(f"Polygon bounds: {polygon.bounds}")

    # Generate mesh using GeoMesher (pandamesh-style API)
    mesher = GeoMesher(gdf)
    vertices, faces = mesher.generate()

    print("\nGenerated mesh with:")
    print(f"  {len(vertices)} vertices")
    print(f"  {len(faces)} triangular faces")

    # Visualize using matplotlib (simple 2D plot)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Plot 1: Original polygon
    ax1.set_title("Original Polygon")
    x, y = polygon.exterior.xy
    ax1.fill(x, y, alpha=0.5, fc="lightblue", ec="black", linewidth=2)
    ax1.plot(x, y, "ko-", markersize=6)
    ax1.set_aspect("equal")
    ax1.grid(visible=True, alpha=0.3)
    ax1.set_xlabel("X")
    ax1.set_ylabel("Y")

    # Plot 2: Generated mesh
    ax2.set_title("Generated Mesh")
    triangulation = tri.Triangulation(vertices[:, 0], vertices[:, 1], faces)
    ax2.triplot(triangulation, "k-", linewidth=0.5, alpha=0.7)
    ax2.plot(vertices[:, 0], vertices[:, 1], "r.", markersize=3)

    # Overlay original polygon boundary
    ax2.fill(x, y, alpha=0.2, fc="lightblue", ec="blue", linewidth=2)
    ax2.set_aspect("equal")
    ax2.grid(visible=True, alpha=0.3)
    ax2.set_xlabel("X")
    ax2.set_ylabel("Y")

    plt.tight_layout()
    plt.show()

    # Print first few vertices and faces (like pandamesh output)
    print("\nFirst 5 vertices (x, y):")
    for i, (x, y) in enumerate(vertices[:5]):
        print(f"  {i}: ({x:.3f}, {y:.3f})")

    print("\nFirst 5 faces (vertex indices):")
    for i, face in enumerate(faces[:5]):
        print(f"  {i}: {face}")


if __name__ == "__main__":
    main()

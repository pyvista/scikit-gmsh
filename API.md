# scikit-gmsh API Documentation

## Overview

scikit-gmsh provides a Python interface to the Gmsh mesh generator, offering both object-oriented and functional APIs for 2D and 3D mesh generation. The library integrates seamlessly with PyVista and supports Shapely geometries.

## Installation

```bash
pip install scikit-gmsh
```

## Quick Start

```python
import skgmsh
import pyvista as pv

# 2D mesh generation
delaunay_2d = skgmsh.Delaunay2D(edge_source=your_polygon)
mesh_2d = delaunay_2d.mesh

# 3D mesh generation  
delaunay_3d = skgmsh.Delaunay3D(edge_source=your_surface)
mesh_3d = delaunay_3d.mesh
```

## Core Classes

### Delaunay2D

**`skgmsh.Delaunay2D(edge_source, shell=None, holes=None, cell_size=None, constrain_edge_size=False)`**

Main class for 2D Delaunay mesh generation.

#### Parameters:
- **edge_source** (`pv.PolyData` | `shapely.geometry.Polygon`): The boundary geometry
- **shell** (`pv.PolyData`, optional): Shell geometry for complex boundaries
- **holes** (`list`, optional): List of hole geometries
- **cell_size** (`float`, optional): Target cell size for mesh generation
- **constrain_edge_size** (`bool`, default=False): Whether to constrain edge sizes

#### Properties:
- **edge_source**: The input boundary geometry
- **mesh**: Generated `pv.UnstructuredGrid` mesh
- **cell_size**: Current cell size setting

#### Methods:
- **enable_recombine()**: Enable quadrilateral recombination
- **disable_recombine()**: Disable quadrilateral recombination

#### Example:
```python
import skgmsh
import shapely.geometry

# Create a polygon
polygon = shapely.geometry.box(0, 0, 10, 10)

# Generate 2D mesh
delaunay_2d = skgmsh.Delaunay2D(edge_source=polygon, cell_size=1.0)
mesh = delaunay_2d.mesh

# Enable quadrilateral elements
delaunay_2d.enable_recombine()
```

### Delaunay3D

**`skgmsh.Delaunay3D(edge_source, cell_size=None)`**

Main class for 3D Delaunay mesh generation.

#### Parameters:
- **edge_source** (`pv.PolyData`): The surface geometry defining the 3D boundary
- **cell_size** (`float`, optional): Target cell size for mesh generation

#### Properties:
- **edge_source**: The input surface geometry
- **mesh**: Generated `pv.UnstructuredGrid` mesh
- **cell_size**: Current cell size setting

#### Example:
```python
import skgmsh
import pyvista as pv

# Load or create a surface mesh
surface = pv.Sphere()

# Generate 3D mesh
delaunay_3d = skgmsh.Delaunay3D(edge_source=surface, cell_size=0.5)
mesh = delaunay_3d.mesh
```

## Functional API

### delaunay_3d

**`skgmsh.delaunay_3d(edge_source, target_sizes=None)`**

Standalone function for 3D Delaunay mesh generation.

#### Parameters:
- **edge_source** (`pv.PolyData`): Surface geometry
- **target_sizes** (`dict`, optional): Target sizes for mesh refinement

#### Returns:
- `pv.UnstructuredGrid`: Generated 3D mesh

#### Example:
```python
import skgmsh
import pyvista as pv

surface = pv.Sphere()
mesh = skgmsh.delaunay_3d(edge_source=surface)
```

### frontal_delaunay_2d

**`skgmsh.frontal_delaunay_2d(edge_source, target_sizes=None, recombine=False)`**

Standalone function for 2D Frontal-Delaunay mesh generation.

#### Parameters:
- **edge_source** (`pv.PolyData` | `shapely.geometry.Polygon`): Boundary geometry
- **target_sizes** (`dict`, optional): Target sizes for mesh refinement
- **recombine** (`bool`, default=False): Enable quadrilateral recombination

#### Returns:
- `pv.UnstructuredGrid`: Generated 2D mesh

#### Example:
```python
import skgmsh
import shapely.geometry

polygon = shapely.geometry.box(0, 0, 5, 5)
mesh = skgmsh.frontal_delaunay_2d(edge_source=polygon, recombine=True)
```

## Utility Classes

### Report

**`skgmsh.Report()`**

System diagnostics and environment reporting, inheriting from `scooby.Report`.

#### Example:
```python
import skgmsh

# Generate system report
report = skgmsh.Report()
print(report)
```

## Constants

### Mesh Algorithms
- `INITIAL_MESH_ONLY_2D`: Initial mesh only for 2D
- `FRONTAL_DELAUNAY_2D`: Frontal-Delaunay algorithm for 2D
- `DELAUNAY_3D`: Delaunay algorithm for 3D

### Configuration
- `SILENT`: Silent mode flag
- `SIMPLE`: Simple mode flag
- `TRUE`/`FALSE`: Boolean constants for Gmsh configuration

## Integration with Scientific Python Ecosystem

### PyVista Integration
scikit-gmsh seamlessly integrates with PyVista for mesh visualization and processing:

```python
import skgmsh
import pyvista as pv

# Generate mesh
delaunay_2d = skgmsh.Delaunay2D(edge_source=polygon)
mesh = delaunay_2d.mesh

# Visualize with PyVista
plotter = pv.Plotter()
plotter.add_mesh(mesh, show_edges=True)
plotter.show()
```

### Shapely Integration
Support for Shapely geometries enables easy geometric operations:

```python
import skgmsh
import shapely.geometry

# Create complex geometry with holes
outer = shapely.geometry.box(0, 0, 10, 10)
hole = shapely.geometry.box(4, 4, 6, 6)
polygon_with_hole = outer.difference(hole)

# Generate mesh
delaunay_2d = skgmsh.Delaunay2D(edge_source=polygon_with_hole)
```

## Error Handling

The library provides informative error messages for common issues:
- Invalid geometry input
- Gmsh execution errors
- Memory limitations
- Unsupported mesh configurations

## Performance Considerations

- **Cell Size**: Smaller cell sizes result in finer meshes but longer computation times
- **Geometry Complexity**: Complex geometries with many features require more processing
- **Memory Usage**: Large 3D meshes can consume significant memory
- **Gmsh Backend**: Performance depends on the underlying Gmsh installation

## Examples

See the `examples/` directory for comprehensive usage examples:
- Basic 2D and 3D mesh generation
- Complex geometries with holes
- PyVista integration
- Mesh refinement techniques
- Visualization workflows

## Dependencies

- **gmsh**: Core mesh generation engine
- **pyvista**: Mesh processing and visualization
- **shapely**: Geometric operations
- **numpy**: Numerical computations
- **scooby**: System reporting
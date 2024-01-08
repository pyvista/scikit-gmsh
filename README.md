<h1 align="center">
  <a href="https://github.com/pyvista/pvgmsh#--------">
    <img src="https://raw.githubusercontent.com/pyvista/pvgmsh/main/branding/logo/logomark/pvgmsh_logo_icon.svg"
         alt="PVGmsh"
         width="200"></a>
</h1>

<h3 align="center">
PyVista accessors for Gmsh to generate 3D finite element mesh.
</h3>

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Motivation

See discussion: https://github.com/pyvista/pyvista/discussions/2133#discussioncomment-2107992

## Usage

```python
    >>> import pyvista as pv
    >>> import pvgmsh as pm
```

We can define the surface using PyVista.

```python
    >>> edge_source = pv.Polygon(n_sides=4, radius=8, fill=False)
    >>> edge_source = edge_source.rotate_z(45, inplace=False)
```

We can then generate a 2D mesh.

```python
    >>> mesh = pm.frontal_delaunay_2d(edge_source, target_size=1.0)
```

To visualize the model we can use PyVista.

```python
    >>> plotter = pv.Plotter()
    >>> _ = plotter.add_mesh(mesh, show_edges=True, line_width=4, color="white")
    >>> _ = plotter.add_mesh(edge_source, show_edges=True, line_width=4, color="red")
    >>> _ = plotter.add_points(
    ...     edge_source.points, style="points", point_size=20, color="red"
    ... )
    >>> plotter.show(cpos="xy")
```

![frontal_delaunay_2d_01](https://github.com/pyvista/pvgmsh/raw/main/frontal_delaunay_2d_01.png)

# pvgmsh

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Documentation Status](https://readthedocs.org/projects/pvgmsh/badge/?version=latest)](https://pvgmsh.readthedocs.io/en/latest/?badge=latest)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/pyvista/pvgmsh/main.svg)](https://results.pre-commit.ci/latest/github/pyvista/pvgmsh/main)
[![NEP29](https://raster.shields.io/badge/follows-NEP29-orange.png)](https://numpy.org/neps/nep-0029-deprecation_policy.html)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Contributor Covenant](https://img.shields.io/badge/contributor%20covenant-2.1-4baaaa.svg)](https://github.com/pyvista/pvgmsh/blob/main/CODE_OF_CONDUCT.md)
[![GitHub Repo stars](https://img.shields.io/github/stars/pyvista/pvgmsh)](https://github.com/pyvista/pvgmsh/stargazers)

[<img src="https://raw.githubusercontent.com/pyvista/pvgmsh/main/docs/_static/pvgmsh_logo_icon.svg" align="left" width="100">](https://github.com/pyvista/pvgmsh#--------)

> PyVista accessors for Gmsh to generate 3D finite element mesh.

The goal of this project is to use the visualization capabilities of PyVista to make all the features of Gmsh easier to use.

This project was initiated to enhance PyVista's Delaunay triangulation of the mesh functionality with Gmsh.

See discussion: https://github.com/pyvista/pyvista/discussions/2133#discussioncomment-2107992

## Table of Contents

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Motivation](#motivation)
- [Installation](#installation)
  - [Developer](#developer)
- [Usage](#usage)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Installation

### Developer

If you simply can't wait for the next release to play with the latest hot features, then you can easily
install the `main` development branch from GitHub:

```shell
pip install git+https://github.com/pyvista/pvgmsh@main
```

## Usage

```python
import pyvista as pv
import pvgmsh as pm
```

We can define the surface using PyVista.

```python
edge_source = pv.Polygon(n_sides=4, radius=8, fill=False)
```

We can then generate a 2D mesh.

```python
mesh = pm.frontal_delaunay_2d(edge_source, target_sizes=2.0)
```

To visualize the model we can use PyVista.

```python
plotter = pv.Plotter()
_ = plotter.add_mesh(
    mesh,
    show_edges=True,
    line_width=4,
    color="white",
    lighting=False,
    edge_color=[153, 153, 153],
)
_ = plotter.add_mesh(edge_source, show_edges=True, line_width=4, color=[214, 39, 40])
_ = plotter.add_points(
    edge_source.points, style="points", point_size=20, color=[214, 39, 40]
)
_ = plotter.add_legend(
    [[" edge source", [214, 39, 40]], [" mesh ", [153, 153, 153]]],
    bcolor="white",
    face="r",
    size=(0.3, 0.3),
)
plotter.show(cpos="xy")
```

![2D mesh](/docs/_static/frontal_delaunay_2d_01.png)

We can also generate a 3D mesh.

```python
edge_source = pv.Cube()
mesh = pm.delaunay_3d(edge_source, target_sizes=0.4)
```

```python
plotter = pv.Plotter()
_ = plotter.add_mesh(
    mesh,
    show_edges=True,
    line_width=4,
    color="white",
    lighting=False,
    edge_color=[153, 153, 153],
)
_ = plotter.add_mesh(edge_source.extract_all_edges(), line_width=4, color=[214, 39, 40])
_ = plotter.add_points(
    edge_source.points, style="points", point_size=20, color=[214, 39, 40]
)
plotter.enable_parallel_projection()
_ = plotter.add_axes(
    box=True,
    box_args={
        "opacity": 0.5,
        "color_box": True,
        "x_face_color": "white",
        "y_face_color": "white",
        "z_face_color": "white",
    },
)
plotter.show()
```

![3D mesh](/docs/_static/delaunay_3d_01.png)

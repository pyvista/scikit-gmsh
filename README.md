🚧 scikit-gmsh is in the pre-alpha stage. The interface could be subject to significant changes soon.

# scikit-gmsh

[<img src="https://raw.githubusercontent.com/pyvista/scikit-gmsh/main/docs/_static/logo.svg" align="left" width="200">](https://github.com/pyvista/scikit-gmsh#--------)

> Scikit for Gmsh to generate 3D finite element mesh.

[![Documentation Status](https://readthedocs.org/projects/scikit-gmsh/badge/?version=latest&style=for-the-badge)](https://scikit-gmsh.readthedocs.io/en/latest/?badge=latest)
[![Contributor Covenant](https://img.shields.io/badge/contributor%20covenant-2.1-4baaaa.svg?style=for-the-badge)](https://github.com/pyvista/scikit-gmsh/blob/main/CODE_OF_CONDUCT.md)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=for-the-badge&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=for-the-badge)](https://github.com/astral-sh/ruff)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=for-the-badge)](https://github.com/prettier/prettier)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg?style=for-the-badge)](https://www.gnu.org/licenses/gpl-3.0)

Contributions _very welcome_ but first see [Contributing](#contributions).
Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md).
By participating in this project you agree to abide by its terms.

---

[![GitHub Repo stars](https://img.shields.io/github/stars/pyvista/scikit-gmsh?style=for-the-badge)](https://github.com/pyvista/scikit-gmsh/stargazers)

Enjoying scikit-gmsh? Show your support with a [Github star](https://github.com/pyvista/scikit-gmsh) — it’s a simple click that means the world to us and helps others discover it too! ⭐️

---

## Table of Contents

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Installation](#installation)
  - [Developer](#developer)
- [Usage](#usage)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Installation

### Developer

If you simply can't wait for the next release to play with the latest hot features, then you can easily
install the `main` development branch from GitHub:

```shell
pip install git+https://github.com/pyvista/scikit-gmsh@main
```

## Usage

```python
import skgmsh as sg
```

We can define the surface using PyVista.

```python
edge_source = sg.Polygon(n_sides=4, radius=8, fill=False)
```

We can then generate a 2D mesh.

```python
mesh = sg.frontal_delaunay_2d(edge_source, target_sizes=2.0)
```

To visualize the model we can use PyVista.

```python
plotter = sg.Plotter()
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

<p align="center">
<img src="https://raw.githubusercontent.com/pyvista/scikit-gmsh/main/docs/_static/frontal_delaunay_2d_01.png" align="center" width=512 >
</p>

We can also generate a 3D mesh.

```python
edge_source = sg.Cube()
mesh = sg.delaunay_3d(edge_source, target_sizes=0.2)
```

```python
plotter = sg.Plotter()
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

<p align="center">
<img src="https://raw.githubusercontent.com/pyvista/scikit-gmsh/main/docs/_static/delaunay_3d_01.png" align="center" width=512 >
</p>

We can clip a mesh by a plane by specifying the origin and normal.
See [clip_with_surface_example](https://docs.pyvista.org/examples/01-filter/clipping-with-surface#clip-with-surface-example) for more examples using this filter.

```python
clipped = mesh.clip(origin=(0.0, 0.0, 0.0), normal=(0.0, 0.0, 1.0), crinkle=True)
```

<p align="center">
<img src="https://raw.githubusercontent.com/pyvista/scikit-gmsh/main/docs/_static/delaunay_3d_02.png" align="center" width=512 >
</p>

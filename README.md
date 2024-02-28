🚧 scikit-gmsh is in the pre-alpha stage the interface could be subject to important changes soon.

# scikit-gmsh

[![Documentation Status](https://readthedocs.org/projects/scikit-gmsh/badge/?version=latest)](https://scikit-gmsh.readthedocs.io/en/latest/?badge=latest)

[<img src="https://raw.githubusercontent.com/pyvista/scikit-gmsh/main/docs/_static/logo.svg" align="left" width="200">](https://github.com/pyvista/scikit-gmsh#--------)

> PyVista accessors for Gmsh to generate 3D finite element mesh.

💡 We expect that this makes it easy to use Gmsh in a Jupyter environment.

💡 Also, this is a collection of 2D and 3D finite element mesh examples.

Contributions _very welcome_ but first see [Contributing](#contributions).
Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md).
By participating in this project you agree to abide by its terms.

---

[![GitHub Repo stars](https://img.shields.io/github/stars/pyvista/scikit-gmsh)](https://github.com/pyvista/scikit-gmsh/stargazers)

Enjoying scikit-gmsh? Show your support with a [Github star](https://github.com/pyvista/scikit-gmsh) — it’s a simple click that means the world to us and helps others discover it too! ⭐️

---

## Table of Contents

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Installation](#installation)
  - [Developer](#developer)
- [Usage](#usage)
- [Contributions](#contributions)
- [License](#license)

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
import pyvista as pv
import skgmsh as sg
```

We can define the surface using PyVista.

```python
edge_source = pv.Polygon(n_sides=12, radius=8, fill=False)
```

We can then generate a 2D mesh.

```python
mesh = sg.frontal_delaunay_2d(edge_source, target_sizes=8.0)
```

To visualize the model we can use PyVista.

```python
plotter = pv.Plotter()
_ = plotter.add_mesh(
    mesh,
    show_edges=True,
    line_width=4,
    color="white",
    lighting=True,
    edge_color=[153, 153, 153],
)
_ = plotter.add_mesh(edge_source, show_edges=True, line_width=4, color=[214, 39, 40])
_ = plotter.add_legend(
    [[" source", [214, 39, 40]], [" mesh", [153, 153, 153]]],
    bcolor="white",
    face="r",
    size=(0.1, 0.1),
)
plotter.show(cpos="xy")
```

<p align="center">
<img src="https://raw.githubusercontent.com/pyvista/scikit-gmsh/main/docs/_static/frontal_delaunay_2d_01.png" align="center" width=512 >
</p>

We can also generate a 3D mesh.

```python
edge_source = pv.Cube()
mesh = sg.delaunay_3d(edge_source, target_sizes=0.2)
```

```python
plotter = pv.Plotter()
_ = plotter.add_mesh(
    mesh,
    show_edges=True,
    line_width=4,
    color="white",
    lighting=True,
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

## Contributions

[![Contributor Covenant](https://img.shields.io/badge/contributor%20covenant-2.1-4baaaa.svg)](https://github.com/pyvista/scikit-gmsh/blob/main/CODE_OF_CONDUCT.md)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/pyvista/scikit-gmsh/main.svg)](https://results.pre-commit.ci/latest/github/pyvista/scikit-gmsh/main)
[![NEP29](https://raster.shields.io/badge/follows-NEP29-orange.png)](https://numpy.org/neps/nep-0029-deprecation_policy.html)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)

## License

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

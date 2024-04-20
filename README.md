🚧 scikit-gmsh is in the pre-alpha stage. The interface could be subject to significant changes soon.

# scikit-gmsh

[<img src="https://raw.githubusercontent.com/pyvista/scikit-gmsh/main/docs/_static/logo.svg" align="left" width="200">](https://github.com/pyvista/scikit-gmsh#--------)

> Scikit for Gmsh to generate 3D finite element mesh.

[![Contributing](https://img.shields.io/badge/PR-Welcome-%23FF8300.svg?style=for-the-badge)](https://github.com/pyvista/scikit-gmsh/issues)

Contributions are _very welcome_ .
This project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md).
By participating in this project, We want you to know that you agree to follow its terms.

---

[![GitHub Repo stars](https://img.shields.io/github/stars/pyvista/scikit-gmsh?style=for-the-badge)](https://github.com/pyvista/scikit-gmsh/stargazers)

Enjoying scikit-gmsh? Show your support with a [GitHub star](https://github.com/pyvista/scikit-gmsh) — it’s a simple click that means the world to us and helps others discover it, too! ⭐️

---

## Table of Contents

[![Documentation Status](https://readthedocs.org/projects/scikit-gmsh/badge/?version=latest&style=for-the-badge)](https://scikit-gmsh.readthedocs.io/en/latest/?badge=latest)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Installation](#installation)
  - [Pip](#pip)
  - [Developer](#developer)
- [Usage](#usage)
- [License](#license)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Installation

scikit-gmsh is available on [PyPI](https://pypi.org/project/scikit-gmsh/).

### Pip

scikit-gmsh is also available on [PyPI](https://pypi.org/project/scikit-gmsh/):

```shell
pip install scikit-gmsh
```

### Developer

If you can't wait for the next release to play with the latest hot features, then you can easily
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
source = sg.Polygon(n_sides=4, radius=8, fill=False)
```

We can then generate a 2D mesh.

```python
mesh = source.frontal_delaunay_2d(edge_source=source, target_sizes=2.0)
```

To visualize the model, we can use PyVista.

```python
plotter = sg.Plotter()
_ = plotter.add_mesh(
    mesh,
    show_edges=True,
    line_width=1,
    color="aliceblue",
    lighting=False,
    edge_color="gray",
)
_ = plotter.add_mesh(source, show_edges=True, line_width=4, color="gray")
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
    line_width=1,
    color="aliceblue",
    lighting=False,
    edge_color="gray",
)
_ = plotter.add_mesh(edge_source.extract_all_edges(), line_width=4, color="gray")
_ = plotter.add_box_axes()
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

## License

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg?style=for-the-badge)](https://www.gnu.org/licenses/gpl-3.0)

This software is published under the [GPLv3 license](https://www.gnu.org/licenses/gpl-3.0.en.html).

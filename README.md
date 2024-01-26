<h1 align="center">
  <a href="https://github.com/pyvista/pvgmsh#--------">
    <img src="https://raw.githubusercontent.com/pyvista/pvgmsh/main/docs/_static/pvgmsh_logo_icon.svg"
         alt="PVGmsh"
         width="200"></a>
</h1>

<h3 align="center">
PyVista accessors for Gmsh to generate 3D finite element mesh.
</h3>

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Documentation Status](https://readthedocs.org/projects/pvgmsh/badge/?version=latest)](https://pvgmsh.readthedocs.io/en/latest/?badge=latest)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/pyvista/pvgmsh/main.svg)](https://results.pre-commit.ci/latest/github/pyvista/pvgmsh/main)
[![NEP29](https://raster.shields.io/badge/follows-NEP29-orange.png)](https://numpy.org/neps/nep-0029-deprecation_policy.html)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Contributor Covenant](https://img.shields.io/badge/contributor%20covenant-2.1-4baaaa.svg)](https://github.com/pyvista/pvgmsh/blob/main/CODE_OF_CONDUCT.md)
[![GitHub Repo stars](https://img.shields.io/github/stars/pyvista/pvgmsh)](https://github.com/pyvista/pvgmsh/stargazers)

## Motivation

See discussion: https://github.com/pyvista/pyvista/discussions/2133#discussioncomment-2107992

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

<details>
<summary>🗒 </summary>

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

</details>

<h1 align="center">
  <img src="https://github.com/pyvista/pvgmsh/raw/main/docs/_static/frontal_delaunay_2d_01.png" width="500">
</h1>

We can also generate a 3D mesh.

```python
edge_source = pv.Cube()
mesh = pm.delaunay_3d(edge_source, target_sizes=0.4)
```

<details>
<summary>🗒 </summary>

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

</details>

<h1 align="center">
  <img src="https://github.com/pyvista/pvgmsh/raw/main/docs/_static/delaunay_3d_01.png" width="500">
</h1>

# Authors

<a href="https://github.com/pyvista/pvgmsh/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=pyvista/pvgmsh" />
</a>

Made with [contrib.rocks](https://contrib.rocks).

## License

pvgmsh is distributed under the terms of the [GNU General Public License v3.0 or later](https://spdx.org/licenses/GPL-3.0-or-later.html) license.

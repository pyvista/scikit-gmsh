> [!CAUTION]
> scikit-gmsh is in the pre-alpha stage. The interface could be subject to significant changes soon. 

# scikit-gmsh

[<img src="https://raw.githubusercontent.com/pyvista/scikit-gmsh/main/docs/_static/logo.svg" align="left" width="200">](https://github.com/pyvista/scikit-gmsh#--------)

> Scikit for Gmsh to generate 3D finite element mesh.

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->

[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)

<!-- ALL-CONTRIBUTORS-BADGE:END -->

[![Contributing](https://img.shields.io/badge/PR-Welcome-%23FF8300.svg?style=flat-square)](https://github.com/pyvista/scikit-gmsh/issues)
[![GitHub Repo stars](https://img.shields.io/github/stars/pyvista/scikit-gmsh?style=flat-square)](https://github.com/pyvista/scikit-gmsh/stargazers)

Contributions are _very welcome_ .
This project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md).
By participating in this project, We want you to know that you agree to follow its terms.

---

Enjoying scikit-gmsh? Show your support with a [GitHub star](https://github.com/pyvista/scikit-gmsh) — it’s a simple click that means the world to us and helps others discover it, too! ⭐️

---

## Table of Contents

[![Documentation Status](https://readthedocs.org/projects/scikit-gmsh/badge/?version=latest&style=flat-square)](https://scikit-gmsh.readthedocs.io/en/latest/?badge=latest)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Contributors ✨](#contributors-)
- [Star History](#star-history)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Installation

[![pypi](https://img.shields.io/pypi/v/scikit-gmsh?style=flat-square&label=pypi&logo=python&logoColor=white)](https://pypi.org/project/scikit-gmsh/)

```shell
pip install scikit-gmsh
```

## Usage

```python
import pyvista as pv
import skgmsh as sg
```

We can define the surface using PyVista.

```python
source = pv.Polygon(n_sides=4, radius=8, fill=False)
```

We can then generate a 2D mesh.

```python
mesh = sg.frontal_delaunay_2d(edge_source=source, target_sizes=2.0)
```

To visualize the model, we can use PyVista.

```python
plotter = pv.Plotter()
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
source = pv.Cube()
mesh = sg.delaunay_3d(edge_source=source, target_sizes=0.2)
```

```python
plotter = pv.Plotter()
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

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg?style=flat-square)](https://www.gnu.org/licenses/gpl-3.0)

This software is published under the [GPLv3 license](https://www.gnu.org/licenses/gpl-3.0.en.html).

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/tkoyama010"><img src="https://avatars.githubusercontent.com/u/7513610?v=4?s=100" width="100px;" alt="Tetsuo Koyama"/><br /><sub><b>Tetsuo Koyama</b></sub></a><br /><a href="#infra-tkoyama010" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/pyvista/scikit-gmsh/commits?author=tkoyama010" title="Tests">⚠️</a> <a href="https://github.com/pyvista/scikit-gmsh/commits?author=tkoyama010" title="Code">💻</a> <a href="#ideas-tkoyama010" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://allcontributors.org"><img src="https://avatars.githubusercontent.com/u/46410174?v=4?s=100" width="100px;" alt="All Contributors"/><br /><sub><b>All Contributors</b></sub></a><br /><a href="https://github.com/pyvista/scikit-gmsh/commits?author=all-contributors" title="Documentation">📖</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=pyvista/scikit-gmsh&type=Date)](https://star-history.com/#pyvista/scikit-gmsh&Date)

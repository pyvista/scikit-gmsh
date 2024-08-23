<h1 align="center">
  <a href="https://github.com/pyvista/scikit-gmsh#--------">
    <img src="https://raw.githubusercontent.com/pyvista/scikit-gmsh/main/docs/_static/logo.svg"
         alt="scikit-gmsh"
         width="200"></a>
</h1>

> Scikit for Gmsh to generate 3D finite element mesh.

[![All Contributors](https://img.shields.io/github/all-contributors/pyvista/scikit-gmsh?color=ee8449)](https://scikit-gmsh.readthedocs.io/en/latest/reference/about.html#contributors)
[![Contributing](https://img.shields.io/badge/PR-Welcome-%23FF8300.svg)](https://github.com/pyvista/scikit-gmsh/issues)
[![Documentation Status](https://readthedocs.org/projects/scikit-gmsh/badge/?version=latest)](https://scikit-gmsh.readthedocs.io/en/latest/?badge=latest)
[![GitHub Repo stars](https://img.shields.io/github/stars/pyvista/scikit-gmsh)](https://github.com/pyvista/scikit-gmsh/stargazers)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

The `scikit-gmsh` package provides a simple interface to the `gmsh` library.
The library has following main objectives:

1. Provide an intuitive, object-oriented API for mesh creation like [scipy.spatial.Delaunay class](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Delaunay.html).
1. Integrate seamlessly with other libraries in the [Scientific Python ecosystem](https://scientific-python.org/).

Contributions are _very welcome_ .
This project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md).
By participating in this project, We want you to know that you agree to follow its terms.

Enjoying scikit-gmsh? Show your support with a [GitHub star](https://github.com/pyvista/scikit-gmsh) — it’s a simple click that means the world to us and helps others discover it, too! ⭐️

## Installation

[![pypi](https://img.shields.io/pypi/v/scikit-gmsh?label=pypi&logo=python&logoColor=white)](https://pypi.org/project/scikit-gmsh/)

```shell
pip install scikit-gmsh
```

## Usage

```python
import skgmsh as sg
```

Now, let's define geometry.

```python
shell = [(0, 0, 0), (0, 10, 0), (10, 10, 0), (10, 0, 0), (0, 0, 0)]
holes = [[(2, 2, 0), (2, 4, 0), (4, 4, 0), (4, 2, 0), (2, 2, 0)]]
```

We can then generate a 2D mesh.

```python
alg = sg.Delaunay2D(shell=shell, holes=holes)
mesh = alg.mesh
```

To visualize the model, we can use PyVista.

```python
mesh.plot(show_edges=True, cpos="xy")
```

<p align="center">
<img src="https://raw.githubusercontent.com/pyvista/scikit-gmsh/main/docs/_static/frontal_delaunay_2d_01.png" align="center" width=400 >
</p>

If you want to set the cell size, you can do so.

```python
alg.cell_size = 0.5
alg.mesh.plot(show_edges=True, cpos="xy")
```

<p align="center">
<img src="https://raw.githubusercontent.com/pyvista/scikit-gmsh/main/docs/_static/frontal_delaunay_2d_02.png" align="center" width=400 >
</p>

We can also generate a 3D mesh.

```python
source = pv.Cube()
delaunay_3d = sg.Delaunay3D(edge_source=source, target_sizes=0.2)
```

```python
plotter = pv.Plotter()
_ = plotter.add_mesh(
    delaunay_3d.mesh,
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
<img src="https://raw.githubusercontent.com/pyvista/scikit-gmsh/main/docs/_static/delaunay_3d_01.png" align="center" width=400 >
</p>

We can clip a mesh by a plane by specifying the origin and normal.
See [clip_with_surface_example](https://docs.pyvista.org/examples/01-filter/clipping-with-surface#clip-with-surface-example) for more examples using this filter.

```python
clipped = delaunay_3d.mesh.clip(
    origin=(0.0, 0.0, 0.0), normal=(0.0, 0.0, 1.0), crinkle=True
)
```

<p align="center">
<img src="https://raw.githubusercontent.com/pyvista/scikit-gmsh/main/docs/_static/delaunay_3d_02.png" align="center" width=400 >
</p>

## License

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This software is published under the [GPLv3 license](https://www.gnu.org/licenses/gpl-3.0.en.html).

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=pyvista/scikit-gmsh&type=Date)](https://star-history.com/#pyvista/scikit-gmsh&Date)

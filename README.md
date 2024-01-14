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
import pyvista as pv
import pvgmsh as pm
```

We can define the surface using PyVista.

```python
edge_source = pv.Polygon(n_sides=4, radius=8, fill=False)
```

We can then generate a 2D mesh.

```python
mesh = pm.frontal_delaunay_2d(edge_source, target_size=2.0)
```

To visualize the model we can use PyVista.

<details>
<summary>🗒 </summary>

```python
plotter = pv.Plotter()
_ = plotter.add_mesh(mesh, show_edges=True, line_width=4, color="white", lighting=False)
_ = plotter.add_mesh(edge_source, show_edges=True, line_width=4, color="red")
_ = plotter.add_points(
    edge_source.points, style="points", point_size=20, color="red"
)
_ = plotter.add_legend([[" source", "red"], [" mesh ", "black"]], bcolor="white", face="r")
plotter.show(cpos="xy")
```
</details>

![frontal_delaunay_2d_01](https://github.com/pyvista/pvgmsh/raw/main/frontal_delaunay_2d_01.png)

We can also generate a 3D mesh.

<details>
<summary>🗒 </summary>

```python
import pyvista as pv
import pvgmsh as pm

edge_source = pv.Cube()
mesh = pm.delaunay_3d(edge_source, target_size=0.5)

plotter = pv.Plotter()
_ = plotter.add_mesh(mesh, show_edges=True, line_width=4, color="white", lighting=False)
_ = plotter.add_mesh(edge_source.extract_all_edges(), line_width=4, color="red")
_ = plotter.add_points(edge_source.points, style="points", point_size=20, color="red")
plotter.enable_parallel_projection()
_ = plotter.add_axes(
    box=True, box_args={"opacity": 0.5, "color_box": True, "x_face_color": "white", "y_face_color": "white", "z_face_color": "white"}
)
plotter.show()
```
</details>

![delaunay_3d_01](https://github.com/pyvista/pvgmsh/raw/main/delaunay_3d_01.png)

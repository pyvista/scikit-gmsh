<h1 align="center">
  <a href="https://github.com/pyvista/scikit-gmsh#--------">
    <img src="https://raw.githubusercontent.com/pyvista/scikit-gmsh/main/docs/_static/logo.svg"
         alt="scikit-gmsh"
         width="200"></a>
</h1>

> Scikit for Gmsh to generate 3D finite element mesh.

[![Status](https://badgen.net/badge/status/alpha/d8624d)](https://badgen.net/badge/status/alpha/d8624d)
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

## Gallery

Check out the example galleries organized by subject here:
<p align="center">
  <a href="https://felupe.readthedocs.io/en/latest/examples/ex01_beam.html"><img src="https://felupe.readthedocs.io/en/latest/_images/sphx_glr_ex01_beam_thumb.png" height="100px"/></a> <a href="https://felupe.readthedocs.io/en/latest/examples/ex02_plate-with-hole.html"><img src="https://felupe.readthedocs.io/en/latest/_images/sphx_glr_ex02_plate-with-hole_thumb.png" height="100px"/></a> <a
  href="https://felupe.readthedocs.io/en/latest/examples/ex03_plasticity.html"><img src="https://felupe.readthedocs.io/en/latest/_images/sphx_glr_ex03_plasticity_thumb.png" height="100px"/></a> <a
  href="https://felupe.readthedocs.io/en/latest/examples/ex04_balloon.html"><img src="https://felupe.readthedocs.io/en/latest/_images/sphx_glr_ex04_balloon_thumb.png" height="100px"/></a> <a
  href="https://felupe.readthedocs.io/en/latest/examples/ex05_rubber-metal-bushing.html"><img src="https://felupe.readthedocs.io/en/latest/_images/sphx_glr_ex05_rubber-metal-bushing_thumb.png" height="100px"/></a> <a
  href="https://felupe.readthedocs.io/en/latest/examples/ex06_rubber-metal-spring.html"><img src="https://felupe.readthedocs.io/en/latest/_images/sphx_glr_ex06_rubber-metal-spring_thumb.png" height="100px"/></a> <a
  href="https://felupe.readthedocs.io/en/latest/examples/ex07_engine-mount.html"><img src="https://felupe.readthedocs.io/en/latest/_images/sphx_glr_ex07_engine-mount_thumb.png" height="100px"/></a> <a
  href="https://felupe.readthedocs.io/en/latest/examples/ex08_shear.html"><img src="https://felupe.readthedocs.io/en/latest/_images/sphx_glr_ex08_shear_thumb.png" height="100px"/></a> <a
  href="https://felupe.readthedocs.io/en/latest/examples/ex09_numeric-continuation.html"><img src="https://felupe.readthedocs.io/en/latest/_images/sphx_glr_ex09_numeric-continuation_thumb.png" height="100px"/></a> <a
  href="https://felupe.readthedocs.io/en/latest/examples/ex10_poisson-equation.html"><img src="https://felupe.readthedocs.io/en/latest/_images/sphx_glr_ex10_poisson-equation_thumb.png" height="100px"/></a> <a
  href="https://felupe.readthedocs.io/en/latest/examples/ex11_notch-stress.html"><img src="https://felupe.readthedocs.io/en/latest/_images/sphx_glr_ex11_notch-stress_thumb.png" height="100px"/></a> <a
  href="https://felupe.readthedocs.io/en/latest/examples/ex12_foot-bone.html"><img src="https://felupe.readthedocs.io/en/latest/_images/sphx_glr_ex12_foot-bone_thumb.png" height="100px"/></a> <a
  href="https://felupe.readthedocs.io/en/latest/examples/ex13_morph-rubber-wheel.html"><img src="https://felupe.readthedocs.io/en/latest/_images/sphx_glr_ex13_morph-rubber-wheel_thumb.png" height="100px"/></a> <a
  href="https://felupe.readthedocs.io/en/latest/examples/ex14_hyperelasticity.html"><img src="https://felupe.readthedocs.io/en/latest/_images/sphx_glr_ex14_hyperelasticity_thumb.png" height="100px"/></a> <a
  href="https://felupe.readthedocs.io/en/latest/examples/ex15_hexmesh-metacone.html"><img src="https://felupe.readthedocs.io/en/latest/_images/sphx_glr_ex15_hexmesh-metacone_thumb.png" height="100px"/></a> <a
  href="https://felupe.readthedocs.io/en/latest/examples/ex16_deeplearning-torch.html"><img src="https://felupe.readthedocs.io/en/latest/_images/sphx_glr_ex16_deeplearning-torch_thumb.png" height="100px"/></a> <a
  href="https://felupe.readthedocs.io/en/latest/examples/ex17_torsion-gif.html"><img src="https://felupe.readthedocs.io/en/latest/_images/sphx_glr_ex17_torsion-gif_thumb.gif" height="100px"/></a> <a
  href="https://felupe.readthedocs.io/en/latest/examples/ex18_nonlinear-viscoelasticity-newton.html"><img src="https://felupe.readthedocs.io/en/latest/_images/sphx_glr_ex18_nonlinear-viscoelasticity-newton_thumb.png" height="100px"/></a> <a
  href="https://felupe.readthedocs.io/en/latest/examples/ex19_taylor-hood.html"><img src="https://felupe.readthedocs.io/en/latest/_images/sphx_glr_ex19_taylor-hood_thumb.png" height="100px"/></a> <a
  href="https://felupe.readthedocs.io/en/latest/examples/ex20_third-medium-contact.html"><img src="https://felupe.readthedocs.io/en/latest/_images/sphx_glr_ex20_third-medium-contact_thumb.png" height="100px"/></a>
</p>

## Other Resources

This library may not meet your needs and if this is this case, consider checking out these other resources:

- [optimesh](https://github.com/meshpro/optimesh) - Mesh optimization, mesh smoothing.
- [pandamesh](https://github.com/Deltares/pandamesh) - 🐼 From geodataframe to mesh ▦.
- [pygalmesh](https://github.com/meshpro/pygalmesh) - A Python interface to CGAL's meshing tools.
- [pygmsh](https://github.com/nschloe/pygmsh) - Gmsh for Python.

## License

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This software is published under the [GPLv3 license](https://www.gnu.org/licenses/gpl-3.0.en.html).

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=pyvista/scikit-gmsh&type=Date)](https://star-history.com/#pyvista/scikit-gmsh&Date)

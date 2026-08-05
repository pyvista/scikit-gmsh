<!-- hy-mt2-i18n:start -->

[English](./README.md) | **中文** | [日本語](./README_ja.md) | [Español](./README_es.md)
<!-- hy-mt2-i18n:end -->

<h1 align="center">
  <a href="https://github.com/pyvista/scikit-gmsh#--------">
    <img src="https://raw.githubusercontent.com/pyvista/scikit-gmsh/main/docs/_static/logo.svg"
         alt="scikit-gmsh"
         width="200"></a>
</h1>

用于通过 Gmsh 生成三维有限元网格的 Scikit 工具。

[![状态](https://badgen.net/badge/status/alpha/d8624d)](https://badgen.net/badge/status/alpha/d8624d)
[![所有贡献者](https://img.shields.io/github/all-contributors/pyvista/scikit-gmsh?color=ee8449)](https://scikit-gmsh.readthedocs.io/en/latest/reference/about.html#contributors)
[![欢迎提交贡献](https://img.shields.io/badge/PR-Welcome-%23FF8300.svg)](https://github.com/pyvista/scikit-gmsh/issues)
[![文档状态](https://readthedocs.org/projects/scikit-gmsh/badge/?version=latest)](https://scikit-gmsh.readthedocs.io/en/latest/?badge=latest)
[![GitHub 仓库星标数](https://img.shields.io/github/stars/pyvista/scikit-gmsh)](https://github.com/pyvista/scikit-gmsh/stargazers)
[![许可证：GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![贡献者契约](https://img.shields.io/badge/contributor%20covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)
[![Scientific Python](https://img.shields.io/badge/SPEC-0-blue.svg)](https://scientific-python.org/specs/spec-0000/)

`scikit-gmsh` 包提供了一个简洁的接口，用于：

- Christophe Geuzaine 和 Jean-François Remacle 开发的 [Gmsh](https://pypi.org/project/gmsh/)

该库的主要目标如下：

1. 提供类似[scipy.spatial.Delaunay类](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Delaunay.html)的直观、面向对象的网格创建API。
1. 能够与[Scientific Python生态系统](https://scientific-python.org/)中的其他库实现无缝集成。

## 安装

[![pypi](https://img.shields.io/pypi/v/scikit-gmsh?label=pypi&logo=python&logoColor=white)](https://pypi.org/project/scikit-gmsh/)

```shell
pip install scikit-gmsh
```

## 示例集锦

点击此处查看按主题分类的示例图集：

<p align="center">
  <a href="https://scikit-gmsh.readthedocs.io/en/latest/examples/icosahedron.html">
    <img src="https://scikit-gmsh.readthedocs.io/en/latest/_images/sphx_glr_icosahedron_thumb.png" height="190px"/>
  </a>
  <a href="https://scikit-gmsh.readthedocs.io/en/latest/examples/polygon_with_hole.html">
    <img src="https://scikit-gmsh.readthedocs.io/en/latest/_images/sphx_glr_polygon_with_hole_thumb.png" height="190px"/>
  </a>
  <a href="https://scikit-gmsh.readthedocs.io/en/latest/examples/cylinder.html">
    <img src="https://scikit-gmsh.readthedocs.io/en/latest/_images/sphx_glr_cylinder_thumb.png" height="190px"/>
  </a>
</p>

## 其他资源

该库可能无法满足您的需求，若是如此，建议您查看这些其他资源：

- [meshwell](https://github.com/simbilod/meshwell) —— 集成光子学功能的 GMSH 封装工具。
- [objectgmsh](https://github.com/nemocrys/objectgmsh) —— 基于面向对象方式的 Gmsh 建模工具。
- [optimesh](https://github.com/meshpro/optimesh) —— 网格优化与网格平滑处理工具。
- [pandamesh](https://github.com/Deltares/pandamesh) —— 用于将地理数据框转换为网格的工具。
- [pygalmesh](https://github.com/meshpro/pygalmesh) —— CGAL 网格生成工具的 Python 接口。
- [pygmsh](https://github.com/nschloe/pygmsh) —— 专为 Python 设计的 Gmsh 工具。
- [pyvista-gridder](https://github.com/INTERA-Inc/pyvista-gridder) —— 基于 PyVista 的网格生成工具。

## 许可证

[![许可证：GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

该软件依据[GPLv3许可证](https://www.gnu.org/licenses/gpl-3.0.en.html)发布。

## 贡献指南

我们_非常欢迎_您的贡献。
本项目附带了一份[贡献者行为准则](CODE_OF_CONDUCT.md)。
通过参与本项目，我们希望您知晓并同意遵守其中的条款。

## 星标历史记录

喜欢 scikit-gmsh 吗？请通过给它添加一个 [GitHub 星标](https://github.com/pyvista/scikit-gmsh)来表达您的支持——只需简单点击一下，这对我们意义重大，同时也有助于更多人发现它！

[![星标数量变化图表](https://api.star-history.com/svg?repos=pyvista/scikit-gmsh&type=Date)](https://star-history.com/#pyvista/scikit-gmsh&Date)

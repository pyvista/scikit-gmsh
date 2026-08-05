<!-- hy-mt2-i18n:start -->
[English](./README.md) | [中文](./README_zh-CN.md) | **日本語** | [Español](./README_es.md)
<!-- hy-mt2-i18n:end -->

<h1 align="center">
  <a href="https://github.com/pyvista/scikit-gmsh#--------">
    <img src="https://raw.githubusercontent.com/pyvista/scikit-gmsh/main/docs/_static/logo.svg"
         alt="scikit-gmsh"
         width="200"></a>
</h1>

3次元有限要素メッシュを生成するためのGmsh向けScikit。

[![Status](https://badgen.net/badge/status/alpha/d8624d)](https://badgen.net/badge/status/alpha/d8624d)
[![All Contributors](https://img.shields.io/github/all-contributors/pyvista/scikit-gmsh?color=ee8449)](https://scikit-gmsh.readthedocs.io/en/latest/reference/about.html#contributors)
[![Contributing](https://img.shields.io/badge/PR-Welcome-%23FF8300.svg)](https://github.com/pyvista/scikit-gmsh/issues)
[![Documentation Status](https://readthedocs.org/projects/scikit-gmsh/badge/?version=latest)](https://scikit-gmsh.readthedocs.io/en/latest/?badge=latest)
[![GitHub Repo stars](https://img.shields.io/github/stars/pyvista/scikit-gmsh)](https://github.com/pyvista/scikit-gmsh/stargazers)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Contributor Covenant](https://img.shields.io/badge/contributor%20covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)
[![Scientific Python](https://img.shields.io/badge/SPEC-0-blue.svg)](https://scientific-python.org/specs/spec-0000/)

`scikit-gmsh`パッケージは、以下の機能へのシンプルなインターフェースを提供します：

- Christophe Geuzaine および Jean-François Remacle 氏による [Gmsh](https://pypi.org/project/gmsh/)

このライブラリには以下の主な目的があります：

1. [scipy.spatial.Delaunay class](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Delaunay.html)のように、メッシュ作成のための直感的でオブジェクト指向のAPIを提供する。
1. [Scientific Pythonエコシステム](https://scientific-python.org/)内の他のライブラリとシームレスに連携する。

## インストール

[![pypi](https://img.shields.io/pypi/v/scikit-gmsh?label=pypi&logo=python&logoColor=white)](https://pypi.org/project/scikit-gmsh/)

```shell
pip install scikit-gmsh
```

## ギャラリー

こちらでテーマ別に整理されたサンプルギャラリーをご覧ください：

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

## その他のリソース

このライブラリがご要望を満たさない場合は、他のリソースもご覧になることをお勧めします：

- [meshwell](https://github.com/simbilod/meshwell) - フォトニクス機能を統合したGMSHラッパー。  
- [objectgmsh](https://github.com/nemocrys/objectgmsh) - オブジェクト指向のGmshモデリングツール。  
- [optimesh](https://github.com/meshpro/optimesh) - メッシュの最適化および平滑化処理を行うツール。  
- [pandamesh](https://github.com/Deltares/pandamesh) - 地理データフレームからメッシュへの変換ツール。  
- [pygalmesh](https://github.com/meshpro/pygalmesh) - CGALのメッシュ生成ツールをPythonで利用するためのインターフェース。  
- [pygmsh](https://github.com/nschloe/pygmsh) - Python向けのGmsh実装。  
- [pyvista-gridder](https://github.com/INTERA-Inc/pyvista-gridder) - PyVistaを利用したメッシュ生成ツール。

## ライセンス

[![ライセンス: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

このソフトウェアは、[GPLv3 ライセンス](https://www.gnu.org/licenses/gpl-3.0.en.html)の下で公開されています。

## 貢献のお願い

ご貢献を心より歓迎します。
このプロジェクトは、【コントリビューター行動規範](CODE_OF_CONDUCT.md)に基づいて公開されています。
本プロジェクトに参加することで、利用者はその規約に従うことに同意したものとみなされます。

## スターの推移履歴

scikit-gmshを気に入りましたか？[GitHubの星マーク](https://github.com/pyvista/scikit-gmsh)を押してご支援ください。これはたった一度のクリックですが、私たちにとって大変意味のあることであり、他の人々がこのツールを見つけるのにも役立ちます！

[![Star History Chart](https://api.star-history.com/svg?repos=pyvista/scikit-gmsh&type=Date)](https://star-history.com/#pyvista/scikit-gmsh&Date)

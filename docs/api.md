# API Reference

This page provides the full API reference for scikit-gmsh.

## Overview

scikit-gmsh provides a Python interface to the Gmsh mesh generator, offering both object-oriented and functional APIs for 2D and 3D mesh generation. The library integrates seamlessly with PyVista and supports Shapely geometries.

## Main Classes

```{eval-rst}
.. autosummary::
   :toctree: generated/
   :template: class.rst

   skgmsh.Delaunay2D
   skgmsh.Delaunay3D
```

## Functions

```{eval-rst}
.. autosummary::
   :toctree: generated/
   :template: function.rst

   skgmsh.delaunay_3d
   skgmsh.frontal_delaunay_2d
   skgmsh.generate_mesh
```

## Utility Classes

```{eval-rst}
.. autosummary::
   :toctree: generated/
   :template: class.rst

   skgmsh.Report
```

## Constants

The following constants are available for mesh algorithm configuration:

```{eval-rst}
.. autodata:: skgmsh.INITIAL_MESH_ONLY_2D
.. autodata:: skgmsh.FRONTAL_DELAUNAY_2D
.. autodata:: skgmsh.DELAUNAY_3D
.. autodata:: skgmsh.INITIAL_MESH_ONLY_3D
.. autodata:: skgmsh.SILENT
.. autodata:: skgmsh.SIMPLE
.. autodata:: skgmsh.TRUE
.. autodata:: skgmsh.FALSE
```

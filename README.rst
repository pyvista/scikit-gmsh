.. |Ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
   :target: https://github.com/astral-sh/ruff
   :alt: Ruff

============
PyVista-Gmsh
============

|Ruff|

`PyVista`_ accessors for `Gmsh`_ to generate 3D finite element mesh.

.. _PyVista: https://docs.pyvista.org/version/stable/
.. _Gmsh: https://gmsh.info/

Motivation
==========

See discussion: https://github.com/pyvista/pyvista/discussions/2133#discussioncomment-2107992

Usage
=====

.. code-block:: python

    >>> import pyvista as pv
    >>> import pvgmsh as pm

We can define the surface using PyVista.

.. code-block:: python

    >>> edge_source = pv.Polygon(n_sides=4, radius=8, fill=False)
    >>> edge_source = edge_source.rotate_z(45, inplace=False)

We can then generate a 2D mesh.

.. code-block:: python

    >>> mesh = pm.frontal_delaunay_2d(edge_source, target_size=1.0)

To visualize the model we can use PyVista.

.. code-block:: python

    >>> plotter = pv.Plotter()
    >>> _ = plotter.add_mesh(mesh, show_edges=True, line_width=4, color="white")
    >>> _ = plotter.add_mesh(edge_source, show_edges=True, line_width=4, color="blue")
    >>> _ = plotter.add_points(
    ...     edge_source.points, style="points", point_size=20, color="blue"
    ... )
    >>> plotter.show(cpos="xy")

.. image:: https://github.com/pyvista/pyvista-gmsh/raw/main/frontal_delaunay_2d_01.png

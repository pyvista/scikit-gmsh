Motivation
==========

`PyVista`_ accessors for `Gmsh`_ to generate 3D finite element mesh.

PyVista is the solution to the following.

`Overview of Gmsh`_

    … and what Gmsh is not so good at
    Here are some known weaknesses of Gmsh:

    * Gmsh is not a multi-bloc mesh generator: all meshes produced by Gmsh are conforming in the sense of finite element meshes;
    * Gmsh’s graphical user interface is only exposing a limited number of the available features, and many aspects of the interface could be enhanced (especially manipulators).
    * Your complaints about Gmsh here :-)

.. _PyVista: https://docs.pyvista.org/version/stable/
.. _Gmsh: https://gmsh.info/
.. _Overview of Gmsh: https://gmsh.info/doc/texinfo/gmsh.html#Overview-of-Gmsh

Usage
=====

.. code-block:: python

    >>> import pyvista as pv
    >>> import pvgmsh

We can define the surface using PyVista.

.. code-block:: python

    >>> geometry = pv.Polygon(n_sides=4, radius=8, fill=False)
    >>> geometry = square.rotate_z(45, inplace=False)

We can then generate a 2D mesh.

.. code-block:: python

    >>> mesh = pvgmsh.frontal_delaunay_2d(geometry, mesh_size=1.0)

To visualize the model we can use PyVista.

.. code-block:: python

    >>> plotter = pv.Plotter(off_screen=True)
    >>> _ = plotter.add_mesh(mesh, show_edges=True, line_width=4, color="white")
    >>> _ = plotter.add_mesh(geometry, show_edges=True, line_width=4, color="blue")
    >>> _ = plotter.add_points(
    ...     geometry.points, style="points", point_size=20, color="blue"
    ... )
    >>> plotter.show(cpos="xy")

.. image:: https://github.com/pyvista/pyvista-gmsh/raw/main/frontal_delaunay_2d_01.png

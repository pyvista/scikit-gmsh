##########
Motivation
##########

`PyVista`_ accessors for `Gmsh`_ to generate 3D finite element mesh.

`PyVista`_ is:

* mesh data structures and filtering methods for spatial datasets
* 3D plotting made simple and built for large/complex data geometries

`Gmsh`_ is:

* A 3D finite element mesh generator with built-in pre- and post-processing facilities

.. _PyVista: https://docs.pyvista.org/version/stable/
.. _Gmsh: https://gmsh.info/

Usage
=====

.. code-block:: python

    >>> import pyvista as pv
    >>> import pvgmsh

We can define the surface using PyVista.

.. code-block:: python

    >>> squar = pv.Polygon(n_sides=4, radius=8, fill=False)
    >>> squar = squar.rotate_z(45, inplace=False)

We can then generate a 2D mesh.

.. code-block:: python

    >>> tess = pvgmsh.frontal_delaunay_2d(edge_source=squar, mesh_size=1.0)

To visualize the model we can use PyVista.

.. code-block:: python

    >>> plotter = pv.Plotter()
    >>> _ = plotter.add_mesh(tess, show_edges=True)
    >>> plotter.show(cpos="xy")

.. image:: https://github.com/pyvista/pyvista-gmsh/raw/main/frontal_delaunay_2d_01.png

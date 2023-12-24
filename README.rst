##########
Motivation
##########

* `PyVista`_ has `delaunay_2d`_  `delaunay_3d`_ function which is easy to use.
* `Gmsh`_ has various meshing algorithm.

This package control Gmsh using PyVista.

.. _PyVista: https://docs.pyvista.org/version/stable/
.. _delaunay_2d: https://docs.pyvista.org/version/stable/api/core/_autosummary/pyvista.PolyDataFilters.delaunay_2d.html
.. _delaunay_3d: https://docs.pyvista.org/version/stable/api/core/_autosummary/pyvista.PointSet.delaunay_3d.html
.. _Gmsh: https://gmsh.info/

Usage
=====

.. code-block:: python

    >>> import pyvista as pv
    >>> import pvgmsh
    >>> squar = pv.Polygon(n_sides=4, radius=8, fill=False)
    >>> squar = squar.rotate_z(45, inplace=False)
    >>> tess = pvgmsh.frontal_delaunay_2d(edge_source=squar, mesh_size=1.0)
    <BLANKLINE>

    >>> tess.clear_data()
    >>> plotter = pv.Plotter()
    >>> _ = plotter.add_mesh(tess, show_edges=True)
    >>> plotter.show(cpos="xy")

.. image:: https://github.com/pyvista/pyvista-gmsh/raw/main/frontal_delaunay_2d_01.png

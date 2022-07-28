import ..pvgmsh
import pyvista


def test_tutorial1():
    # Gmsh Python tutorial 1
    # https://gitlab.onelab.info/gmsh/gmsh/blob/gmsh_4_10_5/tutorials/python/t1.py
    vertices = np.array([[0, 0, 0], [0.1, 0, 0], [0.1, 0.3, 0], [0.3, 0, 0]])
    faces = np.hstack([[4, 0, 1, 2, 3]])
    surf = pyvista.PolyData(vertices, faces)
    # pvgmsh does not support PhysicalGroup; group configuration can be easily done with PyVista.
    mesh = pvgmsh.generate_mesh(surf)
    assert mesh.n_pts > surf.n_pts
    assert mesh.n_cells > surf.n_cells

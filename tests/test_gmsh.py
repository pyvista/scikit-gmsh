import pvgmsh


def test_tutorial1():
    # Gmsh Python tutorial 1
    # https://gitlab.onelab.info/gmsh/gmsh/blob/gmsh_4_10_5/tutorials/python/t1.py

    vertices = np.array([[0, 0, 0], [0.1, 0, 0], [0.1, 0.3, 0], [0.3, 0, 0]])
    faces = np.hstack([[4, 0, 1, 2, 3]])
    surf = pvgmsh.PolyData(vertices, faces)

    surf.set_characteristic_length([1e-2, 1e-2, 1e-2, 1e-2])

    # pvgmsh does not support PhysicalGroup; group configuration can be easily done with PyVista.

    mesh = surf.generate_mesh()
    mesh.save("t1.msh")
    mesh.plot()

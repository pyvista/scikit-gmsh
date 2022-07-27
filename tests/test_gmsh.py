import pvgmsh


def test_tutorial1():
    # Gmsh Python tutorial 1
    # https://gitlab.onelab.info/gmsh/gmsh/blob/gmsh_4_10_5/tutorials/python/t1.py

    vertices = np.array([[0, 0, 0], [0.1, 0, 0], [0.1, 0.3, 0], [0.3, 0, 0]])

    faces = np.hstack([[4, 0, 1, 2, 3]])

    surf = pvgmsh.PolyData(vertices, faces)

    surf["points group number"] = np.array([1, 1, 1])
    surf["surface group number"] = np.array([2])
surf["lc"] = np.array([1e-2, 1e-2, 1e-2])

    surf.add_physical_group(["points group number", "surface group number"])
    mesh = surf.generate_mesh()

    mesh.save("t1.msh")

    mesh.plot()

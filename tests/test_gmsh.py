import pvgmsh


def test_tutorial1():
    # Gmsh Python tutorial 1
    # https://gitlab.onelab.info/gmsh/gmsh/blob/gmsh_4_10_5/tutorials/python/t1.py

    vertices = np.array([[0, 0, 0], [0.1, 0, 0], [0.1, 0.3, 0], [0.3, 0, 0]])

    faces = np.hstack([[4, 0, 1, 2, 3]])

    surf = pvgmsh.PolyData(vertices, faces, lc=1e-2)

    surf["points group number"] = np.array([1, 1, 1])
    surf["surface group number"] = np.array([2])

    surf.add_physical_group(["points group number", "surface group number"])
    surf.generate(2)

    surf.save("t1.msh")

    surf.plot()

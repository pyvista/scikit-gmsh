import gmsh


def generate_mesh(surf):
    gmsh.initialize()
    gmsh.clear()
    return surf

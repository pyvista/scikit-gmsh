# scikit-gmsh documentation

:::{include} ../README.md
:parser: myst_parser.sphinx

## Contributors

:::{include} ../CONTRIBUTORS.md
:parser: myst_parser.sphinx

## Tutorial

### Getting Started

This tutorial will guide you through the basic usage of scikit-gmsh. Below is a simple example to create a 2D mesh for a square domain.

#### Example: Creating a 2D Mesh

1. **Install scikit-gmsh**:
   Make sure you have scikit-gmsh installed. You can install it using pip:

   ```bash
   pip install scikit-gmsh
   ```

2. **Write a Python Script**:
   Create a Python file (e.g., `example.py`) and add the following code:

   ```python
   import skgmsh

   # Create a square domain
   with skgmsh.Geometry() as geom:
       geom.add_rectangle(0, 0, 1, 1)  # Define a rectangle from (0,0) to (1,1)
       mesh = geom.generate_mesh()

   # Save the mesh to a file
   mesh.write("square.msh")
   print("Mesh saved as square.msh")
   ```

3. **Run the Script**:
   Execute the script in your terminal:

   ```bash
   python example.py
   ```

4. **Visualize the Mesh**:
   Use a mesh viewer like Gmsh to open the generated `square.msh` file.

This is a basic example to get you started. For more advanced examples, refer to the `examples/` directory in the repository.

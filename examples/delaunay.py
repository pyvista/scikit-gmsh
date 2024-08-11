"""Example of Delaunay triangulation in 2D."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay

points = np.array([[0, 0], [0, 1.1], [1, 0], [1, 1]])

tri = Delaunay(points)

plt.triplot(points[:, 0], points[:, 1], tri.simplices)
plt.plot(points[:, 0], points[:, 1], "o")
plt.show()

"""The pyvista-gmsh main module for PyVista accessors for Gmsh."""
# Setting the Qt bindings for QtPy
import os
import sys

os.environ["QT_API"] = "pyqt5"

import os

import pyvista as pv
import qdarktheme
from pyvistaqt import MainWindow, QtInteractor
from qtpy import QtWidgets

# import qdarkgraystyle


class MyMainWindow(MainWindow):
    def __init__(self, parent=None, show=True):
        QtWidgets.QMainWindow.__init__(self, parent)

        # create the frame
        self.frame = QtWidgets.QFrame()
        vlayout = QtWidgets.QVBoxLayout()

        # add the pyvista interactor object
        self.plotter = QtInteractor(self.frame)
        vlayout.addWidget(self.plotter.interactor)
        self.signal_close.connect(self.plotter.close)

        self.frame.setLayout(vlayout)
        self.setCentralWidget(self.frame)

        # simple menu to demo functions
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        font = mainMenu.font()
        font.setPointSize(14)
        mainMenu.setFont(font)
        exitButton = QtWidgets.QAction("Exit", self)
        exitButton.setShortcut("Ctrl+Q")
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        # allow adding a sphere
        meshMenu = mainMenu.addMenu("Mesh")
        self.add_sphere_action = QtWidgets.QAction("Add Sphere", self)
        self.add_sphere_action.triggered.connect(self.add_sphere)
        meshMenu.addAction(self.add_sphere_action)

        if show:
            self.show()

    def add_sphere(self):
        """Add a sphere to the pyqt frame"""
        sphere = pv.Sphere()
        self.plotter.add_mesh(sphere, show_edges=True)
        self.plotter.reset_camera()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    qdarktheme.setup_theme()
    window = MyMainWindow()
    sys.exit(app.exec_())

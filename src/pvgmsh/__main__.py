"""The pyvista-gmsh main module for PyVista accessors for Gmsh."""

# Setting the Qt bindings for QtPy
import os
import sys

os.environ["QT_API"] = "pyqt5"

import os

import pyvista as pv
from pyvistaqt import MainWindow, QtInteractor
from qtpy import QtWidgets



class PvgmshWindow(MainWindow):
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
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu("\U0001F6A7 File")
        # font = main_menu.font()
        # font.setPointSize(14)
        # main_menu.setFont(font)

        new_button = QtWidgets.QAction("\U0001F6A7 New", self)
        file_menu.addAction(new_button)

        open_button = QtWidgets.QAction("\U0001F6A7 Open", self)
        file_menu.addAction(open_button)

        open_recent_button = QtWidgets.QAction("\U0001F6A7 Open Recent", self)
        file_menu.addAction(open_recent_button)

        import_button = QtWidgets.QAction("\U0001F6A7 Import", self)
        file_menu.addAction(import_button)

        save_button = QtWidgets.QAction("\U0001F6A7 Save", self)
        file_menu.addAction(save_button)

        save_as_button = QtWidgets.QAction("\U0001F6A7 Save As", self)
        file_menu.addAction(save_as_button)

        export_button = QtWidgets.QAction("\U0001F6A7 Export", self)
        file_menu.addAction(export_button)

        close_results_button = QtWidgets.QAction("\U0001F6A7 Close Results", self)
        file_menu.addAction(close_results_button)

        exit_button = QtWidgets.QAction("Exit", self)
        exit_button.setShortcut("Alt+F4")
        exit_button.triggered.connect(self.close)
        file_menu.addAction(exit_button)

        # allow adding a sphere
        # meshMenu = main_menu.addMenu("Mesh")
        # self.add_sphere_action = QtWidgets.QAction("Add Sphere", self)
        # self.add_sphere_action.triggered.connect(self.add_sphere)
        # meshMenu.addAction(self.add_sphere_action)

        if show:
            self.show()

    # def add_sphere(self):
    #     """Add a sphere to the pyqt frame"""
    #     sphere = pv.Sphere()
    #     self.plotter.add_mesh(sphere, show_edges=True)
    #     self.plotter.reset_camera()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PvgmshWindow()
    sys.exit(app.exec_())

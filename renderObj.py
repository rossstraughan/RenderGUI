#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script integrates VTK with PyQt5 to display 3D OBJ files in a PyQt application. 
Users can load and view OBJ files through a GUI. The VTK, GT integration technique was inspired by a post available at:
https://gist.github.com/paskino/7b7ed6e4541d682bd5ce5d521505dd8f
"""

import sys
import vtk
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QAction
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class MainWindow(QtWidgets.QMainWindow):
    # Main application window inheriting from QMainWindow.
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Set the window title and initial size.
        self.setWindowTitle('VTK OBJ Viewer in PyQt')
        self.setGeometry(100, 100, 800, 600)

        # Setup the main frame and layout for the VTK rendering widget.
        self.frame = QtWidgets.QFrame()
        self.vl = QtWidgets.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        # Initialize the renderer and attach it to the VTK widget.
        self.renderer = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)

        # Get the interactor from the VTK widget's render window.
        self.interactor = self.vtkWidget.GetRenderWindow().GetInteractor()

        # Menu bar with an action to open .obj files.
        self.setupMenu()

        # Set main frame as the central widget.
        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)

    def setupMenu(self):
        # Create the menu bar with a 'File' menu and an 'Open 3D .obj' action.
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        openAction = QAction('&Open 3D .obj', self)
        openAction.triggered.connect(self.openFile) 
        fileMenu.addAction(openAction)

    def openFile(self):
        # Open a file dialog when the 'Open 3D .obj' action is clicked
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open 3D .obj File', '', '3D OBJ (*.obj)')
        if filename:
            self.loadOBJ(filename) 

    def loadOBJ(self, filePath):
        # Clear render contents
        self.renderer.RemoveAllViewProps()

        # Load the .obj file using vtkOBJReader.
        reader = vtk.vtkOBJReader()
        reader.SetFileName(filePath)
        reader.Update()

        # Create a mapper and actor for the .obj geometry.
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInput(reader.GetOutput())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        # Add the actor to the renderer and update the background colour.
        self.renderer.AddActor(actor)
        self.renderer.SetBackground(0.1, 0.2, 0.4)  # Set a background colour.

        # Reset the camera to fit geometry and render 
        self.renderer.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()

if __name__ == "__main__":
    # Start application
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

from window_tools.menu_bar import Menu_Bar
from window_tools.drawing_panel.constants import *
from window_tools.drawing_panel.drawing_panel import Drawing_Panel_Curve
from window_tools.settings_panels.settings_panels import Settings_Frame

import sys

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainter, QColor, QPen, QImage, QPalette, QBrush, QPixmap, QPicture, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSizePolicy, QGraphicsView, QGraphicsScene, QMainWindow, QPushButton, QFileDialog

class Image_Interpolation(QMainWindow):
    loaded_image = None
    windows = []

    def __init__(self):
        super().__init__()
        self.init_UI()
        self.show()


    def init_UI(self):
        self._menu_bar = Menu_Bar(self)
        self._menu_bar.set_spline_creator_action(self.new_spline_creation_project)
        
        self._drawing_panel = Drawing_Panel_Curve(self)
        
        self._settings_frame_curves = Settings_Frame(self, "Curves", DEFAULT_CURVE_COLOR, (SPLINE_SETTINGS_PANEL_CURVE_X, SPLINE_SETTINGS_PANEL_CURVE_Y), 'up')
        self._settings_frame_curves.set_change_curve_color_function( 
            lambda color:  self._drawing_panel.set_curve_color(color) 
        )
        self._settings_frame_curves.set_change_curve_visibility_function(
            lambda visibility: self._drawing_panel.set_curves_visibility( visibility )
        )
        
        self._settings_frame_points = Settings_Frame(self, "Points", DEFAULT_POINT_COLOR, (SPLINE_SETTINGS_PANEL_POINT_X, SPLINE_SETTINGS_PANEL_POINT_Y), 'down')
        self._settings_frame_points.set_change_point_color_function( 
            lambda color:  self._drawing_panel.set_point_color(color) 
        )
        self._settings_frame_points.set_change_point_visibility_function(
            lambda visibility: self._drawing_panel.set_points_visibility( visibility )
        )


        self._new_button = self._create_button(
            QIcon("icons/plus_icon.png"), 
            SPLINE_DRAWING_PANEL_Y,
            self._drawing_panel.new_curve,
            "Add a new curve"
        )

        self._reset_button = self._create_button(
            QIcon("icons/X_icon.png"), 
            self._new_button.y() + self._new_button.height() + 10,
            self._drawing_panel.reset,
            "Delete all points"
        )

        self._open_spline_button = self._create_button(
            QIcon("icons/open_spline_icon.png"),
            self._reset_button.y() + self._reset_button.height() + 10,
            self.open_curve,
            "Load a new curve from file *.json"
        )

        self._save_button = self._create_button(
            QIcon("icons/save_icon.png"),
            self._open_spline_button.y() + self._open_spline_button.height() + 10,
            self.save_curve,
            "Save points to the JSON file"
        )

        self._open_file_button = self._create_button(
            QIcon("icons/open_icon.png"),
            self._save_button.y() + self._save_button.height() + 40,
            self.open_img,
            "Open a new background file"
        )

        self._reset_file_button = self._create_button(
            QIcon("icons/reset_img_icon.png"),
            self._open_file_button.y() + self._open_file_button.height() + 10,
            self.reset_img,
            "Delete background image"
        )

        self.setGeometry(
            SPLINE_WINDOW_X, 
            SPLINE_WINDOW_Y, 
            SPLINE_WINDOW_WIDTH, 
            SPLINE_WINDOW_HEIGHT)

        self.setWindowTitle("Spline Interpolation")


    def _create_button(self, icon, y, action, tooltip):
        button = QPushButton(self)
        button.setIcon(icon)
        button.move(10, y)
        button.resize(30,30)
        button.clicked.connect(action)
        button.setToolTip(tooltip)
        return button

    def open_img(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setWindowTitle("Open Background Image")

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self._drawing_panel.set_img(filenames[0])

    def open_curve(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setWindowTitle("Open Curve")

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self._drawing_panel.open(filenames[0])

    
    def save_curve(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setWindowTitle("Save Curve")

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self._drawing_panel.save(filenames[0])


    def reset_img(self):
        self._drawing_panel.set_img("")



    # Actions

    def new_spline_creation_project(self):
        i = Image_Interpolation()
        self.windows.append(i)



app = QApplication(sys.argv)
widdget = Image_Interpolation()
sys.exit(app.exec_())
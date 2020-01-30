from spline_interpolation import Spline
from menu_bar import Menu_Bar
from drawing_panel import Drawing_Panel_Curve
from settings_panels import Settings_Frame
from constants import *

import sys
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainter, QColor, QPen, QImage, QPalette, QBrush, QPixmap, QPicture
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSizePolicy, QGraphicsView, QGraphicsScene, QMainWindow, QPushButton

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
        self._drawing_panel.set_img("smile.png")
        
        self._settings_frame_curves = Settings_Frame(self, "Curve", DEFAULT_CURVE_COLOR, (SETTINGS_PANEL_CURVE_X, SETTINGS_PANEL_CURVE_Y), 'up')
        self._settings_frame_curves.set_change_curve_color_function( 
            lambda color:  self._drawing_panel.set_curve_color(color) 
        )
        self._settings_frame_curves.set_change_curve_visibility_function(
            lambda visibility: self._drawing_panel.set_curves_visibility( visibility )
        )
        
        self._settings_frame_points = Settings_Frame(self, "Point", DEFAULT_POINT_COLOR, (SETTINGS_PANEL_POINT_X, SETTINGS_PANEL_POINT_Y), 'down')
        self._settings_frame_points.set_change_point_color_function( 
            lambda color:  self._drawing_panel.set_point_color(color) 
        )
        self._settings_frame_points.set_change_point_visibility_function(
            lambda visibility: self._drawing_panel.set_points_visibility( visibility )
        )

        self._reset_button = QPushButton(self)
        self._reset_button.setText("Reset")
        self._reset_button.move(13, 555)
        self._reset_button.clicked.connect(self._drawing_panel.reset)

        self._new_button = QPushButton(self)
        self._new_button.setText("New")
        self._new_button.move(150, 555)
        self._new_button.clicked.connect(self._drawing_panel.new_curve)

        self._save_button = QPushButton(self)
        self._save_button.setText("New")
        self._save_button.move(150, 555)
        self._save_button.clicked.connect(self._drawing_panel.new_curve)

        self.setGeometry(
            SPLINE_WINDOW_X, 
            SPLINE_WINDOW_Y, 
            SPLINE_WINDOW_WIDTH, 
            SPLINE_WINDOW_HEIGHT)

    
    # Actions

    def new_spline_creation_project(self):
        i = Image_Interpolation()
        i.load_image("mushroom.png")
        self.windows.append(i)



app = QApplication(sys.argv)
widdget = Image_Interpolation()
sys.exit(app.exec_())
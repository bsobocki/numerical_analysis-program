from window_tools.menu_bar import MenuBar
from window_tools.drawing_panels.constants import *
from window_tools.drawing_panels.spline_drawing_panel import SplineDrawingPanel
from window_tools.settings_panels.settings_panels import SettingsFrame
from window_tools.drawing_panels.points_manager import Points_Manager

import sys
import json

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainter, QColor, QPen, QImage, QPalette, QBrush, QPixmap, QPicture, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSizePolicy, QGraphicsView, QGraphicsScene, QMainWindow, QPushButton, QFileDialog

class Image_Interpolation(QMainWindow):
    loaded_image = None
    windows = []

    def __init__(self):
        super().__init__()
        self._points_manager = Points_Manager()
        self._init_UI(SplineDrawingPanel(self, self._points_manager.objects()))
        self.show()

    def open_img(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setWindowTitle("Open Background Image")

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self._drawing_panel.set_img(filenames[0])


    def import_objects(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setWindowTitle("Open Curve")

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            with open(filenames[0], 'r') as file:
                data = file.read()
                obj = json.loads(data)
                objects = obj["objects_points"]
                self._points_manager.add_objects(objects)
                self._points_manager.create_new_object()
                self._drawing_panel.redraw()

    def save_objects(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setWindowTitle("Save Curve")

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            _json = json.dumps( {"objects_points" : self._points_manager.objects()} )
            f = open(filenames[0],"w")
            f.write(_json)
            f.close()


    def reset_img(self):
        self._drawing_panel.set_img("")

    def reset_data(self):
        self._points_manager.reset()
        self._drawing_panel.redraw()

    def undo(self):
        self._points_manager.delete_last_point()
        self._drawing_panel.redraw()

    def edit_mode_on(self):
        self._drawing_panel.edit_mode(self._points_manager.objects())
        self._drawing_panel.mousePressEvent = self._panel_empty_function

    def edit_mode_off(self):
        self._drawing_panel.set_objects(self._points_manager.objects())
        self._drawing_panel.redraw()
        self._drawing_panel.mousePressEvent = self._panelMousePressEvent


    # Actions

    def new_spline_creation_project(self):
        i = Image_Interpolation()
        self.windows.append(i)


    # Initialize

    def _init_UI(self, drawing_panel):
        self._menu_bar = MenuBar(self)
        self._menu_bar.set_spline_creator_action(self.new_spline_creation_project)
        self._drawing_panel = drawing_panel
        self._drawing_panel.mousePressEvent = self._panelMousePressEvent
        self._add_settings_frames()
        self._add_buttons()
        self.setGeometry(
            WINDOW_X, 
            WINDOW_Y, 
            WINDOW_WIDTH, 
            WINDOW_HEIGHT
        )

        self.setWindowTitle("Spline Interpolation")

    def _add_settings_frames(self):
        self._settings_frame_curves = SettingsFrame(
            self, 
            "Curves", 
            (SETTINGS_PANEL_CURVE_X, SETTINGS_PANEL_CURVE_Y))
        self._settings_frame_curves.add_color_panel(
            DEFAULT_CURVE_COLOR,
            lambda color:  self._drawing_panel.set_curve_color(color))
        self._settings_frame_curves.add_clicked_label(
            "Hide Curves", 
            lambda : self._drawing_panel.switch_curves_visibility()
        )
        
        self._settings_frame_points = SettingsFrame(
            self, 
            "Points", 
            (SETTINGS_PANEL_POINT_X, SETTINGS_PANEL_POINT_Y))
        self._settings_frame_points.add_color_panel(
            DEFAULT_POINT_COLOR,
            lambda color:  self._drawing_panel.set_point_color(color) 
        )
        self._settings_frame_points.add_clicked_label(
            "Hide Points",
            lambda : self._drawing_panel.switch_points_visibility()
        )

    def _add_buttons(self):
        self._new_button = self._create_button(
            QIcon("icons/plus_icon.png"), 
            DRAWING_PANEL_Y,
            self._points_manager.new_object,
            "Add a new curve"
        )

        self._reset_button = self._create_button(
            QIcon("icons/X_icon.png"), 
            self._new_button.y() + self._new_button.height() + 10,
            self.reset_data,
            "Delete all points"
        )

        self._open_spline_button = self._create_button(
            QIcon("icons/open_spline_icon.png"),
            self._reset_button.y() + self._reset_button.height() + 10,
            self.import_objects,
            "Load a new curve from file *.json"
        )

        self._save_button = self._create_button(
            QIcon("icons/save_icon.png"),
            self._open_spline_button.y() + self._open_spline_button.height() + 10,
            self.save_objects,
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

        self._undo_button = self._create_button(
            QIcon("icons/undo_icon.png"),
            self._reset_file_button.y() + self._reset_file_button.height() + 40,
            self.undo,
            "Undo"
        )

        self._edit_on_button = self._create_button(
            QIcon("icons/edit_on_icon.png"),
            self._undo_button.y() + self._undo_button.height() + 40,
            self.edit_mode_on,
            "Run Edit Mode"
        )

        self._edit_off_button = self._create_button(
            QIcon("icons/edit_off_icon.png"),
            self._edit_on_button.y() + self._edit_on_button.height() + 10,
            self.edit_mode_off,
            "Run Edit Mode"
        )


    def _create_button(self, icon, y, action, tooltip):
        button = QPushButton(self)
        button.setIcon(icon)
        button.move(10, y)
        button.resize(30,30)
        button.clicked.connect(action)
        button.setToolTip(tooltip)
        return button

    """ PANEL """

    def _panelMousePressEvent(self, event):
        x = event.pos().x() - self._drawing_panel._pixmap_pos[0]
        y = event.pos().y() - self._drawing_panel._pixmap_pos[1]
        self._points_manager.add_point(x, y, self._settings_frame_points.get_color())
        self._drawing_panel.redraw()

    def _panel_empty_function(self, event):
        pass
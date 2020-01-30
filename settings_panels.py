from constants import *
from setting_color_panel import Setting_Color_Panel

from PyQt5.QtWidgets import QLabel, QFrame, QWidget, QSpinBox, QCheckBox
from PyQt5.QtGui import QBrush, QPixmap, QPainter, QPen, QColor, QPalette
from PyQt5.QtCore import Qt, QLineF, QRectF, QRect, QSize
from PyQt5 import QtGui


class Settings_Frame(QWidget):
   def __init__(self, parent, title, default_color, pos, type):
      super().__init__(parent)

      self._type = type

      self._label = QLabel(self)
      self._label.setText(title)
      self._label.move(10, 10)

      self._color_panel = Setting_Color_Panel(self, 0, self._label.y()+37, default_color, type)

      self._check_box_label = QLabel(self)
      self._check_box_label.setText("show " + title + "s")
      self._check_box_label.move(30, self._color_panel.y() + self._color_panel.height() + 20)

      self._check_show = QCheckBox(self)
      self._check_show.setChecked(True)
      self._check_show.move(130, self._color_panel.y() + self._color_panel.height() + 21)
      self._check_show.toggled.connect(self._change_visibility)

      self.init_Widget(pos)


   def init_Widget(self, pos):
      self._set_background_color()
      self.setGeometry(
         pos[0], 
         pos[1], 
         SETTINGS_PANEL_WIDTH, 
         SETTINGS_PANEL_HEIGHT)


   def _change_visibility(self, visibility):
        if self._type == 'up': 
            self._set_curve_visibility( visibility )
        else : 
            self._set_point_visibility( visibility )

   def _set_curve_visibility(self, visibility):
      pass

   def _set_point_visibility(self, visibility):
      pass


   def set_change_curve_color_function(self, fun):
      self._color_panel.change_curve_color = fun


   def set_change_point_color_function(self, fun):
      self._color_panel.change_point_color = fun

   
   def set_change_curve_visibility_function(self, fun):
      self._set_curve_visibility = fun


   def set_change_point_visibility_function(self, fun):
      self._set_point_visibility = fun


   def _set_background_color(self, color=QtGui.QColor(62, 62, 62)):
      pal = QPalette();
      pal.setColor(QPalette.Background, color);
      self.setAutoFillBackground(True);
      self.setPalette(pal);


   def paintEvent(self, event):
      painter = QPainter(self)
      pen = QPen(QColor(40, 40, 40))
      pen.setWidth(1)

      painter.setPen(pen)
      painter.drawLine(0, 0, self.width(), 0)
      painter.drawLine(0, 0, 0, self.height())

      painter.drawLine(1, 35, self.width(), 35)

      pen.setColor(QColor(80, 80, 80))
      painter.setPen(pen)
      painter.drawLine(self.width()-1, 0, self.width()-1, self.height()-1)
      painter.drawLine(0, self.height()-1, self.width()-1, self.height())

      painter.drawLine(0, 34, self.width(), 34)
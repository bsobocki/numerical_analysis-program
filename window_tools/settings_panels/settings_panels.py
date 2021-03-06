from window_tools.settings_panels.constants import *
from window_tools.settings_panels.setting_color_panel import SettingColorPanel

from PyQt5.QtWidgets import QLabel, QFrame, QWidget, QSpinBox, QCheckBox
from PyQt5.QtGui import QBrush, QPixmap, QPainter, QPen, QColor, QPalette
from PyQt5.QtCore import Qt, QLineF, QRectF, QRect, QSize
from PyQt5 import QtGui


class SettingsFrame(QWidget):
   def __init__(self, parent, title, pos):
      super().__init__(parent)
      self._items = []
      self._title = title
      
      self._set_title(self._title)

      self._init_Widget(pos)


   def add_item(self, item):
      self._items.append(item)


   def push_item(self, item):
      x,y = self._next_coords()
      item.move(x,y)
      self.add_item(item)


   def add_clicked_label(self,title, action):
      x,y = self._next_coords()

      label = QLabel(self)
      label.setText(title)
      label.move(x,y)
      label.resize(100,30)
      label.mousePressEvent = lambda ev: self._use_label(label, action)
      label.linkActivated.connect(action)
      
      self.add_item(label)


   def add_color_panel(self, default_color, update_object_color):
      self._color_panel = SettingColorPanel(self, default_color, update_object_color)
      self.push_item(self._color_panel)


   def set_change_color_function(self, fun):
      self._color_panel.update_object_color = fun

   def get_color(self):
      return self._color_panel.get_color()



   def _init_Widget(self, pos):
      self._set_background_color()
      self.setGeometry(
         pos[0], 
         pos[1], 
         SPLINE_SETTINGS_PANEL_WIDTH, 
         SPLINE_SETTINGS_PANEL_HEIGHT)
   

   def _set_title(self, title):
      self._label = QLabel(self)
      self._label.setText(title)
      self._label.move(10, 10)
      self.add_item(self._label)


   def _next_coords(self):
      n = len(self._items)
      if n == 0 : return 0
      i = self._items[n-1]
      return 30, i.y() + i.height() + 15


   def _set_background_color(self, color=QtGui.QColor(62, 62, 62)):
      pal = QPalette();
      pal.setColor(QPalette.Background, color);
      self.setAutoFillBackground(True);
      self.setPalette(pal);


   def _use_label(self, label, action):
      action()
      text = ""
      if label.text() == "Hide " + self._title:
         text = "Show " + self._title
      else:
         text = "Hide " + self._title
      label.setText(text)
      label.resize(100,30)


   # Event

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
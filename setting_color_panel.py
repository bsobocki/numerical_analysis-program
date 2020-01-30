from constants import *

from PyQt5.QtWidgets import QLabel, QFrame, QWidget, QSpinBox
from PyQt5.QtGui import QBrush, QPixmap, QPainter, QPen, QColor, QPalette
from PyQt5.QtCore import Qt, QLineF, QRectF, QRect, QSize
from PyQt5 import QtGui


class Setting_Color_Panel(QWidget):
    def __init__(self, parent, x, y, default_color, type):
        super().__init__(parent)

        self._type = type # 'up' / 'down'

        self.move(x, y)
        self.resize(SPLINE_SETTINGS_PANEL_WIDTH, 80)

        self._labels = []

        self._circle = (170, 15, 50, 50)
        self._color = default_color

        self._add_label("red:", (30,0,70,20))
        self._red_sp = self._create_spin_box(0, self._color.red(), self.change_red_event)

        self._add_label("green:", (30,30,70,20))
        self._green_sp = self._create_spin_box(30, self._color.green(), self.change_green_event)
        
        self._add_label("blue:", (30,60,70,20))
        self._blue_sp = self._create_spin_box(60, self._color.blue(), self.change_blue_event)


    
    def _add_label(self, text, rect):
        label = QLabel(self)
        label.setText(text)
        label.move(rect[0], rect[1])
        label.resize(rect[2], rect[3])
        self._labels.append(label)


    def _create_spin_box(self, y, color, valueChanged):
        sp = QSpinBox(self)
        sp.move(90, y)
        sp.resize(60, 20)
        sp.setMinimum(0)
        sp.setMaximum(255)
        sp.setValue(color)
        sp.valueChanged.connect(valueChanged)
        return sp


    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen()
        painter.setPen(pen)
        brush = QBrush(QColor("black"), Qt.SolidPattern) 
        painter.setBrush(brush)
        painter.setPen(pen)

        shadow = QColor(50,50,50)

        pen.setColor(shadow)
        brush.setColor(shadow)
        painter.setBrush(brush)
        painter.setPen(pen)
        painter.drawEllipse(self._circle[0], self._circle[1]+55, self._circle[2]-2, 5)
        
        pen.setColor(self._color)
        brush.setColor(self._color) 
        painter.setBrush(brush)
        painter.setPen(pen)
        painter.drawEllipse(self._circle[0], self._circle[1], self._circle[2], self._circle[3])


    def update_color(self):
        if self._type == 'up': 
            self.change_curve_color(self._color)
        else : 
            self.change_point_color(self._color)


    def change_red_event(self):
        self._color.setRed(self._red_sp.value())
        self.update_color()
        self.update()


    def change_green_event(self):
        self._color.setGreen(self._green_sp.value())
        self.update_color()
        self.update()


    def change_blue_event(self):
        self._color.setBlue(self._blue_sp.value())
        self.update_color()
        self.update()


    def change_curve_color(self, color):
        pass


    def change_point_color(self, color):
        pass
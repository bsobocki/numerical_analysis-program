from PyQt5.QtWidgets import QWidget

class Point(QWidget):
    def __init__(self, x, y, color):
        self._x = x
        self._y = y
        self._color = color

    def dragMoveEvent(self, QDragMoveEvent):
        return super().dragMoveEvent(self, QDragMoveEvent)
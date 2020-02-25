from PyQt5.QtWidgets import QApplication ,QWidget, QGraphicsEllipseItem
from PyQt5.Qt import Qt
from PyQt5.QtCore import QPointF

class Ellipse(QGraphicsEllipseItem):
    def __init__(self, settings):
        top_left_x, top_left_y, color = settings
        super().__init__(0, 0, 7, 7)  # Initial position must be (0,0) to avoid bias in coordinate system...
        self.setPos(top_left_x-3, top_left_y-3)  # ...but we can use setPos to move the object.
        self.setBrush(color)
        self.setAcceptHoverEvents(True)  # hover events are used to change mouse cursor
        self.settings = settings

    def __str__(self):
        return "x: " + str(self.x()) + ", y: " + str(self.y())

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent'):
        """When cursor enters the object, set cursor to open hand"""
        QApplication.instance().setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent'):
        """When cursor leaves the object, restore mouse cursor"""
        QApplication.instance().restoreOverrideCursor()

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent'):
        """mouseMoveEvent is called whenever a mouse button is pressed and the cursor is moved. """
        new_cursor_position = event.scenePos()  # mouse cursor in scene coordinates
        old_cursor_position = event.lastScenePos()
        old_top_left_corner = self.scenePos()
        new_top_left_corner_x = new_cursor_position.x() - old_cursor_position.x() + old_top_left_corner.x()
        new_top_left_corner_y = new_cursor_position.y() - old_cursor_position.y() + old_top_left_corner.y()
        self.setPos(QPointF(new_top_left_corner_x, new_top_left_corner_y))  # update disk top left corner
        self.settings[0] = new_top_left_corner_x
        self.settings[1] = new_top_left_corner_y
        self._redraw()
        
    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent'): pass

    def mouseDoubleClickEvent(self, event: 'QGraphicsSceneMouseEvent'): pass

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent'): pass


    def dragMoveEvent(self, event):
        return super().dragMoveEvent(self, event)

    def _redraw(self): 
        pass

    def set_function_redraw(self, fun): 
        self._redraw = fun
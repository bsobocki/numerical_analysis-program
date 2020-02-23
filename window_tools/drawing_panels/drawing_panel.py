from window_tools.drawing_panels.constants import *

from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QLabel
from PyQt5.QtGui import QBrush, QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QLineF, QRectF, QRect, QSize, QPointF

import json
from window_tools.drawing_panels.points_manager import Points_Manager


class DrawingPanel(QGraphicsView):
    def __init__(self, parent, points):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))

        self._curves_visibility = True 
        self._points_visibility = True

        self._pixmap_src = None
        self._pixmap_pos = [0,0]

        self._objects = points
        self._point_pen = QPen()
        self._point_pen.setWidth(3)
        self.set_point_color(DEFAULT_POINT_COLOR)
        
        self._curve_pen = QPen()
        self._curve_pen.setWidth(3)
        self.set_curve_color(DEFAULT_CURVE_COLOR)

        self._init_drawing_panel()
        self.setSceneRect(
            QRectF( 0, 0, self.width()-10, self.height()-10)
        )
        self.show()


    def _init_drawing_panel(self):
        self.setGeometry(
            DRAWING_PANEL_X, 
            DRAWING_PANEL_Y, 
            DRAWING_PANEL_WIDTH, 
            DRAWING_PANEL_HEIGHT)
        self.setMouseTracking(True)


    """ CURVE """

    def set_curve_thickness(self, thickness):
        self._pen.setWidth(thickness)

    def set_curve_color(self, r, g, b):
        self._curve_pen.setColor(QColor(r, g, b))
        self.redraw()

    def set_curve_color(self, color):
        self._curve_pen.setColor(color)
        self.redraw()

    def get_curve_color(self):
        return self._curve_pen.getColor()
                     
    def switch_curves_visibility(self):
        self._curves_visibility = not self._curves_visibility
        self.redraw()


    """ POINTS """

    def set_point_color(self, r, g, b):
        self._point_pen.setColor(QColor(r, g, b))
        self.redraw()

    def set_point_color(self, color):
        self._point_pen.setColor(color)
        self._point_pen.setBrush(QBrush(color))
        self.redraw()

    def get_point_color(self):
        return self._point_pen.getColor()

    def switch_points_visibility(self):
        self._points_visibility = not self._points_visibility
        self.redraw()
  

    """ ACTIONS """

    def redraw(self):
        self._reset_scene()  
        self._draw_curves()
        self._draw_points()
        self.update()

    def set_img(self, src):
        self.scene().clear()
        self._pixmap_src = src
        if src != "" :
            self.scene().addPixmap(QPixmap(self._pixmap_src))

            scene_rect, panel_rect = self.sceneRect().getRect(), self.rect().getRect()
            self._pixmap_pos = ( (panel_rect[2]-scene_rect[2])/2, (panel_rect[3]-scene_rect[3])/2 )  

        self.setSceneRect(QRectF(0, 0, self.width()-20, self.height()-20))
        
        self._draw_curves()
        self._draw_points()
        self.update()


    """ DRAWING """
        
    def _reset_scene(self):
        self.scene().clear()
        self.set_img(self._pixmap_src)      

    def _get_curve_xs_ys(self, xs, ys): return ((),())

    def _draw_curves(self):
        if self._curves_visibility:
            for obj in self._objects:
                if len(obj) > 1 :
                    x = [p[0] for p in obj]
                    y = [p[1] for p in obj]

                    xs, ys = self._get_curve_xs_ys(x,y)

                    for i in range(1, len(xs)):
                        line = QLineF(xs[i-1], ys[i-1], xs[i], ys[i]) 
                        self.scene().addLine(line, pen=self._curve_pen) 

    def _draw_points(self):
        if self._points_visibility:
            for object in self._objects:
                for point in object:
                    self.scene().addEllipse(point[0], point[1], 4, 4, self._point_pen)  

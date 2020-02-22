from window_tools.drawing_panels.constants import *

from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QLabel
from PyQt5.QtGui import QBrush, QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QLineF, QRectF, QRect, QSize, QPointF

import json


class DrawingPanel(QGraphicsView):
    def __init__(self, parent):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))

        self._curves_visibility = True 
        self._points_visibility = True

        self._points = [[]]

        self._pixmap_src = None
        self._pixmap_pos = [0,0]
        
        self._curve_pen = QPen()
        self._curve_pen.setWidth(3)
        self.set_curve_color(DEFAULT_CURVE_COLOR)

        self._point_pen = QPen()
        self._point_pen.setWidth(3)
        self.set_point_color(DEFAULT_POINT_COLOR)

        self._init_drawing_panel()
        self.show()

    def _init_drawing_panel(self):
        self.setGeometry(
            DRAWING_PANEL_X, 
            DRAWING_PANEL_Y, 
            DRAWING_PANEL_WIDTH, 
            DRAWING_PANEL_HEIGHT)
        self.setMouseTracking(True)


    """ CURVE """

    def new_curve(self):
        self._points.append([])

    def set_curve_thickness(self, thickness):
        self._pen.setWidth(thickness)

    def set_curve_color(self, r, g, b):
        self._curve_pen.setColor(QColor(r, g, b))
        self._redraw()

    def set_curve_color(self, color):
        self._curve_pen.setColor(color)
        self._redraw()

    def get_curve_color(self):
        return self._curve_pen.getColor()
                     
    def switch_curves_visibility(self):
        self._curves_visibility = not self._curves_visibility
        self._redraw()


    """ POINTS """

    def set_point_color(self, r, g, b):
        self._point_pen.setColor(QColor(r, g, b))
        self._redraw()

    def set_point_color(self, color):
        self._point_pen.setColor(color)
        self._point_pen.setBrush(QBrush(color))
        self._redraw()

    def get_point_color(self):
        return self._point_pen.getColor()

    def switch_points_visibility(self):
        self._points_visibility = not self._points_visibility
        self._redraw()
  

    """ ACTIONS """

    def reset(self):
        self._points = [[]]
        self._redraw()

    def open(self, src):
        with open(src, 'r') as file:
            data = file.read()
        obj = json.loads(data)
        self._points = obj["objects_points"]
        self._points.append([])
        self._redraw()

    def save(self, src):
        _json = json.dumps( {"objects_points" : self._points} )
        f = open(src,"w")
        f.write(_json)
        f.close()

    def set_img(self, src):
        self.scene().clear()
        self._pixmap_src = src
        if src != "" :
            self.scene().addPixmap(QPixmap(self._pixmap_src))

            sr, vr = self.sceneRect().getRect(), self.rect().getRect()
            self._pixmap_pos = ( (vr[2]-sr[2])/2, (vr[3]-sr[3])/2 )  

        self.setSceneRect(QRectF(0, 0, self.width()-20, self.height()-20))
        
        self._draw_curves()
        self._draw_points()
        self.update()

    def delete_last_point(self):
        if len(self._points) > 0 and len(self._points[0]) > 0:
            if len(self._points[-1]) >0 : del self._points[-1][-1]
            if len(self._points) > 1 and len(self._points[-1]) == 0 :  del self._points[-1]
            self._redraw()


    """ DRAWING """

    def _redraw(self):
        self._reset_scene()  
        self._draw_curves()
        self._draw_points()
        self.update()
        
    def _reset_scene(self):
        self.scene().clear()
        self.set_img(self._pixmap_src)      

    def _get_curve_xs_ys(self, xs, ys): return ((),())

    def _draw_curves(self):
        if self._curves_visibility:
            for obj in self._points:
                if len(obj) > 1 :
                    x = [p[0] for p in obj]
                    y = [p[1] for p in obj]

                    xs, ys = self._get_curve_xs_ys(x,y)

                    for i in range(1, len(xs)):
                        line = QLineF(xs[i-1], ys[i-1], xs[i], ys[i]) 
                        self.scene().addLine(line, pen=self._curve_pen) 


    def _draw_points(self):
        if self._points_visibility:
            for points in self._points:
                for point in points:
                    self.scene().addEllipse(point[0], point[1], 4, 4, self._point_pen)  


    """ MOUSE EVENTS """

    def mousePressEvent(self, event):
        index = len(self._points)-1
        self._points[index].append( (event.pos().x() - self._pixmap_pos[0], event.pos().y() - self._pixmap_pos[1] ) )
        self._redraw()

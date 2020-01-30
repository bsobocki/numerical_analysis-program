from spline_curve import *
from constants import *

from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QLabel
from PyQt5.QtGui import QBrush, QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QLineF, QRectF, QRect, QSize, QPointF

import json


class Drawing_Panel_Curve(QGraphicsView):
    def __init__(self, parent):
        super().__init__(parent)
        self._curves_visibility = True 
        self._objects_points_visibility = True

        self.setScene(QGraphicsScene(self))

        self._objects_points = [[]]

        self._pixmap = None
        self._pixmap_pos = []
        
        self._curve_pen = QPen()
        self._curve_pen.setWidth(3)
        self.set_curve_color(DEFAULT_CURVE_COLOR)

        self._point_pen = QPen()
        self._point_pen.setWidth(3)
        self.set_point_color(DEFAULT_POINT_COLOR)

        self._start_pos = (0, 0)
        self._end_pos = (0, 0)

        self._init_drawing_panel()

        self.show()


    def _init_drawing_panel(self):
        self.setGeometry(
            DRAWING_PANEL_X, 
            DRAWING_PANEL_Y, 
            DRAWING_PANEL_WIDTH, 
            DRAWING_PANEL_HEIGHT)
        self.setMouseTracking(True)


    def set_curve_thickness(self, thickness):
        self._pen.setWidth(width)


    def set_curve_color(self, r, g, b):
        self._curve_pen.setColor(QColor(r, g, b))
        self._redraw()

    def set_curve_color(self, color):
        self._curve_pen.setColor(color)
        self._redraw()

    def get_curve_color(self):
        return self._curve_pen.getColor()


    def set_point_color(self, r, g, b):
        self._point_pen.setColor(QColor(r, g, b))
        self._redraw()

    def set_point_color(self, color):
        self._point_pen.setColor(color)
        self._point_pen.setBrush(QBrush(color))
        self._redraw()

    def get_point_color(self):
        return self._point_pen.getColor()


    def new_curve(self):
        self._objects_points.append([])
        self._curves.append([])

    
    def reset(self):
        self._curves = [[]]
        self._objects_points = [[]]
        self._redraw()

    def open(self):
        with open('data.json', 'r') as file:
            data = file.read()
        obj = json.loads(data)
        self._objects_points = obj["objects_points"]
        self._objects_points.append([])
        self._redraw()


    def save(self):
        _json = json.dumps( {"objects_points" : self._objects_points} )
        f = open("data.json","w")
        f.write(_json)
        f.close()


    def set_img(self, src):
        self._pixmap = QPixmap(src)
        self.scene().addPixmap(self._pixmap)

        sr, vr = self.sceneRect().getRect(), self.rect().getRect()
        self._pixmap_pos = ( (vr[2]-sr[2])/2, (vr[3]-sr[3])/2 )  

        self.setSceneRect(QRectF(0, 0, self._pixmap.width(), self._pixmap.height()))
        
        self.update()
        

    def _reset_scene(self):
        self.scene().clear()
        self.set_img(self._pixmap)      



    def mousePressEvent(self, event):
        index = len(self._objects_points)-1
        self._objects_points[index].append( (event.pos().x() - self._pixmap_pos[0], event.pos().y() - self._pixmap_pos[1] ) )
        self._redraw()


    def _draw_curves(self):
        for obj in self._objects_points:
            if len(obj) > 1 :
                x = [p[0] for p in obj]
                y = [p[1] for p in obj]

                s = Spline_Curve(x, y)

                """ values of interpolating functions: sx and sy """
                xs, ys = s.get_xs_ys()

                for i in range(1, len(xs)):
                    line = QLineF(xs[i-1], ys[i-1], xs[i], ys[i]) 
                    self.scene().addLine(line, pen=self._curve_pen) 


    def _redraw(self):
        self._reset_scene()  
        self._draw_curves()
        self._draw_points()
        self.update()
                     


    def _draw_points(self):
        if self._objects_points_visibility:
            for points in self._objects_points:
                for point in points:
                    self.scene().addEllipse(point[0], point[1], 6, 6, self._point_pen)  
                    self.scene().addEllipse(point[0], point[1], 2, 2, self._point_pen)  


    def set_curves_visibility(self, visibility):
        self._curves_visibility = visibility
        self._redraw()


    def set_points_visibility(self, visibility):
        self._objects_points_visibility = visibility
        self._redraw()
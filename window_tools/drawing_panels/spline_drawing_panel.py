from window_tools.drawing_panels.numerical_tools.spline_curve import *
from window_tools.drawing_panels.constants import *
from window_tools.drawing_panels.drawing_panel import DrawingPanel

class SplineDrawingPanel(DrawingPanel):
    def __init__(self, parent, points):
        super().__init__(parent, points)
       
    def _get_curve_xs_ys(self, xs, ys):
        s = Spline_Curve(xs, ys)
        """ values of interpolating functions: sx and sy """
        return s.get_xs_ys()
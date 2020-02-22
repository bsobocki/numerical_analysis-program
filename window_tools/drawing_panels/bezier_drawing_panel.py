from window_tools.drawing_panels.numerical_tools.bezier_curve import *
from window_tools.drawing_panels.constants import *
from window_tools.drawing_panels.drawing_panel import DrawingPanel

class BezierDrawingPanel(DrawingPanel):
    def __init__(self, parent):
        super().__init__(parent)
       
    def _get_curve_xs_ys(self, xs, ys):
        b = Bezier_Curve(xs, ys)
        """ values of interpolating functions: sx and sy """
        return b.get_xs_ys()
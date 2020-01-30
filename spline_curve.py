from parametrical_curve import Parametrical_Curve 
from spline_interpolation import Spline

class Spline_Curve(Parametrical_Curve):
    def __init__(self, xs, ys):
        super().__init__()
        n = len(xs)
        
        ts = Parametrical_Curve.t(n-1)
        self.x_spline = Spline(ts, xs)
        self.y_spline = Spline(ts, ys)

        ts = Parametrical_Curve.t(10*n)
        self._xs = [self.x_spline(t) for t in ts] 
        self._ys = [self.y_spline(t) for t in ts]
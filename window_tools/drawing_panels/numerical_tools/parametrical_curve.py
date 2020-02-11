import abc

class Parametrical_Curve:
    def __init__(self):
        self._xs = []
        self._ys = []    
    
    def get_xs_ys(self):
        return self._xs, self._ys

    @staticmethod
    def get_divided_range(start, end):
        # number of range parts
        n = 100
        # divide range start <-> end into n parts
        t = [start + (end-start)*i/n for i in range(0,n+1)]
        return t 

    @staticmethod
    def t(n): return [i/n for i in range (0, n+1)]
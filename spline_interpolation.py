import math

"""
NIFS3 (pl. Naturalna Interpolacyjna Funkcja Sklejana 3-go stopnia)

Polynomial interpolating function using given points (x, f(x)) 

Spline : https://en.wikipedia.org/wiki/Spline_interpolation#Algorithm_to_find_the_interpolating_cubic_spline
"""

class Spline:
    _xs = []
    _ys = []
    _diff_quos = []
    _moments = []

    def __init__(self, xs, ys):
        """
        Spline interpolation object.

        Params:
            @_xs, @_ys - list of x and y coords from the interpolations nodes 
            @_us, @_qs - list of values Pi and Qi needed to calculate interpolation moments
                                                             f(a) - f(b)
            @_diff_quos - list of the differental quotients  -----------
                                                                b - a
            @_moments - list of the interpolation moments equal second derivative of the spline
                            Mi = Si''(x)
        """
        self._xs = xs # sorted with ascending order
        self._ys = ys # corresponding values ​​= f(x)
        if len(xs) > 2 :
            self._diff_quos = Spline.differental_quotients_table(xs, ys)
            self._moments = Spline.table_of_moments(xs, ys,self._diff_quos)

    def __call__(self, x):
        """ make object callable """

        # for 2 points create line 
        if len(self._xs) == 2:
            p = list(zip(self._xs, self._ys))
            return Spline.line(p[0], p[1], x)
            
        # for more points create polynomials
        for i in range(1,len(self._xs)):
            """ check which part of the function you should use """
            if x <= self._xs[i]:
                return Spline.s(i, self._xs, self._ys, self._moments,x)
        return Spline.s(len(self._xs)-1, self._xs, self._ys, self._moments,x)

    def add_point(self,x,y):
        self._xs.append(x)
        self._ys.append(y)
        self._diff_quos.append()

    
    def differental_quotients_row(self, x_n, y_n):
        """ 
        f[n], f[n-1, n], f[n-2, n-1, n] 

        | x    ||   y      |   f[i,j]    |     f[i,j,k]     |
        +------++----------+-------------+------------------+
        | ..   ||  ...     |    ...      |        ...       |
        | xn-1 ||  f[n-1]  | f[n-2, n-1] | f[n-3, n-2, n-1] |
        |      ||        \ |           \ |                  |
        |      ||          \             \                  | 
        |  xn  ||   f[n] --- f[n-1, n] --- f[n-2, n-1, n]   |

        To calculate f[i-1, i, i+1] we need f[i-1, i] ,  f[i, i+1] ,  x[i+1] and x[i],
        so we can calculate new rows in time O(1), because len(row) = 3
        """
        n = len(self._diff_quos)
        
        # f[n]
        f_n  =  y_n  

        # f[n-1, n]
        f_n_1__n  =  ( f_n - self._diff_quos[n-1][0] ) / ( x_n - self._xs[n-1] )
        
        # f[n-2, n-1, n]
        f_n_2__n_1__n  =  ( f_n_1__n - self._diff_quos[n-1][1] ) / ( x_n - self._xs[n-2])

        self._diff_quos.append( [f_n,  f_n_1__n,  f_n_2__n_1__n] )


    @staticmethod
    def differental_quotients_table(x,y):
        """ 
        returns 2d table 'f' contains differential quotients of the interpolated function 

        x  ||  y = f[i] |   f[i,j]   |   f[i,j,k]
        ---++-----------+------------+-------------
        x0 ||     y0    |   0        |   0
        x1 ||     y1    |   f[0,1]   |   0
        x2 ||     y2    |   f[1,2]   |   f[0,1,2]
        x3 ||     y3    |   f[2,3]   |   f[1,2,3]
        x4 ||     y4    |   f[3,4]   |   f[2,3,4]
        .. ||     ..    |   ...      |   ...

                  f[j] - f[i]                   f[j,k] - f[i,j]
        f[i,j] = ------------- ,    f[i,j,k] = ------------------
                    Xj - Xi                         Xk - Xi
  
        self._diff_quos[i][0] == f[i]
        self._diff_quos[i][1] == f[i-1, i]
        self._diff_quos[i][2] == f[i-2, i-1, i] 

        We will be interested in self._diff_quos[i][2].
        """
        n = len(y)
        f = []
        for i in range(0,n):
            f += [ [y[i], 0, 0] ]
        for i in range(1,n):
            f[i][1] = ( f[i][0] - f[i-1][0] ) / (x[i] - x[i-1])
        for i in range(2,n):
            f[i][2] = ( f[i][1] - f[i-1][1] ) / (x[i] - x[i-2])
        return f


    @staticmethod
    def table_of_moments(x,y,differental_quiotients_table):
        """
        create Spline moments table after loading the set of interpolation nodes

        Spline Moments satisfies equality:

        l[k]*M[k-1] + 2*M[k] + (1-l[k])*M[k+1] = 6 * f[k-1, k, k+1]

        so they are expressed by the formula:

                D[k] - l[k]*M[k-1] - (1-l[k])*M[k+1]
        M[k] = ----------------------------------------
                                2

        But we can use the another algorithm!

        Solve system of equations (matrix form): A*M = D
        Where:                          
                                            A                                                 M                   D 

        |    2,  1-l[1],        0,        0,        0,        0,     ...,          0 |  |  M[1]  |         |  d[1]  |
        | l[2],       2,   1-l[2],        0,        0,        0,     ...,          0 |  |  M[2]  |         |  d[2]  |
        |    0,    l[3],        2,   1-l[3],        0,        0,     ...,          0 |  |  M[3]  |         |  d[3]  |
        |    0,       0,     l[4],        2,   1-l[4],        0,     ...,          0 |  |  ...   |  _____  |  ...   |
        |    0,       0,        0,      ...,      ...,      ...,       0,          0 |  |  ...   |  _____  |  ...   |
        |  ...,     ...,      ...,      ...,      ...,      ...,     ...,          0 |  |  ...   |         |  ...   |
        |  ...,     ...,      ...,      ...,      ...,      ...,     ...,          0 |  |  ...   |         |  ...   |
        |    0,       0,        0,        0,        0,   l[n-2],       2,   1-l[n-2] |  | M[n-2] |         | d[n-2] |
        |    0,       0,        0,        0,        0,        0,  l[n-1],          2 |  | M[n-1] |         | d[n-1] |

        We can find Moment's in linear time! ( O(n) )


        Algorithm to solve it:
        +-----
        |
        |  q[0] = 0
        |
        |  U[0] = 0
        |
        |  p[k] =  l[k]*q[k-1] + 2
        |
        |          l[k] - 1  
        |  q[k] = ----------
        |            p[k]
        |
        |
        |          d[k] - l[k]*U[k-1]  
        |  U[k] = ---------------------
        |                  p[k]
        |
        |
        |  M[n-1] = U[n-1]
        |
        |  M[k] = U[k] + q[k]*M[k+1]
        |
        +-----

        where: 
            M[0] = M[n] = 0
            d[k] = 6 * f[k-1, k, k+1]
            q[0] = U[0] = 0

                     x[k] - x[k-1]            h[k]
            l[k] = -----------------  =  ---------------
                    x[k+1] - x[k-1]       h[k+1] + h[k]


            h[k] = x[k] - x[k-1]
        
        M[i] == S''(Xi) 
        """
        n = len(x)
        Momoents = list(range(0,n))
        Momoents[n-1] = 0
        Momoents[0] = 0
        U,q = Spline.U_q_table(x,differental_quiotients_table)
        for i in range(n-2, 0, -1):
            Momoents[i] = U[i] + q[i]*Momoents[i+1] 
        return Momoents


    @staticmethod
    def U_q_table(xs, differental_quiotients_table):
        """ returns lists U and q needed to calculate moments (Mi - ith moment = s''(Xi)) """
        n = len(xs)-1
        U,q = [None],[None]
        U += [3 * differental_quiotients_table[2][2]]                             # U1
        q += [(1 - (xs[1]-xs[0]) / (xs[2]-xs[0])) / 2]     # q1
        for i in range(2,n):
            li = ( xs[i]-xs[i-1] ) / ( xs[i+1]-xs[i-1] )
            di = 6 * differental_quiotients_table[i+1][2]
            pi = 2 + li*q[i-1]
            q.append( ( 1 - li ) / pi )
            U.append( (di - li*U[i-1]) / pi )
        return U,q
        

    @staticmethod
    def s(k, x, y, Momoents, xx):
        """ k-th part of the interpolating polynomial """
        h = x[k] - x[k-1]
        x_xk = xx - x[k-1]
        xk_x = x[k] - xx
        return 1/h*( 1/6 * Momoents[k-1] * xk_x**3  +  
                     1/6 * Momoents[k]   * x_xk**3  +  
                     ( y[k-1] - 1/6 * Momoents[k-1] * (h**2) ) * xk_x +
                     ( y[k]   - 1/6 * Momoents[k]   * (h**2) ) * x_xk )

    @staticmethod
    def line(p1, p2, x):
        a = (p1[1] - p2[1]) / (p1[0] - p2[0])
        b = p1[1] - a*p1[0]
        return a*x + b
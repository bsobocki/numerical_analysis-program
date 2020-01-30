
# dot product of functions ( f , g )N 
class func_dot_product():

    # xs == the list of elements from 'X'
    def __init__(self, xs):
        self._xs = xs

    # ( f, g )N = f(X0)*g(X0) + f(X1)*g(X1) + f(X2)*g(X2) + ... + f(Xm)*g(Xm)
    def __call__(self, f, g): 
        return sum( (f(x)*g(x) for x in self._xs) )

# ---

# least-squares_function_approximation
class l_s_aprox():

    # xs == the list of elements from 'X'
    def __init__(self, degree, points):
        xs = [p[0] for p in points]
        self._dot_prod = func_dot_product(xs)
        self._m = degree

        self._points = {}
        self._add_points(points)

        self._cs = {}
        self._ds = {}
        self._as = [self._a(k) for k in range(0, self._m)]

    def __call__(self, x):
        return sum( (self._as[k]*self._P(k,x) for k in range(0, self._m)) )

    def increase_degree(self):
        self._as.append(self._a(self._m))
        self._m += 1

    def _add_points(self, points):
        for p in points:
            self._points[ p[0] ] = p[1]

    # P0, P1, P2, ..., Pm == ortogonal polynomials
    def _P(self, k, x):
        # P0(x) = 1
        if k==0: return 1
        # P1(x) = x - c1
        if k==1: return x - self._c(1)
        # Pk(x) = (x-ck)*Pk-1(x) - dk*Pk-2(x) 
        res = (x-self._c(k))*self._P(k-1, x) - self._d(k) * self._P(k-2, x)
        return res

    def _c(self, k):
        if not k in self._cs:
            x_Pk_1 = lambda x: x * self._P(k-1, x)
            Pk_1 = lambda x: self._P(k-1, x)
            self._cs[k] = self._dot_prod( x_Pk_1, Pk_1 ) / self._dot_prod( Pk_1, Pk_1 )
        return self._cs[k]

    def _d(self, k):
        if not k in self._ds:
            Pk_1 = lambda x : self._P(k-1, x)
            Pk_2 = lambda x : self._P(k-2, x)
            self._ds[k] = self._dot_prod ( Pk_1, Pk_1 ) / self._dot_prod ( Pk_2, Pk_2 )
        return self._ds[k]

    def _a(self, k):
        f = lambda x: self._points[x]
        Pk = lambda x : self._P(k, x)
        res = self._dot_prod( f, Pk ) / self._dot_prod( Pk, Pk )
        return res

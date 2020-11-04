import math

def sqr(x):
    return x*x

class AbsqrtN:
    sqrtns = {}
    def _getSqrtn(self):
        if not self._n in self.sqrtns:
           self.sqrtns[self._n] = math.sqrt(self._n)
        return self.sqrtns[self._n]

    def _checkEqualN(self, a):
        assert (self._n == a._n), 'ERROR: some operation with AbsqrtNs with _n = ' + str(self._n) + ' and ' + str(a._n)
            
    def _le0(self):
        o = type(self._a)(0)
        if self._a == 0:
            return self._b < 0
        if self._b == 0:
            return self._a < 0
        if self._a > 0 and self._b > 0:
            return False
        if self._a < 0 and self._b < 0:
            return True
        v = self._a * self._a - self._b * self._b * type(o)(self._n)
        if self._a > 0:
            return v < 0
        else:
            return v > 0

    def __init__(self, n, a, b):
        self._n = n
        self._a = a
        self._b = b

    def GetA(self):
        return self._a

    def GetB(self):
        return self._b

    def __eq__(self, a):
        self._checkEqualN(a)
        return self._a == a.GetA() and self._b == a.GetB()

    def __ne__(self, a):
        return not self == a

    def __lt__(self, a):
        return (self - a)._le0()

    def __gt__(self, a):
        return (a - self)._le0()

    def __le__(self, a):
        return not ((a - self)._le0())

    def __ge__(self, a):
        return not ((self - a)._le0())

    def __float__(self):
        return float(self._a) + float(self._b) * self._getSqrtn()

    def __int__(self):
        return int(float(self))

    def __round__(self):
        return round(float(self))

    def __add__(self, a):
        self._checkEqualN(a)
        return AbsqrtN(self._n, self._a + a.GetA(), self._b + a.GetB())  

    def __sub__(self, a):
        self._checkEqualN(a)
        return AbsqrtN(self._n, self._a - a.GetA(), self._b - a.GetB()) 
    
    def __mul__(self, a):
        self._checkEqualN(a)
        T = type(self._a)
        return AbsqrtN(self._n,
                       self._a * a.GetA() + T(self._n) * self._b * a.GetB(),
                       self._a * a.GetB() + self._b * a.GetA()
                      )
           
    def __truediv__(self, a):
        self._checkEqualN(a)
        T = type(self._a)
        assert (a._a != T(0) or a._b != T(0)), 'ERROR: dividing by zero'
        
        ab3 = AbsqrtN(self._n, a.GetA(), -a.GetB())
        ans = self * ab3
        denom = sqr(a.GetA()) - sqr(a.GetB()) * T(self._n)
        return AbsqrtN(self._n, ans.GetA() / denom, ans.GetB() / denom)

    def __neg__(self):
        return AbsqrtN(self._n, -self._a, -self._b)

    def __str__(self):
       ans = str(self._a)
       if self._b != type(self._b)(0):
           ans = ans + '+sqrt(' + str(self._n) + ')*' + str(self._b)
       return ans

    def __hash__(self):
        return hash(str(self))

#WARNING: THERE IS A COPY-PASTE FOR Absqrt2 UNDER THIS CLASS...
class Absqrt3:
    def __init__(self, a, b=None):
        if b is None:
            if type(a) == AbsqrtN and a._n == 3:
                self._obj = a
                return None
            else:
                T = type(a)
                b = T(0)
        self._obj = AbsqrtN(3, a, b)

#    def __init__(self, a):
#        if type(a) == AbsqrtN and a._n == 3:
#            self._obj = a
#            return None

#        T = type(a)
#        self._obj = AbsqrtN(3, a, T(0))

    def GetA(self):
        return self._obj._a

    def GetB(self):
        return self._obj._b

    def __eq__(self, a):
        return self._obj == a._obj

    def __ne__(self, a):
        return self._obj != a._obj

    def __lt__(self, a):
        return self._obj < a._obj

    def __gt__(self, a):
        return self._obj > a._obj

    def __le__(self, a):
        return self._obj <= a._obj

    def __ge__(self, a):
        return self._obj >= a._obj

    def __float__(self):
        return float(self._obj)

    def __int__(self):
        return int(self._obj)

    def __round__(self):
        return round(self._obj)

    def __add__(self, a):
        return Absqrt3(self._obj + a._obj)

    def __sub__(self, a):
        return Absqrt3(self._obj - a._obj)
    
    def __mul__(self, a):
        if type(a) == Absqrt3:
            a = a._obj
        return Absqrt3(self._obj * a)
           
    def __truediv__(self, a):
        return Absqrt3(self._obj / a._obj)

    def __neg__(self):
        return Absqrt3(-(self._obj))

    def __str__(self):
        return str(self._obj)

    def __hash__(self):
        return hash(str(self))

class Absqrt2:
    def __init__(self, a, b=None):
        if b is None:
            if type(a) == AbsqrtN and a._n == 2:
                self._obj = a
                return None
            else:
                T = type(a)
                b = T(0)
        self._obj = AbsqrtN(2, a, b)

#    def __init__(self, a):
#        if type(a) == AbsqrtN and a._n == 3:
#            self._obj = a
#            return None

#        T = type(a)
#        self._obj = AbsqrtN(3, a, T(0))

    def GetA(self):
        return self._obj._a

    def GetB(self):
        return self._obj._b

    def __eq__(self, a):
        return self._obj == a._obj

    def __ne__(self, a):
        return self._obj != a._obj

    def __lt__(self, a):
        return self._obj < a._obj

    def __gt__(self, a):
        return self._obj > a._obj

    def __le__(self, a):
        return self._obj <= a._obj

    def __ge__(self, a):
        return self._obj >= a._obj

    def __float__(self):
        return float(self._obj)

    def __int__(self):
        return int(self._obj)

    def __round__(self):
        return round(self._obj)

    def __add__(self, a):
        return Absqrt2(self._obj + a._obj)

    def __sub__(self, a):
        return Absqrt2(self._obj - a._obj)
    
    def __mul__(self, a):
        if type(a) == Absqrt2:
            a = a._obj
        return Absqrt2(self._obj * a)
           
    def __truediv__(self, a):
        return Absqrt2(self._obj / a._obj)

    def __neg__(self):
        return Absqrt2(-(self._obj))

    def __str__(self):
        return str(self._obj)

    def __hash__(self):
        return hash(str(self))

if __name__ == '__main__':
    from fractions import Fraction
    b = AbsqrtN(3, Fraction(1), Fraction(2))
    print(float(b))
    a = Absqrt3(Fraction(1), Fraction(2))
    print(float(a))
    c = AbsqrtN(2, Fraction(1), Fraction(-2))
    print(float(c))
    d = Absqrt2(Fraction(1), Fraction(-2))
    print(float(d))


'''
c2 = AbsqrtN(2, 1, 1)
c3 = AbsqrtN(3, 1, 1)
c4 = AbsqrtN(2, -1, -1)
print (float(c2))
print (float(c3))
print (float(c4))

print (c2.sqrtns)
print (c3.sqrtns)
print (c4.sqrtns)

a = 5.0
b = 0
print(a)
print(b)
b = type(a)(b)
print(b)


print(int(0))
print (float(c2 + c4))
print (float(c2 - c4))
print (float(c2 * c4))
print (float(c2 / c4))
'''

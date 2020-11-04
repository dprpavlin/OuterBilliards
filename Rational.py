
from fractions import Fraction

print Fraction(28, -21)
print float(Fraction(1, 2))

'''
def findGcd(x, y):
    if x < 0:
        x = -x
    if y < 0:
        y = -y
    while y > 0:
        t = x % y
        x = y
        y = t
    return x

def findAbs(x):
    return -x if x < 0 else x

class Rational:
    def _reduce(self):
        if self._denominator < 0:
            self._nominator *= -1
            self._denominator *= -1
        g = findGcd(self.nominator, self.denominator)
        if g == 1:
            return
        self._nominator /= g
        self._denominator /= g

    def __init__(nominator = 0, denominator = 1):
        self._nominator = nominator
        self._denominator = denominator
        assert(denominator != 0, 'ERROR: 0 is impossible denominator')
        self._reduce()

    def getNominator(self):
        return self._nominator
    def getDenominator(self):
        return self._denominator

    def __add__(self, r):
        return Rational(self._nominator * r.getDenominator() + self._denominator * r.getNominator(), self._denominator * r.getDenominator())

    def __neg__(self):
        return Rational(-self._nominator, self._denominator)
            
    def __sub__(self, r):
        return Rational(self._nominator * r.getDenominator() - self._denominator * r.getNominator(), self._denominator * r.getDenominator())

    def __mul__(self, r):
        return Rational(self._nominator * r.getNominator(), self._denominator * r.getDenominator())
    
    def __truediv__(self, r):
        return Rational(self._nominator * r.getDenominator(), self._denominator * r.getNominator())

    def __eq__(self, r):
        return (self._nominator == r.getNominator() and self._denominator == r.getDenominator())

    def __ne__(self, r):
        return not(self == r)

    def __lt__(self, r):
        return (self._nominator * r.getDenominator() < self._denominator * r.getDenominator())

    def __gt__(self, r):
        return (self._nominator * r.getDenominator() > self._denominator * r.getDenominator())
    
    def __le__(self, r):
        return not(self > r)
    def __ge__(self, r):
        return not(self < r)

    def floor(self):
        return self._nominator / self._denominator

    def ceil(self):
        if self._denominator == 1:
            return self._nominator
        return 1 + nominator / denominator

    def round(self):
        if self._denominator == 1:
            return self._nominator
        ost = self._nominator
        ans = self._nominator / self._denominator
        if 2 * ost >= self._denominator:
            ans++
        return ans

    def getValue(self):
        

    def __float__(self):
        return self.getValue()
#print findGcd(3, 6)
#print findGcd(131313131313131313131313, 131313131313131313131313)
#print findGcd(13131313131313131313, 131313131313131313131313)

#a = 5
#b = a
#a += 1
#print a
#print b

print ((-5) / 2)
print (5 / 2)
print ((-5) % 3)
print 5 % 3
'''

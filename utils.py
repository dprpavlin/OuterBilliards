
def Abs(x):
    T = type(x)
    return -x if x < T(0) else x

def sign(x):
    T = type(x)
    if x == T(0):
        return 0
    return 1 if x > T(0) else -1

def to_key_with_less(mycmp):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj)
        def __gt__(self, other):
            return mycmp(other.obj, self.obj)
        def __eq__(self, other):
           return not(mycmp(self.obj, other.obj)) and not(mycmp(other.obj, self.obj))

        def __le__(self, other):
            return not(mycmp(other.obj, self.obj))
        def __ge__(self, other):
            return not(mycmp(self.obj, other.obj))
        def __ne__(self, other):
           return (mycmp(self.obj, other.obj)) or (mycmp(other.obj, self.obj))
    return K

standardLess = lambda x, y: x < y
standardEq = lambda x, y: x == y

def sort(lst, less=standardLess):
    return sorted(lst, key=to_key_with_less(less))

def unique(lst, eq=standardEq):
    if (len(lst) == 0):
        return []
    ans = [lst[0]]
    for i in range(1, len(lst)):
        if not eq(ans[-1], lst[i]):
            ans.append(lst[i])
    return ans

def copy2dList(lst):
    ans = []
    for i in range(0, len(lst)):
        ans.append(lst[i].copy())
    return ans


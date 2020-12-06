from itertools import zip_longest

class Ilist(list):
    def __add__(self, other):
        tmp = [x + y for x, y in zip_longest(self,other, fillvalue = 0)]
        return Ilist(tmp)
    
    def __sub__(self, other):
        tmp = [x - y for x, y in zip_longest(self,other, fillvalue = 0)]
        return Ilist(tmp)
    
    def __iadd__(self, other):
        return self + other
    
    def __isub__(self, other):
        return self - other
    
    def __lt__(self, other):
        return sum(self) < sum(other)
    
    def __gt__(self, other):
        return sum(self) > sum(other)
    
    def __le__(self, other):
        return sum(self) <= sum(other)
    
    def __ge__(self, other):
        return sum(self) >= sum(other)
    
    def __eq__(self, other):
        return sum(self) == sum(other)
    
    def __ne__(self, other):
        return sum(self) != sum(other)

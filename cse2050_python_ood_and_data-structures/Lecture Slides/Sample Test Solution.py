class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y
    def __getitem__(self, loc):
        if loc == 0 or loc=="x":
            return self._x
        elif loc == 1 or loc=="y":
            return self._y
        else:
            raise Exception("illegal input")
p = Point(2,6)
print(p[0], p[1]) 
print(p["x"], p["y"])

class Range:
    def __init__(self, start, end):
       	 self._start = start
       	 self._end = end
    def __iter__(self):
        self._run = self._start
        return self
    def __next__(self):
        if self._run >= self._end:
            raise StopIteration
        data = self._run
        self._run += 1
        return data
for x in Range(2,5):
    print(x)

def getFreqs(s):
    freqs = {}
    for char in s:
        freqs[char] = freqs.get(char, 0) + 1
    return freqs

print(getFreqs("Hello World!"))
 
    


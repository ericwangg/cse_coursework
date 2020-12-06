## Part 1
class BinaryTree:
    def __init__(self, spec):
        if type(spec) is tuple or type(spec) is list:
            if len(spec) >= 1 and len(spec) <= 3:
                if len(spec) == 1:
                    self.data = spec[0]
                    self.leftChild = None
                    self.rightChild = None
                else:
                    self.data = spec[0]
                    self.leftChild = BinaryTree(spec[1])
                    self.rightChild = BinaryTree(spec[-1])
        else:
            self.data = spec
            self.leftChild = None
            self.rightChild = None

    def printpreorder(self):
        print(self.data)
        if self.leftChild != None:
            self.leftChild.printpreorder()
        if self.rightChild != None:
            self.rightChild.printpreorder()


class Tree:
    def __init__(self, spec):
        if type(spec) is tuple or type(spec) is list:
            self.data = spec[0]
            self.children = [Tree(subSpec) for subSpec in spec[1:]]
        else:
            self.data = spec
            self.children = []

    def printpreorder(self):
        print(self.data)
        for child in self.children:
            child.printpreorder()

    ## Part 2
    def printbookcontent(self, Chap = 0):
        print("Book title: " + str(self.data[0]))
        if Chap == 0:
            for child in range(len(self.children)):
                self.children[child].printbookcontent( str(child + 1) )
        else:
            print ("%s %s, Page %s" % (Chap, self.data[0], self.data[1]))
            for subChild in range(len(self.children)):
                self.children[subChild].printbookcontent(Chap + "." + str(subChild + 1))

        # print('Book title:', self.data[0])
        # yield self.data
        # for child in self.children:
        #     for self.data in child.printpreorder()
        #         yield data

    # def printBChelp(self, count = 0):
    #     if self.data:
    #         print('%s' % i , self.data[0], ', Page %s' % self.data[1])
    #         for head in self.data:
    #             count + 1
    #             head.printpreorder()
    #     elif self.children:
    #         print('%s' % i , self.data[0], ', Page %s' % self.data[1])
    #         for child in self.children:
    #             count + 0.1
    #             child.printpreorder()

    ## Part 3
    def computespace(self):
        space = 0
        if len(self.children) == 0:
            return self.data[1]
        for n in range(len(self.children)):
            if self.data[1] == None:
                space += self.children[n].computespace()
        self.data = (self.data[0], space)
        return space

        # if self.data[1] == None:
        #     print("it passed")
        #     for child in range(len(self.children)):
        #         self.children(child).computespace( str(child + 1))
        # else:
        #     print("CHILD CASE")
        #     for child in self.children:



    def printExpr(self):
        sOut = ""
        if len(self.children) > 0:
            sOut += '(' + self.children[0].printExpr() + ')'
        sOut += str(self.data)
        if len(self.children) > 1:
            sOut += '(' + self.children[1].printExpr() + ')'
        return sOut

    def computeValue(self):
        childValues = [x.computeValue() for x in self.children]
        return value(self.data, childValues)

    def compute(self, evalFunc):
        childValues = [x.compute(evalFunc) for x in self.children]
        return evalFunc(self.data, childValues)



## Part 4
def value(data, values):
    if type(data) is int and values == []:
        return float(data)
    elif data == 'sum':
        return sum(values)
    elif data == '+':
        return (values[0] + values[1])
    elif data == '-':
        return (values[0]  - values[1])
    elif data == '*':
        return (values[0]  * values[1])
    elif data == '/':
        return (values[0]  / values[1])
    elif data == 'min':
        return min(values)
    elif data == 'max':
        return max(values)
    elif data == 'avg':
        return (sum(values) / len(values))


## Part 5
def spaceusage(data, values):
    space = 0
    if values == []:
        return data[1]
    for child in values:
        if type(child) == int:
            space += child
        elif type(child) == tuple:
            space += child[1]
    return space

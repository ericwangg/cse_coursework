import time
import random
import os
#==============  TreeNode class  =================

class TreeNode:
  def __init__(self, val, parent = None):
    self.height = 1
    self.val = val
    self.parent = parent
    self.leftChild = None
    self.rightChild = None
    self.height1 = 1

  def hasLeftChild(self):
    return self.leftChild

  def hasRightChild(self):
    return self.rightChild

#==============  PQ class  =================

class PQ(TreeNode):
  def add(self,val):
    raise NotImplemented

  def peekMin(self):
    raise NotImplemented

  def getMin(self):
    raise NotImplemented

  def __len__(self):
    raise NotImplemented

# ============== LIST CLASS ==================

class ListPQ(PQ):
  def __init__(self):
    self.items = []

  def __len__(self):
    return len(self.items)

  def add(self, val):
    self.items.append(val)

  def peekMin(self):
    return self.getMin(False)

  def getMin(self, toRemove=True):
    if (self.items == []):
      return None
    minIdx = 0
    sz = len(self.items)
    for idx in range(sz):
      if priority(self.items[idx]) < priority(self.items[minIdx]):
        minIdx = idx
    minItem = self.items[minIdx]
    if toRemove:
      del self.items[minIdx]
    return minItem

  def draw(self):
    print(self.items)

# ============== BST CLASS ==================

class BST(PQ):

  def __init__(self):
    self.root = None
    self.size = 0

  def __len__(self):
    return self.size

  ## Part 2
  def height(self, tree):
    if tree is None:
        return 0
    elif tree.leftChild == None and tree.rightChild == None:
        return 1
    else:
        return max(self.height(tree.leftChild), self.height(tree.rightChild)) + 1

  def setHeights(self, tree):
    if tree is not None:
        tree.height1 = self.height(tree)
        self.setHeights(tree.leftChild)
        self.setHeights(tree.rightChild)


  def add(self, val):
    print ("calling add for BST, value", val)
    # self.size += 1
    # def __add (root, val, parent = None):
    #     if root == None:
    #         newNode = TreeNode(val, parent)
    #         newNode.height1 += 1
    #         return TreeNode(val, parent)
    #     if val < root.val:
    #         root.leftChild = __add(root.leftChild, val, root)
    #     else:
    #         root.rightChild = __add(root.rightChild, val, root)
    # self.root = __add(self.root, val)
    # self.draw()
    # # return self.root
    # return newNode

    # new ADD method
    if self.root == None:
        newNode = TreeNode(val)
        self.root = newNode
    else:
        curNode = self.root
        while curNode != None:
            if priority(val) < priority(curNode.val):   # func. input "value" less than (<) current Node value
                if curNode.leftChild is None:
                    newNode = TreeNode(val, curNode)
                    curNode.leftChild = newNode
                    break
                else:
                    curNode = curNode.isLeftChild
            else:
                if curNode.rightChild is None:
                    newNode = TreeNode(val, curNode)
                    curNode.rightChild = newNode
                    break
                else:
                    curNode = curNode.rightChild
    self.size += 1
    self.draw()
    return newNode

  def peekMin(self):
    return self.getMin(False)

  def getMin(self, toRemove=True):
    curNode = self.root     # set current Node to the root
    if not curNode:         # if it's not the current Node
      return None           # returns None
    while curNode.leftChild != None:        # while left Child is None
      curNode = curNode.leftChild           # set curNode to leftChild
    if toRemove:                            # if desire is to Removed
      self._remove(curNode)   ## "__remove" Implemented in Part 3 remove func.
      self.size -= 1                        # removing, therefore size decrease by 1
    return curNode.val                      # returns current Node value

  ## Part 3
  def _remove(self, node):
    print("***********before removing ", node.val)
    curNode = node
    if curNode.parent == None:                      # current Node parent = None?
        self.root = None                            # root is None
    elif curNode.rightChild != None:                        # right Child is NOT none?
        curNode.parent.leftChild = curNode.rightChild               # set parent's left Child to curNode right Child
        curNode.parent.leftChild.leftChild = curNode.leftChild      # set the original leftChild's leftchild to be just the leftChild
    elif curNode.leftChild != None:
        curNode.parent.leftChild = curNode.leftChild
    else:
        curNode.parent.leftChild = None
    self.draw()

  def draw(self):
    drawTree(self.root, 0, True)

# ================ class BalancedBST ===============

class BalancedBST(BST):

  ## Part 4
  def add(self, val):
    print ("calling add for Balanced BST, value", val)
    # Attempt 2
    newNode = BST.add(self, val)
    curNode = newNode

    # Current Node isn't Nothing & it's parrent isn't Nothing
    while curNode != None and curNode.parent != None:
        curNode.parent.height = BST.height(self, curNode)
        if abs(BST.height(self, curNode.parent.leftChild) - BST.height(self, curNode.parent.rightChild)) > 1:    # value check
            def bounceBack(self, tree):                                                                         # rebalancing helper
                def balanceProperty(self, tree):                                                                #
                    return (BST.height(self, tree.leftChild) - BST.height(self, tree.rightChild)) > 1
                if balanceProperty(self, tree) < 0:
                    if balanceProperty(self, tree.rightChild) > 0:
                        self.rotateRight(tree.rightChild)
                        self.rotateLeft(tree)
                    else:
                        self.rotateLeft(tree)
                else:
                    if balanceProperty(self, tree.leftChild) < 0:
                        self.rotateLeft(tree.leftChild)
                        self.rotateRight(tree)
                    else:
                        self.rotateRight(tree)
                bounceBack(self, curNode.parent)
            curNode = curNode.parent
    self.size += 1
    # others
    self.draw()
    return newNode

    def rotateLeft(self,rotRoot):
        newRoot = rotRoot.rightChild
        rotRoot.rightChild = newRoot.leftChild
        if newRoot.leftChild != None:
            newRoot.leftChild.parent = rotRoot
        newRoot.parent = rotRoot.parent
        if rotRoot.isRoot():
            self.root = newRoot
        else:
            if rotRoot.isLeftChild():
                rotRoot.parent.leftChild = newRoot
            else:
                rotRoot.parent.rightChild = newRoot
        newRoot.leftChild = rotRoot
        rotRoot.parent = newRoot

    def rotateRight(self, rotRoot):
        newRoot = rotRoot.leftChild
        rotRoot.leftChild = newRoot.rightChild
        if newRoot.rightChild != None:
            newRoot.rightChild.parent = rotRoot
        newRoot.parent = rotRoot.parent
        if rotRoot.isRoot():
            self.root = newRoot
        else:
            if rotRoot.isRightChild():
                rotRoot.parent.rightChild = newRoot
            else:
                rotRoot.parent.keftChild = newRoot
        newRoot.rightChild = rotRoot
        rotRoot.parent = newRoot

    def draw(self):
      BST.setHeights(self, self.root)
      drawTree(self.root, 0, True)

# ============== simulator ======================

class Simulator:

  def __init__ (self, newPQ, isLoud=True):
    self.pq = newPQ
    self.limit = -1
    self.clock = 0
    self.log = None
    self.addTime = 0
    self.getTime = 0
    self.isLoud = isLoud

  def setLimit(self, num):
    self.limit = num

  def useLog(self, log):
    self.log = log

  def _getNextEvent(self):
    self.clock += 1  # timestamps start at 1 and go up
    if self.log:
      idx = self.clock - 1
      if idx >= len(self.log):
        return None
      line = self.log[self.clock -1 ]
      #print ("found line", line)
      if line[0] == 'g':
        return ()
      else:
        nums = line[2:-1].split(',')
        return (int(nums[0]), int(nums[1]))
    else:  # either generate a new task or get existing task to process
      num = random.randint(1,22)
      isNew = (num % 7 < 4)  # 4/7 of the time we have new task
      if isNew:
        return (num, self.clock)
      else:
        return ()

  def run(self):
    if self.isLoud:
        print("Simulation starting, PQ is ", type(self.pq), ", using log:", bool(self.log), ", limit is", self.limit)
    log = []
    while (self.limit == -1 or self.clock < self.limit):
      val = self._getNextEvent()
      if val == None:
        break
      elif len(val) > 0: # a new task has been generated for processing
        if self.isLoud:
          print("New task", val, "has been generated")
        startTime = time.time()
        self.pq.add(val)
        endTime = time.time()
        log.append("n" + str(val))
        self.addTime += endTime - startTime
      else:
        startTime = time.time()
        val = self.pq.getMin() # system is ready to process next task
        endTime = time.time()
        if self.isLoud:
          print(val, "is being processed next")
        log.append("g" + str(val))
        self.getTime += endTime - startTime
    if self.isLoud:
      self.pq.draw()
    print("Simulation finished,", type(self.pq), "has size", len(self.pq))
    return log

# ============== additional methods ==================

## Part 1
def priority(val):
    return val

def drawTree(node, indent=0, showHeight=False):
    if node == None:
        return
    drawTree(node.rightChild, indent+1, showHeight)

    if node.rightChild:
        print("     " * indent, "  / ")
    if showHeight:
        print("     " * indent, node.val, ", height", node.height1)
    else:
        print("     " * indent, node.val)
    if node.leftChild:
        print("     " * indent, "  \ ")
    drawTree(node.leftChild, indent+1, showHeight)


# =================  testing around ===================

# x = ListPQ() # we can also do BST or BalancedBST here
# x.add(5)
# x.add(9)
# x.add(11)
# x.add(10)
# x.add(3)
# x.add(4)
# x.draw()
#
# # len(x) should be 6, highest priority is 3
# print("This", type(x), "has", len(x), "items, highest priority is", x.peekMin())
# y = x.getMin()
# print("Removed", y, "here is what's left")
# x.draw()
#
# s1 = Simulator(BalancedBST()) # interactive simulator with BalancedBST impl
# s1.setLimit(17) # will stop after processing 17 events
# s1.run()
#
# s = Simulator(ListPQ(),False) # this will be a long run, don't want it loud
# s.setLimit(10000) # will stop after processing 10000 events
# log = s.run()
#
# s2 = Simulator(ListPQ(), False)
# s2.useLog(log) # this will run from log
# log1 = s2.run()  # log and log1 should be identical
# print("Total add time:", s2.addTime, "; Total get time:", s2.getTime)
#
# s3 = Simulator(BST(), False)
# s3.useLog(log) # this will run from log
# log1 = s3.run()  # log and log1 should be identical
# print("Total add time:", s3.addTime, "; Total get time:", s3.getTime)

# once balancing is implemented, we want to compare the times of various impls for long runs!!

import time
import random
import os
#==============  TreeNode class  =================

class TreeNode:
  def __init__(self,val,parent=None):
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

class PQ:
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
    #gets the min (lowest priority)
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

  # Part 2
  def add(self, val):
    if self.root == None:
        newNode = TreeNode(val)
        self.root = newNode
    else:
        node = self.root
        while node != None:
            if priority(val) < priority(node.val):
                if node.leftChild is None:
                    newNode = TreeNode(val, node)
                    node.leftChild = newNode
                    break
                else:
                    node = node.leftChild
            else:
                if node.rightChild is None:
                    newNode = TreeNode(val, node)
                    node.rightChild = newNode
                    break
                else:
                    node = node.rightChild
    self.size += 1
    # self.draw()
    return newNode

  def peekMin(self):
    return self.getMin(False)

  def getMin(self, toRemove=True):
    curNode = self.root
    if not curNode:
      return None
    while curNode.leftChild != None:
      curNode = curNode.leftChild
    if toRemove:
      self._remove(curNode)   ## TO IMPLEMENT
      self.size -= 1
    return curNode.val

  ## Part 3
  def _remove(self, node):
    print("***********before removing ", node.val)
    node1 = node
    if node1.parent == None:
        self.root = None
    elif node.rightChild != None:
        node.parent.leftChild = node.rightChild
        node.parent.leftChild.leftChild = node.leftChild
    elif node.leftChild != None:
        node.parent.leftChild = node.leftChild
    else:
        node.parent.leftChild = None
    self.draw()

  def draw(self):
    drawTree(self.root, 0, True)

# ================ class BalancedBST ===============

class BalancedBST(BST):

  def update_height(self, node):
      if node is None:
          return 0
      node.height = 1+max(self.update_height(node.leftChild),self.update_height(node.rightChild))
      node.height1 = node.height
      return node.height

  def add(self,val):
    newNode = BST.add(self, val)
    while newNode is not None:
        # newNode.parent.height += 1
        self.update_height(newNode)
        if newNode.leftChild is not None or newNode.rightChild is not None:
            if newNode.leftChild is None:
                bal_factor = 0 - newNode.rightChild.height
            elif newNode.rightChild is None:
                bal_factor = newNode.leftChild.height - 0
            else:
                bal_factor = newNode.leftChild.height - newNode.rightChild.height
            if bal_factor > 1 or bal_factor < -1:
                if bal_factor < 0:
                    if newNode.rightChild.leftChild is None:
                        bal_factor_right = 0 - newNode.rightChild.rightChild.height
                    elif newNode.rightChild.rightChild is None:
                        bal_factor_right = newNode.rightChild.leftChild.height - 0
                    else:
                        bal_factor_right = newNode.rightChild.leftChild.height - newNode.rightChild.rightChild.height
                    if bal_factor_right > 0:
                        self.rotateRight(newNode.rightChild)
                        self.update_height(newNode)
                        self.rotateLeft(newNode)
                        self.update_height(newNode)
                    else:
                        self.rotateLeft(newNode)
                        self.update_height(newNode)
                else:
                    if newNode.leftChild.leftChild is None:
                        bal_factor_left = 0 - newNode.leftChild.rightChild.height
                    elif newNode.leftChild.rightChild is None:
                        bal_factor_left = newNode.leftChild.leftChild.height - 0
                    else:
                        bal_factor_left = newNode.leftChild.leftChild.height - newNode.leftChild.rightChild.height
                    if bal_factor_left < 0:
                        self.rotateLeft(newNode.leftChild)
                        self.update_height(newNode)
                        self.rotateRight(newNode)
                        self.update_height(newNode)
                    else:
                        self.rotateRight(newNode)
                        self.update_height(newNode)
        newNode = newNode.parent

    # self.draw()
    return newNode

  def rotateLeft(self,rotRoot):
    newRoot = rotRoot.rightChild
    rotRoot.rightChild = newRoot.leftChild
    if newRoot.leftChild != None:
        newRoot.leftChild.parent = rotRoot
    newRoot.parent = rotRoot.parent
    if rotRoot == self.root:
        self.root = newRoot
    else:
        if rotRoot.hasLeftChild():
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
    if rotRoot == self.root:
        self.root = newRoot
    else:
        if rotRoot.hasRightChild():
            rotRoot.parent.rightChild = newRoot
        else:
            rotRoot.parent.leftChild = newRoot
    newRoot.rightChild = rotRoot
    rotRoot.parent = newRoot

  def draw(self):
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
    print("     " * indent, node.val, ", height", node.height)
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
# # len(x) should be 6, highest priority is 3
# print("This", type(x), "has", len(x), "items, highest priority is", x.peekMin())
# y = x.getMin()
# print("Removed", y, "here is what's left")
# x.draw()
#
# x = BST()
# x.add(5)
# x.add(9)
# x.add(11)
# x.add(10)
# x.add(3)
# x.add(4)
# x.draw()
# print("this ListPQ has", len(x), 'items, highest priority is', x.peekMin())

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

#once balancing is implemented, we want to compare the times of various impls for long runs!!

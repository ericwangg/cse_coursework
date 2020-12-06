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

  def

  def updateheight(self):
      l = 0
      r = 0
      if self.leftChild:
          self.leftChild.updateheight()
          l = self.leftChild.height1 + 1
      if self.rightChild:
          self.rightChild.updateheight()
          r = self.rightChild.height1 + 1
      self.height = max(left, right, 1)



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
    elif tree.leftChild is None and tree.rightChild is None:
      return 1
    else:
      return max(self.height(tree.leftChild), self.height(tree.rightChild))+1

  def setHeights(self, tree):
    if tree is not None:
      tree.height1 = self.height(tree)
      self.setHeights(tree.leftChild)
      self.setHeights(tree.rightChild)


  def add(self,val):
    print ("calling add for BST, value", val)
    self.size += 1
    # if self.root == None:
    #   newNode = TreeNode(val)
    #   self.root = newNode
    # else:
    #   curNode = self.root
    #   while curNode != None:
    #     if priority(val) < priority(curNode.val):
    #       if curNode.leftChild is None:
    #         newNode = TreeNode(val, curNode)
    #         curNode.leftChild = newNode
    #         break
    #       else:
    #         curNode = curNode.leftChild
    #     else:
    #       if curNode.rightChild is None:
    #         newNode = TreeNode(val, curNode)
    #         curNode.rightChild = newNode
    #         break
    #       else:
    #         curNode = curNode.rightChild

    # Method 2
    newNode = TreeNode(val)
    def _add(curNode, val):
        if val < curNode.val:
            if curNode.leftChild is None:
                newNode.parent = curNode
                curNode.leftChild = newNode
            else:
                _add(curNode.leftChild, val)
        elif val > curNode.val:
            if curNode.rightChild is None:
                newNode.parent = curNode
                curNode.rightChild = newNode
            else:
                _add(curNode.rightChild, val)
    if self.root is None:
        self.root = newNode
    else:
        _add(self.root, val)

    self.draw()
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
##    if self.root is None:
##      return None
##    parent = node.parent
##    if parent is not None:
##      if node.rightChild is None:
##        parent.leftChild = None
##      else:
##        parent.leftChild = TreeNode(node.rightChild.val, parent)
##    else:
##      return None
##    curNode = node
##    if curNode.parent == None:
##      self.root = None
##    elif curNode.rightChild != None:
##      curNode.parent.leftChild = curNode.rightChild
##      curNode.parent.leftChild.leftChild = curNode.leftChild
##    elif curNode.leftChild != None:
##      curNode.parent.leftChild = curNode.leftChild
##    else:
##      curNode.parent.leftChild = None
##    self.draw()
    curNode = node
    if curNode.parent == None:
      self.root = None
    elif curNode.rightChild !=None:
      curNode.parent.leftChild = curNode.rightChild
      curNode.parent.leftChild.leftChild = curNode.leftChild
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
  def add(self,val): ## TO IMPLEMENT
    newNode = BST.add(self, val)
    current = newNode

    def rotateLeft(rotRoot):
        newRoot = rotRoot.rightChild
        rotRoot.rightChild = newRoot.leftChild
        if newRoot.leftChild != None:
            newRoot.leftChild.parent = rotRoot
        newRoot.parent = rotRoot.parent
        if self.parent == None:
            self.root = newRoot
        else:
            if node.parent.leftChild == node:
                rotRoot.parent.leftChild = newRoot
            else:
                rotRoot.parent.rightChild = newRoot
                newRoot.leftChild = rotRoot
                rotRoot.parent = newRoot
    def rotateRight(rotRoot):
        newRoot = rotRoot.leftChild
        rotRoot.leftChild = newRoot.rightChild
        if newRoot.rightChild != None:
            newRoot.rightChild.parent = rotRoot
        newRoot.parent = rotRoot.parent
        if self.parent == None:
            self.root = newRoot
        else:
            if node.parent.rightChild == node:
                rotRoot.parent.rightChild = newRoot
            else:
                rotRoot.parent.leftChild = newRoot
                newRoot.rightChild = rotRoot
                rotRoot.parent = newRoot

        def balfact(tree):
            return (BST.height(self, tree.leftChild) - BST.height(self, tree.rightChild))

        def balance(tree):
          if balfact(tree) < 0:
            if tree.rightChild and balfact(tree.rightChild) > 0:
              self.rotateRight(tree.rightChild)
              self.rotateLeft(tree)
            else:
              self.rotateLeft(tree)
          else:
            if tree.leftChild and balfact(tree.leftChild) < 0:
              self.rotateLeft(tree.leftChild)
              self.rotateRight(tree)
            else:
              self.rotateRight(tree)

    if self.root is None:
        self.root = TreeNode(val)
        newNode = self.isRoot
    else:
        newNode = self.root.add(val)
        current = newNode.parent
        while current is not None and current.parent is not None:
            current.parent.height = 0
            # if abs(BST.height(self, current.parent.leftChild) - BST.height(self, current.parent.rightChild)) > 1:
            lheight, rheight = 0, 0
            if current.leftChild:
                lheight = current.leftChild.height
            if current.rightChild:
                rheight = current.rightChild.height
            current.height = max(lheight, rheight) + 1
            if abs(balfact(current)) > 1:
                balance(current)
                self.root.updateheight()
            current = current.parent
    self.size += 1
    ## Write your code here
    self.draw()
    return newNode





    # def isRoot(self):
    #     self.parent = None
    #
    # def isLeftChild(node):
    #     node.parent.leftChild == node
    #
    # def isRightChild(node):
    #     node.parent.rightChild == node


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

x = ListPQ() # we can also do BST or BalancedBST here
x.add(5)
x.add(9)
x.add(11)
x.add(10)
x.add(3)
x.add(4)
x.draw()
# len(x) should be 6, highest priority is 3
print("This", type(x), "has", len(x), "items, highest priority is", x.peekMin())
y = x.getMin()
print("Removed", y, "here is what's left")
x.draw()

s1 = Simulator(BalancedBST()) # interactive simulator with BalancedBST impl
s1.setLimit(17) # will stop after processing 17 events
s1.run()

s = Simulator(ListPQ(),False) # this will be a long run, don't want it loud
s.setLimit(10)#000) # will stop after processing 10000 events
log = s.run()

s2 = Simulator(ListPQ(), False)
s2.useLog(log) # this will run from log
log1 = s2.run()  # log and log1 should be identical
print("Total add time:", s2.addTime, "; Total get time:", s2.getTime)

s3 = Simulator(BST(), False)
s3.useLog(log) # this will run from log
log1 = s3.run()  # log and log1 should be identical
print("Total add time:", s3.addTime, "; Total get time:", s3.getTime)

#once balancing is implemented, we want to compare the times of various impls for long runs!!

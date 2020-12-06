class LinkedListIter:
  def __init__(self, lst):
      self.L = lst
      self.it = iter(lst.L)

#self.position = 0

  def __next__(self):
      return next(self.it)

# if self.position  self.lst.size:
#     raise StopIteration("Err")
# else:
#     self.position += 1
#     return self.lst.L[self.position - 1]

  def __iter__(self):
      return self

class LinkedList:
  def __init__(self, L = [], size = 0):
      self.L = L
      self.size = size

  def addLast(self, x):
      self.L.append(x)
      self.size += 1

  def addFirst(self, x):
#        self.L[0] = x
#        self.size += 1

#      self.L.insert(0, x)
#      self.size += 1
# .insert( , ) method is about x5 faster than the following

# using list slicing
    # self.L = [x] + self.L
    # self.size += 1
      new_list = [x]
      count = 0
      while True:
          try:
              new_list.append(self.L[count])
              count += 1
          except IndexError:
              break
      self.L = new_list
      self.size += 1


# example list recusion helper
#ex.):
# def addFirst(self, x):
#    def helper(lst1, lst2):
#      if lst2 == []:
#             return lst1
#      else:
#           return helper(lst1 + lst2[0:1], lst2[1:])
#      new_list = [x]
#   return helper(new_list, self.L)

  def removeFirst(self):
      if self.L == []:
        return None
      else:
        self.L = self.L[-1:]
        self.size -= 1

# no ".pop"
    # if self.L == []:
    #     return None
    # else:
    #     removed = self.L[0]
    #     self.L = self.L[1:]
    #     return removed
    #     self.L -= 1

# with ".pop"
     # if self.L == []:
     #   return None
     # else:
     #     self.L = self.L.pop(0)
     #     self.size -= 1

  def removeLast(self):
      if self.L == []:
          return None
      else:
          self.L = self.L[:-1]
          self.size -= 1

  def addAt(self, idx, x):
      new_list = []
      count = 0
      while True:
          try:
              if count < idx:
                  new_list.append(self.L[count])
              elif count == idx:
                  new_list.append(x)
              elif count > idx:
                  new_list.append(self.L[count - 1])
              count += 1
          except IndexError:
             break
      if new_list == self.L or new_list == []:
         return False
      else:
         self.L = new_list
         self.size += 1
         return True

# Working with list slicing
      # if idx > self.size:
      #     return False
      # else:
      #     self.L = self.L[:idx] + [x] + self.L[idx:]
      #     self.size += 1
      #     return True

# 2nd method for indexing through a list
# def index_helper(self.L, count):
#     if self.L = []:
#             return count
#     else:
#         del self.L[-1]
#         count += 1
# return helper(self.L, 0)

  def removeAt(self, idx):
      new_list = []
      count = 0
      while True:
          try:
              if count < idx:
                  new_list.append(self.L[count])
              elif count == idx:
                  removed = self.L[idx]
                  new_list.append(self.L[count + 1])
              else:
                  new_list.append(self.L[count + 1])
              count += 1
          except IndexError:
              break
      self.size -= 1
      self.L = new_list
      return removed

#  Work in progress using empty list
#       i = 0
#       new_list = []
#       if i < idx:
#           new_list.append(self.L[i])
#       elif i == idx:
#           removed = self.L[idx]
#           new_list.append(self.L[i+1])
#       elif idx > self.size:
#           return None
#       else:
#           new_list.append(self.L[i+1])
#       i += 1

# Working with list slicing
      # if idx >= self.size:
      #     return None
      # else:
      #     removed = self.L[idx]
      #     post_idx = idx + 1
      #     self.L = self.L[:idx] + self.L[post_idx:]
      #     self.size -= 1
      #     return removed

# Working with .pop
     # if idx > self.size:
     #     return None
     # else:
     #     self.L.pop(idx)
     #     self.size -= 1

  def __str__(self):
    str = ""
    for x in self.L:
        str = str + "%s" % (x) + ";"
    return "[" + str[0:-1] + "]"

  def __contains__ (self, x):
    for n in self.L:
        if n == x:
            return True
        else:
            return False

  def __setitem__(self, idx, x):
      if idx < self.size:
         self.L[idx] = x
      else:
         raise Exception("Invalid index" + " %s" % idx)

  def __getitem__(self, idx):
      if idx < self.size:
          return self.L[idx]
      else:
          raise Exception("Invalid index" + " %s" % idx)

  def __iter__(self):
      return LinkedListIter(self)

  def __len__(self):
    return self.size

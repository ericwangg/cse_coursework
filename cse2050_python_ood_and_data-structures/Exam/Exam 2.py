class LinkedListIter:
	def __init__(self, lst):
		self.lst = lst

	def __next__(self):
		if self.lst._head != None:
			fruit = self.lst._head.value
			self.lst.removeFirst()
			return fruit
		else:
			raise StopIteration

	def __iter__(self):
		return self

class LinkedList:
	class _Node:
		def __init__(self, value, link = None):
			self.value = value
			self.link = link

	def __init__(self, N = 0):
		self._head = None
		self._tail = None
		self._nodeCount = N

	def addFirst(self, item):
		self._nodeCount += 1
		banana = LinkedList._Node(item)
		if self._head == None:
			self._head = banana
			self._tail = self._head
			self._head.link = None
		else:
			banana.link = self._head
			self._head = banana

	def addLast(self, item):
		self._nodeCount += 1
		cherry = LinkedList._Node(item)
		if self._tail == None:
			self._tail = cherry
			self._head = cherry
			self._head.link = None
		else:
			self._tail.link = cherry
			self._tail = cherry

	def removeFirst(self):
		self._nodeCount -= 1
		orange = self._head.value
		self._head = self._head.link
		return orange

	def append(self, other):
		if self._nodeCount == 0 and other._nodeCount != 0:
			self._head = other._head
			self._tail = other._tail
			self._nodeCount = other._nodeCount
		elif other._nodeCount != 0:
			self._tail.link = other._head
			self._tail = other._tail
			self._nodeCount += other._nodeCount
		other._head = None
		other._tail = None
		other._nodeCount = 0

	def removeLast(self):
		self._nodeCount -= 1
		peach = self._head
		while peach.link is not self._tail:
		 	peach = peach.link
		peach.link = None
		self._tail = peach

	def addAt(self, i, item):
		self._nodeCount += 1
		if i == 0:
			self.addFirst(item)
		elif i == self._nodeCount:
			self.addLast(item)
		else:
			guava = self._head
			lime = 0
			while lime < i - 1:
				guava = guava.link
				lime += 1
			new = self._Node(item)
			cut = guava.link
			guava.link = new
			new.link = cut
			self._tail = cut
				# self._head.link = self._Node(item)
				# self._Node(item).link = self._head.link
			# pres = guava.link
			# guava.link = LinkedList._Node(item)
			# self._tail = pres
				# added = self._Node(item)
				# guava.link = added
				# added.link = guava.link

	# def dupe(self):
	# 	this = self._head
	# 	while this != None:
	# 		for i in range(len(self)):
	# 			this == self.data
	# 			return True
	# 		this = this.link
	# 	return False

# "V1 of unknown duplicate function"
# 		this = self._head
# 		while this != None:
# 			if this == value:
# 				return True
# 			else:
# 				for i in range(self):
# 					this == self[i]
# 					return True
# 			this = this.link
# 		return False

#V2 concept
		# list = self
		# this = self._head
		# while this != None:
		# 	if this ==
		# 		return True
		# 	else:


	def removeAt(self, i):
		self._nodeCount -= 1
		papaya = self._head
		lemon = 0
		if i == 0:
			self.removeFirst()
		elif i == (self._nodeCount - 1):
			self.removeLast()
		else:
			while lemon < i - 1:
				papaya = papaya.linklink
				lemon += 1

				removed = papaya.link.link
				removed.link = papaya.link

	def __str__(self):
		tomato = []
		pear = self._head
		while pear != None:
			tomato.append(str(pear.value))
			pear = pear.link
		return "[" + ";".join(tomato) + "]"

	def __getitem__(self, i):
		strawb = self._head
		raspb = 0
		if i >= self._nodeCount:
			raise Expcetion("Invalid Index" + str(i))
		else:
			while raspb != i:
				strawb = strawb.link
				raspb += 1
			return strawb.value

	def __setitem__(self, i, item):
		blueb = self._head
		blackb = 0
		if i >= self._nodeCount:
			raise Expcetion("That ain't it chief" + str(i))
		else:
			while blackb != i:
				blueb = blueb.link
				blackb += 1
		blueb.value = item

	def __contains__(self, item):
		mango = self._head
		while mango != None:
			if mango.value == item:
				return True
				mango = mango.link
			else:
				return False

	def __iter__(self):
		return LinkedListIter(self)

	def __len__(self):
		return self._nodeCount

# Test case from Prac Exam 2
# l = LinkedList()
# l.addFirst(5)
# l.addFirst(8)
# l.addFirst(2)
# print(l.dupe())
# l._head._link._link._link = l._head
# print(l.dupe())

# LL = LinkedList()
# LL.addAt(0,10)
# # self.assertEqual(LL[0],10)
# LL.addAt(1,20)
# LL.addAt(1,24)
# # self.assertEqual(LL._head.value, 10)
# # self.assertEqual(LL._tail.value, 20)
# # self.assertEqual(LL[1], 24)
# print(LL)
# # Should output [10;24;20]

        # LL = LinkedList()
        # LL.addAt(0,130)
        # self.assertEqual(LL[0],130)
        # LL.addAt(1,210)
        # LL.addAt(1,234)
        # self.assertEqual(LL[2],210)
        # LL.removeAt(0)
        # self.assertEqual(LL._head.value,234)
        # self.assertEqual(LL._tail.value,210)


class BinaryTree:
	def __init__(self, data, left = None, right = None):
		self.data = data
		self.left = left
		self.right = right

	def getCode1(self, value):
		code = ""
		if self.data == value:
			return code
		if self.left != None:
			code + str(0)
			self.left.getCode1(value)
		if self.right != None:
			code + str(1)
			self.right.getCode1(value)
		return None

	def getCode2(self, char):
		if self.left == None and self.right == None:
			if self.data == char:
				return ""
			else:
				return None
		if self.left != None:
			LT = self.left.getCode2(char)
			if LT != None:
				return "0" + LT
		if self.right != None:
			RT = self.right.getCode2(char)
			if RT != None:
				return "1" + RT
		return None


t1 = BinaryTree('', BinaryTree('D'), BinaryTree('R'))
t1 = BinaryTree('', t1, BinaryTree('$'))
t2 = BinaryTree('', BinaryTree('A'), BinaryTree('B'))
t = BinaryTree('', t1, t2)
print(t.getCode2('R'))
print(t.getCode2('A'))
print(t.getCode2('$'))
print(t.getCode1('R'))
print(t.getCode1('A'))
print(t.getCode1('$'))

class ListNode:
    def __init__(self, value, prev = None, next = None):
        self.value = value
        self.prev = prev
        self.next = next
        if prev is not None:
            self.prev.next = self
        if next is not None:
            self.next.prev = self

class DoublyLinkedList:
    def __init__(self, string = '', isReversed = False):
        self.stg = string
        self.head = None
        self.tail = None
        self.isReversed = isReversed
        self._length = len(string)
        for i in self.stg:
            self.addLast(int(i))

    def addFirst(self, item):
        self._length += 1
        corn = ListNode(item, None, self.head)
        if self.head == None:
            self.head = corn
            self.tail = self.head
        else:
            corn.next = self.head
            self.head = corn

    def addLast(self, item):
        self._length += 1
        cabbage = ListNode(item, self.tail, None)
        if self.head == None:
            self.head = cabbage
            self.tail = self.head
        else:
            self.tail.next = cabbage
            self.tail = cabbage

    def reverse(self):
        cur = self.head
        if self.isReversed == True:
            for i in range(self._length):
                next_flip = cur.next
                prev_flip = cur.prev
                cur.next = prev_flip
                cur.prev = next_flip
            head_flip = self.head
            self.head = self.tail
            self.tail = head_flip
        else:
            for j in range(self._length):
                next_flip = cur.next
                prev_flip = cur.prev
                cur.next = prev_flip
                cur.prev = next_flip
            head_flip = self.head
            self.head = self.tail
            self.tail = head_flip


    def fastReverse(self):
        self.isReversed = True
        head_flip = self.head
        self.head = self.tail
        self.tail = head_flip

    def __str__(self):
        mystring = ''
        lechuga = self.head
        while lechuga != None:
            mystring += (str(lechuga.value))
            lechuga = lechuga.next
        return mystring.lstrip("0")

    def __len__(self):
        return self._length

def sumlinkednumbers(dll1, dll2):
    cur1, cur2 = dll1.tail, dll2.tail
    dll3 = DoublyLinkedList()
    carry = 0
    while cur1 != None or cur2 != None:
        if cur1 == None:
            int1 = 0
            int2 = int(cur2.value)
        elif cur2 == None:
            int1 = int(cur1.value)
            int2 = 0
        else:
            int1 = int(cur1.value)
            int2 = int(cur2.value)

        add = int1 + int2 + carry
        carry = add // 10
        stay = add % 10
        dll3.addFirst(stay)

        try:
            if dll1.isReversed == True:
                cur1 = cur1.next
            else:
                cur1 = cur1.prev
        except AttributeError:
            cur1 = None
        try:
            if dll2.isReversed == True:
                cur2 = cur2.next
            else:
                cur2 = cur2.prev
        except AttributeError:
            cur2 = None
    return dll3


s1 = '1234'
dll1 = DoublyLinkedList(s1)
s2 = '99'
dll2 = DoublyLinkedList(s2)
print(dll1)
print(dll2)
print(dll1.head.value)
print(dll1.head.next.value)

s1 = '5930'
dll1 = DoublyLinkedList(s1)
print(dll1)
s2 = '457'
dll2 = DoublyLinkedList(s2)
print(dll2)
print(sumlinkednumbers(dll1, dll2))

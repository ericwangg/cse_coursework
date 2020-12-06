import unittest
import random
from mapping import *

class TestGameTree(unittest.TestCase):
	def testinit(self):
		HM = HashMapping()
		self.assertEqual(len(HM),0)
		self.assertEqual(HM._size,1000)

		HM2 = HashMapping(4)
		self.assertEqual(len(HM),0)
		self.assertEqual(HM2._size,4)

	def testshakespearetoken(self):
		import random
		randLen = random.randint(0,100)
		s = ShakespeareToken("a"*randLen)
		self.assertEqual(hash(s),randLen)

		self.assertEqual(s == 10,type(s) == type(10))
		self.assertFalse(s == 10)
		self.assertFalse(s == "HelloWorld")

	def testextendabledoubling(self):
		f = open('shakespeare.txt', 'r')
		data = f.read()
		f.close()
		data = data.split()

		map1 = ExtendableHashMapping()
		for i in range(len(data)):
			key = data[i]
			s = ShakespeareToken(key)
			if key not in map1:
				map1[key] = hash(s)%map1._size

		self.assertEqual(len(map1._buckets), 64000)

		map2 = ExtendableHashMapping()
		randKey = []
		randVal = []

		i = 0
		while i < 5000:
		    randKey.append(random.randint(0,9))
		    randVal.append(random.randint(0,9))
		    i += 1

		randKey = str(randKey)
		randVal = str(randVal)
		map2[randKey] = randVal

		self.assertEqual(len(map2._buckets), 1000)

	def teststatistics(self):
		f = open('shakespeare.txt', 'r')
		data = f.read()
		f.close()

		data = data.split()

		map1 = HashMapping()
		for i in range(len(data)):
		   key = data[i]
		   s = ShakespeareToken(key)	## try the other two ShakespeareToken classes
		   if key not in map1:
		       map1[key] = hash(s)%map1._size

		stats = map1.statistics()
		self.assertEqual(stats[0], 1000)
		self.assertEqual(stats[1], 0)
		self.assertTrue(50 < stats[2] < 60)
		self.assertEqual(stats[3], 33.505)
		self.assertTrue(5.0 < stats[4], 6.5)

		map2 = ExtendableHashMapping()
		for i in range(len(data)):
		   key = data[i]
		   s = ShakespeareToken(key)	## try the other two ShakespeareToken classes
		   if key not in map2:
		       map2[key] = hash(s)%map2._size

		stats = map2.statistics()
		self.assertEqual(stats[0], 64000)
		self.assertTrue(35000 < stats[1] < 40000)
		self.assertTrue(3 < stats[2] < 10)
		self.assertTrue(0.3 < stats[3], 0.7)
		self.assertTrue(0.4 < stats[4], 0.9)

if __name__ == "__main__":
    unittest.main()
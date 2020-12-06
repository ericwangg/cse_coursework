import operator
import math
import time

## Part 3
class ShakespeareToken(str):
	def __init__(self, string):
		self._string = string
		self._length = len(string)

	def __hash__(self):
		return self._length

## Part 4
class SkakespeareToken2(str):
	def __init__(self, string):
		self._string = string
		self._length = len(string)

	def __hash__(self):
		sum = 0
		for v in self._string:
			sum += len(string)
		return sum

class SkakespeareToken3(str):
	def __init__(self, string):
		self._string = string
		self._length = len(string)

	def __hash__(self):
		hashvalue = 0
		for v2 in range(self._length):
			hashvalue += int(ord(self._string[v2])) * (53 ** v2)
		return hashvalue

class Entry:
	def __init__(self, key, value):
		self.key = key
		self.value = value

	def __str__(self):
		return "%d: %s" % (self.key, self.value)

class ListMapping:
	def __init__(self):
		self._entries = []

	def put(self, key, value):
		#print("ListMapping put", key)
		e = self._entry(key)
		if e is not None:
			e.value = value
		else:
			self._entries.append(Entry(key, value))

	def get(self, key):
		#print("ListMapping get", self, key)
		e = self._entry(key)
		if e is not None:
			return e.value
		else:
			raise KeyError

	def _entry(self, key):
		#print("ListMapping _entry", self, key)
		for e in self._entries:
			if e.key == key:
				return e
		return None

	def _entryiter(self):
		return (e for e in self._entries)

	def __str__(self):
		return str([str(e) for e in self._entries])

	def __getitem__(self, key):
		return self.get(key)

	def __setitem__(self, key, value):
		self.put(key, value)

	def __len__(self):
		return len(self._entries)

	def __contains__(self, key):
		if self._entry(key) is None:
			return False
		else:
			return True

	def __iter__(self):
		return (e.key for e in self._entries)

	def values(self):
		return (e.value for e in self._entries)

	def items(self):
		return ((e.key, e.value) for e in self._entries)

## Part 2
class HashMapping:
	def __init__(self, size = 1000):
		self._size = size
		self._buckets = [ListMapping() for i in range(self._size)]
		self._length = 0

	def __iter__(self):
		return (e.key for e in self._entryiter())

	def _entryiter(self):
		return (e for bucket in self._buckets for e in bucket._entryiter())

	def get(self, key):
		bucket = self._bucket(key)
		return bucket[key]

	def put(self, key, value):
		bucket = self._bucket(key)
		if key not in bucket:
			self._length += 1
		bucket[key] = value

	def __getitem__(self, key):
		return self.get(key)

	def __setitem__(self, key, value):
		return self.put(key, value)

	def items(self):
		return ((e.key, e.value) for e in self._entryiter())

	def __contains__(self, key):
		bucket = self._bucket(key)
		return key in bucket

	def __len__(self):
		return self._length

	def _bucket(self, key):
		return self._buckets[hash(key) % self._size]

	def statistics(self):
		totalBuckets = self._size
		print('Total number of buckets: ', totalBuckets)

		emptyBuckets = 0
		for e in self._buckets:
			if len(e) == 0:
				emptyBuckets += 1
		print('Number of empty buckets: ', emptyBuckets)

		largestBucket = 0
		for bucket in self._buckets:
			if len(bucket) > largestBucket:
				print(bucket)
				print(self._buckets)
				largestBucket = bucket
		print('Size of the largest bucket: ', largestBucket)

		AvgSZ = self._size / self._length
		print('Average size: ', AvgSZ)

		# Std Dev
		SDcount = 0
		for bucket in self._buckets:
			Var = (len(bucket._entries) - AvgSZ ** 2)
			SDcount += Var
		AvgSD = SDcount / totalBuckets
		StdDev = math.sqrt(AvgSD)
		print('Standard Deviation: ', )

		return (totalBuckets, emptyBuckets, largestBucket, AvgSZ, StdDev)

## Part 5
## Don't forget to inherit HashMapping!
class ExtendableHashMapping(HashMapping):
	def get(self, key):
		bucket = self._bucket(key)
		return bucket[key]

	def put(self, key, value):
		bucket = self._bucket(key)
		if key not in bucket:
			self._length += 1
		bucket[key] = value
		if self._length > self._size:
			self._double()

	def __getitem__(self, key):
		return self.get(key)

	def __setitem__(self, key, value):
		self.put(key, value)

	def _double(self):
		oldbuckets = self._buckets
		self._size *= 2
		self._buckets = [ListMapping() for i in range(self._size)]
		for bucket in oldbuckets:
			for key, value in bucket.items():
				m = self._bucket(key)
				m[key] = value

## Part 1
def getTokensFreq(file):
	f = open(file)
	txt = f.read()
	words = txt.split()
	count = {}
	for w in words:
		w = w.lower()
		if w in count:
			count[w] += 1
		else:
			count[w] = 1
	return count

def getMostFrequent(d, k):
	lstfreq = sorted(d.items(), key = operator.itemgetter(1), reverse = True)
	countMost = []
	for n in range(k):
		countMost.append(lstfreq(n))
	return countMout

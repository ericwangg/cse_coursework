import unittest, random, time
from pattern import *

class TestPattern(unittest.TestCase):
    def testfindMatch(self):
        pat = Pattern('abc')
        text = 'abbabcabc'
        self.assertEqual(pat.findMatch(text), 3)

    def testfindmatchwildcard(self):
        pat = Pattern('a*c', '*')
        text = 'aaaabbaac'
        self.assertEqual(pat.findMatch(text), 6)

    def testfindmatchotherwildcard(self):
        pat = Pattern('a?c', '?')
        text = 'aaaabbaac'
        self.assertEqual(pat.findMatch(text), 6)

    def testmisfindmatch(self):
        pat = Pattern('abc')
        text = 'abababab'
        self.assertEqual(pat.findMatch(text), -1)

    def testmisfindmatchwildcard(self):
        pat = Pattern('a*c', '*')
        text = 'aaaabbacb'
        self.assertEqual(pat.findMatch(text), -1)

    def testnomatchnowildcard(self):
        pat = Pattern('a*c')
        text = 'aaaabbaac'
        self.assertEqual(pat.findMatch(text), -1)

    def testlongexample(self):
        pat = Pattern('a' * 1000)
        text = 'b' * 1000 + 'a' * 10000 + 'c' * 1000
        self.assertEqual(pat.findMatch(text), 1000)

    def testfindmatchcasesensitive(self):
        pat = Pattern("abc")
        text = 'ABCababcabababc'
        pat._set_case_sensitive(True)
        self.assertEqual(pat.findMatch(text), 5)


    ## test findMatches
    def testfindMatches(self):
        pat = Pattern('iss')
        text = 'mississippi'
        self.assertEqual(pat.findMatches(text), [1, 4])

    def testfindmatcheswildcard(self):
        pat = Pattern('i**', '*')
        text = 'mississippi'
        self.assertEqual(pat.findMatches(text), [1, 4, 7])

    def testfindmatchesotherwildcard(self):
        pat = Pattern('si?', '?')
        text = 'mississippi'
        self.assertEqual(pat.findMatches(text), [3, 6])

    def testmisfindmatches(self):
        pat = Pattern('isi')
        text = 'mississippi'
        self.assertEqual(pat.findMatches(text), [])

    def testmisfindmatcheswildcard(self):
        pat = Pattern('a*c', '*')
        text = 'aaaabbacb'
        self.assertEqual(pat.findMatches(text), [])

    def testnofindmatchesmatchnowildcard(self):
        pat = Pattern('a*c')
        text = 'aaaabbaac'
        self.assertEqual(pat.findMatches(text), [])

    def testfindmatchescasesensitive(self):
        pat = Pattern("abc")
        text = 'ABCababcabababc'
        pat._set_case_sensitive(True)
        self.assertEqual(pat.findMatches(text), [5, 12])

    #Time complexity tests
    def testtimeonepatternanyindex(self):
        testedPattern = Pattern('a' * 1000)

        # Take the 1000 characters for a string and place them anywhere
        randPos = random.randrange(0,1999000)
        reallyLong = 'x' * randPos
        reallyLong += 'a' * 1000
        reallyLong += 'x' * (2000000 - (randPos + 1000))
        self.assertEqual(len(reallyLong),2000000)

        # These units of time are in seconds. They are also
        # given to variable as floating point integers.
        starttime = time.time()
        self.assertEqual(testedPattern.findMatches(reallyLong), [randPos])
        self.assertTrue(time.time() - starttime < 3)

    def testtimeonewildcardanyindex(self):
        # There will be 999 chracters of a and one k randomly
        # placed in the string.
        randomWildCard = chr(random.randrange(98,120))
        randWildPos = random.randrange(0,1000)
        stringWithWild = ['a' for i in range(0,1000)]
        stringWithWild[randWildPos] = randomWildCard
        stringWithWild = "".join(stringWithWild)
        testedPattern = Pattern(stringWithWild, randomWildCard)

        # Take the 1000 characters for a string and place them anywhere
        # There is also a random wild card used in this test
        randPos = random.randrange(0,1999000)
        reallyLong = 'x' * randPos
        reallyLong += stringWithWild
        reallyLong += 'x' * (2000000 - (randPos + 1000))

        # Same as before. However now they have to check for the wildcards as well
        starttime = time.time()
        self.assertEqual(testedPattern.findMatches(reallyLong), [randPos])
        self.assertTrue(time.time() - starttime < 3)

if __name__ == '__main__':
    unittest.main()

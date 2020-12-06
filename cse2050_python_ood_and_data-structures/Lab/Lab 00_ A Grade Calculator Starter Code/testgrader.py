import unittest
from grader import assigngrade, average, droplowest

class TestGrader(unittest.TestCase):
    def testassigngradeA(self):
        self.assertEqual(assigngrade(95), 'A')
        self.assertEqual(assigngrade(95.1), 'A')
        self.assertEqual(assigngrade(90), 'A')
        self.assertNotEqual(assigngrade(89.9), 'A')

    def testassigngradeB(self):
        self.assertEqual(assigngrade(89), 'B')
        self.assertEqual(assigngrade(80), 'B')
        self.assertEqual(assigngrade(80.001), 'B')
        self.assertNotEqual(assigngrade(79.999), 'B')

    def testassigngrades(self):
        examples = [(0, 'F'), (65, 'D'), (70, 'C'), (80, 'B'), (90, 'A')]
        for score, grade in examples:
            self.assertEqual(assigngrade(score), grade)

    def testassigngradescustom(self):
        grades = ['Pass', 'Fail', 'Srsly?']
        cutoffs = [60, 7, 0]
        self.assertEqual(assigngrade(59, grades, cutoffs), 'Fail')
        self.assertEqual(assigngrade(7, grades, cutoffs), 'Fail')
        self.assertEqual(assigngrade(60, grades, cutoffs), 'Pass')
        self.assertEqual(assigngrade(59.99, grades, cutoffs), 'Fail')
        self.assertEqual(assigngrade(61, grades, cutoffs), 'Pass')
        self.assertEqual(assigngrade(1, grades, cutoffs), 'Srsly?')
        self.assertEqual(assigngrade(0, grades, cutoffs), 'Srsly?')

    def testaverage(self):
        self.assertEqual(average([2, 3, 4]), 3)
        self.assertEqual(average([2, 3, 4]), 3.0)
        self.assertEqual(average([0, 0, 15]), 5.0)

    def testaveragewithnonintegeroutput(self):
        self.assertEqual(average([0, 0, 0, 6]), 1.50)
        self.assertEqual(average([5, 4, 3, 2, 1, 5, 1, 5]), 3.25)

    def testaveragewithnonintegerinput(self):
        self.assertEqual(average([0, 0, 0, 7.5, 0]), 1.50)
        self.assertEqual(average([5, 4, 3, 2, 1, 5, 1, 5, 3.25]), 3.25)

    def testdroplowest(self):
        L = [3,1,5,2,4]
        droplowest(L)
        self.assertEqual(L, [3,5,2,4])
        droplowest(L)
        self.assertEqual(L, [3,5,4])
        droplowest(L)
        self.assertEqual(L, [5,4])
        droplowest(L)
        self.assertEqual(L, [5])
        droplowest(L)
        self.assertEqual(L, [])

    def testdroplowestwithduplicates(self):
        L = [2,2,1,1,2,1,2]
        droplowest(L)
        self.assertEqual(len(L), 6)
        droplowest(L)
        droplowest(L)
        self.assertEqual(L, [2,2,2,2])

if __name__ == '__main__':
    unittest.main()

import unittest
from cipher import *

class TestCipher(unittest.TestCase):
	## test string operation
	def testdecodestring(self):
		codestring = ("BCDEFGHIJKLMNOPQRSTUVWXYZA-")
		self.assertEqual(decode_string(codestring, "CDE"), "BCD")
		self.assertEqual(decode_string(codestring, "ZZZAB"), "YYYZA")
		self.assertNotEqual(decode_string(codestring, "ABC"), "ABC")

	def testdecodestringwithextras(self):
		codestring = ("JMBCYEKLFDGUVWHINXRTOSPZQA-")
		self.assertEqual(decode_string(codestring, "JMB,-CY::"), "ABC, DE::")
		self.assertEqual(decode_string(codestring, "---APS#$!"), "   ZWV#$!")
		self.assertEqual(decode_string(codestring, "1234567..."), "1234567...")

	def testdecodestringwithlowercase(self):
		codestring = ("JMBCYEKLFDGUVWHINXRTOSPZQA-")
		self.assertEqual(decode_string(codestring, "jMb,-cy::"), "ABC, DE::")
		self.assertEqual(decode_string(codestring, "---Aps#$!"), "   ZWV#$!")

	def testencodestring(self):
		codestring = ("BCDEFGHIJKLMNOPQRSTUVWXYZA-")
		self.assertEqual(encode_string(codestring, "DEF"), "EFG")
		self.assertEqual(encode_string(codestring, "AAAB"), "BBBC")
		self.assertNotEqual(encode_string(codestring, "ABC"), "ABC")

	def testencodestringwithlowercase(self):
		codestring = ("JMBCYEKLFDGUVWHINXRTOSPZQA-")
		self.assertEqual(encode_string(codestring, "Abc, De::"), "JMB,-CY::")
		self.assertEqual(encode_string(codestring, "   zwv#$!"), "---APS#$!")
		self.assertNotEqual(encode_string(codestring, "   APS#$!"), "---APS#$!")

	def testencodestringwithextras(self):
		codestring = ("JMBCYEKLFDGUVWHINXRTOSPZQA-")
		self.assertEqual(encode_string(codestring, "ABC, DE::"), "JMB,-CY::")
		self.assertEqual(encode_string(codestring, "   ZWV#$!"), "---APS#$!")
		self.assertEqual(encode_string(codestring, "1234567..."), "1234567...")

if __name__ == '__main__':
    unittest.main()

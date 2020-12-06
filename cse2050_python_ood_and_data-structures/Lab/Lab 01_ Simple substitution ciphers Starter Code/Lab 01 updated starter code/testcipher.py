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

	def testdecodelist(self):
		codestring = ("BCDEFGHIJKLMNOPQRSTUVWXYZA")
		self.assertEqual(decode_list(create_dlist(codestring), "CDE"), "BCD")
		self.assertEqual(decode_list(create_dlist(codestring), "ZZZAB"), "YYYZA")
		self.assertNotEqual(decode_list(create_dlist(codestring), "ABC"), "ABC")

	def testdecodelistwithextras(self):
		codestring = ("JMBCYEKLFDGUVWHINXRTOSPZQA")
		self.assertEqual(decode_list(create_dlist(codestring), "JMB,-CY::"), "ABC, DE::")
		self.assertEqual(decode_list(create_dlist(codestring), "---APS#$!"), "   ZWV#$!")
		self.assertEqual(decode_list(create_dlist(codestring), "1234567..."), "1234567...")

	def testdecodelistwithlowercase(self):
		codestring = ("JMBCYEKLFDGUVWHINXRTOSPZQA")
		self.assertEqual(decode_list(create_dlist(codestring), "jMb,-cy::"), "ABC, DE::")
		self.assertEqual(decode_list(create_dlist(codestring), "---Aps#$!"), "   ZWV#$!")

	def testencodelist(self):
		codestring = ("BCDEFGHIJKLMNOPQRSTUVWXYZA")
		self.assertEqual(encode_list(create_elist(codestring), "DEF"), "EFG")
		self.assertEqual(encode_list(create_elist(codestring), "AAAB"), "BBBC")
		self.assertNotEqual(encode_list(create_elist(codestring), "ABC"), "ABC")

	def testencodelistwithlowercase(self):
		codestring = ("JMBCYEKLFDGUVWHINXRTOSPZQA")
		self.assertEqual(encode_list(create_elist(codestring), "Abc, De::"), "JMB,-CY::")
		self.assertEqual(encode_list(create_elist(codestring), "   zwv#$!"), "---APS#$!")
		self.assertNotEqual(encode_list(create_elist(codestring), "   APS#$!"), "---APS#$!")

	def testencodelistwithextras(self):
		codestring = ("JMBCYEKLFDGUVWHINXRTOSPZQA")
		self.assertEqual(encode_list(create_elist(codestring), "ABC, DE::"), "JMB,-CY::")
		self.assertEqual(encode_list(create_elist(codestring), "   ZWV#$!"), "---APS#$!")
		self.assertEqual(encode_list(create_elist(codestring), "1234567..."), "1234567...")

	## test dictionary operation
	def testcreateedict(self):
		codestring1 = "JMBCYEKLFDGUVWHINXRTOSPZQA-"
		codestring2 = "HIJKLMNOPQRSTUVWXYZABCDEFG-"
		codestring3 = "JKQRSTUVWXYZABCDEFGLMNOPHI-"
		edict1 = {'A': 'J', 'B': 'M', 'C': 'B', 'D': 'C', 'E': 'Y', 'F': 'E', 'G': 'K', 'H': 'L', 'I': 'F', 'J': 'D', 'K': 'G', 'L': 'U', 'M': 'V', 'N': 'W', 'O': 'H', 'P': 'I', 'Q': 'N', 'R': 'X', 'S': 'R', 'T': 'T', 'U': 'O', 'V': 'S', 'W': 'P', 'X': 'Z', 'Y': 'Q', 'Z': 'A', ' ': '-'}
		edict2 = {'A': 'H', 'B': 'I', 'C': 'J', 'D': 'K', 'E': 'L', 'F': 'M', 'G': 'N', 'H': 'O', 'I': 'P', 'J': 'Q', 'K': 'R', 'L': 'S', 'M': 'T', 'N': 'U', 'O': 'V', 'P': 'W', 'Q': 'X', 'R': 'Y', 'S': 'Z', 'T': 'A', 'U': 'B', 'V': 'C', 'W': 'D', 'X': 'E', 'Y': 'F', 'Z': 'G', ' ': '-'}
		edict3 = {'A': 'J', 'B': 'K', 'C': 'Q', 'D': 'R', 'E': 'S', 'F': 'T', 'G': 'U', 'H': 'V', 'I': 'W', 'J': 'X', 'K': 'Y', 'L': 'Z', 'M': 'A', 'N': 'B', 'O': 'C', 'P': 'D', 'Q': 'E', 'R': 'F', 'S': 'G', 'T': 'L', 'U': 'M', 'V': 'N', 'W': 'O', 'X': 'P', 'Y': 'H', 'Z': 'I', ' ': '-'}
		self.assertEqual(create_edict(codestring1), edict1)
		self.assertEqual(create_edict(codestring2), edict2)
		self.assertEqual(create_edict(codestring3), edict3)

	def testcreateddict(self):
		codestring1 = "JMBCYEKLFDGUVWHINXRTOSPZQA-"
		codestring2 = "HIJKLMNOPQRSTUVWXYZABCDEFG-"
		codestring3 = "JKQRSTUVWXYZABCDEFGLMNOPHI-"
		d_dict1 = {'J': 'A', 'M': 'B', 'B': 'C', 'C': 'D', 'Y': 'E', 'E': 'F', 'K': 'G', 'L': 'H', 'F': 'I', 'D': 'J', 'G': 'K', 'U': 'L', 'V': 'M', 'W': 'N', 'H': 'O', 'I': 'P', 'N': 'Q', 'X': 'R', 'R': 'S', 'T': 'T', 'O': 'U', 'S': 'V', 'P': 'W', 'Z': 'X', 'Q': 'Y', 'A': 'Z', '-': ' '}
		d_dict2 = {'H': 'A', 'I': 'B', 'J': 'C', 'K': 'D', 'L': 'E', 'M': 'F', 'N': 'G', 'O': 'H', 'P': 'I', 'Q': 'J', 'R': 'K', 'S': 'L', 'T': 'M', 'U': 'N', 'V': 'O', 'W': 'P', 'X': 'Q', 'Y': 'R', 'Z': 'S', 'A': 'T', 'B': 'U', 'C': 'V', 'D': 'W', 'E': 'X', 'F': 'Y', 'G': 'Z', '-': ' '}
		d_dict3 = {'J': 'A', 'K': 'B', 'Q': 'C', 'R': 'D', 'S': 'E', 'T': 'F', 'U': 'G', 'V': 'H', 'W': 'I', 'X': 'J', 'Y': 'K', 'Z': 'L', 'A': 'M', 'B': 'N', 'C': 'O', 'D': 'P', 'E': 'Q', 'F': 'R', 'G': 'S', 'L': 'T', 'M': 'U', 'N': 'V', 'O': 'W', 'P': 'X', 'H': 'Y', 'I': 'Z', '-': ' '}
		self.assertEqual(create_ddict(codestring1), d_dict1)
		self.assertEqual(create_ddict(codestring2), d_dict2)
		self.assertEqual(create_ddict(codestring3), d_dict3)

	def testdecodedict(self):
		codestring = "BCDEFGHIJKLMNOPQRSTUVWXYZA-"
		self.assertEqual(decode_dictionary(create_ddict(codestring), "CDE"), "BCD")
		self.assertEqual(decode_dictionary(create_ddict(codestring), "ZZZAB"), "YYYZA")
		self.assertNotEqual(decode_dictionary(create_ddict(codestring), "ABC"), "ABC")

	def testdecodedictwithextras(self):
		codestring = ("JMBCYEKLFDGUVWHINXRTOSPZQA-")
		self.assertEqual(decode_dictionary(create_ddict(codestring), "JMB,-CY::"), "ABC, DE::")
		self.assertEqual(decode_dictionary(create_ddict(codestring), "---APS#$!"), "   ZWV#$!")
		self.assertEqual(decode_dictionary(create_ddict(codestring), "1234567..."), "1234567...")

	def testdecodedictwithlowercase(self):
		codestring = ("JMBCYEKLFDGUVWHINXRTOSPZQA-")
		self.assertEqual(decode_dictionary(create_ddict(codestring), "jMb,-cy::"), "ABC, DE::")
		self.assertEqual(decode_dictionary(create_ddict(codestring), "---Aps#$!"), "   ZWV#$!")

	def testencodedict(self):
		codestring = ("BCDEFGHIJKLMNOPQRSTUVWXYZA-")
		self.assertEqual(encode_dictionary(create_edict(codestring), "DEF"), "EFG")
		self.assertEqual(encode_dictionary(create_edict(codestring), "AAAB"), "BBBC")
		self.assertNotEqual(encode_dictionary(create_edict(codestring), "ABC"), "ABC")

	def testencodedictwithlowercase(self):
		codestring = ("JMBCYEKLFDGUVWHINXRTOSPZQA-")
		self.assertEqual(encode_dictionary(create_edict(codestring), "Abc, De::"), "JMB,-CY::")
		self.assertEqual(encode_dictionary(create_edict(codestring), "   zwv#$!"), "---APS#$!")
		self.assertNotEqual(encode_dictionary(create_edict(codestring), "   APS#$!"), "---APS#$!")

	def testencodedictwithextras(self):
		codestring = ("JMBCYEKLFDGUVWHINXRTOSPZQA-")
		self.assertEqual(encode_dictionary(create_edict(codestring), "ABC, DE::"), "JMB,-CY::")
		self.assertEqual(encode_dictionary(create_edict(codestring), "   ZWV#$!"), "---APS#$!")
		self.assertEqual(encode_dictionary(create_edict(codestring), "1234567..."), "1234567...")

if __name__ == '__main__':
    unittest.main()

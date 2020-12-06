alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
codestring = ("JMBCYEKLFDGUVWHINXRTOSPZQA-")
plaintext = "---APS#$!"
plaintext = "ZZZAB"

## encode and decode functions using string operations
def encode_string(codestring, plaintext):
	ciphertext = ""
	for char in plaintext:
		char = char.upper()
		if char in codestring:
			ciphertext = ciphertext + codestring[alphabet.index(char)]
		elif char == " ":
			ciphertext = ciphertext + "-"
		else:
			ciphertext = ciphertext + char
	return ciphertext

def decode_string(codestring, ciphertext):
	plaintext = ""
	for char in ciphertext:
		char = char.upper()
		if char in codestring:
			plaintext = plaintext + alphabet[codestring.index(char)]
		elif char == "-":
			plaintext = plaintext + " "
		else:
			plaintext = plaintext + char
	return plaintext

### encode and decode functions for lists
# creating e+list and d_list

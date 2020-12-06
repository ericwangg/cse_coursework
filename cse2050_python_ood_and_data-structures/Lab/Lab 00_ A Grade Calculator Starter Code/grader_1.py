alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
codestring = ("JMBCYEKLFDGUVWHINXRTOSPZQA-")
plaintext = "---APS#$!"
plaintext = "ZZZAB"
## ----------------------------------------------------------------------------------------
## encode and decode functions using string operations - write here what you did in the lab
## ----------------------------------------------------------------------------------------
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

## -----------------------------------------------------------------------------------------
## encode and decode functions using lists
## -----------------------------------------------------------------------------------------
alphabet = "ABCDE"
codestring = "CDEAB"

def create_elist(codestring):
	e_list = []
	for char in codestring:
		e_list.append(char)

def create_dlist(codestring):
	d_list = []
	for char in alphabet:
		d_list.append(char)

def encode_list(e_list, plaintext):
	ciphertext = []
	for char in plaintext:
		char = char.upper()
		if char in e_list:
			ciphertext = ciphertext + codestring[alphabet.index(char)]
		elif char == [-]

		else:
			ciphertext = ciphertext + char
	return ciphertext

def decode_list(d_list, ciphertext):
	pass

## -----------------------------------------------------------------------------------------
## encode and decode functions using dictionaries
## -----------------------------------------------------------------------------------------
def create_edict(codestring):
	pass

def create_ddict(codestring):
	pass

def encode_dictionary(e_dict, plaintext):
	pass

def decode_dictionary(d_dict, ciphertext):
	pass

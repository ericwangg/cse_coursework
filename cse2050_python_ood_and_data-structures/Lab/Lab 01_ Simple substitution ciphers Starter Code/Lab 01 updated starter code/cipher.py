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

def create_elist(codestring):
	e_list = [char for char in codestring]
	return e_list

def create_dlist(codestring):
	d_list = [alphabet[codestring.index(char)] for char in alphabet if char in codestring]
	return d_list

# Working d_list
# d_list = [a[c.index(x) for x in a]]

def encode_list(e_list, plaintext):
	list = []
	for char in plaintext:
		char = char.upper()
		if char in e_list:
			num = alphabet.index(char)
			list.append(e_list[num])
		elif char == " ":
			list.append("-")
		else:
			list.append(char)
	codestring = "".join(list)
	return codestring

def decode_list(d_list, ciphertext):
	list = []
	for char in ciphertext:
		char = char.upper()
		if char in d_list:
			list.append(d_list[alphabet.index(char)])
		elif char == "-":
			list.append(" ")
		else:
			list.append(char)
	plainstring = "".join(list)
	return plainstring

## -----------------------------------------------------------------------------------------
## encode and decode functions using dictionaries
## -----------------------------------------------------------------------------------------
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
codestring = ("JMBCYEKLFDGUVWHINXRTOSPZQA-")

def create_edict(codestring):
	e_dict = {}
	for char in codestring:
		e_dict[alphabet[codestring.index(char)]] = char
	return e_dict

def create_ddict(codestring):
	d_dict = {}
	for char in codestring:
		d_dict[char] = alphabet[codestring.index(char)]
	return d_dict

def encode_dictionary(e_dict, plaintext):
	ciphertext = ""
	for char in plaintext:
		char = char.upper()
		if char in e_dict:
			ciphertext = ciphertext + e_dict[char]
		elif char == " ":
			ciphertext = ciphertext + "-"
		else:
			ciphertext = ciphertext + char
	return ciphertext

def decode_dictionary(d_dict, ciphertext):
	plaintext = ""
	for char in ciphertext:
		char = char.upper()
		if char == "-":
			plaintext = plaintext + " "
		elif char in d_dict:
			plaintext = plaintext + d_dict[char]
		else:
			plaintext = plaintext + char
	return plaintext

#	CSE3666 Lab 2

	.data		#data segment

        # The next variable (symbol) should starts at an address that is a multiple of 4.
        # define a single word and an array of words.
	.align 2
w:	.word 0x41424344
warray:	.word 0x5678ABCD, -112, 0xC5E03666, 4, 5, 6, 7, 8

        # Just reserve 128 bytes space for a variable (array). Not initialized.
        # you can use it as an array of words, halwords, or bytes.
        # we will use it as a word array.
	.align 2
buf:	.space 128

        # Define two ASCIIZ strings. 
        # asciiz with z means 0 (not character '0') is placed after the last character. 

	.align 2
        # Just a new line character
newline: .asciiz "\n"	        

	.align 2
        # Course number, lab number, and your name
name:	.asciiz "CSE3666: Lab 1: ERICWANG \n\n"

	.text				# Code segment
	.globl	main			# declare main to be global

main:	
	# load an address, which is a 32-bit value. 
	# la is a pseudo instruction. It is converted into two instructions.
	# See the real instructions in the text segment window after the code is assembled

	# load the address of string name in $a0, and use syscall 4 to print a null-terminated string
	# li is a pseudoinstruction that load an immediate in a register
	la	$a0, name
	li	$v0, 4
	syscall
	

	# copy two words in warray to buf
	# buf[0] = warray[0]
	# buf[1] = warray[1]
	la	$s0, warray	# EW: loads word array "warray" into $s0
	lw	$t0, 0($s0)	# EW: loads index "0" of warray at $s0
	la	$s1, buf	# EW: loads array "buf" into $a1
	sw	$t0, 0($s1)	# EW: copies $t0 value which is the 0th index of the warray into 0 index of buf
	
	#repeat the same process for buf[1]
	lw	$t0, 4($s0)	# EW: 4 is for the amount of bytes in a word, requires "conversion"
	sw	$t0, 4($s1)
	
	# Print warray[2] as an signed integer and an unsigned integer
	lw	$a0, 8($s0)	# EW: loads warray[2] into register $a0
	li	$v0, 1		# EW: prints the integer within warray[2]
	syscall
	
	la	$a0, newline	# EW: loads newline character
	li	$v0, 4		# EW: prints the newline character string
	syscall
	# add	$a1, $0, $zero
	lw	$a0, 8($s0)	# EW: load warray[2] again
	li	$v0, 36		# EW: prints the warray[2] as unsigned integer
	syscall
	
	la	$a0, newline	
	li	$v0, 4		# EW: print newline again
	syscall
	
	
	# Print the word located at name in hexadecimal
	lw	$a0, name	# EW: loads word located at "name"
	li	$v0, 34		# EW: prints the integer in hexadecimal form
	syscall

	# System call, type 10, standard exit
Exit:	addi	$v0, $0, 10	
	syscall
	
# Answer the following questions. Remember to make your 
#
# Example: What is the address of w in hexadecimal and decimal?
# Answer: 0x10010000 268500992
#
# Q1: What is the address of buf in hexadecimal and decimal?
# A1: 0x10010024  268501028
#
# Q2: What is the value of warray[0] in decimal?
# A2: 145074887
#
# Q3: What is the value of warray[1] in hexadecimal?
# A3: 0xffffff90
#
# Q4: What is the address of warray[2] in hexadecimal and decimal?
# A4: 0x5e03666 -975161754
#
# Q5: What is the address of name in hexadecimal and decimal?
# A5: 0x100100a8  268501160
#
# Q6: Find the string name in data segment window. Toggle the checkbox for ASCII option. 
#     Observe how bytes are displayed as words in the data segment window.
#     Does the simulator work in big endian mode or littel endian mode?
# A6: The simulator works in Big endian mode

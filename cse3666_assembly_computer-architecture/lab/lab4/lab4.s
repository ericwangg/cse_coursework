################################ data segment
	.data
name:	.asciiz "CSE3666: Lab 4: ERICWANG (erw16108)\n\n"
str:    .space 128

################################ code segment
	.text
	.globl	main		# declare main to be global

main: 
	la	$a0, name	# load the address of "name" into $a0
	li	$v0, 4		# system call, type 4, print an string
	syscall			# system call

main_loop:
	# use a system call to read a string into str
	la	$a0, str	# EW: string char c
	li	$a1, 128	# EW: reads s
	li	$v0, 8		# EW: syscall, type 8, read string
	syscall

	# TODO
	# call strtoupper
	jal	strtoupper	# EW: jump and link the recursion
	beq	$t0, $0, Exit	# EW: if the $t0 byte == 0, Exit
	beq	$t0, 10, Exit	# EW: if the $t0 byte == '\n', Exit
	# EW: performing bottom control to avoid an extra first loop
	# EW: per 9/24/19 lecture
	
	# EW: We wouldn't have misloop since $t0 is initialized within strtoupper and 
	# EW: any character that isn't recognized is sumply skipped in strtoupper_skip
	
	# print the returned string
	la	$a0, str	# EW: 
	li	$v0, 4		# EW: syscall, type 4, print string
	syscall
	
	# if str[0] is '\n' or 0, exit from the loop. 
	# Goto main_loop otherwise.tst
	
Exit:	
	# print the returned string
	la	$a0, str	# EW: 
	li	$v0, 4		# EW: syscall, type 4, print string
	syscall
	
	li	$v0, 10		# System call, type 10, standard exit
	syscall			# ...and call the OS

# TODO
# your implementation of strtoupper
strtoupper: 
	# sub	$sp, $sp, 32	# 128 bit = 2^8 = require 8 registers saved
	# ^^^ ignore
	
	# EW: Creating an exit condition and skip none alphabet character conditions
	# EW: strtoupper_skip and strtroupper_exit resectively
	# Stack initialize
	addi	$sp, $sp, -8
	sw	$a0, 4($sp)	# push str in 
	sw	$ra, ($sp)	# push $ra into stack 
	
	# "second loop check" - crashed here the first t
	lb	$t0, ($a0)	# EW: load byte $a0 str into $t0
	beq	$t0, $0, strtoupper_exit	# another comparison of char == 0, then exit
	
	# shift chararacters through string 2 loops
	# if chargreater than "z"
	# ASCII: 122
	
	sgt	$t1, $t0, 122	# have to maintain $t0 as the lower case character of string
	beq	$t1, 1, strtoupper_skip	# $t1 is char > a
	add	$t1, $0, $0	# return this shift to 0
	
	# if char less than "a"
	# ASCII: 97
	slti	$t2, $t0, 97	# can't use slt??
	beq	$t2, 1, strtoupper_skip	# $t2 is a char < a
	add	$t2, $0, $0	# return this shift to 0	
	
	# Make char capital
	addi	$t0, $t0, -32	# EW: Make character capital, by ASCII -32
	sb	$t0, ($a0)	# EW: store byte to stack 
	
strtoupper_skip:
	addi	$a0, $a0, 1	# EW: adds increment of "1" character to str at $a0
	jal	strtoupper	# EW: post skip jump and link back to strtoupper loop
	
strtoupper_exit:
	addi	$sp, $sp, 8	# EW: push return address onto back onto stack
	lw	$ra, ($sp)
	lw	$a0, 4($sp)	# 
        jr 	$ra            	# EW: return to calling routine

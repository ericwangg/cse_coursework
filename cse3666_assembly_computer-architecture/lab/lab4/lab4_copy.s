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
	li	$a1, 128	# EW: reads string
	li	$v0, 8		# EW: syscall, type 8, read string
	syscall

	# TODO
	# call strtoupper
	li 	$t0, 0		# EW: load "0" into $t0 to compare
	bne 	$a0, $zero, strtoupper	
	# strtoupper:	# EW: if the string is equal to 0, base case exit
	
	# print the returned string
	la	$a0, str	# EW: 
	li	$v0, 4		# EW: syscall, type 4, print string
	syscall

	# if str[0] is '\n' or 0, exit from the loop. 
	# Goto main_loop otherwise.tst
	
Exit:	li	$v0, 10		# System call, type 10, standard exit
	syscall			# ...and call the OS

# TODO
# your implementation of strtoupper
strtoupper: 
	addi	$sp, $sp, -32	# EW: load stack with 8 words allocations
	sw	$ra, 0($sp)	# use $ra as first register
	sw	$s0, 4($sp)	# use saved registers $s0 and on
	sw	$s1, 8($sp)
	sw	$s2, 12($sp)
	sw	$s3, 16($sp)
	sw	$s4, 20($sp)
	sw	$s5, 24($sp)	
	sw	$s6, 28($sp)	# last push in stack
	
strtoupper_exit:
	#addi	$a1, $a1, 1	# (s + 1)
	
        lw	$s6, 28($sp)	# EW: begin pop of entire stack to return capitalized words
	lw	$s5, 24($sp)
	lw	$s4, 20($sp)
	lw	$s3, 16($sp)
	lw	$s2, 12($sp)
	lw	$s1, 8($sp)
	lw	$s0, 4($sp)
	lw	$ra, 0($sp)	# last pop with $ra
	addi	$sp, $sp, 32	# EW: push return address onto back onto stack
        jr 	$ra            	# EW: return to calling routine

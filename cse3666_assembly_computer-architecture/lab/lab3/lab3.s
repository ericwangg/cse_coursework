################################ data segment
	.data
name:	.asciiz "CSE3666: Lab 3: ERIC WANG (erw16108)\n\n"
nl:	.asciiz "\n"

# set alignment for words. 
# Use 5 here so you can find the array in the data segment easily
	.align 5
buffer:	.space 4096		# allocate space for 1K words

################################ code segment
	.text
	.globl	main		# declare main to be global

main: 
        # specify the size of the array, must be less than 1024
	la	$s0, buffer	# address of the buffer in $s0
	li	$s1, 1024       # number of elements in $s1

	la	$a0, name	# load the address of "name" into $a0
	li	$v0, 4		# system call, type 4, print an string
	syscall			# system call

	# call init_array() to initialize the array with random values
	move	$a0, $s0	# use pseudoinstructions
	move	$a1, $s1
	jal	init_array	
	

	# TODO
	# call your find_max function with proper arguments
	move	$a0, $s0
	move 	$a1, $s1	
	jal	max_abs		# using psuedo instruction jal
	

	# print the returned value
	add	$a0, $0, $v0	# 
	li	$v0, 1		# integer print
	syscall
	
	# print the newline character
	la	$a0, nl		# newline
	li	$v0, 4		# character print
	syscall

Exit:	li	$v0,10		# System call, type 10, standard exit
	syscall			# ...and call the OS

# TODO
# your implementation of max_abs
max_abs:				#my implementation of max_abs
	addi	$v0, $0, -1		# $v0 the max value of interest
	li 	$t1, 0			#t1 is "i"
	j	max_test		#jump to loop test for max
	
max_loop:
	sll 	$t2, $t1, 2		# moves "i" to nex address
	add 	$t2, $t2, $a0		# buffer for correct address
	lw 	$t3, ($t2)		# load word into temp register 3
	
	
	slti	$at, $t3, 0		# set $at to 0, unless $t2, then set to 1
	beq	$at, $0, abs_skip	# don't skip next line if $at = 1 neg.
	sub	$t3, $0, $t3		# max negated "made abs."
	sw	$t3, ($t2)		# store word for neg. value
	
abs_skip:
	slt	$at, $v0, $t3		# if $t3 the new max., $at = 1
	beq	$at, $0, max_skip	# if t2 not the new max, sk
	move	$v0, $t3		# make new max
	
max_skip:
	addi	$t1, $t1, 1		# ++ action

max_test:
	slt	$at, $t1, $a1		#
	bne	$at, $0, max_loop	# if i < n, go to max_loop
	jr 	$ra			# if bne doesn't go to max_loop, then go to main

     
##### No need to change anything below
# void init_array(int *p, int n), or
# void init_array(int p[], int n) 
# use pseudorandom system calls in MARS
init_array:
	#save parameters
	addi	$t0, $a0, 0
	addi	$t1, $a1, 0

	# set the seed
	li	$a0, 0
	li	$a1, 3666
	li	$v0, 40
	syscall

	lui	$t2, 0x8000
	
	# A while loop to put random numbers in the array
	j	llinit_test

llinit_loop:
	li	$a0, 0			# syscall 41: rand()
	li	$v0, 41
	syscall
	
	# retry if the random number is 0x80000000
	beq	$a0, $t2, llinit_loop	

	sw	$a0, ($t0)		# save the random value
	addi	$t0, $t0, 4		# move to the next word
	addi	$t1, $t1, -1		# n --

llinit_test:
	slti	$at, $t1, 1		  # n < 1?
	beq	$at, $zero, llinit_loop   # if not, goto loop

	jr	$ra

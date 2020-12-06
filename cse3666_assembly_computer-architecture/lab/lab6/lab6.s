################################ data segment
	.data
name:	.asciiz "CSE3666: Lab 6: ERIC WANG (erw16108) \n\n"
errmsg: .asciiz "The number is too large.\n"
nl:	.asciiz "\n"
str:    .space 128

space:	.asciiz	" "	 #EW: defining space character

################################ code segment
	.text
	.globl	main		# declare main to be global

main: 
	la	$a0, name	# load the address of "name" into $a0
	li	$v0, 4		# system call, type 4, print an string
	syscall			# system call

main_loop:
	# use a system call to read a string into str
	la	$a0, str
	li	$a1, 128
	li	$v0, 8
	syscall

	# TODO
	# if str[0] is '\n' or 0, exit from the loop.
	lb	$t0, 0($a0)	#EW: loads first byte (character) of string into $t0 "also 0($a0)"
	beq	$t0, 0, Exit	#EW: if the $t0 byte == 0, Exit, using psuedo beqz vs beq and 0
	beq	$t0, 10, Exit	#EW: if the $t0 byte == '/n' , Exit
	
	# call myatoi(str)
	jal	myatoi			#EW: calling of myatoi
	bne	$v0, -1, no_error	#EW: if there no error, jump to no_error processing
				
	la	$a0, errmsg		#EW: otherwise stay and print error
	li	$v0, 4			#EW: $v0, 4 - print string for errmsg
	syscall
	j	main_loop		#EW: if therre is overflow, return to top of main loop, reloop
	
	# if the return value is the error code, print error message 
	# otherwise, print the return value in 3 formats
	
	
	
no_error:
	# print return value in three different formats, separated by a space.
	# syscall 11 can be used to print a character (e.g., a space, a new line).
	
	la	$a0, nl
	li	$v0, 4
	syscall
	
	#EW: first value - hexadecimal
	la	$a0, ($s1)	#EW: printing $s0, or v for post atoi value
	li	$v0, 34		#EW: 34 for hex
	syscall
	
	la	$a0, space
	li	$v0, 4
	syscall
	
	#EW: 2nd value - decimal unsigned
	la	$a0, ($s1)
	li	$v0, 36		#EW: 36 for unsigned in base 10
	syscall
	
	la	$a0, space
	li	$v0, 4
	syscall

	#EW: 3rd value - decimal signed	
	la	$a0, ($s1)
	li	$v0, 1		#EW: 1 for signed int base 10
	syscall
	
	la	$a0, nl
	li	$v0, 4
	syscall
	
	j	main_loop	# back to main loop
	
	
main_continue:
	b	main_loop
	
Exit:	li	$v0, 10		# System call, type 10, standard exit
	syscall			# ...and call the OS

# TODO
# your implementation of myatoi
myatoi: 		#EW: pre-loop intializers
	# add	$t1, $0, $0	#EW: initialize i = 0 to $t1
	addu 	$s1, $0, $0 	#EW: initialize v = 0 to $s2
	#add			#EW: put i in s[] "s[i]"	# must to inside loop to increment i
	#add	$t3, 		#EW: initialize c = s[i]	
	move 	$s0, $a0	#EW: moving address of string for func. use

myatoi_loop:
	lb	$t0, 0($s0)		#EW: 1st character in c, or c[i]
	blt	$t0, 48, my_exit	#EW: inverse of while loop, exit if c < 0
	bgt	$t0, 57, my_exit	#EW: c > 9
	
	addi	$t1, $zero, 10		# 10 + (c + '0')
	multu	$s1, $t1		# v * 10
	
	mfhi	$t2			#EW: move from high
	mflo	$s1			#EW: move from low 
	
	bne	$t2, $0, overflow	#EW: anything "Hi" in #t4 --> overflow
	subi	$t0, $t0, 48		#EW: char ASCII for hex??? 0 start at 48 so use this
	addu	$s4, $s1, $t0		#EW: add unsigned s[i] to c
	
	bltu	$s4, $s1, overflow	#EW: addition smaller than total --> overflow
	move	$s1, $s4		#EW: copy total from calcs. over to v
	
	add	$s0, $s0, 1		# increment i <-- issue here, didn't increment
					# doing i++ wrong essentially, not getting to next char
					# therefore, always analzying on first character until
					# length or something, and the end value is over the max
					
	j	myatoi_loop		#EW:  while loop in myatoi
	
overflow:
	addi	$v0, $0, -1		#EW: overflow return to caller jump
	jr	$ra		
	
my_exit:
        jr 	$ra                 # return to calling routine
   

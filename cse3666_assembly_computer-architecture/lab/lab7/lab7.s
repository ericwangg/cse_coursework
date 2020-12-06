################################ data segment
	.data
name:	.asciiz "CSE3666: Lab 7: ERICWANG (erw16108)\n\n"
nl:	.asciiz "\n"

	.align 2
fconst: .float	0.0, 1.0, 2.0
arr:    .float	0.1, 0.2, 0.3, 0.4, 0.5, 0.7853981, 1.570796, 3.1415927, 0.0

################################ code segment
	.text
	.globl	main		# declare main to be global

main: 
	la	$a0, name	# load the address of "name" into $a0
	li	$v0, 4		# system call, type 4, print an string
	syscall			# system call

	la	$s0, arr	
	li	$s1, 9		# the number of elements in the array
	sll	$s1, $s1, 2
	add	$s1, $s1, $s0

main_loop:
	# TODO
	# EW: once the array equals the # of elems. in the array, then exit
	beq	$s0, $s1, Exit
	jal 	sin
	
	li	$v0, 2		# EW: print float syscall code 2
	syscall		
	la	$a0, nl		# EW: print newline char
	li	$v0, 4
	syscall

	# for valid index i = 0, 1, ..., 
	# print sin(arr[i]), and nl
	
main_continue:
	addi	$s0, $s0, 4
	bne	$s0, $s1, main_loop
	
Exit:	li	$v0, 10		# System call, type 10, standard exit
	syscall			# ...and call the OS

# TODO
# your implementation of sin
sin: 
        # return x for now
        # EW: pre for loop initializations
        
        la	$s2, fconst	# EW: load address from fconst values 0.0, 1.0, 2.0
        l.s	$f0, 0($s2)	# EW: set 0.0 to $f0
        l.s	$f1, 4($s2)	# EW: set 1.0 to $f1
        l.s	$f2, 8($s2)	# EW: set 2.0 to $f2
        
        lwc1	$f7, 0($s0)	# EW: set x = arr[i] load into coprocessor 1
        
        add.s	$f5, $f1, $f0	# EW: sign = 1.0 (do 1.0 + 0.0)
        add.s	$f4, $f1, $f0	# EW: n = 1.0
        add.s	$f3, $f1, $f0	# EW: fact = 1.0
        
        add.s	$f6, $f7, $f0	# power = x
        add.s	$f12, $f7, $f0	# v = x
        
        addi	$t0, $0, 0	# intialize i = 0 for for loop
        
sin_loop:
	#beq	$t0, $t1, Exit
	
	# EW: power (old, wrong pi answer)
	# mul.s	$f8, $f7, $f7	# x * x ->
	# mul.s	$f6, $f6, $f8	# power *= x*x    or     power *= $f8 > $f7
	
	# EW: new power
	mul.s 	$f6, $f6, $f7	# power *= x
	mul.s 	$f6, $f6, $f7	# power *= x again
		
	# EW: fact
	add.s	$f9, $f4, $f1		# n + 1.0 > $f9
	add.s	$f10, $f4, $f2		# n + 2.0 > $f10
	mul.s	$f8, $f9, $f10	# $f8 now open after power use, (n + 1.0) * (n + 2.0) > $f11
	mul.s	$f3, $f3, $f8		# fact *= $f11
	
	# EW: n += 2.0
	add.s	$f4, $f4, $f2	# n += 2.0
	
	# sign
	neg.s	$f5, $f5	# sign = -sign
	
	# final line in for loop "v += ..."
	mul.s	$f9, $f3, $f5	# fact * sign 
	div.s	$f10, $f6, $f9	# power / fact * sign
	add.s 	$f12, $f12, $f10	# v += $f14
	
	#mul.s	$f9, $f6, $f4	#$f9 = factorial * sign
	#div.s	$f10, $f7, $f9	#$f10 = power / factorial * sign
	# add.s	$f8, $f8, $f10
	
	# for loop things
	addi	$t0, $t0, 1	# i++
	blt	$t0, 20, sin_loop	#if i < 20 still, keep for looping, otherwise return
					# bottom control vs. top statement beq to exit etc.
	# 	mov.s	$f0, $f12
        jr 	$ra                 # return
   

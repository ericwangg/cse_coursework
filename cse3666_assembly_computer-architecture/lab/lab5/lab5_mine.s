#	Lab 5
# Eric Wang, Kieran Clarke
#	Merge Sort

	.data			#data segment
	.align 2
buffer:	.space 4096		#allocate space for 1K words

	.align 2
name:	.asciiz "CSE3666: Lab 5: ERIC WANG, KIERAN CLARKE (erw16108)\n"

	.text			# Code segment
	.globl	main		# declare main to be global
main: 
        # specify the size of the array, must be less than 1024
	la	$s0, buffer	# address of the buffer in $s0
	li	$s1, 1024	# number of elements in $s1

	la	$a0, name	# load the address of "name" into $a0
	li	$v0, 4		# system call, type 4, print an string
	syscall			# system call

	# call init_array() to initialize the array with random values
	move	$a0, $s0	# use pseudoinstructions
	move	$a1, $s1
	jal	init_array	

	# check array
	move	$a0, $s0
	move	$a1, $s1
	jal	check_array

	# call merge_sort function with proper arguments
	move	$a0, $s0
	move	$a1, $s1
	jal	merge_sort 	# call merge_sort

	# check array
	move	$a0, $s0
	move	$a1, $s1
	jal	check_array

Exit:	li	$v0, 10		# System call, type 10, standard exit
	syscall			# ...and call the OS


##################################TODO#########################################
####START_OF_MERGE_SORT
###############################################################################
#######################void merge_sort(int p[], int n)
# TODO
merge_sort:
	# Start pushing registers into stack
	addi	$sp, $sp, -24		# EW: stack initialize
	
	move	$t0, $a1, 		# length of array --> $t0
	sll	$t0, $t0, 4		# multiply array elements by 4 --> $t0
	add	$a1, $a0, $t0		# store
	sw	$ra, 8($sp)
	sw	$a1, 4($sp)
	sw 	$a0, 0($sp)		# EW: stack pushes 
	
	sub	$t0, $a1, $a0		# the difference between start and end addresses
	ble	$t0, 4, ms_end		# if array = 1 item, send to end
	
	srl	$t0, $t0, 3		# $t0 = 4 * elements, divide by 8 to find half the elements
					# "n / 2"
	sll	$t0, $t0, 2		# multiply by 4 to have size of array
	add	$a1, $a0, $t0		# find split array address (n/2 address)
	sw	$a1, 12($sp)		# store this halfway address in stack for future use
	jal	merge_sort		# Bottom recursive call, first half will be split 
					# into individual array units ("single lists")
	
	lw	$a1, 8($sp)		# load end of array address from stack
	lw	$a0, 12($sp)		# load halfway array address from stack
	jal	merge_sort		# like first half, recursive call, split into individual 
					# element arrays 
	
	lw	$a0, 4($sp)		# load array start
	lw	$a1, 12($sp)		# load array mid
	lw	$a2, 8($sp)		# load array end
	jal	ms_merge		# merge two split halves
		
	jr	$ra
   
ms_end:
	lw	$ra, 0($sp)		# load to return address
	addi	$sp, $sp, 24		
	jr	$ra			# return to caller
	
ms_merge:
	addi	$sp, $sp, -16		# stack pointer initialize
	sw	$ra, 0($sp)		# save word - return address
	sw 	$a0, 4($sp)		# save word - start address
	sw	$ra, 8($sp)		# save word - midpoint address
	sw 	$a0, 12($sp)		# save word - end address
	
	move	$s0, $a0		# copy 1st half address
	move	$s1, $a1		# copy 2nd half address
	
ms_loop:				
	lw	$t0, 0($s0)		# save 1st half position pointer
	lw	$t1, 0($s1)		# save 2nd half position pointer
	lw	$t0, 0($t0)		# save 1st half position value
	lw	$t1, 0($t1)		# save 2nd half position value
	
	bgt	$t1, $t0, ms_skip	# skip if first value is already smaller
	
	move	$a0, $s1		# Load argument - element move
	move	$a1, $s0		# Load argument - address move
	jal	ms_shift		# Shift element to new position 
	
	addi	$s1, $s1, 4		# index of second half ++;
	
ms_skip:
	addi	$s0, $s0, 4		# index of first half ++;
	lw	$a2, 12($sp)		# load end address
	bge	$s0, $a2, ms_loopend	
	bge	$s1, $a2, ms_loopend	# both halves empty? end
	j 	ms_loop
	
ms_loopend:
	lw	$ra, 0($sp)		# load return address
	addi	$sp, $sp, 16		
	jr 	$ra			# return to caller
	
ms_shift:
	ble	$a0, $a1, ms_shiftend	# Stop when at location
	addi	$t6, $a0, -4		# Find previous address in array
	lw	$t7, 0($a0)		# Current pointer
	lw	$t8, 0($t6)		# Prev pointer
	sw	$t7, 0($t6)		# Save word - current pointer to prev address
	sw	$t8, 0($a0)		# Save word - prev pointer to current address
	move	$a0, $t6		# Shift current position back 
	j 	ms_shift		# loop itself
	
ms_shiftend:
	jr	$ra			# ending ms shift loop, return to caller
	
       
####END_OF_MERGE_SORT

# void copy_array(int dst[], int src[], int n)
# This funciton is a leaf function
copy_array:
	b	ll_copy_array_test	
	
ll_copy_array_loop:
	lw	$t0, ($a1)
	sw	$t0, ($a0)
	addi	$a2, $a2, -1
	addi	$a1, $a1, 4
	addi	$a0, $a0, 4

ll_copy_array_test:
	bne 	$a2, $0, ll_copy_array_loop
	jr	$ra

####END_OF_copy_array
###############################################################################

################################################################################
##### No need to change anything below
################################################################################
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
	
        .data   #data segment
        .align	2
ais_sum:.word   0
msg0:	.asciiz "Sorted\n"
msg1:	.asciiz "Not sorted\n"
msg2:	.asciiz "Error: data were corrupted.\n"
msg3:	.asciiz "Error: array length is less than 1.\n"

        .text

# void check_array(int p[], int n)
# return 0 if the array elements are in ascending order
# return a non-zero value if not sorted or other errors
# p is in $a0, n is in $a1
check_array:

	# if (n < 1) return 0
	slti	$at, $a1, 1
	bne	$at, $0, ll_ais_exit3

	# save sum in $t2	
	li	$t2, 0
	li	$v0, 0

	# load 	first word in $t0
	lw	$t0, ($a0)
	b	ll_ais_test

ll_ais_loop:
	lw	$t1, ($a0)
	
	slt 	$at, $t1, $t0	# if $t1 < $t0
	beq	$at, $0, ll_ais_skip

	li	$v0, 1		# not sorted

ll_ais_skip:
	move	$t0, $t1

ll_ais_test:
	xor	$t2, $t2, $t0
	addi	$a0, $a0, 4
	addi	$a1, $a1, -1
	bne	$a1, $0, ll_ais_loop   # if there are elements goto loop

	la	$t4, ais_sum
	lw	$t0, ($t4)
        sw      $t2, ($t4)
        
        beq	$t0, $0, ll_ais_sum_ok
        bne	$t0, $t2, ll_ais_exit2
        
ll_ais_sum_ok:
	beq	$v0, $0, ll_ais_exit0

ll_ais_exit1:	# return 1
	la	$a0, msg1
	li	$v0, 4
	syscall
	li	$v0, 1
	b	ll_ais_exit
	
ll_ais_exit2:	# return 2
	la	$a0, msg2
	li	$v0, 4
	syscall
	li	$v0, 2
	b	ll_ais_exit

ll_ais_exit3:	# return 3
	la	$a0, msg3
	li	$v0, 4
	syscall
	li	$v0, 3
	b	ll_ais_exit

ll_ais_exit0:	# return 0
	la	$a0, msg0
	li	$v0, 4
	syscall
	li	$v0, 0

ll_ais_exit:
	jr	$ra
#######################################################################

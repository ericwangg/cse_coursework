#include    <stdio.h>
#include    <stdlib.h>
#include    <string.h>
#include    <ctype.h>
#include    <assert.h>

#define     ARGV_STEP      16
#define     LINESIZE_STEP  32
#define     NEW_LINE       '\n'

#define     MIN_STACKSIZE     10

int     is_number(char *s);

enum ErrorNumber {ERR_OK, ERR_EMPTY, ERR_NOOPERANDS, ERR_NOMEM, ERR_END}; 

// print an error message by an error number, and return
// the function does not exit from the program
// the function does not return a value
void    error_message(enum ErrorNumber errno)
{
    char    *messages[] = {"OK", 
        "Stack is empty.",
        "Not enough operands.", 
        "Memory allocaton failed.", 
        "Invalid error number."};

    if (errno < 0 || errno >= ERR_END)
        errno = ERR_END;
    printf("rpn: %s\n", messages[errno]);
}

// struct for holding tokens from a line
typedef     struct {
    int     num_entries;
    int     argc;
    char ** argv;
} tokens_t;

void    init_tokens(tokens_t *t)
{
    // One way to initialize all members of a structure to 0
    tokens_t t0 = {0};

    // struct assignments
    *t = t0;
}

// get tokens from a line from stdin
// Return values:
// -1:  EOF or error 
// 0:   argc, and argv in line is set.
int     get_tokens(tokens_t *t)
{
    char    * line;
    size_t  line_size, line_len;
    int     ch;

    init_tokens(t);

    // initialize variables
    line = NULL;
    line_size = line_len = 0;

    // This is also an example showing how to realloc a block
    // if more space is needed. 
    do {
        ch = getchar();

        if (ch == EOF) {
            if (line) 
                free(line);
            return -1;
        }

        // append ch to line
        // if not enough space, realloc
        if (line_len + 2 > line_size) {
            line_size += LINESIZE_STEP;
            line = realloc(line, line_size * sizeof(char)); 
            if (line == NULL) {
                error_message(ERR_NOMEM);
                exit(1);
            }
            // you can check how line_size grows
            // printf("line_size=%lu,ch=%c\n", line_size, ch);
        }

        // there should be at least 2 bytes available
        // one for ch and one for NUL
        line[line_len ++] = ch; 
    } while (ch != NEW_LINE);

    // line should not be NULL. It has NEW_LINE at least.
    line[line_len] = '\0';  // put NUL at the end

    int argc = 0;

    char * pch;
    pch = strtok (line," \t\n");
    while (pch != NULL) {
        if (argc == t->num_entries) {
            t->argv = realloc(t->argv, (t->num_entries + ARGV_STEP)*sizeof(char *));
            if (t->argv == NULL) {
                // free(line);  going to exit anyway
                error_message(ERR_NOMEM);
                exit(1);
            }
            t->num_entries += ARGV_STEP;
        }
        // malloc() is done in strdup()
        t->argv[argc++] = strdup(pch);
        // printf ("%s\n",pch);
        pch = strtok (NULL, " \t\n");
    }
    t->argc = argc;
    free(line);
    return argc;
}

// free space in token
// Do not free(t) in this program
void    free_tokens(tokens_t *t)
{
    // TODO BEGIN
    for(int i = 0; i < t->argc; i++){
    	free(t -> argv[i]);			// for every array entry "i'"
    }								// free that argv location, (substrcture of t)
    free(t -> argv);				// then free argv in its entirety at the end
}

/*  stack_t  */
typedef struct {
    int     num_entries;
    int     sp;     // index of the number at the top. -1 for empty stack
    int     *stack;
} stack_t;

void    init_stack(stack_t * stack)
{
    stack->num_entries = 0;
    //when stack is empty, stack->sp should be -1.
    stack->sp = -1;
    stack->stack = NULL;
}

// return the numer of elements on the stack (not the number of entries)
int     stack_size(stack_t * stack)
{
    return stack->sp + 1;
}

//  Stack pop.
//  Parameters:
//  stack:  the stack
//  pn:     the location to store the value at the top of stack
//  Return values:
//  0:      the value is in *pn
//  -1:     stack is empty
int     stack_pop(stack_t *stack, int *pn)
{
    // TODO BEGIN
    // int sp = stack->sp;					// abbreviations
    // int stk = stack->stack;				
    // int nums = stack->num_entries;
    
    // if(sp < 0){								// array indexing error, change to less than 0...
    // 	error_message(ERR_EMPTY);			// vs. -1: Underflow: "Stack is empty. "
    // 	return -1;
    // }
    // else{
    // 	*pn = stack->stack[sp];				// *pn now the top of stack 
    // 	sp--;								// decrement stack pointer from pop
    // 	if (nums > 3*sp){
    // 		if(2*sp > MIN_STACKSIZE){
    // 		// shrink num entries if more tan 3x stack pointer
    // 		// and that 2x the stack pointer is more than min stack size
    // 			stk = realloc(stk, 2*4*sp);		// resize memory allocation
    // 			nums = 2*sp;					// shrink num entries
    // 		}
    // 		else{
    // 			stk = realloc(stk, 4*MIN_STACKSIZE);
    // 			nums = MIN_STACKSIZE;
    // 		}
    // 	}
    // }
    // return 0;		// successful pop
    
    // Take 2 - No abbrv. pop
    if (stack->sp < 0){
    	return -1;
    }
    else{
    	*pn = stack->stack[stack->sp];
    	stack->sp--;
    	if (stack->num_entries > 3*stack->sp){
    		if(2*stack->sp > MIN_STACKSIZE){
    			stack->stack = realloc(stack->stack, 2*4*stack->sp);
    			stack->num_entries = 2*stack->sp;
    		}
    		else{
    			stack->stack = realloc(stack->stack, 4*MIN_STACKSIZE);
    			stack->num_entries = MIN_STACKSIZE;
    		}
    	}
    }
    return 0;
}

//  Stack push
//  Parameters:
//  stack:  the stack
//  n:      the value to be pushed onto the stack
//  This function does not return a value    
void    stack_push(stack_t *stack, int n)
{
    // TODO BEGIN
    // int sp = stack->sp;					// stack pointer abbreviation
    // int stk = stack->stack;				// stack abbrv.
    // int nums = stack->num_entries;		// num_entries abbrv.
    
    // if (nums == stack_size(stack)){
    // 	if(nums*2 > MIN_STACKSIZE){
    // 		stk = realloc(stk, 2*4*nums);	// ex. nums = 20, stack size = 20, need to up it to 40
    // 		nums *= 2;						
    // 		// sp++;
    // 		// stack->stack[sp] = n;
    // 	}
    // 	else if(nums < MIN_STACKSIZE){
    // 		stk = realloc(stk, 4*MIN_STACKSIZE);
    // 		nums = MIN_STACKSIZE;
    // 		// sp++;
    // 		// stack->stack[sp] = n;
    // 	}
    // }
    // else{
    // 	// stk = realloc(stk, nums*4);	// reallocating memory for increased array size
    // }								// set num. entries to min. stack size
    // sp++;							// increment stack pointer
    // stack->stack[sp] = n;			// set top stack value to the integer "n" 
    
    
    //Take 2 - implement without abbreviation
    if(stack->num_entries == stack_size(stack)){
    	if(stack->num_entries*2 > MIN_STACKSIZE){
    		stack->stack = realloc(stack->stack, 2*4*stack->num_entries);
    		stack->num_entries *= 2;
    	}
    	else{
    		stack->stack = realloc(stack->stack, 4*MIN_STACKSIZE);
    		stack->num_entries = MIN_STACKSIZE;
    	}
    }
    stack->sp++;
    stack->stack[stack->sp] = n;
    
    
}

void    free_stack(stack_t * stack)
{
    if (stack->stack) {
        free(stack->stack);
        stack->stack = NULL;
    }
}

// print information about the stack
void    print_stack_info(stack_t * stack)
{
    printf("num_entries=%d\n", stack->num_entries);

    int sp = stack->sp;
    // int spv = stack->stack[sp];
    printf("sp=%d\n", sp);

    // print up to 5 numbers on the stack
    for (int i = 0; i < 5 && sp >= 0; i ++, sp --) {
        printf("stack[%d]=%d\n", sp, stack->stack[sp]);
    }
}

void    print_stack_top(stack_t * stack)
{
    // could have implemented a peek function
    if (stack_size(stack) < 1)
        error_message(ERR_EMPTY);
    else 
        printf("%d\n", stack->stack[stack->sp]); 
}

// perform different tasks by the token
// Return value:
// 0: continue
// 1: exit
int     process_tokens(stack_t * stack, tokens_t *t)
{
    for (int i=0; i < t->argc; i ++) {
        char *cur = t->argv[i];
        if (! strcmp(cur, "exit")) {
            return 1;
        }
        else if (! strcmp(cur, "info") || ! strcmp(cur, "i")) {
            print_stack_info(stack);
        }
        else if (! strcmp(cur, "p")) {
            print_stack_top(stack);
        }
        // deal with more commands or operators
        /*  You could handle each operator separatly. */
        else if (! strcmp(cur, "+") || ! strcmp(cur, "-") || ! strcmp(cur, "*")) {
            // process +, -, and *
            //     pop the correct number of operands off the stack
            //     perform the operation
            //     push the result onto the stack
            // All these operators require two operands
            // if there are not enough operands on the stack, 
            //     report error by calling error_message(ERR_NOOPERANDS);
            //     and continue to process the next token.
            //     the stack should not be changed. 
            // TODO BEGIN
                // if not enough operand tokens, report error_message(ERR_NOOPERANDS);
                

        	
        	// perform the respective 3 operations
        	if(stack->sp < 1){
        		error_message(ERR_NOOPERANDS);
        	}
        	else{
        		int ops1;		// initiate 2 variables to operate on for memory location of
            	int ops2;		// popped token values
            
        		stack_pop(stack, &ops1);		// use address in memory of where last value popped off
        		stack_pop(stack, &ops2);		// same for ops2 varaiable of 2nd pop off
	    		if(strcmp(cur, "+") == 0){
	        		int sum = ops1 + ops2;
	        		stack_push(stack, sum);
	        	}
	        	else if(strcmp(cur, "-") == 0){
	        		int sub = ops1 - ops2;
	        		stack_push(stack, sub);
	        	}
	        	else if(strcmp(cur, "*") == 0){
	        		int prod = ops1 * ops2;
	        		stack_push(stack, prod);
	        	}
        	}
        	// else if(stack_size(stack) < 1){
        	// 	error_message(ERR_NOOPERANDS);
        	//   }
        }
        // better to use strtol(). Example is in "man strtol"
        // you do not need to change it
        else if (is_number(cur)) {
            // do not deal with overflow.
            int v = atoi(cur);
            stack_push(stack, v);
        }
        else {
            printf("rpn: unknown token: %s\n", cur);
        }
    }
    return 0;
}

/* main */
int main(void)
{
    tokens_t t; 
    stack_t stack;
    int     flag = 0;    // exit if flag != 0

    init_stack(&stack);

    while (flag == 0 && get_tokens(&t) >= 0) {
        flag = process_tokens(&stack, &t);
        free_tokens(&t);
    }

    free_stack(&stack);
    return 0;
}

// check if a string is a decimal number
// could have a DFA, and recognize hex nubmers too 
int     is_number(char *s)
{
    // skip '+' or '-'
    if (*s == '+' || *s == '-'){
        s ++;
    }
    // the rest must be digits

    // if empty, not a number
    if (! *s){
        return 0;
    }
    while (isdigit(*s)) {
        s ++;
    }

    // could do return (! *s);
    if (*s){
        return 0;
    }
    return 1;
}

#include    <stdio.h>
#include    <stdlib.h>
#include    <string.h>
#include    <ctype.h>
#include    <assert.h>

/***** Search TODO to find the sections you need to work on ******/

/***** macros, function prototypes, and types ******/
#define     STACKSIZE_STEP      4
enum ErrorNumber {ERR_OK, ERR_EMPTY, ERR_NOMEM, ERR_END}; 

char  * get_line(void);
void    error_message(enum ErrorNumber errno);
void    check_pointer(void *p);

// define string stack type 
typedef struct {
    int     num_entries;
    int     sp;     // index of the element at the top. -1 for empty stack
    char    **stack;
} stack_t;

/***** functions on stack_t ******/

// initialze the stack pointed to by pstack. Set sp to -1 and clear members
// pstack must not be NULL.
void    init_stack(stack_t * pstack)
{
    if (pstack) {
        pstack->num_entries = 0;
        pstack->sp = -1;
        pstack->stack = NULL;
    }
}

// return the numer of elements on the stack (not the number of entries)
// stack must not be NULL.
int     stack_size(stack_t * pstack)
{
    return pstack->sp + 1;
}

// print information about the stack
// stack must not be NULL.
void    print_stack_info(stack_t * pstack)
{
    int sp = pstack->sp;

    printf("> num_entries:%3d  ", pstack->num_entries);
    printf("sp:%3d ", sp);

    // print top string on the stack
    // if sp is >= 0, pstack->stack must have at least one pointer
    if (sp >= 0) {
        printf("stack[%3d]:%s", sp, pstack->stack[sp]);
    }
    printf("\n");
}

/***** The section you need to work on starts here ******/  
/***** TODO ******/
//  Stack push
//  Parameters:
//  pstack: a pointer to the stack. Must not be NULL.
//  str:    a pointer to the string to be pushed onto the stack
//          the string is NOT duplicated in this function
//  This function does not return a value. 
void    stack_push(stack_t * pstack, char * s)
{
    // TODO Begin
}

//  Stack pop.
//  Parameters:
//  pstack: a pointer to the stack. Must not be NULL.
//  ps:     the location to store the top pointer
//          the string is NOT duplicated
//  Return values:
//  0:      the top pointer is saved in the location pointed to by ps
//  -1:     stack is empty
//  this function does not print any message
int     stack_pop(stack_t *pstack, char **ps)
{
    // TODO Begin
    return -1;
}

//  Stack free.
//      free memory used by strings on the stack (if any) and by the stack member for storing pointers
//      Do not free pstack as the structure may not be dynamically allocated
//  Parameters:
//      pstack: a pointer to a stack_t structure. Must not be NULL.
void    free_stack(stack_t * pstack)
{
    // TODO Begin
}

// process a line
// Parameters:
//   pstack: a pointer to a stack_t structure. Must not be NULL.
//   line: the string to be processed
// This function does not return a value
void    process_line(stack_t * pstack, char *line)
{
    if (! strcmp(line, "i")) {
        // display stack info
        print_stack_info(pstack);
    } else if (! strcmp(line, "p")) {
        // pop a pointer off the stack
        // if successful, print the string by calling printf("%s\n", s);
        // if not successful, print an error message by calling error_message(ERR_EMPTY);
        // think about how to prevent memory leaks
        char *s;     // a pointer to save the address of the string at the top
        // TODO Begin
    } else {
        // Add the string in line to stack. 
        // Duplicate line first and then call stack_push()
        // line is going to be freed outside of this function, if necessary
        // you could use malloc() and then strcpy(), instead of strdup()
        char *copy = strdup(line);
        check_pointer(copy);
        stack_push(pstack, copy);
    }
}

/***** Do not change code below ******/
void  hardcoded(stack_t * pstack, int nlines);

int main(int argc, char **argv)
{
    stack_t stack;

    init_stack(&stack);

    if (argc <= 1) {
        // if there is no argument, read from stdin
        char    *line;
        while ((line = get_line()) != NULL) {
            process_line(&stack, line);
            free(line);
        }
    } else {
        // use hard coded line
        hardcoded(&stack, atoi(argv[1]));  
    }
    free_stack(&stack);
    return 0;
}

#define     NEW_LINE       '\n'
#define     LINESIZE_STEP  32

// get a line from stdard input
// the returned string is dynamicaly allocated in the function
// The new line character is removed
// Return values:
// NULL:  EOF or error 
// Otherwise: a pointer to the line (a string)
char * get_line(void)
{
    char    * line;
    size_t  line_size, line_len;
    int     ch;

    // initialize variables
    line = NULL;
    line_size = line_len = 0;

    // This is also an example showing how to realloc a block
    // if more space is needed 
    do {
        ch = getchar();

        if (ch == EOF) {
            if (line) 
                free(line);
            return NULL;
        }

        // append ch to line
        // if not enough space, realloc
        if (line_len + 2 > line_size) {
            line_size += LINESIZE_STEP;
            line = realloc(line, line_size * sizeof(char)); 
            check_pointer(line);
        }

        // there should be at least 2 bytes available
        // one for ch and one for NUL
        line[line_len ++] = ch; 
    } while (ch != NEW_LINE);

    // line should not be NULL. It has NEW_LINE at least
    line[line_len-1] = '\0';  // put NUL where '\n' is
    return line;
}

void  hardcoded(stack_t * pstack, int nlines) 
{
    static char * lines[] = {
        "s0", "s1", "s2", "s3", "i", 
        "s4 increase num_entries to 8", "i",
        "s5", "s6", "s7", "s8 num_entries should be 12", "i",
        "s9", "s10", "s11", "s12", "i",
        "p",  "p",  "p",  "p", "i",  // s8 is at the top  
        "p", "i", // s7 is at the top, shrinks to 12 
        "p",  "p",  "p", "p", "p", "i",
        NULL
    };

    int i = 0;

    if (nlines <= 0) 
        nlines = sizeof(lines)/sizeof(char *);

    while (i < nlines && lines[i]) {
        process_line(pstack, lines[i]);
        i ++;
    }
}

// print an error message by an error number, and return
// the function does not exit from the program
// the function does not return a value
void    error_message(enum ErrorNumber errno)
{
    char    *messages[] = {"OK", 
        "Stack is empty.",
        "Memory allocaton failed.", 
        "Invalid error number."};

    if (errno < 0 || errno >= ERR_END)
        errno = ERR_END;
    printf("strstack: %s\n", messages[errno]);
}

void    check_pointer(void *p)
{
    if (p == NULL) {
        error_message(ERR_NOMEM);
        exit(-1);
    }
}

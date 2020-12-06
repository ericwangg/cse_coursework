#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

// Search TODO to find locations where code is to be completed

#define     LINE_SIZE   512

typedef struct {
   char *   prefix;     // the prefix
   char *   suffix;     // the suffix
   size_t   prefix_len; // the length of the prefix
   size_t   suffix_len; // the length of the suffix
} pattern_t;

// report error and exit
void die(char *s)
{
    if (errno) 
        perror(s);
    else 
        fprintf(stderr, "Error: %s\n", s);
    exit(EXIT_FAILURE);
} 

// This function removes the new line character at the end of a string.
// It removes at most one character.
//
// Return value:
//  0: The line does not end with a new line. 
//  1: A new line was removed at the end of the string. 
int remove_newline(char *s)
{
    size_t len = strlen(s);
    
    // check len first, to avoid index - 1
    if (len && s[len - 1] == '\n') {
        s[len - 1] = 0;
        return 1;
    }
    return 0;
}

// The function redirects stdin of the process
// to the file specified by fn.
//
// You do not need to check if fn is "-" or empty.
//  
// Parameter:
//      fn:    Specify the file to be used as stdin 
//
// This function does not return a value.
// If any function fails, call die() to exit.
//
// Check the return value of all function calls!
void redirect_stdin(const char *fn)
{
    // TODO
    // pattern_t pat_in;
    int reIn = dup2(fn, stdin);
    if(fn < 0){
    	die("stdin() failed");
    }
    if(reIn < 0){
    	die("dup2() failed");
    }
    
    
}

// The function redirects stdout of the process
// to the file specified by fn.
//
// You do not need to check if fn is "-" or empty.
//
// When calling open(), use 0600 for the mode (permission).
//  
// Parameter:
//      fn:    Specify the file to be used as stdout
//
// This function does not return a value.
// If any function fails, call die() to exit.
//
// Check the return value of all function calls!
void redirect_stdout(const char *fn)
{
    // TODO
    // pid_t pid = fork();		// no forking necessary why would you do that
    // if(pid == 0){
    	
    // }
    int reOut = dup2(fn, stdout);
    if(fn < 0){
    	die("fn failed");
    }
    if(reOut < 0){
    	die("dup2() failed");
    }
    
    int file = open(fn, O_WRONLY | O_TRUNC | O_CREAT, 0600);

    if(file < 0){
    	die("open() failed");
    }
    close(fn);
    // execvp(prog->argv[0], prog->argv);	
}

// This function checks if a string matches the pattern
//
// We could use const char *s.
//
// Paramters:
//  s:          the string
//  ppattern:   the glob pattern
//
// Return value:
//  1:      The string s matches the pattern
//  0:      No. They do not match
int is_match(char *s, const pattern_t * ppattern)
{
    // TODO
    if(strstr(&s, &ppattern) != NULL){
    	return 1;
    }
    else{
    	return 0;
    }
    
}

/******** do not change code below ***********/

// This function reads lines from stdin and prints to stdout lines that matches a pattern.
// assume all lines has at most (LINE_SIZE - 2) ASCII characters.
//
// Paramters:
//  ppattern: the glob pattern to match lines
//
// This function does not return a value
void print_matched_lines(const pattern_t * ppattern)
{
    // define a buffer for the line
    char    line[LINE_SIZE];

    while (1) {
        char  * p = fgets(line, LINE_SIZE, stdin);

        // End of file
        if (p == NULL)
            break;

        if (! remove_newline(line)) 
            die("The line is too long.");
        
        if (is_match(line, ppattern)) {
            printf("%s\n", line);
        }
    }
}

int main(int argc, char **argv)
{
    if (argc != 4) {
        fprintf(stderr, "Usage: %s <input-fn> <output-fn> <pattern>\n", argv[0]);
        return 1;
    }

    char pattern_str[LINE_SIZE];

    // make a copy of the pattern
    strncpy(pattern_str, argv[3], LINE_SIZE);
    if (pattern_str[LINE_SIZE-1])
        die("pattern is too long.");

    pattern_t pattern;
    char * suffix;

    // find suffix by finding '*'
    // we can use strstr(), but let us use a loop first
    suffix = strchr(pattern_str, '*');

    if (suffix == NULL)
        die("no * found in the pattern.");

    // *suffix must be '*'
    *suffix++ = 0;

    // we use strstr() to check if there is an '*' in the suffix 
    if (strchr(suffix, '*')) 
        die("the pattern can only have one *");

    // initialize the pattern structure
    // including the length of prefix and suffix
    pattern.prefix = pattern_str;
    pattern.suffix = suffix;
    pattern.prefix_len = strlen(pattern_str);
    pattern.suffix_len = strlen(suffix);

    // printf("'%s'*'%s'\n", pattern.prefix, pattern.suffix);

    // redirect input and output
    // OK, we check more conditions here.
    // We only redirect if fn is not empty and it is not "-"
    char * fn;
    fn = argv[1];
    if (fn && strlen(fn) > 0 && strcmp(fn, "-")) 
        redirect_stdin(fn);
    fn = argv[2];
    if (fn && strlen(fn) > 0 && strcmp(fn, "-")) 
        redirect_stdout(fn);

    print_matched_lines(&pattern);

    return 0;
}

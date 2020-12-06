#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <assert.h>
#include <string.h>
#include <sys/wait.h>
#include <errno.h>
#include <sys/types.h>
#include <dirent.h>

// search TODO to find the place you need to work on

void die(char *s)
{
    fprintf(stderr, "Error: %s\n", s);
    if (errno)
        perror("errno");
    exit(EXIT_FAILURE);
}

#define MAX_VALUE       1000
#define MSG_BUF_SIZE    100
#define PIPEFD_READ		0
#define PIPEFD_WRITE	1

typedef  struct {
    int v;
    int num_attempts;
    char message[MSG_BUF_SIZE]; 
} gmn_t;

void gmn_init(gmn_t *pg, int seed)
{
    srand(seed);
    pg->v = rand() % MAX_VALUE + 1;
    pg->num_attempts = 0;
    strcpy(pg->message, "You have not got the right number yet.\n");
} 

int gmn_check(gmn_t *pg, int guess)
{
    pg->num_attempts ++;
    if (pg->v == guess) {
        snprintf(pg->message, MSG_BUF_SIZE, 
                "It took you %d attempt(s) to guess the number %d.\n", 
                pg->num_attempts, pg->v);  
        return 0;
    }
    if (pg->v > guess)
        return 1;
    return -1;
}

char * gmn_get_message(gmn_t *pg)
{
    return pg->message;
}

int    gmn_get_max()
{
    return MAX_VALUE;
}

// this function runs the demo session
// all gmn_ functions should be called in child process 
// and then send the result to the parent process
void guess_my_number(int seed)
{
    gmn_t gmn;

    // initialize the game
    gmn_init(&gmn, seed);

    int min = 1;
    int max = gmn_get_max();
    int result;

    do {
        // make a guess
        int guess = (min + max)/2;
        printf("My guess: %d\n", guess);

        // check
        result = gmn_check(&gmn, guess);

        // if not correct, prepare for the next guess
        if(result > 0) 
            min = guess + 1;
        else if(result < 0)
            max = guess - 1;
    } while (result != 0);

    // print out the final message
    fputs(gmn_get_message(&gmn), stdout);
}


// Tasks for the child process. 
// 
// Parameters:
//  fdp:    the pipe for parent to write and for child to read 
//  fdc:    the pipe for child to write and for parent to read
//  seed:   seed for the random numer
//
// This function should not return.
// This function does not print any characters, except for error messages.
void    child_main(int fdp[], int fdc[], int seed)
{
    gmn_t   gmn;

    gmn_init(&gmn, seed);

    // TODO
    //  close unused file descriptors
    //  send max value to the parent 
    //  repeat the following until guess from parent is correct 
    //      wait for a guess from parent 
    //      call gmn_check() 
    //      send the result to parent
    //  send the final message back (as a string) 
    //  close all pipe file descriptors
    
    // pid_t child = fork();		// no need to create child here, created in main
    								// fdc - fork descriptor parent (fdc - child)
    								// close unused fds
    close(fdp[PIPEFD_WRITE]);		// close parent write to child parent(1)
    close(fdc[PIPEFD_READ]);		// close child read to parent  child(0)
    
    // int guess = guess_my_number(seed);		// set seed for gmn #
    int guess;									// simply hold the guess value for now
    int MAX_VALUE_TEMP = 1000; 					// integer point casting issues to defined integer
    write(fdc[PIPEFD_WRITE], &MAX_VALUE_TEMP, sizeof(int));			// send max value to parent from child
    // Note: must use address instead of direct value to be able to point and reference items
    // *** outsides of child function.
	while(1){					// while True
		int readBytes_c = read(fdp[PIPEFD_READ], &guess, sizeof(int));	// read from parent's guess in parent to child pipe
		int check = gmn_check(&gmn, guess);								// check that the bytes read are the correct guess
		write(fdc[PIPEFD_WRITE], &check, sizeof(int));					// child tells parents if the check is a good guess or not by writing to it
		if (check == 0){		// if gmn_check finds that it is the correct number in guess
			break;				// break out, stop while looping
		}
		
	}
    write(fdc[PIPEFD_WRITE], gmn.message, MSG_BUF_SIZE);		// write final message string
   	// sending from child to parent, includes the message buffer size of 100 
   	// use "structure.attribute" to dereference and obtain value
    
    // don't leave pipe file descriptor open
    close(fdp[PIPEFD_READ]);		// close parent read to child	parent(0)
	close(fdc[PIPEFD_WRITE]);			// close child write to parent	child(1)
    exit(EXIT_SUCCESS);
}

void    print_file_descriptors(int child);

int main(int argc, char *argv[])
{
    int seed = 3100;
    int demo = 0;
    int lsof = 0;

    // parse the command line arguments

    for (int i = 1; i < argc; i ++) {
        if (! strcmp(argv[i], "demo")) {
            demo = 1;
        } else if (! strcmp(argv[i], "lsof")) {
            lsof = 1;
        } else if (! strcmp(argv[i], "-h")) {
            fprintf(stderr, "Usage: %s [<seed>] [demo] [lsof]\n", argv[0]);
            return 1;
        } else {
            seed = atoi(argv[i]);
            if (seed <= 0)
                die("seed must be a postive number.");
        }
    }

    if (demo) {
        guess_my_number(seed);
        exit(0);
    }

    // Now, we do it using two processes
    // The child generates a random number
    // The parent tries to guess the number.
    // The child tell the parent

    // two pipes
    // fdp : parent writes
    // fdc : child writes
    
    int fdp[2], fdc[2];

    //pipe creation
    if (pipe(fdp) == -1)
        die("pipe() failed.");

    if (pipe(fdc) == -1)
        die("pipe() failed.");

    pid_t pid;
    pid = fork();

    if (pid < 0)
        die("fork() failed.");

    if(pid == 0)
        child_main(fdp, fdc, seed); // never returns
    
    // parent continues
    
    int min = 1;
    int max;
    int guess;
    int result;

    // TODO
    //      close unused pipe file descriptor
    //      get max from the child
    
    // EW: closing the opposite file descriptors vs. child and make new character array for the message buffer size
    char array[MSG_BUF_SIZE];
    
    close(fdp[PIPEFD_READ]);		// close parent to child's read 
    close(fdc[PIPEFD_WRITE]);		// close child to parent's write
    int getMax = read(fdc[PIPEFD_READ], &max, sizeof(int));		// gets the max number, stores in address of "max" as previously defined
    
    if (lsof) {
        print_file_descriptors(pid);
        print_file_descriptors(getpid());
    }

    do { 
        guess = (min + max)/2;
        printf("My guess: %d\n", guess);

        // TODO
        //     send guess to the child
        //     wait for the result from the child
        
        // EW: have previously defined guess to be (min + max / 2)
        int writeBytes_p = write(fdp[PIPEFD_WRITE], &guess, sizeof(int));	// write guess parent to child pipe 
        int writeRead_p = read(fdc[PIPEFD_READ], &result, sizeof(int)); 	// read the result from child to see if guess is right 

        if (result > 0)
            min = guess + 1;
        else if (result < 0)
            max = guess - 1;
    } while (result != 0);

    // flush stdout buffer
    fflush(stdout);

    // TODO
    //      receive the final message and print it to stdout
    //      close all pipe file descriptors
    //wait for the child process to finish
    
    // EW: change getMax, print array, then close everything
    getMax = read(fdc[PIPEFD_READ], array, MSG_BUF_SIZE);	// take final message string
    printf("%s", array);									// print final message string > stdout
    
    close(fdp[PIPEFD_READ]);		// close all fds of both parent and child
    close(fdp[PIPEFD_WRITE]);
    close(fdc[PIPEFD_READ]);
    close(fdc[PIPEFD_WRITE]);
    
    wait(NULL);
    return 0;
}

// This function prints the open file descriptors for a process
// Works only on Linux like system
// if pid is -1
void    print_file_descriptors(int pid)
{
    char buf[64];

    snprintf(buf, sizeof(buf), "/proc/%i/fd/", pid);

    fprintf(stdout, "open FDs: ");

    DIR *dir = opendir(buf);
    if (dir == NULL) {
        fprintf(stdout, "error\n");
        return;
    }

    int thisfd = -1;
    if (pid == getpid()) { 
        thisfd = dirfd(dir);
    }

    struct dirent *entry;

    while ((entry = readdir(dir)) != NULL) {
        if (entry->d_name[0] == '.')
            continue;
        if (atoi(entry->d_name) == thisfd)
            continue;
        fprintf(stdout, "%s ", entry->d_name); 
    }
    fprintf(stdout, "\n");
    closedir(dir);
}

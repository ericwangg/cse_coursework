#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <unistd.h>
#include <assert.h>
#include <string.h>
#include <sys/wait.h>
#include <errno.h>

#define MAX_N 100000
#define PFD_READ     0
#define PFD_WRITE    1

/*************  error handling functions  ****************/
void die(char *s)
{
    if (errno)
        perror(s);
    else
        fprintf(stderr, "Error: %s\n", s);
    exit(EXIT_FAILURE);
}

// print numbers in array arr
// n is the number of elements in arr
// upto is the number of elements to be printed
// if upto is 0, all elements are printed
void print_array(int arr[], int n, int upto)
{
    if (upto == 0 || n < upto)
        upto = n;
    for(int i=0; i<upto; i++) 
        printf("%d\n", arr[i]);
}

// This function is the compare function used by the qsort()
int compare_int(const void *a, const void *b)
{
    return *((int *)a) - *((int *)b);
}

// merge the sorted arrays a[] and b[] to a sorted array c[]
// both a[] and b[] have n integers
// all arrays are sorted in increasing order 
void merge(int a[], int b[], int c[], int n)
{
    int i, j, k;

    i = j = k = 0;

    while (i < n || j < n)
    {
        if (j == n || (i < n && a[i] < b[j])) {
            c[k++] = a[i];
            i++;
        } else {
            c[k++] = b[j];
            j++;
        }
    }
}


void parse_command_line(int argc, char *argv[], int *seed, int *n, int *print_sorted, int *num_printed);

int main(int argc, char *argv[])
{
    int seed = 3100, n, print_sorted = 1, num_printed = 0;

    // parse command line arguments
    parse_command_line(argc, argv, &seed, &n, &print_sorted, &num_printed);

    fprintf(stderr,"seed=%d n=%d print_sorted=%d num_printed=%d\n", seed, n, print_sorted, num_printed);

    srand(seed);        // set the seed

    // prepare arrays
    // u has all the integers to be sorted
    // a is the first half and b is the second half
    int u[n];
    int *a, *b;
    int half = n / 2;

    a = u;
    b = a + half;

    for (int i = 0; i < n; i++)
        u[i] = rand() % n;

    if (! print_sorted) {
        print_array(u, n, num_printed);
        fprintf(stderr, "The unsorted array has been printed to stdout.\n"); 
        exit(EXIT_SUCCESS);
    }

    int pd1[2], pd2[2];

    // create pipes
    if(pipe(pd1) == -1)
        die("pipe() 1");

    if(pipe(pd2) == -1)
        die("pipe() 2");

    // a is the starting address of the first half
    // b is the starting address of the second half
    // each of a and b has `half` integers
     
    // TODO
    // create 2 child processes to sort arrays a and b, into increasing order
    pid_t cpid_1 = fork();
    pid_t cpid_2 = fork(); 
    
    //  child 1:  
    //      close file descriptors that are not needed
    //      call qsort() to sorts a, 
    //      writes sorted integers to pipe 1 (pd1)
    //      close file descriptor(s) and exit

    if(cpid_1 < 0){
    	perror("fork() failed 1");
    	exit(1);
    }
    else if(cpid_2 < 0){
    	perror("fork() failed 2");
    	exit(1);
    }
    else if(cpid_1 == 0){			// child a
	    if(close(pd1[0]) == -1){		// before for child a
	    	die("close() failed 1 read");
	    }
	    if(close(pd2[0]) == -1){		// before for child a
	    	die("close() failed 2 read");
	    }
	    
	    // try this 
	    // int size = sizeof(a) / sizeof(a[0]);
	    
    	qsort(a, half, sizeof(int), compare_int);		// LOOK qsort may return array not just int, void?
    	int writeA = write(pd1[1], &a, sizeof(int));
    	
    	if(writeA == -1){
    		die("write() failed A");
    	}
    	
    	if(close(pd1[1]) == -1){		// after
    	die("close() failed 1 write");		
    	}
    	if(close(pd2[1]) == -1){		// before for child a
	    	die("close() failed 2 write");
	    }
	    
    	exit(0);
    }
    else if(cpid_2 == 0){			// child b
		if(close(pd2[0]) == -1){		// before child b
			die("close() failed 2 read");
		}
		if(close(pd1[0]) == -1){		// before for child a
	    	die("close() failed 1 read test me");
	    }
	    
    	qsort(b, half, sizeof(int), compare_int);
    	int writeB = write(pd2[1], &a, sizeof(int));
    	
    	if(writeB == -1){
    		die("write() failed B");
    	}
    	
    	if(close(pd2[1]) == -1){		// after
    	die("close() failed 2 write");		
    	}
    	if(close(pd1[1]) == -1){		// before for child a
	    	die("close() failed  write");
	    }
	    
    	exit(0);
    }
    else{							// parent
    	if(close(pd1[1]) == -1) die("close failed");	// close pds for parent (write)
        if(close(pd2[1]) == -1) die("close failed");
        
    	int readA = read(pd1[0], &a, sizeof(int));		// read sorted from both children
    	int readB = read(pd2[0], &b, sizeof(int));
    	if(readA == -1){
    		die("read() failed A");
    	}
    	
    	if(readB == -1){
    		die("read() failed B");
    	}
    	
    	if(close(pd1[0]) == -1) die("close failed");	// close pds for parent (read)
        if(close(pd2[0]) == -1) die("close failed");
    	
    	
    	waitpid(cpid_1, NULL, 0);		// wait for both kids
    	waitpid(cpid_2, NULL, 0);
    	return 0;
    }
    
    
    
    
    //
    //  child 2:  
    //      close file descriptors that are not needed
    //      call qsort() to sorts b, 
    //      writes sorted integers to pipe 2 (pd2)
    //      close file descriptor(s) and exit
    
    //
    // The parent process reads sorted integers from child processes. 
    //      Results from child 1 are saved in a. 
    //      Results from child 2 are saved in b. 
    // Parent should wait for child processes.
    
    
    //
    // If any of read(), write(), or fork() fails, 
    //      report error and exit from the process
    //
    // All processes should close file descriptors that are not needed.
    
    


    int sorted[n];
    merge(a, b, sorted, half);
    if (print_sorted)
        print_array(sorted, n, num_printed);
    return 0;
}

void parse_command_line(int argc, char *argv[], int *seed, int *n, int *print_sorted, int *num_printed)
{
    int flag = 0;

    for (int i = 1; i < argc; i++) {
        if (! strcmp(argv[i], "-u")) {
            *print_sorted = 0;
        } else if (strncmp(argv[i], "-s", 2) == 0) {
            *seed = atoi(&argv[i][2]);
            if (*seed <= 0) {
                fprintf(stderr, "seed must be a positive integer: %s\n", &argv[i][2]);
                exit(EXIT_FAILURE);
            }
        } else if (strncmp(argv[i], "-p", 2) == 0) {
            *num_printed = atoi(&argv[i][2]);
            if (*num_printed < 0) {
                fprintf(stderr, "number of integers to be printed must be a non-negative integer: %s\n", &argv[i][2]);
                exit(EXIT_FAILURE);
            }
        } else if (isdigit(argv[i][0])) {
            *n = atoi(argv[i]);
            if (*n <= 0 || *n > MAX_N || *n % 2) {
                fprintf(stderr, "The number of elements must be a postive even integer <= %d.\n", MAX_N);
                exit(EXIT_FAILURE);
            }
            flag = 1;
        } else {
            break;
        }
    }
    if (!flag) {
        fprintf(stderr, "Usage: %s <N> [-s<N>] [-p<N>] [-b]\n"
                "<N>     : number of integers to sort. Must be specified.\n"
                "-s<N>   : seed. Default value is 3100.\n"
                "-p<N>   : number of integers to print. Default value is 0, which prints all.\n"
                "-u      : print the numbers before sorting and exit.\n"
                , argv[0]);
        exit(EXIT_FAILURE);
    }
}

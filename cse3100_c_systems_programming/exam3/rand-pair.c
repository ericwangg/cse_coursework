#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include <errno.h>

// Search TODO to find the locations where code needs to be completed

/*************  macros related to random numbers for MT ****************/
// Use functions in POSIX.1-2001.

// Use the following macro in your thread function before any calls to get random values.
#define RANDOM_INIT(x)  (g_random_buffer[0]=3100,g_random_buffer[1]=(x), g_random_buffer[2] = (x) >> 16)

// RANDOM_DOUBLE() returns a random number uniformly distributed between [0, 1)
#define RANDOM_DOUBLE() (erand48(g_random_buffer))

void die(char *s)
{
    if (errno)
        perror(s);
    else
        fprintf(stderr, "Error: %s\n", s);
    exit(EXIT_FAILURE);
}

// check the return value of pthread functions
// if the return value (rv) is not 0, reprot error and exit 
// better to use macro check_pthread_return
static void check_pthread_return_f(int rv, int lineno)
{
    char buf[80];
    if (rv == 0)
        return;
    strerror_r(rv, buf, sizeof(buf));
    fprintf(stderr, "Error: %s(line %d): %s", __FILE__, lineno, buf);
    exit(EXIT_FAILURE);
}

#define check_pthread_return(rv)    check_pthread_return_f((rv), __LINE__)

typedef struct {
    double d; 

    int n_threads;      // Number of threads participating
    int n_trials;       // Number of trials per thread

    int n_total;        // Total number of trials completed. Intialized to 0.
    int n_events;       // Number of events. Initialized to 0.

    // TODO
    pthread_mutex_t		mutex;
    // add necessary fields for synchronization
} experiment_t;

typedef struct {
    int id;         // thread id
    int seed;       // seed for generating random numbers for the thread
    experiment_t * expt;    // the shared exprement structure
} thread_arg_t;

// the function that prints the result
// this function does not return a value
// do not change this function
void    experiment_print_result(experiment_t *expt)
{
    printf("n_total=%d n_events=%d probability=%.8f\n", 
            expt->n_total, expt->n_events, ((double)expt->n_events) / expt->n_total);
}

// Initialize any fields you have added to experiment_t
// Use macro check_pthread_return() to check the return values of pthread functions
// This function does not return a value
void    experiment_init_extra(experiment_t *expt)
{
    // TODO
	int rv = pthread_mutex_init(&expt->mutex, NULL);
	check_pthread_return(rv);
    
}

// Destroy any fields you have added to experiment_t
// Use macro check_pthread_return() to check the return values of pthread functions
// This function does not return a value
void    experiment_destroy(experiment_t *expt)
{
    // TODO
    int rv = pthread_mutex_destroy(&expt->mutex);
    check_pthread_return(rv);
    
}

/* The thread main function*/
void * thread_experiment(void* arg_in)
{
    unsigned short g_random_buffer[3]; // buffer for random numbers

    thread_arg_t *arg  = arg_in;
    experiment_t *expt = arg->expt;

    RANDOM_INIT(arg->seed);

    // the last thread sets report to 1 to report results and clean up
    int report = 0;

    int n_trials = expt->n_trials;
    double d = expt->d; 
    int n_events = 0;       // events counter
    
    // TODO
    /*
     * Perform the following operations n_trials times:
            Use RANDOM_DOUBLE() to get two random values in [0, 1)
            For example,
                double x = RANDOM_DOUBLE();
                double y = RANDOM_DOUBLE();
            Increment n_events if | x - y | < d. 
            The condition can be checked without computing the absolute value of a double.
            If you really want to compute the absolute value, do not use math library function.

        Add the results from this thread to n_total and n_events in expt
        This step is outside of the loop. Do not add the result after each trial 

        Set report to 1 if this is the last thread that finishes
        To check if this is the last thread, compare n_total with the expected value
    */
    pthread_mutex_lock(&expt->mutex);
    for(int i = 0; i < n_trials; i++){
    	double x = RANDOM_DOUBLE();
		double y = RANDOM_DOUBLE();
    	double dif;	// difference between x and y
    
	    if((x - y) < 0){		// taking absolute value without using math library function
	    	dif = y - x;		// if x-y a negative number 
	    }
	    else{
	    	dif = x - y;
	    }
	    if(dif < d){
	    	n_events++;
	    }
    }
    
    expt->n_total += n_trials;		// adding results from 
    expt->n_events += n_events;
    pthread_mutex_unlock(&expt->mutex);
    
    int expt_mul = expt->n_threads * n_trials;
    
    // when total # of trials from experiment 
    // equates to # of threads X # of trials 
    // exit
    
    if(expt->n_total == expt_mul){		
    	report = 1;
    }
    
    
    // The last one will print results and clean up
    if (report) {
        experiment_print_result(expt);
        experiment_destroy(expt);
    }

    // printf("Thread %d exiting ...\n", arg->id);
    return NULL;
}

// do not change the main function 
int main(int argc, char* argv[])
{
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <d> <total_num_of_trials> <num_of_threads>\n", argv[0]);
        exit(1);
    }

    double d = atof(argv[1]);
    int n_total = atoi(argv[2]);
    int n_threads = atoi(argv[3]);

    if (d < 0 || d > 1) 
        die("d must be in [0, 1].");    

    if (n_total <= 0 )
        die("total number of trials must be positive.");    

    if (n_threads <= 0)
        die("number of threads must be positive.");    

    // make the code simpler
    if (n_total % n_threads != 0)
        die("total number of trials must be divisible by the number of threads.");    

    // number of trials per thread
    int n_trials = n_total / n_threads;

    printf("d=%.5f n_total=%d n_threads=%d n_trials(per thread)=%d\n", 
            d, n_total, n_threads, n_trials);

    // set all fields to 0
    experiment_t experiment = {0};

    experiment.d = d;
    experiment.n_threads = n_threads;
    experiment.n_trials = n_trials;

    // additional initialization
    experiment_init_extra(&experiment);

    pthread_t tids[n_threads];
    thread_arg_t args[n_threads];

    // create threads
    for (int i = 0; i < n_threads; i++) {
        args[i].id = i;
        args[i].seed = (3100 * i + 0xAB55CD) & i;
        args[i].expt = &experiment;
        int rv = pthread_create(&tids[i], NULL, thread_experiment, &args[i]);
        check_pthread_return(rv);
    }

    // wait for threads
    for (int i = 0; i < n_threads; i++) {
        int rv = pthread_join(tids[i], NULL);
        check_pthread_return(rv);
    }

    return 0;
}

#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

// search TODO to find the place you need to work on

/*************  macros related to random numbers for MT ****************/
// Use functions in POSIX.1-2001.

// Use the following macro in your thread function before any calls to get random values.
#define RANDOM_INIT(x)  (g_random_buffer[0]=3100,g_random_buffer[1]=(x),g_random_buffer[2] = (x) >> 16)

// RANDOM_INT() returns a random number uniformly distributed between [0, 2^31)
#define RANDOM_INT() (nrand48(g_random_buffer))

void die(char *s)
{
    if (errno)
        perror(s);
    else 
        fprintf(stderr, "Error: %s\n", s);
    exit(EXIT_FAILURE);
}

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

void my_msleep(int r)
{
    struct timespec req = {0, (r % 50 + 1) * 1000000};
    nanosleep(&req, NULL);
}

// default values

#define DEFAULT_N_SMALL_GROUPS   5
#define DEFAULT_N_BIG_GROUPS     5
#define DEFAULT_N_BIG_TABLES     3
#define DEFAULT_N_SMALL_TABLES   3
#define DEFAULT_N_MEALS          5

typedef struct restaurant_t_tag {
    int     n_small_tables;         // number of small tables in the restaurant 
    int     n_small_taken;          // number of small tables taken
    int     n_small_waiting;        // number of small groups waiting
    int     n_big_tables;           // number of big tables in the restaurant
    int     n_big_taken;            // number of big tables taken
    int     n_big_waiting;          // number of big groups waiting
    pthread_mutex_t mutex;          // mutex to protect shared data
    pthread_cond_t  cond_big;       // condition variable for big groups
    pthread_cond_t  cond_small;     // condition variable for small groups
} restaurant_t;

// used to indicate both group and table sizes
enum {SIZE_SMALL, SIZE_BIG}; 

typedef struct group_t_tag {
    int id;                 // group id
    int sz;                 // group size, SIZE_SMALL or SIZE_BIG
    int n_meals;            // number of meals the group will have
    int seed;               // seed for random numbers
    int time_to_dine;       // time_to_dine
    restaurant_t  * restaurant; // pointer to restaurant
} group_t;

// Macros
#define WAITING()   my_msleep(RANDOM_INT())

#define SIZE_STR(sz)  ((sz) == SIZE_SMALL ? "small" : "big")

#define DINING(grp)   my_msleep((grp)->time_to_dine)

#define PRINT_ARRIVING_MSG(grp) printf("group %2d, %5s, is arriving...\n", (grp)->id, SIZE_STR((grp)->sz))
#define PRINT_WAITING_MSG(grp)  printf("group %2d, %5s, is waiting...\n", (grp)->id, SIZE_STR((grp)->sz))
#define PRINT_SEATED_MSG(grp, tsz)   printf("group %2d, %5s, is seated at a %s table...\n", (grp)->id, SIZE_STR((grp)->sz), SIZE_STR(tsz))
#define PRINT_LEAVING_MSG(grp, tsz)  printf("group %2d, %5s, is leaving from a %s table...\n", (grp)->id, SIZE_STR((grp)->sz), SIZE_STR(tsz))

// this function shows the steps a group takes for dining 
void dining_process(group_t * grp)
{
    /* Try to get a table for the group. 

       maitain counters in mutex protected section 

       for small groups, keep the table size to be used 
       with this group in a local variable, e.g., table_size
       
       lock the mutex
       while (! predicate) {
            PRINT_WAITING_MSG(grp) 
            pthread_cond_wait(...);
       }
       PRINT_SEATED_MSG(grp, table_size);
       unlock the mutex

    */

    DINING(grp);  // dining

    /* Leaving
       
       lock the mutex
       maintain counters and signal properly
       PRINT_LEAVING_MSG(grp, table_size);
       unlock the mutex

    */
}

/* This funciton handles the dining process for small groups 
 *
 * Read the dining_process() function above for steps to take.
 * */ 
 
 
// Eric Wang: abbr. for predicates to simplify
// If there are small tables left
#define Yes_ST	restt->n_small_tables - restt->n_small_taken > 0
#define No_ST	restt->n_small_tables - restt->n_small_taken == 0

// If there are big tables left
#define Yes_BT	restt->n_big_tables - restt->n_big_taken > 0
#define No_BT	restt->n_big_tables - restt->n_big_taken == 0

//Waiting...
#define Yes_SW	restt->n_small_waiting > 0
#define No_SW	restt->n_small_waiting == 0

#define Yes_BW	restt->n_big_waiting > 0
#define No_BW	restt->n_big_waiting == 0

 
void small_group_dining(group_t * grp) 
{
    restaurant_t * restt = grp->restaurant;

    // a small group may dine at a big table
    // this variable keeps track of table size used by this group 
    int     table_size;

    // TODO
    pthread_mutex_lock(&restt->mutex);
    restt->n_small_waiting++;
    
    while( (No_ST && No_BT) || (No_ST && No_BT && Yes_BW) ) {
    	PRINT_WAITING_MSG(grp);
        pthread_cond_wait(&restt->cond_small, &restt->mutex);
    }
    restt->n_small_waiting--;
    
    if(Yes_ST){
    	table_size = SIZE_SMALL;
    	restt->n_small_taken++;
    	PRINT_SEATED_MSG(grp, table_size);
    	
	    pthread_mutex_unlock(&restt->mutex);
	    
	    DINING(grp);
	    
	    pthread_mutex_lock(&restt->mutex);
	    restt->n_small_taken--;
	    pthread_cond_broadcast(&restt->cond_small);
	    
	    PRINT_LEAVING_MSG(grp, table_size);
	    pthread_mutex_unlock(&restt->mutex);
    	// take small table
    }
    else{	// NoST && YesBT && No_BW
    	table_size = SIZE_BIG;
    	
    	PRINT_SEATED_MSG(grp, table_size);
    	restt->n_big_taken++;
		pthread_mutex_unlock(&restt->mutex);
		
		DINING(grp);
		
		pthread_mutex_lock(&restt->mutex);
		restt->n_big_taken--;
		pthread_cond_broadcast(&restt->cond_small);
		
		PRINT_LEAVING_MSG(grp, table_size);
		pthread_mutex_unlock(&restt->mutex);	
    	// take big table
    }
    
    // PRINT_SEATED_MSG(grp, table_size);
    // pthread_mutex_unlock((&restt->mutex);
    
    // DINING(grp);
    
    // pthread_mutex_lock((&restt->mutex);
    // pthread_cond_signal(&restt->cond_big, &restt->mutex);
    
    // PRINT_LEAVING_MSG(grp, table_size);
    // pthread_mutex_unlock((&restt->mutex);
}

/* This funciton handles the dining process for big groups 
 *
 * Read the dining_process() function above for steps to take.
 * */ 
void big_group_dining(group_t * grp) 
{
    restaurant_t * restt = grp->restaurant;

    // TODO
    int table_size = SIZE_BIG;
    
    pthread_mutex_lock(&restt->mutex);
    restt->n_big_waiting++;
    
    while(No_BT){
    	PRINT_WAITING_MSG(grp); 
        pthread_cond_wait(&restt->cond_big, &restt->mutex);
    }
    restt->n_big_waiting--;
    
    restt->n_big_taken++;
    PRINT_SEATED_MSG(grp, table_size);
    pthread_mutex_unlock(&restt->mutex);
    
    DINING(grp);
    
    pthread_mutex_lock(&restt->mutex);
    restt->n_big_taken--;
    pthread_cond_broadcast(&restt->cond_big);	// may be signal since only signaling big groups
    
    PRINT_LEAVING_MSG(grp, table_size);
    pthread_mutex_unlock(&restt->mutex);
}

/***********************************************************************/
/* Do not change code below.                                           */
/***********************************************************************/

// thread main function for each group.
//
// Each group dines for n_meals times. Call functions to handle the
// actual dining process.
void * thread_grp(void *arg_orig)
{
    unsigned short g_random_buffer[3]; // buffer for random numbers

    group_t *grp = arg_orig;

    if (grp->seed) {
        int actual_seed = (grp->seed << 10) + grp->id; 
        RANDOM_INIT(actual_seed);
    } else {
        int actual_seed = 3100 * grp->id + 12345;
        RANDOM_INIT(actual_seed);
    }

    for (int i = 0; i < grp->n_meals; i ++) {
        // waiting for some time
        if (grp->seed) {
            WAITING();
        }
        grp->time_to_dine = RANDOM_INT();

        PRINT_ARRIVING_MSG(grp);

        // call functions to handle dining process
        if (grp->sz == SIZE_SMALL)
            small_group_dining(grp);
        else 
            big_group_dining(grp);
    }
    return NULL;
}

void print_help(void);

int main(int argc, char *argv[]) 
{
    int i, n;
    int n_small_groups = DEFAULT_N_SMALL_GROUPS, n_big_groups = DEFAULT_N_BIG_GROUPS;
    int n_small_tables = DEFAULT_N_SMALL_TABLES, n_big_tables = DEFAULT_N_BIG_TABLES;
    int n_meals = DEFAULT_N_MEALS;
    int seed_small, seed_big;

    seed_small = seed_big = 3100;

    for (i = 1; i < argc; i++) {
        if (! strncmp(argv[i], "-g", 2) && isdigit(argv[i][2])) { 
            n_small_groups = atoi(&argv[i][2]);
        } else if (! strncmp(argv[i], "-G", 2) && isdigit(argv[i][2])) { 
            n_big_groups = atoi(&argv[i][2]);
        } else if (! strncmp(argv[i], "-m", 2) && isdigit(argv[i][2])) { 
            n_meals = atoi(&argv[i][2]);
        } else if (! strncmp(argv[i], "-t", 2) && isdigit(argv[i][2])) {
            n_small_tables = atoi(&argv[i][2]);
        } else if (! strncmp(argv[i], "-T", 2) && isdigit(argv[i][2])) { 
            n_big_tables = atoi(&argv[i][2]);
        } else if (! strncmp(argv[i], "-s", 2) && isdigit(argv[i][2])) {
            seed_small = atoi(&argv[i][2]);
        } else if (! strncmp(argv[i], "-S", 2) && isdigit(argv[i][2])) {
            seed_big = atoi(&argv[i][2]);
        } else {
            print_help();
        }
    }

    printf("Options: -g%d -G%d -t%d -T%d -m%d -s%d -S%d\n", 
            n_small_groups, n_big_groups, n_small_tables, n_big_tables, n_meals, seed_small, seed_big);

    int rv;

    restaurant_t restt = {0};
    restt.n_big_tables = n_big_tables;
    restt.n_small_tables = n_small_tables;

    rv = pthread_mutex_init(&restt.mutex, NULL);
    check_pthread_return(rv);
    rv = pthread_cond_init(&restt.cond_small, NULL);
    check_pthread_return(rv);
    rv = pthread_cond_init(&restt.cond_big, NULL);
    check_pthread_return(rv);

    n = n_big_groups + n_small_groups;      // number of threads to create
    
    pthread_t tid[n];
    group_t   grps[n];

    for (i = 0; i < n; i++) {
        grps[i] = (group_t){i, SIZE_SMALL, n_meals, seed_small, 0, &restt};
        if (i >= n_small_groups) {
            grps[i].sz = SIZE_BIG;
            grps[i].seed = seed_big;
        }
        rv = pthread_create(&tid[i], NULL, thread_grp, &grps[i]);
        check_pthread_return(rv);
    }

    for(i = 0; i < n; i++) {
        rv = pthread_join(tid[i], NULL);
        check_pthread_return(rv);
    }

    rv = pthread_mutex_destroy(&restt.mutex);
    check_pthread_return(rv);
    rv = pthread_cond_destroy(&restt.cond_small);
    check_pthread_return(rv);
    rv = pthread_cond_destroy(&restt.cond_big);
    check_pthread_return(rv);

    return 0;
}

void print_help(void)
{
    char * helpmsg =
    	"Usage: ./restt [options]\n"
        "-g<N>    number of small groups (default:5).\n"
        "-G<N>    number of big groups (default:5).\n"
        "-t<N>    number of small tables (default:3).\n"
        "-T<N>    number of big tables (default:3).\n"
        "-m<N>    number of meals (default:5).\n"
        "-s<N>    seed for small groups (default:3100).\n"
        "-S<N>    seed for big groups (default:3100).\n";
    fprintf(stderr, "%s", helpmsg);
    exit(EXIT_FAILURE);
}

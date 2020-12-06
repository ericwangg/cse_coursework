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
#define RANDOM_INIT(x)  (g_random_buffer[0]=3100,g_random_buffer[1]=(x), g_random_buffer[2] = (x) >> 16)

// RANDOM_INT() returns a random number uniformly distributed between [0, 2^31)
#define RANDOM_INT() (nrand48(g_random_buffer))

void die(char *s)
{
    fprintf(stderr, "Error: %s\n", s);
    if (errno)
        perror("errno");
    exit(EXIT_FAILURE);
}

void check_pthread_return(int rv, char *msg)
{
    if (rv == 0)
        return;
    errno = rv;
    die(msg);
}

void my_msleep(int r)
{
    // limit to 100ms
    struct timespec req = {0, (r % 100 + 1) * 1000000};

    nanosleep(&req, NULL);
}

#define DEFAULT_NTRIPS     10
#define DEFAULT_NCARS_EAST 5
#define DEFAULT_NCARS_WEST 5
#define DEFAULT_MAX_CROSSING 2

#define CROSS_BRIDGE(car)   my_msleep((car)->time_to_cross)

enum {EAST, WEST}; 

typedef struct bridge_t_tag {
    int     direction;          // current direction
    int     n_crossing;         // number of cars on the bridge
    int     max_crossing;       // max number of cars on the bridge
    int     n_crossed;          // number of cars that have crossed the bridge in current direction
    int     max_crossed;        // max number of cars that can cross if a car is waiting in opposite direction
    int     eastb_waiting;      // number of cars waiting, eastbound
    int     westb_waiting;      // number of cars waiting, westbound
    pthread_mutex_t mutex;      // mutex to protect shared info
    pthread_cond_t  cond_east;  // condition variable for eastbound cars
    pthread_cond_t  cond_west;  // condition variable for westbound cars
} bridge_t;

typedef struct car_t_tag {
    int id;
    int direction;
    int n_trips;
    int seed;
    int time_to_cross;
    bridge_t * bridge;
} car_t;

#define CAR_DIRECTION(car)  ((car)->direction ? "westbound" : "eastbound")

#define PRINT_ARRIVING_MSG(car)  printf("car %2d, %s, is arriving...\n", (car)->id, CAR_DIRECTION(car))
#define PRINT_WAITING_MSG(car)  printf("car %2d, %s, is waiting...\n", (car)->id, CAR_DIRECTION(car))
#define PRINT_GETTINGON_MSG(car)  printf("car %2d, %s, is getting on the bridge...\n", (car)->id, CAR_DIRECTION(car))
#define PRINT_LEAVING_MSG(car)  printf("car %2d, %s, is leaving ...\n", (car)->id, CAR_DIRECTION(car))

// this function shows what a car does if it does not care about rules
// comments have some requirements/suggestions for multithreaded version 
void cross_bridge_single(car_t * car)
{
    /*  A car may wait if it follows the rules.
     *  If it needs to wait, it should wait in a loop and print a message.
    while (....) { 
        PRINT_WAITING_MSG(car);
        pthread_cond_wait(...);
    }
    */

    // messages should be printed when mutex is locked.
    PRINT_GETTINGON_MSG(car); // mutex is locked

    CROSS_BRIDGE(car);  // drive on the bridge, should be done when mutex is unlocked.

    PRINT_LEAVING_MSG(car); // mutex is locked
}


//EW: Definitions for a more concise conditions
// Directions
#define Eastbound	bridge->direction == EAST		// for EASTBOUND
#define Westbound	bridge->direction == WEST		// For WESTBOUND

// Conds that causes the car to wait or switch directions
// Opposite of what keeps the car flowing in Eastbound (or respective) direction
#define Cond1		bridge->n_crossing >= bridge->max_crossing
#define Cond2		bridge->n_crossed + bridge->n_crossing >= bridge->max_crossed
// Opposite of each
#define Cond1op		bridge->n_crossing < bridge->max_crossing
#define Cond2op		bridge->n_crossed + bridge->n_crossing < bridge->max_crossed

// Waiting conditions 
#define NoWW		bridge->westb_waiting == 0	// No West Waiting... etc.
#define YesWW		bridge->westb_waiting > 0
#define NoEW		bridge->eastb_waiting == 0
#define YesEW		bridge->eastb_waiting > 0

// Crossing conditions
#define NoCross		bridge->n_crossing == 0
#define YesCross	bridge->n_crossing != 0


void cross_bridge_eastbound(car_t * car) 
{
    bridge_t* bridge = car->bridge;

    // TODO
    
    // PRINT_ARRIVING_MSG(car);
    
    pthread_mutex_lock(&bridge->mutex);
    
    // Cars need to wait, passing conditions aren't satisfied
    // OG --
    // (Eastbound && Cond2 && YesWW) || (Westbound && Cond2op && YesWW) || (Eastbound && Cond1) || (Westbound && YesCross)
    
    // Original Conditions-1 
    // ((Eastbound && Cond2 && bridge->westb_waiting > 0) || (Eastbound && Cond1) || (Westbound && Cond2))
    // Conditions-2
    // (Eastbound && ((Cond2 && YesWW) || Cond1) ) || (Westbound && Cond2) 
    // Take-3
    // Cond2 || (Eastbound && Cond1) || (Westbound && YesCross)
    // Take-4 Back to modified OG--
    // (Eastbound && ((Cond2 && YesWW) ||  Cond1)) || (Westbound && ((Cond2op && YesWW) || YesCross)))
    
    
    // if( Cond2 && YesEW && NoWW){
    // 	bridge->n_crossed = 0;	// reset if cars hang and wait
    // 	printf("\n ___________ Stay at East, RESET n_crossed ___________ \n");
    // }
    
    bridge->eastb_waiting++;
    //printf("\n\n ___________ car_id=%d, car_direction=%d, bridge_direction=%d ___________\n\n", car->id, car->direction, bridge->direction);
    
    while ( (Eastbound && Cond2 && YesWW) || (Westbound && Cond2op && YesWW) || (Eastbound && Cond1) || (Westbound && YesCross)  ) {
    	PRINT_WAITING_MSG(car);
        pthread_cond_wait(&bridge->cond_east, &bridge->mutex);
    }
    bridge->direction = EAST;
    
    
    PRINT_GETTINGON_MSG(car);
    bridge->eastb_waiting--;
    bridge->n_crossing++;
    
    pthread_mutex_unlock(&bridge->mutex);		
    // only unlock after car accessed values finish access
    
    // If not waiting --> then crossing, then crosses
   	CROSS_BRIDGE(car);
    
    pthread_mutex_lock(&bridge->mutex);
    
    PRINT_LEAVING_MSG(car);
    bridge->n_crossing--;
    bridge->n_crossed++;
    
    //printf("\n\n ___________ n_crossed=%d, n_crossing=%d, eastb_waiting=%d, westb_waiting=%d ___________\n\n", bridge->n_crossed, bridge->n_crossing, bridge->eastb_waiting, bridge->westb_waiting);
    
    // Post crossing --> change directions, else stay same direction
    // OG Cond:
    // ( NoCross && ( YesWW && (Cond2  || (Eastbound && NoEW))) )
    // Take 2
    // YesWW && (Cond2 || (NoEW && Eastbound && NoCross))
    // Take 3
    // ((Cond2 && YesWW) || (NoEW && Eastbound && YesWW)) && (Eastbound && NoCross)
    // Take 4
    // YesWW && (Cond2  || (Eastbound && NoEW)) && (Eastbound && NoCross) 
    
    if ( ((Cond2 && YesWW) || (NoEW && Eastbound && YesWW)) && (Eastbound && NoCross) ) {	
    				
    	//printf("\n ___________ Switched to West ___________ \n");
    	// change to West
    	
    	bridge->direction = WEST; // TRUE for Westbound, see thread_car
    	bridge->n_crossed = 0;
    	pthread_cond_broadcast(&bridge->cond_west);
    	
    	// max_crossed and max_crossing # obviously does NOT change
    	//pthread_mutex_unlock(&bridge->mutex);
    }
    // else if( Cond2 && YesEW && NoWW ){
    // 	bridge->n_crossed = 0;			// n_crossed is reset to allow more cars to pass
    // 	//printf("\n ___________ Stay at East ___________ \n");
    // 	pthread_cond_broadcast(&bridge->cond_east);
    // }
    else{
    	//printf("\n ___________ Stay at East ___________ \n");
    	pthread_cond_broadcast(&bridge->cond_east);
    }
	pthread_mutex_unlock(&bridge->mutex);
    // 😊😊
}

void cross_bridge_westbound(car_t * car) 
{
    bridge_t* bridge = car->bridge;

    // TODO
    pthread_mutex_lock(&bridge->mutex);
    
  
    bridge->westb_waiting++;
    //printf("\n___________ car_id=%d, car_direction=%d, bridge_direction=%d ___________\n", car->id, car->direction, bridge->direction);
    
    // OG Cond:
    // ((Eastbound && Cond2 && bridge->westb_waiting > 0) || (Eastbound && Cond1) || (Westbound && Cond2))
    // Take-2
    // ( (Westbound && (Cond1 || Cond2)) || (Eastbound && YesEW && YesCross) )
    
    while ( (Westbound && Cond2 && YesEW) || (Eastbound && Cond2op && YesEW) || (Westbound && Cond1) || (Eastbound && YesCross) ) {
    	PRINT_WAITING_MSG(car);
        pthread_cond_wait(&bridge->cond_west, &bridge->mutex);
        
    }
    bridge->direction = WEST;
    
    PRINT_GETTINGON_MSG(car);
    bridge->westb_waiting--;
    bridge->n_crossing++;
    
    pthread_mutex_unlock(&bridge->mutex);		

   	CROSS_BRIDGE(car);
    
    pthread_mutex_lock(&bridge->mutex);
    
    PRINT_LEAVING_MSG(car);
    bridge->n_crossing--;
    bridge->n_crossed++;
    
    //printf("\n\n ___________ n_crossed=%d, n_crossing=%d, westb_waiting=%d, eastb_waiting=%d ___________\n\n", bridge->n_crossed, bridge->n_crossing, bridge->westb_waiting, bridge->eastb_waiting);
    
    // Post crossing --> change directions, else stay same direction
    // OG Cond:
    // ( NoCross && ( YesEW && (Cond2  || (Westbound && NoWW))) )
    // Take 2
    // NoWW || (NoCross && ( YesEW && (Cond2  || Westbound))) 
    // Take 3
    // ((NoWW && YesEW) || Cond2) &&  NoCross
    // Take 4
    // YesEW && (Cond2  || (Westbound && NoWW)) && (Westbound && NoCross)
    
    
    if ( ((Cond2 && YesEW) || (NoWW && Westbound && YesEW)) && (Westbound && NoCross)) {
    	
    	bridge->direction = EAST; 
    	bridge->n_crossed = 0;
    	pthread_cond_broadcast(&bridge->cond_east);
    				// Reset # of crossed
    	// max_crossed and max_crossing # obviously does NOT change
    }
	// else if( Cond2 && YesWW && NoWW ){
	 //   	bridge->direction = WEST;
	 //   	pthread_cond_broadcast(&bridge->cond_west);
	 //   	bridge->n_crossed = 0;			// n_crossed is reset to allow more cars to pass
	 //   }
    else{
    	// Stay East
    	pthread_cond_broadcast(&bridge->cond_west);
    }
    pthread_mutex_unlock(&bridge->mutex);
	
}

void * thread_car(void *arg_orig)
{
    unsigned short g_random_buffer[3]; // buffer for random numbers

    car_t *car = arg_orig;

    if (car->seed) {
        car->seed = (car->seed << 10) + car->id; 
        RANDOM_INIT(car->seed);
    }

    for (int i = 0; i < car->n_trips; i ++) {
        // driving for some time
        if (car->seed) 
            my_msleep(RANDOM_INT());
        else 
            my_msleep(0);

        PRINT_ARRIVING_MSG(car);

        // need to cross the bridge
        if (car->seed) 
            car->time_to_cross = RANDOM_INT();
        if (car->direction) {
            cross_bridge_westbound(car);
        } else {
            cross_bridge_eastbound(car);
        }
    }
    return NULL;
}

void print_help(void);

int main(int argc, char *argv[]) 
{
    int i, n, ncars_west = DEFAULT_NCARS_WEST, ncars_east = DEFAULT_NCARS_EAST;
    int max_crossing = DEFAULT_MAX_CROSSING, max_crossed = DEFAULT_MAX_CROSSING * 2;
    int n_trips = DEFAULT_NTRIPS;
    int seede, seedw;

    seede = seedw = 3100;

    for (i = 1; i < argc; i++) {
        if (! strncmp(argv[i], "-w", 2) && isdigit(argv[i][2])) { 
            ncars_west = atoi(&argv[i][2]);
        } else if (! strncmp(argv[i], "-e", 2) && isdigit(argv[i][2])) { 
            ncars_east = atoi(&argv[i][2]);
        } else if (! strncmp(argv[i], "-m", 2) && isdigit(argv[i][2])) { 
            max_crossing = atoi(&argv[i][2]);
            if (max_crossing == 0)
                die("max number of cars on the bridge must be positive");
        } else if (! strncmp(argv[i], "-c", 2) && isdigit(argv[i][2])) {
            max_crossed = atoi(&argv[i][2]);
            if (max_crossing == 0)
                die("max number of cars on the bridge must be positive");
        } else if (! strncmp(argv[i], "-t", 2) && isdigit(argv[i][2])) { 
            n_trips = atoi(&argv[i][2]);
            if (n_trips == 0)
                die("number of trips must be positive");
        } else if (! strncmp(argv[i], "-se", 3) && isdigit(argv[i][3])) {
            seede = atoi(&argv[i][3]);
        } else if (! strncmp(argv[i], "-sw", 3) && isdigit(argv[i][3])) {
            seedw = atoi(&argv[i][3]);
        } else {
            print_help();
        }
    }

    printf("Options: -w%d -e%d -m%d -c%d -t%d -se%d -sw%d\n", 
            ncars_west, ncars_east, max_crossing, max_crossed, n_trips, seede, seedw);

    int rv;

    bridge_t bridge = {0};
    bridge.max_crossing = max_crossing;
    bridge.max_crossed = max_crossed;

    rv = pthread_mutex_init(&bridge.mutex, NULL);
    check_pthread_return(rv, "pthread_mutex_init");
    rv = pthread_cond_init(&bridge.cond_east, NULL);
    check_pthread_return(rv, "pthread_cond_init");
    rv = pthread_cond_init(&bridge.cond_west, NULL);
    check_pthread_return(rv, "pthread_cond_init");

    n = ncars_west + ncars_east;      // number of threads to create
    pthread_t tid[n];
    car_t cars[n];

    for (i = 0; i < n; i++) {
        cars[i] = (car_t){i, EAST, n_trips, seede, 0, &bridge};
        if (i >= ncars_east) {
            cars[i].direction = WEST;
            cars[i].seed = seedw;
        }
        rv = pthread_create(&tid[i], NULL, thread_car, &cars[i]);
        check_pthread_return(rv, "pthread_create");
    }
    for(i = 0; i < n; i++) {
        rv = pthread_join(tid[i], NULL);
        check_pthread_return(rv, "pthread_join");
    }

    rv = pthread_mutex_destroy(&bridge.mutex);
    check_pthread_return(rv, "pthread_mutex_destroy");
    rv = pthread_cond_destroy(&bridge.cond_east);
    check_pthread_return(rv, "pthread_cond_destroy");
    rv = pthread_cond_destroy(&bridge.cond_west);
    check_pthread_return(rv, "pthread_cond_destroy");

    return 0;
}

void print_help(void)
{
    char * helpmsg =
    	"Usage: ./bridge [options]\n"
        "-w<N>    number of westbound cars (default:5).\n"
        "-e<N>    number of eastbound cars (default:5).\n"
        "-t<N>    number of trips each car makes (default:10).\n"
        "-m<N>    max number of cars on the bridge (default:2).\n"
        "-c<N>    max number of cars that can cross the bridge in a phase,\n"
        "         if a car in opposite direciton is waiting. (default:4)\n"
        "-se<N>   seed for eastbound cars (default:3100).\n"
        "-sw<N>   seed for westbound cars (default:3100).\n";
    fprintf(stderr, "%s", helpmsg);
    exit(EXIT_FAILURE);
}

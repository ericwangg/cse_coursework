/*
 ** server.c -- a stream socket server demo
 */

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <sys/wait.h>
#include <signal.h>
#include <time.h>
#include <pthread.h>

/***** socket io functions *****/

#include "socketio.c"

void die(char *s)
{
    if (errno)
        perror(s);
    else
        fprintf(stderr, "Error: %s\n", s);
    exit(EXIT_FAILURE);
}

void check_pthread_return(int rv, char *msg)
{
    if (rv == 0)
        return;
    errno = rv;
    die(msg);
}

/***** Applicaton specific section *****/

#define BUF_SIZE    1024

#define SZ_MOVIE_TITLE  80
#define NUM_MOVIES      5
#define DEFAULT_NUM_TICKETS 50

/* global variables to keep track the number of concurrent connections. */
int g_num_connected = 0;
int g_max_connected = 0;
pthread_mutex_t g_mutex = PTHREAD_MUTEX_INITIALIZER;

void new_connection()
{
    pthread_mutex_lock(&g_mutex);
    g_num_connected ++;
    if (g_num_connected > g_max_connected)
        g_max_connected = g_num_connected;
    pthread_mutex_unlock(&g_mutex);
} 

void close_connection()
{
    pthread_mutex_lock(&g_mutex);
    g_num_connected --;
    pthread_mutex_unlock(&g_mutex);
}

typedef struct movie_t_tag {        // a movie 
    int qty;            //number of the tickets available for this movie
    char title[SZ_MOVIE_TITLE];    //title of the movie
} movie_t;

typedef struct moviedb_t_tag {
    movie_t  movies[NUM_MOVIES];
    // TODO 
    // add necessary fields here for synchronization
    // there is no need to protect individual movies
    pthread_rwlock_t rwlock;		// read write locks most appropriate over barrier, etc.
} moviedb_t;

// global variable
moviedb_t   g_mdb;

/* initialize movie database mdb. */
void mdb_init (moviedb_t *mdb, int num_tickets)
{
    char * titles[NUM_MOVIES] = {
        "Mutex traps",
        "Nightmare of pointers", 
        "Return of recursion",
        "Revenge of pipes", 
        "A socket's life", 
    };

    movie_t *movies = mdb->movies;

    for (int i = 0; i < NUM_MOVIES; i ++) {
        strcpy(movies[i].title, titles[i]);
        movies[i].qty = num_tickets;
    }

    // TODO
    // initialzie any variables used for synchronization
    int rv = pthread_rwlock_init(&mdb->rwlock, NULL);
    // check return value of pthread functions with check_pthread_return()
    check_pthread_return(rv, "rwlock failed to init");
    
}

/* clean up 
 * actually, this function is not called in this program */ 
void mdb_destroy(moviedb_t *mdb)
{
	free(mdb);
}


/* This function compiles the movie info message 
 * into the buffer specified. The buffer has buf_sz bytes.
 * The movie info has a terminating NUL.
 *
 * Note that the movie info message only lists movies that have tickets. 
 *
 * The buffer should be enough. If the buffer is too small, 
 * call die() to terminate the process.
 *
 * If any pthread synchronization function is called, 
 * check return value of pthread functions with check_pthread_return().
 * 
 * Return values:
 *   0: success
 *  -1: all movies are sold out
 *  */
int mdb_get_movie_info(moviedb_t *mdb, char *buf, size_t buf_sz)
{
    // TODO
    movie_t * m = mdb->movies;
    size_t buffer_size = BUF_SIZE;
    int state = 0, msg;
    
    pthread_rwlock_rdlock(&mdb->rwlock);
    
    for(int i = 0; i < NUM_MOVIES; i++){
    	if(sizeof(buf) > buf_sz){		// if the buffer is too small, shouldn't ever happen
	    	die("overflow in buffer size\n");
	    }
	    else if(m[i].qty >= 1){			// if the movie is sold out 
	    	msg = snprintf(buf, buffer_size, "%d. %s (%d)\n", i, m[i].title, m[i].qty);	
	    	if(msg < 0){
	    		die("snprinft() failed\n");
	    	}
	    	buffer_size -= msg;
	    	buf += msg;
	    	state = 1;
	    }
    }
	pthread_rwlock_unlock(&mdb->rwlock);
	
	if (state == 0){
		return -1;
	}
    return 0;
}

/* Buy qty tickets for movie id
 *
 * call check_pthread_return() to check the return value of pthread functions.
 * If there is an error, the process is terminated.
 *
 * Return values:
 *  0:  success.
 * -1:  id is invalid (out of range).
 * -2:  not enough tickets.
 *  */
int mdb_buy_ticket(moviedb_t *mdb, int id, int qty)
{
    int rv = 0; 

    if (id < 0 || id >= NUM_MOVIES)
        return -1;

    // TODO:
    //      Add necessary synchronization mechanism
    // EW: added write lock/unlock
    pthread_rwlock_wrlock(&mdb->rwlock);

    if (mdb->movies[id].qty >= qty) {
        int tmp = mdb->movies[id].qty;
        tmp -= qty;
        usleep(50);
        mdb->movies[id].qty = tmp;
    } else {
        rv = -2;
    }
    
	pthread_rwlock_unlock(&mdb->rwlock);
    return rv;
}

typedef struct thread_arg_tag {
    int sockfd;
    moviedb_t   * mdb;            // movie database
} thread_arg_t;

void thread_die(thread_arg_t *arg)
{
    close_connection();
    printf("server: thread using socket fd %d exiting ...\n", arg->sockfd);
    close(arg->sockfd);
    free(arg);
    pthread_exit(NULL);
}

// my_assert() is not fatal to process
#define my_assert(a)  do {if(!(a)){fprintf(stderr,"Error: line %d\n", __LINE__);thread_die(arg);}} while(0)

enum message_id_tag {M_WELCOME, M_PROMPT, M_SOLDOUT, M_CONFIRM, M_E_MOVIEID, M_E_QTY, M_E_FORMAT, M_E_MAX};

/* send a message to client. 
 *
 * The message is specified by msg_id, which is one of enumerate value
 * defined above.  
 *
 * The function returns the return value from send_str().
 *
 * */
int send_message(int sockfd, int msg_id)
{
    char *msgs[] = {
        "Welcome! NOT USED.\n",
        "Please select a movie and specify the number tickets you like (e.g., 1 2):\n",
        "All tickets are sold out. Please come back tomorrow.\n",
        "Thank you! You are all set. Enjoy the movie.\n",
        "Error: we did not find the movie you asked.\n",
        "Error: there are not enough tickets.\n",
        "Error: we could not understand your request.\n",
        "Error: we have technical issues.\n",
    };

    if (msg_id < 0 || msg_id > M_E_MAX)
        msg_id = M_E_MAX;
    return send_str(sockfd, msgs[msg_id]); 
} 

/*  The main function of the thread handling the client.
 * 
 *  use my_assert() to check the return value of socket 
 *  related function. See the code for sending movie
 *  info, prompt, and soldout messages. 
 *  The errors are fatal to the thread, but not to the process. 
 * */
void * thread_main(void * arg_in)
{
    thread_arg_t *arg = arg_in;
    int sockfd = arg->sockfd; 
    moviedb_t * mdb = arg->mdb;
    char buf[BUF_SIZE];

    int rv = mdb_get_movie_info(mdb, buf, BUF_SIZE);

    if (rv == 0) {
        // send movie list
        rv = send_str(sockfd, buf);
        printf("buf = \n %s\b", buf);
        my_assert(rv == 0);
        // sometimes, we add a little delay 
        if (strlen(buf) & 1)
            usleep(10);
        rv = send_message(sockfd, M_PROMPT);
        printf("M_PROMPT\n");
        my_assert(rv == 0);
    } else {
        rv = send_message(sockfd, M_SOLDOUT);
        my_assert(rv == 0);
		printf("M_SOLDOUT\n");
        // terminate the thread 
        thread_die(arg);
    }

    // TODO
    // Continue to complete the rest of the protocol
    //movie_t * movies = mdb->movies;
    char buf_2[BUF_SIZE]; // new buffer to avoid overwriting, conflicts, etc.
    int mov_id, tix_qty;
    int kiosk_order = recv_lines(sockfd, buf_2, BUF_SIZE);	
    
    if(kiosk_order){
    	close(sockfd);
        die("Received no order from kiosk client (recv_lines failed.)\n");
    }
    my_assert(kiosk_order == 0);
    
    // if sccanf doesn't receive 2 #s for movid id and ticket quantity
    if(sscanf(buf_2, "%d %d\n", &mov_id, &tix_qty) != 2){		
    	send_message(sockfd, M_E_FORMAT);	// failure, cannot understand kiosk input
    	//printf("M_E_FORMAT");
    	close(sockfd);
    	pthread_exit(NULL);
    }
    
    //else if(recv_lines(sockfd, buf, BUF_SIZE) == 0){
    int order = mdb_buy_ticket(mdb, mov_id, tix_qty);
	if(order == 0){				// success, send confirm message
		my_assert(send_message(sockfd, M_CONFIRM) == 0);
		//printf("M_CONFIRM");
		//thread_die(arg);
	}
	else if(order == -1){		// failure, bad movie id
		my_assert(send_message(sockfd, M_E_MOVIEID) == 0);
		//printf("M_E_MOVIEID");
		//thread_die(arg);
	}
	else if(order == -2){		// failure, not enough tickets
		my_assert(send_message(sockfd, M_E_QTY) == 0);
		//printf("M_E_QTY");
		//thread_die(arg);
	}
    
    thread_die(arg);
    return NULL;
    
    
}

/* create a thread to talk to the client.
 *
 * Return values:
 * 0:   success
 * -1:  error. new_fd is not closed.
 * */
int create_handler(int new_fd, moviedb_t *mdb) 
{
    pthread_t   tid;
    int     rv;

    thread_arg_t * arg = malloc(sizeof(thread_arg_t));

    if (arg == NULL)
        return -1; 

    arg->sockfd = new_fd;
    arg->mdb = mdb;

    rv = pthread_create(&tid, NULL, thread_main, arg);
    if (rv) {
        free(arg);
        return -1;
    }

    // not much we can do if it fails. could just kill the process.
    pthread_detach(tid);
    return 0;
}

/***** Applicaton specific section *****/

#define PORT "3129"  // the port users will be connecting to
#define BACKLOG 20	 // how many pending connections queue will hold

// get sockaddr, IPv4 or IPv6:
void *get_in_addr(struct sockaddr *sa)
{
    if (sa->sa_family == AF_INET) {
        return &(((struct sockaddr_in*)sa)->sin_addr);
    }

    return &(((struct sockaddr_in6*)sa)->sin6_addr);
}

int main(int argc, char * argv[])
{
    int sockfd, new_fd;  // listen on sock_fd, new connection on new_fd
    struct addrinfo hints, *servinfo, *p;
    struct sockaddr_storage their_addr; // connector's address information
    socklen_t sin_size;
    int yes=1;
    int rv;
    int num_tickets = DEFAULT_NUM_TICKETS;

    for (int i = 1; i < argc; i++) {
        if (! strncmp(argv[i], "-t", 2) && isdigit(argv[i][2])) {
            num_tickets = atoi(&argv[i][2]);
            if (num_tickets == 0)
                die("number of tickets must be positive");
        }
    }

    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags = AI_PASSIVE; // use my IP

    if ((rv = getaddrinfo(NULL, PORT, &hints, &servinfo)) != 0) {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
        return 1;
    }

    // loop through all the results and bind to the first we can
    for(p = servinfo; p != NULL; p = p->ai_next) {
        if ((sockfd = socket(p->ai_family, p->ai_socktype,
                        p->ai_protocol)) == -1) {
            perror("server: socket");
            continue;
        }

        if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &yes,
                    sizeof(int)) == -1) {
            perror("setsockopt");
            exit(1);
        }

        if (bind(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
            close(sockfd);
            perror("server: bind");
            continue;
        }

        break;
    }

    freeaddrinfo(servinfo); // all done with this structure

    if (p == NULL)  {
        fprintf(stderr, "server: failed to bind\n");
        exit(1);
    }

    if (listen(sockfd, BACKLOG) == -1) {
        perror("listen");
        exit(1);
    }

    printf("server: waiting for connections on port %s...\n", PORT);

    mdb_init(&g_mdb, num_tickets);

    while(1) {  // main accept() loop
        sin_size = sizeof their_addr;
        new_fd = accept(sockfd, (struct sockaddr *)&their_addr, &sin_size);
        if (new_fd == -1) {
            perror("accept");
            continue;
        }

        // call a function to create a thread to deal with the client 
        new_connection();
        printf("server: new connection. max=%d fd=%d\n", g_max_connected, new_fd);
        if (create_handler(new_fd, &g_mdb)) {
            close(new_fd);
        }
    }

    return 0;
}

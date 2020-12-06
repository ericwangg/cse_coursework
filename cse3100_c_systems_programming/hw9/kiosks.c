#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <ctype.h>
#include <netdb.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <time.h>
#include <pthread.h>

#include <arpa/inet.h>

#define DEFAULT_PORT "3129" // the port client will be connecting to 

/*************  macros related to random numbers for MT ****************/
// Use functions in POSIX.1-2001.
__thread unsigned short g_random_buffer[3];

// Use the following macro in your thread function before any calls to get random values.
#define RANDOM_INIT(x)  (g_random_buffer[0]=3100,g_random_buffer[1]=(x), g_random_buffer[2] = (x) >> 16)

// RANDOM_INT() returns a random number uniformly distributed between [0, 2^31)
#define RANDOM_INT() (nrand48(g_random_buffer))

#define	WAITING()	my_msleep(RANDOM_INT()%20)
#define	THINKING()	my_msleep(RANDOM_INT()%50)
#define	GET_NUM_TICKETS()	((RANDOM_INT() % 4)+1)
#define	SELECT_MOVIE(n)	        ((RANDOM_INT() % (n)))

void my_msleep(int r)
{
    struct timespec req = {0, (r % 100 + 1) * 1000000};

    nanosleep(&req, NULL);
}

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

#include "socketio.c"

#define	LINE_SIZE   1024
#define NUM_MOVIES  5

typedef struct {
    int id;
    int seed;
    int opt_wait;
    int opt_think;
    char *hostname;
    char *port;
    int movie_id;
    int num_tickets;
} kiosk_t;

/* This function buys ticket for a group.
 *      connect to server
 *      follow the protocol
 *      close the socket
 *
 * If purchase is successful, kk->movie_id and kk->num_tickets
 * are the movie ID and the number of tickets, respecively.
 *
 * Return values:
    0:  success
   -1:  communication error
   -2:  all tickets are sold out
   -3:  server returns an error message
*/

#define M_WELCOME	"Welcome! NOT USED.\n"
#define M_PROMPT	"Please select a movie and specify the number tickets you like (e.g., 1 2):\n"
#define M_SOLDOUT	"All tickets are sold out. Please come back tomorrow.\n"
#define	M_CONFIRM	"Thank you! You are all set. Enjoy the movie.\n"
#define M_E_MOVIEID	"Error: we did not find the movie you asked.\n"
#define	M_E_QTY		"Error: there are not enough tickets.\n"
#define M_E_FORMAT	"Error: we could not understand your request.\n"
#define M_E_MAX		"Error: we have technical issues.\n"

int buy_tickets(kiosk_t * kk)
{
    int sockfd;
    struct addrinfo hints, *servinfo, *p;
    int rv;

    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    if ((rv = getaddrinfo(kk->hostname, kk->port, &hints, &servinfo)) != 0) {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
        return -1;
    }

    // loop through all the results and connect to the first we can
    for(p = servinfo; p != NULL; p = p->ai_next) {
        if ((sockfd = socket(p->ai_family, p->ai_socktype,
                        p->ai_protocol)) == -1) {
            perror("client: socket");
            continue;
        }

        if (connect(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
            perror("client: connect");
            close(sockfd);
            continue;
        }
        break;
    }

    if (p == NULL) {
        fprintf(stderr, "client %d: failed to connect\n", kk->id);
        return -1;
    }

    freeaddrinfo(servinfo); // all done with this structure

    char buf[LINE_SIZE];
    int mid[NUM_MOVIES];  //array to store movie IDs in movie info message 
    int num_movies = 0;

    //TODO
    //  receive movie info message (or soldout message)
    //  find out the number of movies available
    //  call THINKING() to think if kk->opt_think is non-zero
    //      if (kk->opt_think) THINKING();
    //  randomly pick a movie and the number of tickets
    //  send order message
    //  wait for confirmation or error messages
    
    char prompt_buf[LINE_SIZE];
    rv = recv_lines(sockfd, buf, LINE_SIZE);
    if(rv){
    	printf("rv() failed\n");
    }
    if(strncmp(buf, "Error", 5)  == 0){
    	return -3;
    }
    if(strcmp(buf, M_SOLDOUT) == 0){
    	return -2;
    }
    if(buf[strlen(buf) - 2] != ':' ){
    	rv = recv_lines(sockfd, prompt_buf, LINE_SIZE);
		strcat(buf, prompt_buf);
    }
    
    

    if( rv ){
    	close(sockfd);
    	die("Kiosk didn't receive move info\n");
    }
    printf("%s\n", buf);

    if(strcmp(buf, M_SOLDOUT) == 0){		// if string match
    		close(sockfd);
    		fprintf(stderr, M_SOLDOUT);
    		return -2;
    }

	int temp_mid;
    char * buf_top = buf;
    while( *buf_top != '\0'){
    	if(isdigit(*buf_top) != 0){
    		sscanf(buf_top, "%d", &temp_mid);
    		mid[num_movies] = temp_mid;
    		num_movies++;
    		while( *buf_top != '\n'){
    			buf_top++;				// push to end of line at \n
	    	}
	    	buf_top++;					// push over to next line
    	}
    	if(isalpha(*buf_top) != 0){		// check last line for M_PROMPT
    		break;						// finish loading
    	}
    }
    // for(int i = 0; i < num_movies; i++){
    // 	printf("mid = %d\n", mid[i]);
    // }
    // printf("num_movies = %d\n", num_movies);

	// if (kk->opt_think != 0) THINKING();

	int get_mov = mid[SELECT_MOVIE(num_movies)];
	int get_tix = GET_NUM_TICKETS();
	
	//fprintf(stdout, "\n\nselect_movie is %d\t\t", get_mov);
	//printf(stdout, "get_num_tickets is %d\n", get_tix);

	kk->movie_id = get_mov;
	kk->num_tickets = get_tix;

	int sel_movie = snprintf(buf, LINE_SIZE,  "%d %d\n", get_mov, get_tix);
	if(sel_movie < 0){
		die("snprintf() failed");
	}
	int kiosk_order = send_str(sockfd, buf);
	if(kiosk_order < 0){
		die("send_str() failed");
	}

	printf("kiosk buf back to server = \n %s\n", buf);
	
	//if(kk->opt_think != 0)	THINKING();
	THINKING();		// think again
	
	char buf_2[LINE_SIZE];
	if( recv_lines(sockfd, buf_2, LINE_SIZE) ){
		fprintf(stderr, "recv_lines failed() in return_buf\n");
    	exit(EXIT_FAILURE);
	}
	
	// EW: test prints
	//fprintf(stdout,"\n\nbuf is %s\n", buf);
	//printf("buf2 from server = \n %s\n ", buf_2);
	
	char * buf_top_2 = buf_2;
	
	if(!strncmp(buf, "Error", 5) ){
        close(sockfd);
        return -3;
    }
    close(sockfd);
    return 0;
}

void * thread_kiosk(void * arg_in)
{
    kiosk_t *kk = arg_in;

    int actual_seed = (kk->seed << 7) + kk->id; 
    RANDOM_INIT(actual_seed);

    int     rv = 0;
    int     group = 0;
    int     error_count = 0;

    while (rv != -2) {
        if (kk->opt_wait)
            WAITING();
        rv = buy_tickets(kk);
        if (rv == 0) 
            printf("Kiosk %d: group %d bought %d tickets for movie %d.\n", 
                kk->id, group, kk->num_tickets, kk->movie_id); 
        else if (rv == -2) 
            printf("Kiosk %d: all tickets are sold out.\n", kk->id);
        else if (rv == -3) 
            printf("Kiosk %d: order was not successful.\n", kk->id);
        else  {
            printf("Kiosk %d: group %d has communication errors.\n", kk->id, group);
            error_count ++;
            if (error_count == 3) {
                fprintf(stderr, "Error: persistent errors at kiosk %d. shutting down ...\n", kk->id); 
                exit(EXIT_FAILURE);
            }
            continue;
        }
        error_count = 0;
        group ++;
    }
    return NULL;
}

void print_help(void)
{
    char * helpmsg =
        "Usage: ./kiosks hostname [options]\n"
        "-s<N>    seed (default:3100).\n"
        "-n<N>    the number of threads (kiosks) (default:4).\n"
        "-W       do not wait before buy_tickets (default:wait).\n"
        "-T       do not think before sending order (default:think).\n"
        "hostname server to connect to (default: localhost).\n"
        "-h       print help message and exit.\n";
    fprintf(stderr, "%s", helpmsg);
    exit(EXIT_FAILURE);
}

int main(int argc, char *argv[])
{
    int i, n = 4;
    int seed;
    char * hostname = "localhost";
    char * port = DEFAULT_PORT;
    int opt_wait=1, opt_think=1;

    seed = 3100;

    for (i = 1; i < argc; i++) {
        if (! strncmp(argv[i], "-n", 2) && isdigit(argv[i][2])) {
            n = atoi(&argv[i][2]);
            if (n == 0)
                die("number of kiosks must be positive");
        } else if (! strncmp(argv[i], "-s", 2) && isdigit(argv[i][2])) {
            seed = atoi(&argv[i][2]);
            if (seed == 0)
                die("seed must be positive");
        } else if (! strcmp(argv[i], "-W")) {
            opt_wait=0;
        } else if (! strcmp(argv[i], "-T")) {
            opt_think=0;
        } else if (! strcmp(argv[i], "-h")) {
            print_help();
        } else {
            hostname = argv[i];
        }
    }

    int rv;

    pthread_t tid[n];
    kiosk_t kks[n];

    for (i = 0; i < n; i++) {
        kks[i] = (kiosk_t){i, seed, opt_wait, opt_think, hostname, port};
        rv = pthread_create(&tid[i], NULL, thread_kiosk, &kks[i]);
        check_pthread_return(rv, "pthread_create");
    }
    for(i = 0; i < n; i++) {
        rv = pthread_join(tid[i], NULL);
        check_pthread_return(rv, "pthread_join");
    }
    return 0;
}

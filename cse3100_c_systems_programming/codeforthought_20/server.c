//In this assignment, we implement a server that processes
//query requests from clients.
//An example of a query pattern is "z??e".
//A client sends a query pattern like the above to the server,
//and the server looks through all the words in a dictionary
//to find up to 100 words that match this pattern.
//And sends the results back to the client.
//The client will print the results on the screen.
//For example, the only word that matches the above pattern "z??e"
//is "zone". Note a "?" stands for one unknown letter.
  
//We use multi-threads to handle requests from clients.
//Each thread can handle one query client.
//The client code is given, we only need to implement the server.

//A client can send a pattern "bye" to indicate that no more queries.
//When "bye" is received by the server, the server will send "bye\n" to
//the client, and then close the scoket and terminate the thread.

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

#define PORT "3100"  // the port users will be connecting to

#define BACKLOG 10	 // how many pending connections queue will hold

#define MAX 100

#define MAX_WORD_COUNT 60000                //we have less than 60000 words
#define MAX_WORD_LENGTH 60                //each word is less than 80 letters

char words[MAX_WORD_COUNT][MAX_WORD_LENGTH];        //2-d array to hold all the words
int count = 0;                    //number of words, initilized to 0

void read_file_to_array(char *filename)
{
    FILE *fp;

    //open the file for reading
    fp = fopen("dict.txt", "r");
    if(fp==NULL)
    {
        printf("Cannot open the file.\n");
        exit(-1);
    }
    while(!feof(fp))
    {
        fscanf(fp, "%s\n", words[count]);
        count ++;
    }
    fclose(fp);
}


//test wether a word is in the array words
int is_word(char *word)
{
    //fill in the code below
    //return 1 if word is in the array words
    //otherwise, return 0
    for(int i = 0; i< count; i++)
    {
        if(!strcmp(words[i], word)) return 1;
    }
    return 0;
}
//check whether a word matches the pattern

int is_match(const char *pattern, const char *word)
{
	if(strlen(pattern) != strlen(word))
		return 0;
	//fill in the code below
	// EW: if at least one letter of the same index location is same, is true, return 1
	
	char word_reset[MAX_WORD_LENGTH];
	char pattern_reset[MAX_WORD_LENGTH];
	
	strcpy(word_reset, word);
	strcpy(pattern_reset, pattern);
	
	// char * match = strcmp(pattern_reset, word_reset);
	
	for(int i = 0; i < strlen(pattern_reset); i++){
		if( pattern_reset[i] == '?'){				// if character is unknown "?"
			;		// pass
		}
		else if((isalpha(word_reset[i]) != 0) && (isalpha(pattern_reset[i]) != 0)){
			if(word_reset[i] != pattern_reset[i]){
				return 0;		// if letter matches, therefore a pattern match
			}
		}
		else{
			;
		}
	}	
	return 1;
	// !strcmp(word_reset[i], pattern_reset[i]		
} 

//write up to no_limit matched words to results
//At the end of each matched word, a new line '\n' is added
//If no match, the results is ""
 
void matches(const char *pattern, char *results, int no_limit)
{
	int no = 0;
	strcpy(results, "");
	//fill in the code below 
	// EW: this code won't return anything, just copies matches to results
	
	//for(no; no < no_limit; no++){
	for(int i = 0; i < MAX_WORD_COUNT; i++){			// no "number", indexing
		if( is_match(pattern, words[i]) ){
			strcat(results, words[i]);
			strcat(results, "\n");
			
			no++;
		}
		if(no == no_limit){
			break;
		}
	}
}

// get sockaddr, IPv4 or IPv6:
void *get_in_addr(struct sockaddr *sa)
{
    if (sa->sa_family == AF_INET) {
        return &(((struct sockaddr_in*)sa)->sin_addr);
    }

    return &(((struct sockaddr_in6*)sa)->sin6_addr);
}

int create_handler(int new_fd);

int main(void)
{
    int sockfd, new_fd;  // listen on sock_fd, new connection on new_fd
    struct addrinfo hints, *servinfo, *p;
    struct sockaddr_storage their_addr; // connector's address information
    socklen_t sin_size;
    int yes=1;
    char s[INET6_ADDRSTRLEN];
    int rv;

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

    printf("server: waiting for connections...\n");

    read_file_to_array("dict.txt");

    while(1) {  // main accept() loop
        sin_size = sizeof their_addr;
        new_fd = accept(sockfd, (struct sockaddr *)&their_addr, &sin_size);
        if (new_fd == -1) {
            perror("accept");
            continue;
        }

        inet_ntop(their_addr.ss_family,
                get_in_addr((struct sockaddr *)&their_addr),
                s, sizeof s);

        // call a function to create a thread to deal with the client 
        fprintf(stderr, "server: got connection from %s. fd is %d.\n", s, new_fd);
        if (create_handler(new_fd)) {
            close(new_fd);
        }
    }

    return 0;
}

#include "socketio.c"

#define BUF_SIZE    1024

// Use a structure, although we hvae only one field
// It is easier to add more fields in other programs
typedef struct thread_arg_tag {
    int sockfd;
} thread_arg_t;

void thread_die(thread_arg_t *arg)
{
    printf("thread using socket fd %d exiting ...\n", arg->sockfd);
    close(arg->sockfd);
    free(arg);
    pthread_exit(NULL);
}

/* The main function of the thread handling the client.
 * */
void * thread_main(void * arg_in)
{
    thread_arg_t *arg = arg_in;
    int sockfd = arg->sockfd; 
    int rv;

    char pattern[BUF_SIZE];
	char response[MAX*(MAX_WORD_COUNT + 1)];	

	int done = 0;
	do
	{	
		rv = recv_lines(sockfd, pattern, BUF_SIZE);
		if (rv < 0) thread_die(arg);

		//remove the new line at the end
		pattern[strlen(pattern)-1] = '\0';
		printf("received pattern: %s\n", pattern);
		if(!strcmp(pattern, "bye"))
		{
			strcpy(response, "bye\n");	
			done = 1;	
		}
		else
		{
			matches(pattern, response, MAX);
			if(strlen(response) == 0)
			{
				strcpy(response, "No matches found.\n");
			}
		}
		rv = send_str(sockfd, response);
		if (rv < 0) thread_die(arg);
	}while(!done);
	thread_die(arg);
	return NULL;
}

/* create a thread to talk to the client.
 *
 * Return values:
 * 0:   success
 * -1:  error. new_fd is not closed.
 * */
int create_handler(int new_fd) 
{
    pthread_t   tid;
    int     rv;

    thread_arg_t * arg = malloc(sizeof(thread_arg_t));

    if (arg == NULL)
        return -1; 

    arg->sockfd = new_fd;

    rv = pthread_create(&tid, NULL, thread_main, arg);
    if (rv) {
        free(arg);
        return -1;
    }

    // not much we can do if it fails. could just kill the process.
    pthread_detach(tid);
    return 0;
}

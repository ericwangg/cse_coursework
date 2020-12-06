//client
 
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <netdb.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <time.h>

#include <arpa/inet.h>

#define PORT "3100" // the port client will be connecting to 

#define MAX 60

// get sockaddr, IPv4 or IPv6:
void *get_in_addr(struct sockaddr *sa)
{
    if (sa->sa_family == AF_INET) {
        return &(((struct sockaddr_in*)sa)->sin_addr);
    }

    return &(((struct sockaddr_in6*)sa)->sin6_addr);
}

#include "socketio.c"

#define	LINE_SIZE	10000

void print_lines(int sid, char * buf, int n)
{
    if (recv_lines(sid, buf, n) == -1) {
        fprintf(stderr, "recv_line returned -1.\n");
        exit(EXIT_FAILURE);
    }
    printf("%s", buf);
}

int main(int argc, char *argv[])
{
    int sockfd;
    char buf[LINE_SIZE];
    struct addrinfo hints, *servinfo, *p;
    int rv;
    char s[INET6_ADDRSTRLEN];

    if (argc != 2) {
        fprintf(stderr,"usage: client hostname\n");
        exit(1);
    }

    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    if ((rv = getaddrinfo(argv[1], PORT, &hints, &servinfo)) != 0) {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
        return 1;
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
        fprintf(stderr, "client: failed to connect\n");
        return 2;
    }

    inet_ntop(p->ai_family, get_in_addr((struct sockaddr *)p->ai_addr),
            s, sizeof s);
    printf("client: connecting to %s\n", s);

    freeaddrinfo(servinfo); // all done with this structure

    char pattern[MAX];
	int done = 0;	
	
	do
	{
		fgets(pattern, MAX, stdin);
		if(!strcmp(pattern, "bye\n")) done = 1;
    	rv = send_str(sockfd, pattern);
    	if(rv < 0)
    	{
        	close(sockfd);
        	perror("send");
        	exit(-1);
		}

    	rv = recv_lines(sockfd, buf, LINE_SIZE);
    	if (rv < 0)
		{
			close(sockfd);
			perror("recv");
        	exit(-1);
		}

		printf("%s", buf);
	}while(!done);
    close(sockfd);

    return 0;
}


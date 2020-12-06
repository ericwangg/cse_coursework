//In this assignment, we practice dup2() and fork().
//The main() function takes a command line argument.
//In the main() function we use fork() to create a
//child process. The child process redirects the
//standard output to a file named "output.txt" using dup2().
//Moreover, it prints out the command line argument in capital letters.
//The parent process simply prints out the command line argument. 

#include <stdio.h> 
#include <stdlib.h>
#include <string.h>
#include <unistd.h> 
#include <fcntl.h> 
#include <ctype.h> 
#define MAX_LINE 1024

int main(int argc, char *argv[])
{

	if(argc!=2)
	{
		printf("Usage: %s message\n", argv[0]);
		return -1; 
	}
    pid_t pid;
    pid = fork();
    if(pid == 0)
    {

		//Make sure when the file is created, the user has the read and write access 
		int fd = open("output.txt", O_WRONLY | O_CREAT, S_IRUSR | S_IWUSR); 
		if(fd < 0)
		{ 
			printf("Cannot open the file\n");
			return -1;
		} 
        char buffer[MAX_LINE];
        strcpy(buffer, argv[1]);
		//TODO
		//fill in the code below
		
		// EW: strcpy copied arv[1] command over to buffer string
		int i = 0;
		// char arr[MAX_LINE];						// copy array
		// while(buffer[i]){
		// 	arr[i] = toupper(buffer[i]);			// to upper makes uppercase
		// 	printf("%c", arr[i]);					// also works, creates redundant arr
		// 	i++;
		// }
		dup2(fd, 1);	// EW: duplicating from the buffer to the open file at fd
		while(buffer[i]){
			buffer[i] = toupper(buffer[i]);
			printf("%c", buffer[i]);
			i++;
		}
		printf("\n");
		close(fd);
		exit(0);
	}
	printf("%s\n", argv[1]);
	return 0;
} 

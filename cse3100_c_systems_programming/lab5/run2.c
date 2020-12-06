#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main(int argc, char ** argv)
{
    // pid_t child;			// EW: comment out, require 2
    // int exitStatus;		// EW: likewise for exitStatus here, will require 2

    // at least, there should be 3 arguments
    // 2 for the first command, and the rest for the second command
    if (argc < 4) {
        fprintf(stderr, "Usage: %s cmd1 cmd1_arg cmd2 [cmd2_args ..]\n", argv[0]);
        return 1;
    }

    // TODO
    pid_t child_1 = fork();			// child 1
    if(child_1 < 0){					// if there is a forking error
    	perror("fork()");			// error reporting!
    	exit(1);					// and exit outta there
    }
	else if(child_1 == 0){			// child process created
		int err_1 = execlp(argv[1], argv[1], argv[2], NULL);					
									// err_1 holds the first error value
									// execlp runs the 1st program
		if(err_1 == -1){
			perror("execlp()");		// error reporting!
			exit(1);				// and then get outta there lol
		}
	}
	else{
		int exitStatus_1;			// create a exit save spot
		int deadChild_1 = waitpid(child_1, &exitStatus_1, 0);
									// waitpid waits for the first child process to finish first
		if(deadChild_1 != child_1){
			perror("waitpid()");
		}
		else{
			printf("exited=%d exitstatus=%d\n", WIFEXITED(exitStatus_1), WEXITSTATUS(exitStatus_1));
		}
		pid_t child_2 = fork();
		if (child_2 < 0){
			perror("fork()");		// error reporting!
			exit(1);				// exit
		}
		else if(child_2 == 0){
			char** skip = argv + 3;	// go directly to argv[3] without having to use for loop
			execvp(argv[3], skip);	// increment base address by 3 when taking in 2nd program
			perror("execvp()");		// report error on execvp()
			exit(1);				// exit
			
		}
		int exitStatus_2;		// exit Status 2
		int deadChild_2 = waitpid(child_2, &exitStatus_2, 0);		// idk what to do here lol, mirror deadChild_1?
    	if(deadChild_2 != child_2){
    		perror("waitpid()");
    	}
    	else{
    		printf("exited=%d exitstatus=%d\n", WIFEXITED(exitStatus_2), WEXITSTATUS(exitStatus_2));
    	}
    // wait til 1st one, then fork for 2nd one
    
	// pid = fork();
	// if(pid == -1){
    }
    return 0;
}

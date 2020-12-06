//In this practice exam, we use multiple processes to simulate a word game named hangman.
//In the original hangman game, the number of guesses are limited and some graphical display of a hangman 
//is involved to indicate the progress of the game.
//We simplify the game to not to draw a hangman, and not limit the number of guesses.
//The simplified game works as follows.
//Player one chooses a word and indicates the length of the word
// and let the second player to guess the word. For example, the first player
// shows the following string to indicate that the word has 4 letters.
// ----
//The player two suggests a letter, for example, the letter 'e'. 
//The player one responses by displaying the correct guess at the right places in the word. 
//For example, player one tells player two the following string
// --ee
//Player two suggests another letter, a letter 'f' this time.
//The player one displays the same string
// --ee
//This is because the letter 'f' is not in the word.
//Player two suggests another letter 't'.
//The first player displays
// t-ee
//Then the second player suggests another letter 'r'.
//Player one displays
// tree
//Now since all the hidden letters are displayed. The game is over.
//In this practice exam, we need to use two processes to simulate the two players.
//Also, we need to use pipes for the communications between the two players.
//To be more specific, the child process is player one; the parent process is player two.
//A user will type guesses from the standard input to play the game. 

// Search TODO to find the location where the code needs to be completed.

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <assert.h>
#include <sys/wait.h>
#include <errno.h>
#include <ctype.h>

#define     PFD_READ    0
#define     PFD_WRITE   1

#define MAX_WORD_COUNT 60000              //we have less than 60000 words
#define MAX_WORD_LENGTH 80                //each word is less than 80 letters

void die(char *s)
{
    if (errno)
        perror(s);
    else
        fprintf(stderr, "Error: %s\n", s);
    exit(EXIT_FAILURE);
} 

char words[MAX_WORD_COUNT][MAX_WORD_LENGTH];        //2-d array to hold all the words
int count = 0;                    //number of words, initilized to 0

//read words from the file to the array words declared above
//also update the number of words (update variable count)
//We could have avoided using global variables. Try to revise it yourself.
void read_file_to_array(char *filename)
{
    FILE *fp;

    //open the file for reading
    fp = fopen(filename, "r");
    if(fp==NULL)
        die("Cannot open the word list file.");

    // TODO
    
    // EW: could be done with while loop (count < MAX_WORD_COUNT), then count ++
    // EW: perform same words adding to arr[count][for loop to increment i per count]
    
    // char fullword[MAX_WORD_LENGTH];
    // for(int i = 0; i < MAX_WORD_COUNT; i++){
    // 	for(int j = 0; j < MAX_WORD_LENGTH; j++){
    // 		//fullword = fgets(length, sizeof(length), fp);
    // 		fscanf(fp, "%s", fullword);
    // 		char * subword = strtok(fullword, "");
    // 		while(subword != NULL){
    // 			words[i][j] = &subword;
    // 		}
    // 	}
    // 	count ++;
    // }
    
   
    while(fscanf(fp, "%79s", words[count]) == 1){
    	count++;
    }
    
    // while(fgets(length, sizeof(length), fp) != NULL){	// keeps while looping before end of file
    // 	for(int i = 1; i < MAX_WORD_COUNT; i++){
    // 		fgets(fp, str);
    // 		words[count][];
    // 		count++;
    // 	}
    // }
    
    // make sure when each word is saved in the array words,
    // There is no white space in words, we can use fscanf().
    // We could also use fgets(). Need to remove '\n' at the end.
    fclose(fp);    
}

// write a character to a pipe
void write_char(int pd, char value)
{
    if (write(pd, &value, sizeof(char)) != sizeof(char))
        die("write()");
}

// write a string to FD pd , add '\n' at the end
void write_word(int pd, char *word)
{
    size_t len = strlen(word);

    if (write(pd, word, len) != len)
        die("write()");
    write_char(pd, '\n');
}

// read a char from FD pd and save the result in *pc 
// return the return value from read()
int read_char(int pd, char *pc)
{
    return read(pd, pc, sizeof(char));
}

// read a line from FD pd 
//
void read_word(int pd, char buffer[], int sz)
{
    char c;
    int count = 0;

    while (read_char(pd, &c) > 0)
    {
        if (count >= sz) 
           die("line is too long in read_word()."); 
        if (c == '\n') {
            buffer[count] = 0;
            return;
        }
        buffer[count ++] = c;
    }
    // could handle error better
    die("read() failed in read_word");
}

//check if the character guess is in the word
//if it is in the word, update the string so_far in the right places
//for example, if guess is 'e', so_far is "----", and word is 'tree'
//then so_far will be updated to be '--ee'
//if guess is 't', so_far is '--ee', and word is 'tree'
//then so_far will be updated to be 't-ee' 
// Return value:
// 0:   guess is not in the word
// 1:   guess is in the word
int check_guess(char guess, char *so_far, const char *word)
{
    // TODO 
    				// the amount of times the guess character shows up in the word 
    for(int i = 0; i < (strlen(word)); i++){		// string is 0 to length - 1
    	count = 0;
    	if(word[i] == guess){							// if the character == guess character
    		so_far[i] = guess;							// update so far word array with guess
    		count++;
    	}
    }
    if(count == 0){		// if the guess if found 0 times in the word, return 0
    	return 0;
    }
    else{				// otherwise guess is in the word
    	return 1;
    }
}

int main(int argc, char* argv[]) 
{

    if(argc!= 2)
    {
        printf("Usage: %s seed\n", argv[0]);
        return -1;
    }
    int seed = atoi(argv[1]);
    assert(seed > 0);

    int pdp[2];
    //pipe creation
    if(pipe(pdp) == -1)
    {
        perror("Error.");
        return -1;
    }

    int pdc[2];
    //pipe creation
    if(pipe(pdc) == -1)
    {
        perror("Error.");
        return -1;
    }

    pid_t pid;
    pid = fork();
    if(pid == 0)
    {
        // TODO
        //  close some file descriptors
        
        // EW: parent guesses letters, needs to write to pipe
        // EW: child  takes the input from parent, reads from pipe
        // close child read and parent write ones we don't use
        if(close(pdp[1]) == -1){		// pipe descriptor parent read
        	perror("close() failed");
        }
        if(close(pdc[0]) == -1){		// pipe descriptor parent read
        	perror("close() failed");
        }

        // read the list in child process
        read_file_to_array("dict.txt");

        char *my_word;
        char so_far[MAX_WORD_LENGTH];

        srand(seed);
        my_word = words[rand() % count];
        fprintf(stderr, "Child: debugging: the word is %s\n", my_word);

        // Note that so_far should have enough space
        size_t  len = strlen(my_word);
        for(int i = 0; i<len; i++)
            so_far[i] = '-';
        so_far[len] = 0;

        //TODO
        //repeatly doing the following
        //      send so_far to parent
        //      receive a guess (a character) from parent
        //      exit from the loop if it was not successful
        //      check_guess
        
        
        char guess;						// place holder for guess for now
        while(1){
        	write_word(pdc[1], so_far);
        	int readGuess = read_char(pdp[0], &guess);
        	if(readGuess != 1){
        		break;
        	}
        	else{
        		int guessCheck = check_guess(guess, so_far, my_word);
        		// if(guessCheck == 0){		// if guessCheck is found to be the right word
        		// 	break;					// exit loop
        		// }
        	}
        	
        }
        
        //Do some clean up before exit from the process
        
        if(close(pdp[0]) == -1){		// pipe descriptor parent read
        	perror("close() failed");
        }
        if(close(pdc[1]) == -1){		// pipe descriptor parent read
        	perror("close() failed");
        }
        exit(EXIT_SUCCESS);
        return 0;
    }
    else
    {
        char guess;
        char so_far[MAX_WORD_LENGTH];

        // TODO
        // close some file descriptors
        
        // EW: the other 2 file descript that were used, but now done using
        
        // close(pdc[PFD_READ]);		// pipe descriptor parent write 
        // close(pdp[PFD_READ]);		// pipe descriptor parent read
        // close(pdc[PFD_WRITE]);		// pipe descriptor child write 
        // close(pdp[PFD_WRITE]);		// pipe descriptor child read
        
        if(close(pdc[1]) == -1) die("close failed");
        if(close(pdp[0]) == -1) die("close failed");

        
        // Then do the following in a loop:
        //      read a word from child 
        //      print it to stdout
        //      if there is no '-', exit from the loop
        //      read a character from stdin until a ltter is found
        //      report error if EOF found.
        //      turn the character to lower case
        //      send it to child
        while(1){
        	read_word(pdc[0], so_far, MAX_WORD_LENGTH);
        	//fprintf(stdout, "%d\n", readChar);
        	printf("%s\n", so_far);
        	if(strchr(so_far, '-') == NULL){	// does not have "-" ASCII #45 in word, exit
        			break;						// exit loop 
        		}
        	while(1){
        		if(scanf("%c", &guess) == 1){
        			if(guess == EOF){
        				die("scanf() failed");
        			}
        			if(isalpha(guess)){
        				break;
        			}
        		}
        	}
        	if (guess >= "A" && guess <= "Z"){
        		guess += 32;
        	}
        	write_char(pdp[1], guess);
        }
        
        // if(close(pdc[0]) == -1){
        // 	die("close failed");
        // }
        // if(close(pdp[1]) == -1){
        // 	die("close failed");
        // }
      
        if(close(pdp[1]) == -1) die("close failed");
        if(close(pdc[0]) == -1) die("close failed");
        
        exit(EXIT_SUCCESS);
        // close file descriptors before exit from the process

    //wait for the child process to finish
    waitpid(pid, NULL, 0);
    return 0;
    }
}

//below is a sample output
//it can also be found in the file sample-output.txt
/*
   ./hangman 8
   To help debugging: the word is pride
   -----
   e
   ----e
   a
   ----e
   t
   ----e
   i
   --i-e
   r
   -ri-e
   p
   pri-e
   d
   pride
   The word is pride.
   */

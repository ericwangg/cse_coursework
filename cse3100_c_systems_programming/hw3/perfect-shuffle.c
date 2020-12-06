#include    <stdio.h>
#include    <stdlib.h>

// return the number of perfect shuffles that place a deck of n cards back to original order
// n must be positive
int find_cycle(int n){
    // TODO
    // Memory pointer method instead
    if (n == 1){			// 1 card check
    	return 1;
    }
    int     count = 0;		// 
    int		deck[n];		// deck of "n" cards
    int		newdeck[n];		// new deck to add to and work with
    int		i;				// new deck to deal with
    int 	leftdeck[(n/2)+(n%2)];	// left deck, takes the extra odd card always
    int		rightdeck[(n/2)];		// right deck
    for(i = 0; i < n; i++){	// putting values both deck and the newd deck
    	deck[i] = i;		// use for loops for no matter the amount of cards
    	newdeck[i] = i;
    }

	// for(int x = 0; x < n; x++){
	// 	printf("%d ", deck[x]);
	// }
    
    // test for run regardless of odd or even # of cards
    
    // perform first shuffle, check if deck[1] == newdeck[1]. 
    // If yes, return. If not keep shuffling until ^^^ becomes true. 
    
    while(1){								// while TRUE "1"
    	count++;							// increment the shuffle count
    	if(n % 2 != 0){						// check odd # of cards
    		for(int j = 0; j < ((n/2)+1); j++){		// 
    			leftdeck[j] = newdeck[j];
    			rightdeck[j] = newdeck[j + ((n/2)+1)];
    		}
    		for(int k = 0; k < n; k++){
    			if(k % 2 == 0){
    				newdeck[k] = leftdeck[k/2];
    			}
    			else{
    				newdeck[k] = rightdeck[k/2];
    			}
    		}
    		if (deck[1] == newdeck[1]){			// if the decks equate, give count
    			return count;
    		}
    	}
    	else{								// check even # of cards
    		for(int j = 0; j < (n/2); j++){
    			leftdeck[j] = newdeck[j];
    			rightdeck[j] = newdeck[(n/2) + j];
    		}
    		for(int k = 0; k < n; k++){
    			if(k % 2 == 0){					// COPIED FROM ODD ARRAY OP, 
    				newdeck[k] = leftdeck[k/2];
    			}
    			else{
    				newdeck[k] = rightdeck[k/2];
    			}
    		}
    		if (deck[1] == newdeck[1]){		// if the decks equate, give count
    			return count;
    		}
    	}
	}
}


int main(int argc, char **argv)
{
    int     n;

    /* the upper bound of n is not checked. Try what happens if you enter a large number */
    if (argc == 1) {
        int     rv;
        while ((rv = scanf("%d", &n)) >= 0) {
            if (rv != 1 || n < 1) {
                printf("Number of cards must be a positive integer.\n");
                return 1;
            }
            printf("%d %d\n", n, find_cycle(n)); 
        }
    }
    else {
        for (int i = 1; i < argc; i ++) {
            n = atoi(argv[i]);
            if (n < 1) {
                printf("Number of cards must be a positive integer.\n");
                return 1;
            }
            printf("%d %d\n", n, find_cycle(n)); 
        }
    }
    return 0;
}

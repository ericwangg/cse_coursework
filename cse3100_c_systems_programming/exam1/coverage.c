#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#define     MAX_SIZE    99999

/***** Search TODO to find the function you need to work on ******/

// Return the coverage of the walker on an array.
//
// Parameters:
//      a:  starting address of an array
//      n:  number of unsigned int's in the array
// Return value:
//      the coverage of the walker 
double coverage (unsigned int a[], int n)
{
    // TODO Begin
    int num = 0;	// numerator, for the amount of indices that have been traversed
    int j = 0;	
    
    // for loop with variable "k" created to increment 
    for(int k = 0, k < n, k++){		
    	if(j == k){					// the node a[i] has been traversed before
    		return 	num / n;			// break out of the while loop to return the coverage ratio
    	}
    	else{					// else keep traversing and incrementing the coverage #/numerator
    		j = (i + a[i]) % n;
    		num++;
    	}
    }
}

/***** do not change the code below. ******/

// initialize an array, a[i] = i + 1;
// the function does not return a value
void init_array(unsigned int a[], int n)	// sets array index 0 to have value of 1
{											// a[1] = 2, and so forth
    for (int i = 0; i < n; i++)
        a[i] =  i + 1;
}

int main(int argc, char *argv[])
{
    if(argc < 2)
    {
        printf("Usage: %s n\n", argv[0]);
        return -1;
    }

    for (int i = 1; i < argc; i ++ ) {
        int n = atoi(argv[i]);
        if (n < 1 || n > MAX_SIZE) {
            printf("The array size must be >= 1 and <= %d.\n", MAX_SIZE);
            return -1;
        }

        unsigned int a[n];
        init_array(a, n);
        printf("%5d: %lf\n", n, coverage(a, n));
    }
}

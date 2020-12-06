#include <stdio.h>

/* This function calculates n-th Catalan number.
 * n is assumed to be non-negative.
 * Do not worry about overflow.
 * Do not print anything in this function.
 * Do not use floating-point numbers (or operations).
 */
long catalan_number(int n)
{
	long cat = 1;	// Cat number of n0 = 1
    if (n < 0){		// If Cat # is negative, it returns 0, can't have negative
        return 0;
    }
    else if (n == 0){	// returns the Catalan # after n decrements to 0
    	return cat;
    }
    else{				// the beef, must multiply by C_(k-1), then multiply by "k+1"
    	cat = ((4 * n - 2) * catalan_number(n - 1)) / (n + 1);
    }	
		
}

/* do not change main function */
int main(void)
{
    int n;

    while (scanf("%d", &n) == 1) {
        if (n < 0) 
            printf("C(%2d) is not defined.\n", n);
        else 
            printf("C(%2d)=%18ld\n", n, catalan_number(n));
    }
    return 0;
}

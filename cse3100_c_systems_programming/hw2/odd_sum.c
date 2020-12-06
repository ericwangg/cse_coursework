#include <stdio.h>

/* Search for `count' distinct odd numbers that 
 * are smaller than `bound' and add up to `sum'.  
 *
 * Return value:
 *  1: A solution is found and printed.
 *  0: No solution was found.
 */
 
int recur; // okurrrr
 
int odd_sum(int count, int bound, int sum)
{
	if (count == 0){ // count = 0
		return 0;
	}
	else if(count != 0 && sum <= 0){	// count not 0, sum less than eq 0
		return 0;
	}
	else if(count == 0 && sum == 0){	// count is 0, sum also 0
		return 1;
	}
	else if(count == 1 && sum < bound && sum%2 == 1){	// count is 1, sum less than up bound, sum is odd
		printf("%d ", sum);
		return 1;
	}
	else if(count%2 != sum %2) {
		return 0;
	}
	else{ // eureka or something like that, #lebeef mooooo
		for (int i = 1; i < bound; i += 2){
			recur = odd_sum(count - 1, (2 * (bound/2) - i), sum - (2*(bound/2) -i));
			if(recur ==1){
				printf("%d ", (2*(bound/2) - i));
				return 1;
			}
		}
	}
	return 0;
}

/* Do not change the main() function */
int main(void)
{
    int value;
    int c, b, s;

    printf("Please enter 3 positive integers: count, bound, and sum:\n");
    if (scanf("%d%d%d", &c, &b, &s) != 3) {
        printf("Please enter 3 integers.\n");
        return 1;
    }

    if (c <= 0 || b <= 0 || s <= 0) {
        printf("Integers must be positive.\n");
        return 1;
    }

    value = odd_sum(c, b, s);
    if (value)
        printf("\n");
    else
        printf("There are no solutions.\n");
    return 0;
}

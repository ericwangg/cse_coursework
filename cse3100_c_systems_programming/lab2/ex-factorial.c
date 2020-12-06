/* This program should read a single integer from standard input then
 * compute its factorial. For example, if the user enters 5, the program should
 * output 120 because 1*2*3*4*5=120. */

#include <stdio.h>

int factorial(int n)
{
    long long result = 1;
    if(n == 0){
        return result;
    }
	result = factorial(n - 1) * n;
    return result;
}

int main()
{
    int n, result;

    if (scanf("%d", &n) != 1){ 
    	printf("Error: Please enter a non-negative integer.\n");
    	return 1;
    }
    if (n < 0){
    	printf("Error: Please enter a non-negative integer.\n");
    	return 0;
    }
    result = factorial(n);
    printf("%d\n", result);
    return 0;
}
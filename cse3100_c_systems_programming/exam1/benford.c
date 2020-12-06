#include <stdio.h>
#include <stdlib.h>

#define MAX_N   100000
#define N_DIGITS    10

/***** Search TODO to find the functions you need to work on ******/

// This function returns the first digit
// of an unsigned integer k (in decimal representation).
// Return values:
//  0:   if k is 0
//  1 - 9:  the leading digit of k 
int first_digit (unsigned long k)		// long int = 4 byte still
{
    // TODO Begin
    
    // Method:convert int to string, take first value of string, convert back to int
    // might be able to use itoa()
    // char conv = fgetc(k);
    
    char snum[5];
    //char conv = itoa(k, snum, 10);
    
    print("%d, conv");
    
    // update k and return k
    return k;
}

// This function finds out the frequencies of each digit 
// as the leading digits in numbers in array of n elements, 
// and stores them in array freq.
// Parameters:
//  a:  an array of n elements.
//  n:  number of elements in array a.
//  freq: the array that stroes frequencies of digits
//        the array must have N_DIGITS elements
// The function does not return a value.
void frequencies (unsigned long a[], int n, unsigned long freq[])
{
    // TODO Begin
    
    // EW: create 2D array where a[] are pointers that point to each respective freq[] next_index
    for(int i =0; i < n; i++){
    	freq[i] = a[i];
    }
    for(int j=0; j < 10, j++){
    	printf("%d:%d", a[j], freq[j]);
    }
}

/***** do not change the code below. ******/

// print out the frequencies stored in array freq
// there must be N_DIGITS elements in freq
void print_freq(unsigned long freq[])
{
    for(int i=0; i<N_DIGITS; i++) {
        printf("%2d:%-5lu", i, freq[i]);
    }
    printf("\n");
}

// initialize an array
// the function does not return a value
void init_array_uniform(unsigned long a[], int n)
{
    for(int i = 0; i < n; i++)
        a[i] =  i + 1;
}

// initialize an array with a pattern
// the function does not return a value
void init_array(unsigned long a[], int n)
{
    a[0] = 1;
    for(int i = 1; i < n; i++)
    {
        a[i] = a[i-1] + i + 1;
    }
}

int main(int argc, char ** argv)
{
    int n = MAX_N;

    if (argc >= 2) {
        n = atoi(argv[1]);
        if (n < 1 || n > MAX_N) {
            printf("the integer must be >= 1 and <= %d\n", MAX_N);
            return -1;
        }  
    } 

    unsigned long a[n];
    unsigned long freq[N_DIGITS];

    // init freq, for testing purpose
    for (int i = 0; i < N_DIGITS; i ++)
        freq[i] = (unsigned long) -1 >> 1;

    init_array_uniform(a, n);
    frequencies(a, n, freq);
    print_freq(freq);

    init_array(a, n);
    frequencies(a, n, freq);
    print_freq(freq);

    return 0;
}

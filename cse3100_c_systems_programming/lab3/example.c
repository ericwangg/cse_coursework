#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int n;
    int* arr;

    n = 10;

    /* Allocate array */
    arr = malloc(n);

    /* Store values in array */
    for(int i = 0; i <= n; i++)
        arr[i] = n-i;

    /* Print out values */
    for(int i = 0; i <= n; i++)
        printf("%d, ", arr[i]);
    printf("\n");
}

// This is the starter code for lab0. Only one line comment.

#include <stdio.h>
int main(void)
{
printf("Hello, World!\n");
    int i, sum;
    sum = 0;
	i = 0;
	while (i < 200) {
		sum = sum + i;
		i = i + 2;
	}
	printf("%d\n", sum);
    return 0;
}

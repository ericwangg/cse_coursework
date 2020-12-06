// Only this line of comment is provided 

#include <stdio.h>

int main(void) {
    double x;
    float total, avg = 0;
    int i = 1;
    while (scanf("%lf", &x) == 1) {
        total += x;
        avg = (avg + x) / i;
        i++;
        printf("Total=%f Average=%f\n", total, avg);
    }
    return 0;
}
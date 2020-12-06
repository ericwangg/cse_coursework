/* Compute e ** x, using Taylor series.  */

#include <stdio.h>

// Taylor Series help function that takes in double "x" and int "n", computes it by the given formula
double taylor(double x, int n){
    double taylor_sum;
    for (int i = n; i > 0; --i) // using location variable i to represent "n", as it's greater than 0, per for loop decrement by 1
        taylor_sum = 1 + x * taylor_sum / i;
    return taylor_sum;
}

int main() {
    double x, my_exp;
    int n;
    while(scanf("%lf %d", &x, &n) == 2) {
        my_exp = taylor(x, n);
        printf("exp(%.10f)=%.10f\n", x, my_exp);
    }
}
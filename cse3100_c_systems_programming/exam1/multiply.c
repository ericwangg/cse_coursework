#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

int multiply(int a, int b){
  /* Fill this in based on the pseudocode */
  int res = 0;
  while(b > 0){
    if(b%2 == 1){
    	res += a;
    }
    a = a << 1;
    b = b >> 1;
  }
  return res;
}


int main(int argc, char** argv){
  /*
    I'm only using atoi because this is a trivial program. Don't use it in practice!
   */
  srand(161609595);
  int b = rand() % 1000;
  if(argc == 2){
    int a = atoi(argv[1]);
    assert(a>0 && a<=100);
    printf("%d\n", multiply(a, b));
  }else{
    printf("usage: %s a\n", argv[0]);
    printf("Here a should be a positive integer between 1 and 100.\n");
  }
}

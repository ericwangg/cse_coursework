#define more variables so it is easier to make changes
CC=gcc
CFLAGS=-g -Wall -std=c99
TARGETS=rotate prime multiply value_of_e

all: $(TARGETS)

rotate: rotate.c
	$(CC) $(CFLAGS) -o $@ $@.c

prime: prime.c
	$(CC) $(CFLAGS) -o $@ $@.c

multiply: multiply.c
	$(CC) $(CFLAGS) -o $@ $@.c

value_of_e: value_of_e.c
	$(CC) -g -Wall -o $@ $@.c

clean:
	rm -rf *.o *~ $(TARGETS)

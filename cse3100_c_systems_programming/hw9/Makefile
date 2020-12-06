TARGETS=server_tickets kiosks
SRCS=$(patsubst %,%.c,$(TARGETS))
SRCINC=socketio.c
CC=gcc
CFLAGS=-g -Wall -pthread

all: $(TARGETS)

client_tickets: client_tickets.c $(SRCINC)
	$(CC) $(CFLAGS) -o $@ $<

server_tickets: server_tickets.c $(SRCINC)
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -rf *.o *~ $(TARGETS) *.out

sub:
	@zip $${PWD##*/}.zip $(SRCS) Makefile $(SRCINC)

#!/usr/bin/python3
import sys, re
import fileinput
import os.path

def     sys_error(s):
    print ("Error: " + s)
    sys.exit(1)

def     print_help():
    print('''Useage: check-tickets.py [options] [filename]
-t<N>:    specify the initial number of tickets 
filename: the output of the program. If missing, read from stdin. 
''')
    sys.exit(1)

def     print_bridge_status():
    global car_direction, direction, n_corssing, n_crossed, max_crossing, eastb_waiting, westb_waiting;

    print("check: max={},{} direction={} n_crossing={} n_crossed={} eastb_waiting={} westb_waiting={}".
            format(max_crossing, max_crossed, direction, n_crossing, n_crossed, eastb_waiting, westb_waiting))

def     my_error(s):
    global n_lines, line, opt_verbose
    if opt_verbose < 1:
        print(line, end='')
    if opt_verbose < 2:
        print_bridge_status()
    sys_error("Line {}: {}".format(n_lines, s))

opt_verbose = 0
opt_checK_waiting = False 
num_tickets = 50
filenames = []
for a in sys.argv[1:]:
    if a == '-h':
        print_help()
    elif a.startswith('-t'):
        num_tickets = int(a[2:])
    elif len(filenames) == 0 and os.path.isfile(a):
        filenames = [ a ]
    else:
        print_help()

pattern = re.compile('Kiosk (\d+): group (\d+) bought (\d+) .+ (\d+)')

NUM_MOVIES = 5

nt_per_movie = [0] * NUM_MOVIES

num_kiosks = 0
nt_per_kiosk = [0] * 100;

n_lines = 0
for line in fileinput.input(filenames):
    if opt_verbose >= 1:
        print(line, end='')

    n_lines += 1
    m = re.search(pattern, line)
    if (m):
        kk = int(m.group(1), 0)
        nt = int(m.group(3), 0)
        movie = int(m.group(4), 0)

        nt_per_movie[movie] += nt
        nt_per_kiosk[kk] += nt 

        num_kiosks = max(num_kiosks, kk+1)

        if opt_verbose >= 2:
            print_bridge_status()

if not all(c == num_tickets for c in nt_per_movie):
    print(nt_per_movie)
    sys_error("The number of tickets sold for some movies is not {}.".format(num_tickets))

total = num_tickets * NUM_MOVIES;
if sum(nt_per_kiosk) != total:
    sys_error("The total number tickets sold is not {}.".format(total))

sys.exit(0)

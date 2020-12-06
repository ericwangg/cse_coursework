#!/usr/bin/python3
import sys, re
import fileinput
import os.path

def     sys_error(s):
    print ("Error: " + s)
    sys.exit(1)

def     print_help():
    print('''Useage: check-dining.py [options] [filename]
-v:       print lines
-V:       print status after each line
filename: the output of the program. If missing, read from stdin. 
''')
    sys.exit(1)

def     print_status():
    global n_small_tables, n_big_tables, n_small_taken, n_big_taken, n_small_waiting, n_big_waiting
    print("check: n_small_(tables,taken,waiting)={},{},{} n_big_(tables,taken,waiting)={},{},{}".
            format(n_small_tables, n_small_taken, n_small_waiting, n_big_tables, n_big_taken, n_big_waiting))

def     my_error(s):
    global n_lines, line, opt_verbose
    if opt_verbose < 1:
        print(line, end='')
    if opt_verbose < 2:
        print_status()
    sys_error("Line {}: {}".format(n_lines, s))

opt_verbose = 0
filenames = []
for a in sys.argv[1:]:
    if a == '-h':
        print_help()
    elif a == '-v':
        opt_verbose = 1
    elif a == '-V':
        opt_verbose = 2
    elif len(filenames) == 0 and os.path.isfile(a):
        filenames = [ a ]
    else:
        print_help()

pattern = re.compile('(\d+), +(small|big).+ is ([awsl])')
cfg_pattern= re.compile('Options: -g(\d+) -G(\d+) -t(\d+) -T(\d+) -m(\d+)')

# group status 
n_grps = 0;
grps = [];
grp_n_meals = [];

# configurations
n_big_tables = n_small_tables = 0;
n_big_waiting = n_small_waiting = n_big_taken = n_small_taken = 0
n_meals = 0

n_lines = 0
for line in fileinput.input(filenames):
    if opt_verbose >= 1:
        print(line, end='')

    n_lines += 1
    if n_lines == 1:
        m = re.search(cfg_pattern, line)
        if not m:
            sys_error('Did not see the options line.')
        n_small_groups = int(m.group(1))
        n_big_groups = int(m.group(2))
        n_small_tables = int(m.group(3))
        n_big_tables = int(m.group(4))
        n_meals = int(m.group(5))
        n_grps = n_small_groups + n_big_groups;

        assert n_small_groups >= 0
        assert n_big_groups >= 0
        assert n_small_tables >= 0
        assert n_big_tables >= 0
        assert n_meals > 0

        grps = [None] * n_grps;
        grp_n_meals = [0] * n_grps; 
        continue

    m = re.search(pattern, line)
    if (m):
        grp_id = int(m.group(1), 0)
        grp_sz = m.group(2)
        status = m.group(3)

        if status == 'a':    # arriving
            if not grps[grp_id] is None:
                my_error("group {} is not in a state that can arrive.".format(grp_id))
            grp_n_meals[grp_id] += 1
            grps[grp_id] = status

        elif status == 'w':  # waiting
            if grps[grp_id] != 'w' and grps[grp_id] != 'a':
                my_error("group {} is not in a state that can wait, e.g., it has not arrived yet.".format(grp_id))

            if grp_sz == 'big' and n_big_taken < n_big_tables:
                my_error("group {} does not have to wait".format(grp_id))

            if grp_sz == 'small':
                if n_small_taken < n_small_tables:
                    my_error("group {} does not have to wait".format(grp_id))
                if n_big_taken < n_big_tables and n_big_waiting == 0:
                    my_error("group {} does not have to wait".format(grp_id))

            # increment waiting counter if it is not already waiting 
            if grps[grp_id] != 'w':
                if grp_sz == 'small':
                    n_small_waiting += 1
                else:
                    n_big_waiting += 1
                grps[grp_id] = 'w'

        elif status == 's':  # seated
            if 'small table' in line:
                table_size = 'small'
                if n_small_taken >= n_small_tables:
                    my_error("all small tables are taken.");
            else:
                table_size = 'big'
                if n_big_taken >= n_big_tables:
                    my_error("all big tables are taken.");

            if grps[grp_id] != 'w' and grps[grp_id] != 'a':
                my_error("group {} cannot be seated.".format(grp_id))

            if grp_sz == 'big':  # big group
                if table_size != 'big': 
                    my_error("group {} should be seated at a big table.".format(grp_id))
                if grps[grp_id] == 'w':
                    n_big_waiting -= 1
            else: # small group
                if n_small_taken < n_small_tables and table_size == 'big' :
                    my_error("group {} should be seated at a small table.".format(grp_id))
                if grps[grp_id] == 'w':
                    n_small_waiting -= 1

            if table_size == 'small':
                n_small_taken += 1
            else:
                n_big_taken += 1
            grps[grp_id] = table_size

        elif status == 'l':  # leaving
            if 'small table' in line:
                table_size = 'small'
            else:
                table_size = 'big'

            if grps[grp_id] != table_size:
                my_error("group {} is seated at a {} table, not a {} table.".format(grp_id, grps[grp_id], table_size))

            if grps[grp_id] == 'small':
                n_small_taken -= 1
            else:
                n_big_taken -= 1
            grps[grp_id] = None

        else:
            my_error("Should never be here.")

        if opt_verbose >= 2:
            print_status()

if not all(c is None for c in grps[0:n_grps]):
    print(grps[0:n_grps])
    sys_error("Some groups are still in the restaurant.")

if not all(c == n_meals for c in grp_n_meals[0:n_grps]):
    print(grp_n_meals[0:n_grps])
    sys_error("Some groups did not have {} meals.".format(n_meals))

sys.exit(0)

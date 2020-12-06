#include <stdio.h>
#include <ctype.h>

#define     MIN_YEAR    1600
#define     MAX_YEAR    2399
#define     YEAR_OFFSET 2000

#define     RV_NODATE   0
#define     RV_VALIDDATE 1
#define     RV_INVALIDDATE 2

/***** DFA *****/

/* The function checks if a date is present at the beginning of a line,
 * and if the date is valid.
 *
 * Return values:
 *
 * 0:  Not date was found.
 * 1:  Date is valid.
 * 2:  Date was found, but not valid.
 */
 
// Helper for ASCII Conversions to use int
int convert(int a){
	return a - 48;
}

// Leap Year logic
// Handles logic 
int leap_year(int year){
	if (((year % 4 == 0) && (year % 100 != 0)) || (year % 400 == 0)) {
		return 1;	// if conditions satisfying "Leap Year" is true, return True
	}
	else {
		return 0; //o.t. return False
	}
}

// Date logic and conditions check
// checks in the order of day -> month -> year
int check_date(int d, int m, int y) {
    if (((y >= 0) && (y < 100)) || ((y >= MIN_YEAR) && (y <= MAX_YEAR)) ) {
        if ((m > 0) && (m < 13)) {
            if (((d > 0) && (d < 32)) && ((m == 1) || (m == 3) || (m == 5) || (m == 7) || (m == 8) || (m == 10) || (m == 12))) {
                return 1;
            } 
            else if (((d > 0) && (d < 31)) && ((m == 4) || (m == 6) || (m == 9) || (m == 11))) {
                return 1;
            } 
            else if ((d > 0) && (d < 29) && (m == 2)) {
                return 1;
            }
            else if ((d > 0) && (d < 30) && (m == 2) && ((leap_year(y) == 1) || (y == 0))) {
                return 1;
            }
            else {
                return 2;
            }
        }
        else {
            return 2;
        }
    }
    else {
        return 2;
    }
    return 2;
}


// le beef of le program, get that date
// "str" int is used to interate over the length of the date string
int get_date() {
	int day, month, year, gc, str, temp, mycase;
	str = 0;
    temp = 0;	// temp value hold variable
    mycase = 1;	// my kind of swtich statement I guess
    
    gc = getchar();

    // length tracker variables
	int dd, mm, yy, iden;
	dd = 0;
	mm = 0;
	yy = 0; // initializing the lenght variables for date, month, year
    iden = 0;	// for exiting get_date after date has been identified
    
    while (gc != '\n' && gc != EOF) {
        if (isblank(gc)) {
            if (str != 0) {
                iden = 1;
            }
        }
        else if (iden == 0) {
            if (gc == 47) {
                if (temp == 0) {
                    mycase = 0;
                }
                if (str == 0) {
                    month = temp;
                }
                else if (str == 1) {
                    day = temp;
                }
                else if (str == 2) {
                    year = temp;
                }
                temp = 0;
                str++;
            }
            else if ((gc > 47) && (gc < 58)) {
                if (str== 0) {
                    mm++;
                }
                else if (str == 1) {
                    dd++;
                }
                else if (str == 2) {
                    yy++;
                }
                temp = temp * 10 + convert(gc);
            }
            else {
                mycase = 0;
            }
        }
        gc = getchar();
    }
    year = temp;
    if (mycase == 0 || str == 0 || yy > 4 || yy < 2 || yy == 3 || dd > 2 || mm > 2) {
        return 0;
    } 
    else if (yy > 2 && year < MIN_YEAR) {
        return 2;
    } 
    else {
        return check_date(day, month, year);
    }
}

/***** main *****/
/* Do not change the main function. */
int main(void) 
{
    // run the loop until hit end of file
    do  {
        int rv = get_date();

        if (!feof(stdin)) {
            switch (rv) {
                case RV_NODATE:
                    printf("No date found.\n");
                    break;
                case RV_VALIDDATE:
                    printf("Valid date.\n");
                    break;
                case RV_INVALIDDATE:
                    printf("Invalid date.\n");
                    break;
                default:
                    printf("Unknown return value %d.\n", rv); 
                    break;
            }
        }
    } while (! feof(stdin));

    return 0;
}

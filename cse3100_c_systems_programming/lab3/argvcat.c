#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* print out an error message and exit */
void my_error(char *s)
{
    perror(s);
    exit(1);
}

/* Concatnate two strings.
 * Dynamically allocate space for the result.
 * Return the address of the result.
 */
char *my_strcat(char *s1, char *s2)
{
	char *newstr = calloc(1, strlen(s1)+strlen(s2)+1);	
	// 1 = size of char
	// concatenation occurs between s1 and s2
	// +1 for empty char at string's end
    strcpy(newstr, s1);	
    strcat(newstr, s2);
    return newstr;
}

int main(int argc, char *argv[])
{
    char    *s;

    s = my_strcat("", argv[0]);

    for (int i = 1; i < argc; i ++) {
    	char *newstr = s;
        s = my_strcat(s, argv[i]);
        free(newstr);
    }

    printf("%s\n", s);
    free(s);	//calloc now freed

    return 0;
}

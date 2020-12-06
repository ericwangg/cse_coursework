#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include "matrix.h"

#define     NUM_THREADS     2

typedef struct {
    unsigned int id;
    TMatrix *m, *n, *t;
} thread_arg_t;

/* the main function of threads */
static void * thread_main(void * p_arg)
{
    // TODO
    thread_arg_t * arg = p_arg;	// set threads into p_arg
    
    // set names for arguments to prevent dereferencing
    TMatrix *m, *n, *t;

    // TMatrix ** mData = arg-> m->data;
    // TMatrix ** nData = arg-> n->data;
    // TMatrix ** tData = arg-> t->data;	
    
    m = arg->m;
    n = arg->n;
    t = arg->t;
    
    int id = arg->id;
	int i, j;
	
	for(i = id; i < m->nrows; i+=2){
		for(j = 0; j < m->ncols; j++){
			t->data[i][j] = n->data[i][j] + m->data[i][j];
			//tData[i][j] = nData[i][j] + mData[i][j];
		}
	}
	
    return NULL;
}

/* Return the sum of two matrices. The result is in a newly creaed matrix. 
 *
 * If a pthread function fails, report error and exit. 
 * Return NULL if something else is wrong.
 *
 * Similar to addMatrix, but this function uses 2 threads.
 */
TMatrix * addMatrix_thread(TMatrix *m, TMatrix *n)
{
    if (    m == NULL || n == NULL
         || m->nrows != n->nrows || m->ncols != n->ncols )
        return NULL;

    TMatrix * t = newMatrix(m->nrows, m->ncols);
    if (t == NULL)
        return t;
    
    // TODO
	pthread_t thread_ids[NUM_THREADS];
	thread_arg_t	thread_args[NUM_THREADS];
	
	for(int i = 0; i < NUM_THREADS; i++){
		thread_args[i].id = i;
		thread_args[i].m = m;
		thread_args[i].n = n;
		thread_args[i].t = t;
		int ms = pthread_create(&thread_ids[i], NULL, thread_main, &thread_args[i]);
		if(ms){
			fprintf(stderr, "ERROR; pthread_create() returned %d\n", ms);
			exit(1);
		}
	}
	for(int i = 0; i < NUM_THREADS; i++){
		int ms = pthread_join(thread_ids[i], NULL);
		if(ms){
			fprintf(stderr, "ERROR; pthread_create() returned %d\n", ms);
			exit(1);
		}
	}
    
    
    return t;
}

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include "matrix.h"

// Search TODO to find the locations where code needs to be completed

#define     NUM_THREADS     2

typedef struct {
    unsigned int id;
    TMatrix *m, *n, *t;
} thread_arg_t;

static void * thread_main(void * p_arg)
{
    // TODO
    thread_arg_t * arg = p_arg;		// use arg-> converted p_arg of thread_arg_t type
    
    int beg, end;					// set the beginning of the matrix for partitioning
    
    int mRows = arg->m->nrows;		// abbr.
    int nCols = arg->n->ncols;
    int mCols = arg->m->ncols;
    
    int id = arg->id;
    
    if(id == 0){		// if the id is 0, run first half of array
    	beg = 0;			// 1st
    	end = mRows/2;		// half of the matrix array
    }
    else{
    	beg = mRows/2;		// half of M, for 2nd half	
    	end = mRows;		// end of the matrix array 
    }
    
    double ** mData = arg-> m->data;
    double ** nData = arg-> n->data;
    double ** tData = arg-> t->data;
    
    for(int i = beg; i < end; i++){
		for(int j = 0; j < nCols; j++){		// n columsn NOT m columns
			TElement mul = (TElement)0;							// ??? - why 0 after (TElement)
			for (int k = 0; k < mCols; k++){		// this is m columns
				mul += mData[i][k] * nData[k][j];
			}
			//t->data[i][j] = n->data[i][j] + m->data[i][j];
			tData[i][j] = mul;
		}
	}
	
    return NULL;
}

/* Return the sum of two matrices.
 *
 * If any pthread function fails, report error and exit. 
 * Return NULL if anything else is wrong.
 *
 * Similar to mulMatrix, but with multi-threading.
 */
TMatrix * mulMatrix_thread(TMatrix *m, TMatrix *n)
{
    if (    m == NULL || n == NULL
         || m->ncols != n->nrows )
        return NULL;

    TMatrix * t = newMatrix(m->nrows, n->ncols);
    if (t == NULL)
        return t;

    // TODO
    pthread_t		thread_ids[NUM_THREADS];
    thread_arg_t	thread_args[NUM_THREADS];
    
    for(int i = 0; i < NUM_THREADS; i++){
    	thread_args[i].id = i;
    	thread_args[i].m = m;
    	thread_args[i].n = n;
    	thread_args[i].t = t;
    	int pt = pthread_create(&thread_ids[i], NULL, thread_main, &thread_args[i]);
    	if( pt ){
    		fprintf(stderr, "ERROR: pthread_create() returned %d\n", pt);
    		exit(1);
    	} 
    }
    for(int j = 0; j < NUM_THREADS; j++){
    	int pt = pthread_join(thread_ids[j], NULL);
    	if ( pt ){
    		fprintf(stderr, "ERROR: pthread_join returned %d\n", pt);
    		exit(1);
    	}
    }
    
    return t;
}

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>

#include "nqueens.h"

#define N 5
#define CUT_OFF_VALUE 4

long wtime();

int main(int argc, char** argv) {
	int size = N;
	int cut_off_value = CUT_OFF_VALUE;
	long start_time, end_time;
	
	if(argc > 1)
		size = atoi(argv[1]);
	
	if(argc > 2)
		cut_off_value = atoi(argv[2]);
	
	start_time = wtime();
	int solutions = find_queens(size, cut_off_value);
	end_time = wtime();
	
	#pragma omp parallel
	#pragma omp master
	printf("Nqueens openmp_task;size: %d;threads: %d;cut_off: %d;time: %ld;solutions: %d\n", 
			 size, omp_get_num_threads(), cut_off_value, (long) (end_time - start_time), solutions);
}

/* wtime */
long wtime() {
   struct timeval t;
   gettimeofday(&t, NULL);
   return t.tv_sec*1000000 + t.tv_usec;
}
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>

#include "nqueens.h"

#define N 5
#define THREADS 1

long wtime();

int main(int argc, char** argv) {
	int size = N, threads = THREADS;
	long start_time, end_time;
	
	if(argc > 1)
		size = atoi(argv[1]);
	
	if(argc > 2)
		threads = atoi(argv[2]);
	
	start_time = wtime();
	int solutions = find_queens(size, threads);
	end_time = wtime();
	
	printf("Nqueens openmp_parallel;size: %d;threads: %d;cut_off: 0;time: %ld;solutions: %d\n", 
			 size, threads, (long) (end_time - start_time), solutions);
}

/* wtime */
long wtime() {
   struct timeval t;
   gettimeofday(&t, NULL);
   return t.tv_sec*1000000 + t.tv_usec;
}
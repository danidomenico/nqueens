/**********************************************************************************************/
/*  This program is part of the Barcelona OpenMP Tasks Suite                                  */
/*  Copyright (C) 2009 Barcelona Supercomputing Center - Centro Nacional de Supercomputacion  */
/*  Copyright (C) 2009 Universitat Politecnica de Catalunya                                   */
/*                                                                                            */
/*  This program is free software; you can redistribute it and/or modify                      */
/*  it under the terms of the GNU General Public License as published by                      */
/*  the Free Software Foundation; either version 2 of the License, or                         */
/*  (at your option) any later version.                                                       */
/*                                                                                            */
/*  This program is distributed in the hope that it will be useful,                           */
/*  but WITHOUT ANY WARRANTY; without even the implied warranty of                            */
/*  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                             */
/*  GNU General Public License for more details.                                              */
/*                                                                                            */
/*  You should have received a copy of the GNU General Public License                         */
/*  along with this program; if not, write to the Free Software                               */
/*  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA            */
/**********************************************************************************************/

/*
 * Original code from the Cilk project (by Keith Randall)
 * 
 * Copyright (c) 2000 Massachusetts Institute of Technology
 * Copyright (c) 2000 Matteo Frigo
 */

#include <stdlib.h>
#include <stdio.h>
#include <memory.h>
#include <alloca.h>
#include <omp.h>

#include "nqueens.h"


/* Checking information */
static int solutions[] = {
        1,
        0,
        0,
        2,
        10, /* 5 */
        4,
        40,
        92,
        352,
        724, /* 10 */
        2680,
        14200,
        73712,
        365596,
        2279184, /* 15 */
        14772512,
        95815104,
        666090624
};
#define MAX_SOLUTIONS sizeof(solutions)/sizeof(int)

int total_count;
int cut_off_value;

/*
 * Returns 1 if none of the queens conflict, and returns 0 otherwise.
 */
int ok(int queen_number, int row_position, int* position) {
	int i;

	// Check each queen before this one
	for(i = 0; i < queen_number; i++) {
		// Get another queen's row_position
		int other_row_pos = position[i];

		// Now check if they're in the same row or diagonals
		if (other_row_pos == row_position || // Same row
			other_row_pos == row_position - (queen_number - i) || // Same diagonal
			other_row_pos == row_position + (queen_number - i))   // Same diagonal
			return 0;
	}

	return 1;
}

void nqueens_ser(int size, int queen_number, int* board, int *solutions) {
	int i, res;
	if(size == queen_number) {
		/* good solution, count it */
		*solutions = 1;
		return;
	}

	*solutions = 0;

	/* try each possible board for queen <queen_number> */
	for(i = 0; i < size; i++) {
		board[queen_number] = i;
		
		if(ok(queen_number, i, board)) {
			nqueens_ser(size, queen_number + 1, board, &res);
			*solutions += res;
		}
	}
}

void nqueens(int size, int queen_number, int* board, int *solutions, int depth) {
	int *csols;
	int i;

	if(size == queen_number) {
		*solutions = 1;
		return;
	}
	
	*solutions = 0;
	csols = alloca(size * sizeof(int));
	memset(csols, 0, size * sizeof(int));
	
	for(i = 0; i < size; i++) {
		if(depth < cut_off_value) {
 			#pragma omp task untied
			{
				int* board_aux = alloca(size * sizeof(int));
				memcpy(board_aux, board, queen_number * sizeof(int));
				board_aux[queen_number] = i;
				if(ok(queen_number, i, board_aux))
					nqueens(size, queen_number + 1, board_aux, &csols[i], depth+1);
			}
		} else {
			board[queen_number] = (char) i;
			if(ok(queen_number, i, board))
				nqueens_ser(size, queen_number + 1, board, &csols[i]);
		}
	}

	#pragma omp taskwait
	for(i = 0; i < size; i++) 
		*solutions += csols[i];
}

int find_queens(int size, int cut_off) {
	total_count=0;
	cut_off_value = cut_off;
	
	#pragma omp parallel
	{
		#pragma omp master
		{
			int* board;
			board = alloca(size * sizeof(int));
			
			nqueens(size, 0, board, &total_count, 0);
		}
	}
	
	return total_count;
}
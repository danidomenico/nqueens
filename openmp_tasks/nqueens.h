#ifndef _NQUEENS_H_
#define _NQUEENS_H_

int ok(int queen_number, int row_position, int* position);
void nqueens_ser(int size, int queen_number, int* board, int *solutions);
void nqueens(int size, int queen_number, int* board, int *solutions, int depth);
int find_queens(int size, int cut_off); //return: number of solutions

#endif /* _NQUEENS_H_ */


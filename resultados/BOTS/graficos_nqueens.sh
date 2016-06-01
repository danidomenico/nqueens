echo Dados...
python bots_nqueens.py -n N_Queens -c gcc -co 4 -e dados/2015-09-12_09-43-50-gcc.txt
python bots_nqueens.py -n N_Queens -c icc -co 5 -e dados/2015-09-12_11-58-34-icc.txt

echo Graficos...
cd nqueens

gnuplot plot-speedup-gcc.gpi
gnuplot plot-cutoff-gcc.gpi

gnuplot plot-speedup-icc.gpi
gnuplot plot-cutoff-icc.gpi

gnuplot plot-tempo.gpi

cd ..

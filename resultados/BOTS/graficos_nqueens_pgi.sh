echo Dados...
python bots_nqueens.py -n N_Queens -c pgi -co 4 -e dados/2014-05-06_14-09-47-pgi.txt

echo Graficos...
cd nqueens

gnuplot plot-speedup-pgi.gpi
gnuplot plot-cutoff-pgi.gpi

gnuplot plot-tempo.gpi

cd ..

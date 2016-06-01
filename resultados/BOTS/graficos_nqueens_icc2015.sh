echo Dados...
python bots_nqueens.py -n N_Queens -c icc2015 -co 5 -e dados/2015-11-03_17-33-39_icc2015.txt

echo Graficos...
cd nqueens

gnuplot plot-speedup-icc2015.gpi
gnuplot plot-cutoff-icc2015.gpi

gnuplot plot-tempo.gpi

cd ..

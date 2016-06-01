echo Dados...
python bots_nqueens.py -n N_Queens -e dados/versoes/result.txt dados/versoes/result2.txt

echo Graficos...
cd nqueens

gnuplot plot-version.gpi

cd ..

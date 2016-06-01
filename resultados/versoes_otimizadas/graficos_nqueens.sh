echo Dados...
python bots_nqueens.py -n Nqueens -c gcc -v parallel -e dados/2015-10-06_10-25-49_gcc_parallel.txt
python bots_nqueens.py -n Nqueens -c gcc -v task -e dados/2015-10-06_10-43-35_gcc_tasks.txt

python bots_nqueens.py -n Nqueens -c icc -v parallel -e dados/2015-10-06_11-08-47_icc_parallel.txt
python bots_nqueens.py -n Nqueens -c icc -v task -e dados/2015-10-06_11-26-43_icc_tasks.txt

python bots_nqueens.py -n Nqueens -c pgi -v parallel -e dados/2014-05-06_14-35-16_pgi_parallel.txt
python bots_nqueens.py -n Nqueens -c pgi -v task -e dados/2014-05-06_16-26-01_pgi_tasks.txt

python bots_nqueens.py -n Nqueens -c icc2015 -v parallel -e dados/2015-11-03_18-57-36_icc2015_parallel.txt
python bots_nqueens.py -n Nqueens -c icc2015 -v task -e dados/2015-11-20_12-38-20_icc_tasks.txt

echo Graficos...
cd nqueens

gnuplot plot-speedup.gpi
gnuplot plot-tempo.gpi

cd ..
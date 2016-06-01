#!/usr/bin/env python

import sys
import uteis
import argparse
from datetime import datetime

#Variaveis globais
plot_file = "\t\'" + "stats-{0}-{1}.csv" + "\'"
#plot_er_margin = " using 1:(${0}-${1}):(${0}+${1}) with filledcu lc rgb color_em notitle, ''"
plot_linha = " using 1:{0} with linespoints t columnheader {1},\\" 

versao = "manual ({0})"

def calc_stats(dados, n=0, threads=0, version=""):
	#Indice das colunas
	nsize = 0
	nversion = 2
	nthreads = 3
	time = 5
	
	#Filtro size
	desc_size = "N=" + str(n) 
	
	linhas = filter(lambda x: desc_size == x[nsize] and version in x[nversion] and str(threads) == x[nthreads], dados)
	#print len(linhas)
	if len(linhas) < 1:
		return 0.0, 0.0, 0.0
	amostra = []
	for a in linhas:
		amostra.append(float(a[time]));
	return uteis.calc_stats(amostra)

def stats_tempo(benchmark, compilador, cutoff, dados):
	print "Gerando tempo..."
	
	nsizes = [14]
	ncpus = [1, 2, 4, 8]
	
	saida = open(benchmark.lower() + "/stats-tempo-" + compilador + ".csv", 'w')
	
	#Header e Plotagem
	saida.write("Index;CPUs")
	
	plot_index = 3
	plot_index_ls = 1
	for n in nsizes:
		saida.write(";\"" + str(n) + "N-" + versao.format(cutoff) + "\";sd")
		print plot_file.format("tempo", compilador) \
			+ plot_linha.format(plot_index, "ls " + str(plot_index_ls))
		plot_index += 1
		plot_index_ls += 1
	
	#Dados do arquivo
	index = 1
	for t in ncpus:
		saida.write("\n" + str(index) + ";" + str(t))
		index += 1
		for n in nsizes:
			mean, sd, error = calc_stats(dados, n, t, versao.format(cutoff))
			saida.write(";" + str(mean) + ";" + str(sd))

	saida.close()
	print "Concluido \n"
	print "Gerando size..."
	
	nsizes = [13, 14, 15]
	ncpus = [1, 2, 4]

	saida = open(benchmark.lower() + "/stats-size.csv", 'w')
	
	#Header e Plotagem
	saida.write("Index;Size")
	plot_index = 3
	plot_index_ls = 1
	for t in ncpus:
		saida.write(";\"" + str(t) + " Thread(s)-manual" + "\"")
		
		print plot_file.format("size", benchmark.lower()) \
			+ plot_linha.format(str(plot_index) + ":xtic(2)", "ls " + str(plot_index_ls))
		plot_index += 1
		plot_index_ls += 1
	
	#Dados do arquivo
	index = 1
	for n in nsizes:
		saida.write("\n" + str(index) + ";\"" + str(n) + "N\"")
		index += 1
		for t in ncpus:
			mean, sd, error = calc_stats(dados, n, t, "manual")
			saida.write(";" + str(mean))

	saida.close()
	print "Concluido \n"
	
def stats_speedup(benchmark, compilador, cutoff, dados):
	print "Gerando speedup..."
	
	nsizes = [14]
	ncpus = [1, 2, 4, 8]
	
	saida = open(benchmark.lower() + "/stats-speedup-" + compilador + ".csv", 'w')
	
	#Header e Plotagem
	saida.write("CPUs;\"Ideal\"")
	
	#Ideal
	print plot_file.format("speedup", compilador) \
			+ plot_linha.format(2, "ls 13")
	
	plot_index = 3
	plot_index_ls = 1
	for n in nsizes:
		saida.write(";\"" + str(n) + "N-" + versao.format(cutoff) + "\"")
		print plot_file.format("speedup", compilador) \
			+ plot_linha.format(plot_index, "ls " + str(plot_index_ls))
		plot_index += 1
		plot_index_ls += 1
	
	#Dados do arquivo
	tempo1cpu = []
	for n in nsizes:
		mean, sd, error = calc_stats(dados, n, 1, versao.format(cutoff))
		tempo1cpu.append(mean);
			
	for t in ncpus:
		saida.write("\n" + str(t) + ";" + str(t))
		index = 0
		for n in nsizes:
			mean, sd, error = calc_stats(dados, n, t, versao.format(cutoff))
			saida.write(";" + str(tempo1cpu[index]/mean))
			index += 1

	saida.close()
	print "Concluido \n"
	
def stats_cutoff(benchmark, compilador, cutoff, dados):
	print "Gerando cutoff..."
	
	nsizes = [14]
	ncpus = [1, 2, 4, 8]
	ncutoff = []
	if compilador == "starpu-ws":
		ncutoff = range(1, 3+1)
	else:
		ncutoff = range(1, 5+1)
	
	saida = open(benchmark.lower() + "/stats-cutoff-" + compilador + ".csv", 'w')
	
	#Header e Plotagem
	saida.write("Cutoff")
	plot_index = 2
	plot_index_ls = 1
	for t in ncpus:
		saida.write(";\"" + str(t) + " Thread(s)\"")
		print plot_file.format("cutoff", compilador) \
			+ plot_linha.format(str(plot_index), "ls " + str(plot_index_ls))
		plot_index += 1
		plot_index_ls += 1
	
	#Dados do arquivo
	index = 1
	for n in nsizes:
		for c in ncutoff:
			saida.write("\n" + str(c))
			for t in ncpus:
				mean, sd, error = calc_stats(dados, n, t, versao.format(c))
				saida.write(";" + str(mean))

	saida.close()
	print "Concluido \n"
	
def stats_version(benchmark, dados):
	print "Gerando version..."
	
	nsizes = [14, 15]
	nversion = ["none", "pragma-if", "manual"]
	ncpus = 4
	
	saida = open(benchmark.lower() + "/stats-version.csv", 'w')
	
	#Header e Plotagem
	saida.write("Index;Size")
	plot_index = 3
	plot_index_ls = 1
	for v in nversion:
		saida.write(";\"" + str(ncpus) + " Thread(s)-" + v + "\"")
		print plot_file.format("version", benchmark.lower()) \
			+ plot_linha.format(str(plot_index) + ":xtic(2)", "ls " + str(plot_index_ls))
		plot_index += 1
		plot_index_ls += 1
	
	#Dados do arquivo
	index = 1
	for n in nsizes:
		saida.write("\n" + str(index) + ";" + str(n) + "N")
		index += 1
		for v in nversion:
			mean, sd, error = calc_stats(dados, n, ncpus, v)
			saida.write(";" + str(mean))

	saida.close()
	print "Concluido \n"

def main():
	dados = [] # array das linhas
	
	parser = argparse.ArgumentParser(description='Estatistica.')
	parser.add_argument("-n", "--nome", help="nome do benchmark")
	parser.add_argument("-c", "--compilador", choices=["gcc", "icc", "icc2015", "pgi", "starpu-prio", "starpu-dm", "starpu-ws", "starpu-eager"], help="compilador do programa")
	parser.add_argument("-co", "--cutoff", help="cutoff")
	parser.add_argument("-e", "--entrada", nargs='+', help="arquivos de entrada")
	#parser.add_argument("-s", "--sizes", nargs='+',   help="tamanhos a processar")
	#parser.add_argument("-w", "--energia", nargs='+', help="arquivos de energia")
	args = parser.parse_args()
	
	uteis.le_dados_execucao(args.nome.replace("_", " "), args.entrada, dados)
	
	#print len(dados)
	#print dados[0]
	
	#stats_speedup(args.nome.replace("_", ""), args.compilador, args.cutoff, dados)
	stats_tempo(args.nome.replace("_", ""), args.compilador, args.cutoff, dados)
	#stats_cutoff(args.nome.replace("_", ""), args.compilador, args.cutoff, dados)
	#stats_version(args.nome.replace("_", ""), dados)
	
	
if __name__ == "__main__":
	main()


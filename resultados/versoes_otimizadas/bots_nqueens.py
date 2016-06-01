#!/usr/bin/env python

import sys
import uteis
import argparse
from datetime import datetime

#Variaveis globais
plot_file = "\t\'" + "stats-{0}-{1}.csv" + "\'"
#plot_er_margin = " using 1:(${0}-${1}):(${0}+${1}) with filledcu lc rgb color_em notitle, ''"
plot_linha = " using 1:{0} with linespoints t columnheader {1},\\" 

versao = "openmp-{0}"

def calc_stats(dados, size=0, threads=0):
	#Indice das colunas
	nsize = 0
	nthreads = 1
	time = 3
	
	linhas = filter(lambda x: str(size) in x[nsize] and str(threads) in x[nthreads], dados)
	#print len(linhas)
	if len(linhas) < 1:
		return 0.0, 0.0, 0.0
	amostra = []
	for a in linhas:
		amostra.append(float(a[time].split(":")[1])/1000000.0); #de micro para segundos
	return uteis.calc_stats(amostra)

def stats_tempo(benchmark, compilador, tipo_versao, dados):
	print "Gerando tempo..."
	
	nsizes = [15]
	ncpus = [1, 2, 4, 8]
	
	saida = open(benchmark.lower() + "/stats-tempo-" + tipo_versao + "-" + compilador + ".csv", 'w')
	
	#Header e Plotagem
	saida.write("Index;CPUs")
	
	plot_index = 3
	plot_index_ls = 1
	for n in nsizes:
		saida.write(";\"" + str(n) + "N-" + versao.format(tipo_versao) + "-" + compilador + "\";sd")
		print plot_file.format("tempo", tipo_versao + "-" + compilador) \
			+ plot_linha.format(str(plot_index)+":xtic(2)", "ls " + str(plot_index_ls))
		plot_index += 1
		plot_index_ls += 1
	
	#Dados do arquivo
	index = 1
	for t in ncpus:
		saida.write("\n" + str(index) + ";" + str(t))
		index += 1
		for n in nsizes:
			mean, sd, error = calc_stats(dados, n, t)
			saida.write(";" + str(mean) + ";" + str(sd))

	saida.close()
	print "Concluido \n"
	
def stats_speedup(benchmark, compilador, tipo_versao, dados):
	print "Gerando speedup..."
	
	nsizes = [15]
	ncpus = [1, 2, 4, 8]
	
	saida = open(benchmark.lower() + "/stats-speedup-" + tipo_versao + "-" + compilador + ".csv", 'w')
	
	#Header e Plotagem
	saida.write("CPUs;\"Ideal\"")
	
	#Ideal
	print plot_file.format("speedup", tipo_versao + "-" + compilador) \
			+ plot_linha.format(2, "ls 13")
	
	plot_index = 3
	plot_index_ls = 1
	for n in nsizes:
		saida.write(";\"" + str(n) + "N-" + versao.format(tipo_versao) + "-" + compilador + "\"")
		print plot_file.format("speedup", tipo_versao + "-" + compilador) \
			+ plot_linha.format(plot_index, "ls " + str(plot_index_ls))
		plot_index += 1
		plot_index_ls += 1
	
	#Dados do arquivo
	tempo1cpu = []
	for n in nsizes:
		mean, sd, error = calc_stats(dados, n, 1)
		tempo1cpu.append(mean);
			
	for t in ncpus:
		saida.write("\n" + str(t) + ";" + str(t))
		index = 0
		for n in nsizes:
			mean, sd, error = calc_stats(dados, n, t)
			saida.write(";" + str(tempo1cpu[index]/mean))
			index += 1

	saida.close()
	print "Concluido \n"

def main():
	dados = [] # array das linhas
	
	parser = argparse.ArgumentParser(description='Estatistica.')
	parser.add_argument("-n", "--nome", help="nome do benchmark")
	parser.add_argument("-c", "--compilador", choices=["gcc", "icc", "icc2015", "pgi"], help="compilador do programa")
	parser.add_argument("-v", "--versao", choices=["parallel", "task"], help="versao do paralelismo")
	parser.add_argument("-e", "--entrada", nargs='+', help="arquivos de entrada")
	args = parser.parse_args()
	
	#print args.nome + " " + versao.format(args.versao)
	uteis.le_dados_execucao(args.nome + " " + versao.format(args.versao).replace("-", "_"), args.entrada, dados)
	
	#print len(dados)
	#print dados[0]
	
	#stats_speedup(args.nome, args.compilador, args.versao, dados)
	stats_tempo(args.nome, args.compilador, args.versao, dados)
	
if __name__ == "__main__":
	main()


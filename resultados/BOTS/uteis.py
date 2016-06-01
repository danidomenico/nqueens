#!/usr/bin/env python

import sys
import math
import numpy
from scipy.stats import t
import csv

def le_dados_execucao(benchmark, arquivos, dados):
	if len(arquivos) < 1:
		return
	for a in arquivos:
		with open(a, 'rb') as f:
			reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
			filtro = filter(lambda x: len(x) > 0 and x[0].upper() == benchmark.upper(), reader)
			for linha in filtro:
				dados.append(linha[1:])

def calc_stats(amostra):
	# confidence interval of 95%
	tdist = t.ppf(0.95, len(amostra)-1)
	mean = numpy.mean(amostra)
	std = numpy.std(amostra)
	error = tdist*(std/math.sqrt(len(amostra)))
	return mean, std, error
class ColetaDados(object):
	
	qtd_entradas = 0
	qtd_saidas = 0
	qtd_abastecimentos = [0,0,0,0]
	
	tempo_abastecimentos = 0
	
	def __init__ (self):
		
		qtd_entradas = 0
		qtd_saidas = 0
		qtd_abastecimentos = [0,0,0,0]

	# Fim __init__
	
	def addEntrada(self):
		
		self.qtd_entradas += 1
	
	# Fim addEntrada
	
	def addSaida(self):
		
		self.qtd_saidas += 1
	
	# Fim addSaida
	
	def addAbastecimento(self, i):
		
		self.qtd_abastecimentos[i] += 1
	
	# Fim addAbastecimento
	
	def addTempoAbastecimento(self, t):
		
		self.tempo_abastecimentos += t
	
	# Fim addTempoAbastecimento
	
	def printDados(self):
		print('\n\nEstatisticas:')
		print('  Quantidade de entradas: %d' % self.qtd_entradas)
		print('  Quantidade de saidas: %d' % self.qtd_saidas)
		print('  Throughput: %.2f%%' % ((self.qtd_saidas/self.qtd_entradas)*100))
		print('  Abastecimentos: %s' % self.qtd_abastecimentos)
		print('  Custo total de abastecimentos: %d minutos e %d segundos' % ((self.tempo_abastecimentos/60), ((self.tempo_abastecimentos%60))))
		print('\n')

	# Fim printDados
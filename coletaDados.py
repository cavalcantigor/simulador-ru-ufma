class ColetaDados(object):
	
	qtd_entradas = 0
	qtd_saidas = 0
	qtd_abastecimentos = [0,0,0,0]
	
	qtd_furoes = 0
	
	tempo_abastecimentos = 0
	
	tempo_ocupacao_b1 = []
	ocupacao_b1 = []
	
	def __init__ (self):
		
		qtd_entradas = 0
		qtd_saidas = 0
		qtd_abastecimentos = [0,0,0,0]
		qtd_furoes = 0
		tempo_ocupacao_b1 = 0.0
		
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
	
	def addFurao(self):
		
		self.qtd_furoes += 1
		
	# Fim addFurao
	
	def getFurao(self):
		
		return self.qtd_furoes
	
	# Fim getFurao
	
	def addOcupacaoB1(self, t):
		
		last = 0
		if len(self.ocupacao_b1) > 0:
			last = self.ocupacao_b1[-1]
		
		self.ocupacao_b1.append(t + last)
	
	# Fim addOcupacaoB1
	
	def addTempoOcupacaoB1(self, t):
		
		self.tempo_ocupacao_b1.append(t)
	
	# Fim addOcupacaoB1
	
	def getOcupacaoB1(self):
		
		return self.ocupacao_b1
	
	# Fim getOcupacaoB1
	
	def getTempoOcupacaoB1(self):
		
		return self.tempo_ocupacao_b1
	
	# Fim getOcupacaoB1
	
	def lista_utilizacao_b1(self):
		
		lista_utilizacao = []
		for i in range(0, len(self.ocupacao_b1)):
			lista_utilizacao.append((self.ocupacao_b1[i]/self.tempo_ocupacao_b1[i])*100)
		
		return lista_utilizacao
	
	def printDados(self):
		print('\n\nEstatisticas:')
		print('  Quantidade de entradas: %d' % self.qtd_entradas)
		print('  Quantidade de saidas: %d' % self.qtd_saidas)
		print('  Throughput: %.2f%%' % ((self.qtd_saidas/self.qtd_entradas)*100))
		print('  Quantidade de furoes: %d' % self.qtd_furoes)
		print('  Abastecimentos: %s' % self.qtd_abastecimentos)
		print('  Custo total de abastecimentos: %d minutos e %d segundos' % ((self.tempo_abastecimentos/60), ((self.tempo_abastecimentos%60))))
		#print('  Ocupacao da bandeja 1: %.2f%%' % ((self.tempo_ocupacao_b1/8100) * 100))
		print('\n')

	# Fim printDados
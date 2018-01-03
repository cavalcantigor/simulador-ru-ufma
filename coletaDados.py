class ColetaDados(object):
	
	qtd_entradas = 0
	qtd_saidas = 0
	qtd_abastecimentos = [0,0,0,0]
	
	qtd_furoes = 0
	
	tempo_abastecimentos = 0
	
	tempo_ocupacao_b1 = []
	ocupacao_b1 = []
	tempo_ocupacao_b2 = []
	ocupacao_b2 = []
	tempo_ocupacao_b3 = []
	ocupacao_b3 = []
	tempo_ocupacao_b4 = []
	ocupacao_b4 = []
	
	def __init__ (self):
		
		qtd_entradas = 0
		qtd_saidas = 0
		qtd_abastecimentos = [0,0,0,0]
		qtd_furoes = 0
		
		tempo_ocupacao_b1 = []
		ocupacao_b1 = []
		tempo_ocupacao_b2 = []
		ocupacao_b2 = []
		tempo_ocupacao_b3 = []
		ocupacao_b3 = []
		tempo_ocupacao_b4 = []
		ocupacao_b4 = []
	
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
	
	def addOcupacao(self, t, i):
		
		if i == 1:		
			last = 0
			if len(self.ocupacao_b1) > 0:
				last = self.ocupacao_b1[-1]
			
			self.ocupacao_b1.append(t + last)
		elif i == 2:
			last = 0
			if len(self.ocupacao_b2) > 0:
				last = self.ocupacao_b2[-1]
			
			self.ocupacao_b2.append(t + last)
		elif i == 3:
			last = 0
			if len(self.ocupacao_b3) > 0:
				last = self.ocupacao_b3[-1]
			
			self.ocupacao_b3.append(t + last)
		else:
			last = 0
			if len(self.ocupacao_b4) > 0:
				last = self.ocupacao_b4[-1]
			
			self.ocupacao_b4.append(t + last)
		# Fim if
		
	# Fim addOcupacao
	
	def addTempoOcupacao(self, t, i):
		
		if i == 1:		
			self.tempo_ocupacao_b1.append(t)
		elif i == 2:
			self.tempo_ocupacao_b2.append(t)
		elif i == 3:
			self.tempo_ocupacao_b3.append(t)
		else:
			self.tempo_ocupacao_b4.append(t)
		# Fim if
	
	# Fim addTempoOcupacao
	
	def getOcupacao(self, i):

		if i == 1:		
			return self.ocupacao_b1
		elif i == 2:
			return self.ocupacao_b2
		elif i == 3:
			return self.ocupacao_b3
		else:
			return self.ocupacao_b4
		# Fim if
		
	# Fim getOcupacao
	
	def getTempoOcupacao(self, i):
		
		if i == 1:		
			return self.tempo_ocupacao_b1
		elif i == 2:
			return self.tempo_ocupacao_b2
		elif i == 3:
			return self.tempo_ocupacao_b3
		else:
			return self.tempo_ocupacao_b4
		# Fim if
		
	# Fim getTempoOcupacao
	
	def lista_utilizacao(self, i):
		
		lista_utilizacao = []
		if i == 1:		
			for i in range(0, len(self.ocupacao_b1)):
				lista_utilizacao.append((self.ocupacao_b1[i]/self.tempo_ocupacao_b1[i])*100)
			return lista_utilizacao
		elif i == 2:
			for i in range(0, len(self.ocupacao_b2)):
				lista_utilizacao.append((self.ocupacao_b2[i]/self.tempo_ocupacao_b2[i])*100)
			return lista_utilizacao
		elif i == 3:
			for i in range(0, len(self.ocupacao_b3)):
				lista_utilizacao.append((self.ocupacao_b3[i]/self.tempo_ocupacao_b3[i])*100)
			return lista_utilizacao
		else:
			for i in range(0, len(self.ocupacao_b4)):
				lista_utilizacao.append((self.ocupacao_b4[i]/self.tempo_ocupacao_b4[i])*100)
			return lista_utilizacao
		# Fim if
	
	# Fim lista_utilizacao
	
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
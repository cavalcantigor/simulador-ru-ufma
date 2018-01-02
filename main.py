import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

# Variaveis globais

TEMPO_SIMULACAO = 8100							# Tempo total de simulacao (segundos) - corresponde ao horario das 11:30 as 13:45

TEMPO_ALTO_FLUXO = 5400							# Tempo de alto fluxo (segundos) - corresponde ao horario de 11:30 as 12:59
TEMPO_MEDIO_FLUXO = 7200						# Tempo de medio fluxo (segundos) - corresponde ao horario de 13:00 as 13:29
TEMPO_BAIXO_FLUXO = 8100						# Tempo de baixo fluxo (segundos) - corresponde ao horario de 13:30 as 13:45

TEMPO_MEDIO_REFEICAO = 10						# Tempo medio de refeicao (minutos) para uma pessoa

CHEGADAS_ALTO_FLUXO = 5							# Tempo entre chegadas em alto fluxo (chegadas por minuto)
CHEGADAS_MEDIO_FLUXO = 15						# Tempo entre chegadas em medio fluxo (chegadas por minuto)
CHEGADAS_BAIXO_FLUXO = 30						# Tempo entre chegadas em baixo fluxo (chegadas por minuto)

CHEGADAS_POR_MINUTO = 5							# Quantidade de chegadas em 1 minuto
PROBABILIDADE_FURO = 15							# Probabilidade de ter alguem furando a fila

QUANTIDADE_INICIAL_FILA = 30					# Quantidade inicial de pessoas na fila

QTD_REFEICOES_BANDEJA = [150, 230, 80, 130] 	# Quantidade de refeicoes servidas por bandeja
QTD_INICIAIS_BANDEJAS = [150, 230, 80, 130]		# Quantidades iniciais das refeicoes


def individuo(env, nome, fila_principal, fila_secundaria, recurso_talher, recurso_bandeja_1, recurso_bandeja_2, recurso_bandeja_3, recurso_bandeja_4, recurso_assento):

	# Cria requisicao para fila principal
	req_fila_principal = fila_principal.request()
	
	# Requisita fila principal
	yield req_fila_principal
	
	print('%s chegou na fila principal no tempo %.1f' % (nome, env.now))
	
	# Apos ganhar o uso da fila, passa 1 segundo até pegar a fila da direita ou esquerda
	yield env.timeout(1)
	
	# Cria requisicao para fila secundaria
	req_fila_secundaria = fila_secundaria.request()
	
	# Requista fila secundaria
	yield req_fila_secundaria
	
	print('%s chegou na fila da esquerda no tempo %.1f' % (nome, env.now))
	
	# Libera fila principal
	fila_principal.release(req_fila_principal)
	
	# Apos ganhar o uso da fila, faz um get_fila para ter ou nao atraso por conta de furo
	yield env.process(get_fila(env))
	
	# Cria requisicao pare recurso talher
	req_talher = recurso_talher.request()
	
	# Requisita recurso talher
	yield req_talher
	
	print('%s chegou para escolher talher no tempo %.1f' % (nome, env.now))
	
	# Libera fila secundaria
	fila_secundaria.release(req_fila_secundaria)
	
	# Tempo para escolher talher e bandeja - tempo medio de escolha
	yield env.timeout(3)
	
	req_bandeja_1 = recurso_bandeja_1.request()
	
	# Requisita recurso bandeja 1
	yield req_bandeja_1
	
	print('%s chegou na bandeja 1 no tempo %.1f' % (nome, env.now))
	
	# Libera talher
	recurso_talher.release(req_talher)
	
	# Pega refeicao e reabastece se for o caso
	yield env.process(get_refeicao(env, 0))
	
	req_bandeja_2 = recurso_bandeja_2.request()
	
	yield req_bandeja_2
	
	print('%s chegou na bandeja 2 no tempo %.1f' % (nome, env.now))
	
	recurso_bandeja_1.release(req_bandeja_1)
	
	# Pega refeicao e reabastece se for o caso
	yield env.process(get_refeicao(env, 1))
	
	req_bandeja_3 = recurso_bandeja_3.request()
	
	yield req_bandeja_3
	
	print('%s chegou na bandeja 3 no tempo %.1f' % (nome, env.now))
	
	recurso_bandeja_2.release(req_bandeja_2)
	
	# Pega refeicao e reabastece se for o caso
	yield env.process(get_refeicao(env, 2))
	
	req_bandeja_4 = recurso_bandeja_4.request()
	
	yield req_bandeja_4
	
	print('%s chegou na bandeja 4 no tempo %.1f' % (nome, env.now))
	
	recurso_bandeja_3.release(req_bandeja_3)
	
	# Pega refeicao e reabastece se for o caso
	yield env.process(get_refeicao(env, 3))
	
	req_assento = recurso_assento.request()
	
	yield req_assento
	
	print('%s chegou no assento no tempo %.1f' % (nome, env.now))
	
	recurso_bandeja_4.release(req_bandeja_4)
	
	yield env.timeout(abs(np.random.normal(TEMPO_MEDIO_REFEICAO, 3.0, size=None)) * 60)
	
	recurso_assento.release(req_assento)
	
	print('%s completou seu ciclo e saiu do restaurante no tempo %.1f' % (nome, env.now))
	
# Fim individuo


def get_fila(env):
	
	# Escolhe um numero entre 1 e 100
	n = random.randint(1, 100)
	
	if n >= PROBABILIDADE_FURO:
		yield env.timeout(abs(np.random.normal(5, 2.0, size=None))) # Gera um atraso de media 5 variacao 2
	else:
		yield env.timeout(abs(np.random.normal(2, 0.5, size=None))) # Gera um atraso de media 2 variacao 1
	
	# Fim if
	
# Fim get_fila


def get_refeicao(env, i):
	
	QTD_INICIAIS_BANDEJAS[i] -= 1
	
	if QTD_INICIAIS_BANDEJAS[i] == 0:
		# Tempo medio para troca de bacia de refeicao
		yield env.timeout(25)
		
		QTD_INICIAIS_BANDEJAS[i] = QTD_REFEICOES_BANDEJA[i]
		
	else:
		yield env.timeout(3)

# Fim get_refeicao
		
def gerador_individuo(env, fila_principal, fila_secundaria, recurso_talher, recurso_bandeja_1, recurso_bandeja_2, recurso_bandeja_3, recurso_bandeja_4, recurso_assento):
	
	request = fila_principal.request()
	yield request
	
	i = 0
	while True:
		
		if env.now <= TEMPO_ALTO_FLUXO:
			tempo_chegada = abs(np.random.normal(CHEGADAS_ALTO_FLUXO, 3.0, size=None))
		else:
			if env.now <= TEMPO_MEDIO_FLUXO:
				tempo_chegada = abs(np.random.normal(CHEGADAS_MEDIO_FLUXO, 3.0, size=None))
			else:
				if env.now <= TEMPO_BAIXO_FLUXO:
					tempo_chegada = abs(np.random.normal(CHEGADAS_BAIXO_FLUXO, 5.0, size=None))
				# Fim if
			# Fim if
		# Fim if
		
		# Consumindo tempo de simulacao para chegada do proximo individuo
		yield env.timeout(tempo_chegada)

		print('Individuo %d chegou no tempo %.1f' % (i, env.now))
		
		# Adicionando tempo para grafico
		lista_tempos.append(env.now)
		
		# Adicionando tamanho da fila para grafico
		lista_lotacao.append(len(fila_principal.queue))
		
		# Adicionando ocupacao de assento
		lista_assentos_ocupados.append(len(recurso_assento.users))
		
		# Inicia processo para individuo
		env.process(individuo(env, ('Individuo %d' % i), fila_principal, fila_secundaria, recurso_talher, recurso_bandeja_1, recurso_bandeja_2, recurso_bandeja_3, recurso_bandeja_4, recurso_assento))
		
		# Incrementa quantidade de pessoas que chegaram
		i += 1
		
		if i == QUANTIDADE_INICIAL_FILA:
			fila_principal.release(request)
		# Fim if
	# Fim while

# Fim gerador_individuo


def print_stats(res):
	print('%d de %d estao alocados.' % (res.count, res.capacity))
	print('  Usuarios:', res.users)
	print('  Quantidade em fila: %d' % len(res.queue))

# Fim print_stats

def plota_queue_fila():
	plt.figure(1)
	plt.plot(lista_tempos, lista_lotacao, 'go')
	plt.plot(lista_tempos, lista_lotacao, 'k:', color='orange')
	plt.grid(True)
	plt.xlabel('Tempo de Simulacao')
	plt.ylabel('Tamanho da fila')
	#plt.show()

# Fim plota_queue_fila

def plota_assentos():
	plt.figure(2)
	plt.plot(lista_tempos, lista_assentos_ocupados, 'go')
	plt.plot(lista_tempos, lista_assentos_ocupados, 'k:', color='orange')
	plt.grid(True)
	plt.xlabel('Tempo de Simulacao')
	plt.ylabel('Assentos ocupados')
	#plt.show()

# Fim plota_assentos
	

print('Simulacao da fila do RU')

# Cria ambiente de simulacao
env = simpy.Environment()

# Cria recurso fila principal
fila_principal = simpy.Resource(env, 1)

# Cria recurso fila secundaria
fila_secundaria = simpy.Resource(env, 1)

# Cria recurso talher
recurso_talher = simpy.Resource(env, 1)

# Cria recurso bandeja 1
recurso_bandeja_1 = simpy.Resource(env, 1)

# Cria recurso bandeja 2
recurso_bandeja_2 = simpy.Resource(env, 1)

# Cria recurso bandeja 3
recurso_bandeja_3 = simpy.Resource(env, 1)

# Cria recurso bandeja 4
recurso_bandeja_4 = simpy.Resource(env, 1)

# Cria recurso assento
recurso_assento = simpy.Resource(env, 200)

# Processo de geracao de individuos
proc = env.process(gerador_individuo(env, fila_principal, fila_secundaria, recurso_talher, recurso_bandeja_1, recurso_bandeja_2, recurso_bandeja_3, recurso_bandeja_4, recurso_assento))

# Variaveis para obtencao de grafico da queue da fila principal
lista_tempos = []
lista_lotacao = []

# Variavel para obtencao de grafico dos assentos
lista_assentos_ocupados = []

# Roda a simulacao
env.run(until=TEMPO_SIMULACAO)

print_stats(fila_principal)

plota_queue_fila()
plota_assentos()
plt.show()
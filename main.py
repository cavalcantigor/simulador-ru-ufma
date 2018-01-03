import simpy
import random
import numpy as np
import matplotlib.pyplot as plt
import datetime
from coletaDados import ColetaDados

# Variaveis globais

# Tempo adicionado 15 minutos iniciais
TEMPO_SIMULACAO = 9000							# Tempo total de simulacao (segundos) - corresponde ao horario das 11:30 as 13:45

TEMPO_ALTO_FLUXO = 6300							# Tempo de alto fluxo (segundos) - corresponde ao horario de 11:30 as 12:59
TEMPO_MEDIO_FLUXO = 8100						# Tempo de medio fluxo (segundos) - corresponde ao horario de 13:00 as 13:29
TEMPO_BAIXO_FLUXO = 9000						# Tempo de baixo fluxo (segundos) - corresponde ao horario de 13:30 as 13:45

TEMPO_MEDIO_REFEICAO = 10						# Tempo medio de refeicao (minutos) para uma pessoa

TEMPO_GET_REFEICAO = 3							# Tempo (segundos) em que individuo leva para ser servido em media
TEMPO_GET_TALHER = 3							# Tempo (segundos) em que o individuo leva para pegar talher

CHEGADAS_ALTO_FLUXO = 5							# Tempo entre chegadas em alto fluxo (chegadas por minuto)
CHEGADAS_MEDIO_FLUXO = 15						# Tempo entre chegadas em medio fluxo (chegadas por minuto)
CHEGADAS_BAIXO_FLUXO = 30						# Tempo entre chegadas em baixo fluxo (chegadas por minuto)

PROBABILIDADE_FURO = 15							# Probabilidade de ter alguem furando a fila

QTD_REFEICOES_BANDEJA = [150, 230, 80, 130] 	# Quantidade de refeicoes servidas por bandeja
QTD_INICIAIS_BANDEJAS = [150, 230, 80, 130]		# Quantidades iniciais das refeicoes

QTD_ASSENTOS = 200								# Quantidade de assentos disponiveis no restaurante

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
	yield env.process(get_fila(env, nome, fila_principal, fila_secundaria, recurso_talher, recurso_bandeja_1, recurso_bandeja_2, recurso_bandeja_3, recurso_bandeja_4, recurso_assento))
	
	# Cria requisicao pare recurso talher
	req_talher = recurso_talher.request()
	
	# Requisita recurso talher
	yield req_talher
	
	print('%s chegou para escolher talher no tempo %.1f' % (nome, env.now))
	
	# Libera fila secundaria
	fila_secundaria.release(req_fila_secundaria)
	
	# Tempo para escolher talher e bandeja
	yield env.process(get_talher(env))
	
	req_bandeja_1, tempo_fim, tempo_inicio_b1 = yield env.process(rotina_bandeja(env, nome, recurso_bandeja_1, 'bandeja 1', 0, recurso_talher, req_talher))
	
	req_bandeja_2, tempo_fim_b1, tempo_inicio_b2 = yield env.process(rotina_bandeja(env, nome, recurso_bandeja_2, 'bandeja 2', 1, recurso_bandeja_1, req_bandeja_1))
	
	dados.addOcupacao((tempo_fim_b1 - tempo_inicio_b1), 1)
	dados.addTempoOcupacao((tempo_fim_b1 - 900), 1)
	
	req_bandeja_3, tempo_fim_b2, tempo_inicio_b3 = yield env.process(rotina_bandeja(env, nome, recurso_bandeja_3, 'bandeja 3', 2, recurso_bandeja_2, req_bandeja_2))
	
	dados.addOcupacao((tempo_fim_b2 - tempo_inicio_b2), 2)
	dados.addTempoOcupacao((tempo_fim_b2 - 900), 2)
	
	req_bandeja_4, tempo_fim_b3, tempo_inicio_b4 = yield env.process(rotina_bandeja(env, nome, recurso_bandeja_4, 'bandeja 4', 3, recurso_bandeja_3, req_bandeja_3))
	
	dados.addOcupacao((tempo_fim_b3 - tempo_inicio_b3), 3)
	dados.addTempoOcupacao((tempo_fim_b3 - 900), 3)
	
	req_assento = recurso_assento.request()
	
	yield req_assento
	
	print('%s chegou no assento no tempo %.1f' % (nome, env.now))
	
	recurso_bandeja_4.release(req_bandeja_4)
	
	tempo_fim_b4 = env.now
	
	dados.addOcupacao((tempo_fim_b4 - tempo_inicio_b4), 4)
	dados.addTempoOcupacao((tempo_fim_b4 - 900), 4)
	
	# Media de 10 minutos para almocar
	yield env.timeout(TEMPO_MEDIO_REFEICAO * 60)
	
	recurso_assento.release(req_assento)
	
	print('%s completou seu ciclo e saiu do restaurante no tempo %.1f' % (nome, env.now))
	
	# Adicionando uma saida aos dados
	dados.addSaida()
	
# Fim individuo

def individuo_furao(env, nome, fila_secundaria, recurso_talher, recurso_bandeja_1, recurso_bandeja_2, recurso_bandeja_3, recurso_bandeja_4, recurso_assento):
	
	# Adiciona mais uma entrada
	dados.addEntrada()
	
	# Cria requisicao para fila secundaria
	req_fila_secundaria = fila_secundaria.request()
	
	# Requista fila secundaria
	yield req_fila_secundaria
	
	print('%s chegou na fila da esquerda no tempo %.1f' % (nome, env.now))

	# Apos ganhar o uso da fila, individuo furao apenas pega a fila
	yield env.timeout(abs(np.random.normal(2, 0.5, size=None))) # Gera um atraso de media 2 variacao 1
	
	# Cria requisicao pare recurso talher
	req_talher = recurso_talher.request()
	
	# Requisita recurso talher
	yield req_talher
	
	print('%s chegou para escolher talher no tempo %.1f' % (nome, env.now))
	
	# Libera fila secundaria
	fila_secundaria.release(req_fila_secundaria)
	
	# Tempo para escolher talher e bandeja
	yield env.process(get_talher(env))
	
	req_bandeja_1, tempo_fim, tempo_inicio_b1 = yield env.process(rotina_bandeja(env, nome, recurso_bandeja_1, 'bandeja 1', 0, recurso_talher, req_talher))
	
	req_bandeja_2, tempo_fim_b1, tempo_inicio_b2 = yield env.process(rotina_bandeja(env, nome, recurso_bandeja_2, 'bandeja 2', 1, recurso_bandeja_1, req_bandeja_1))
	
	dados.addOcupacao((tempo_fim_b1 - tempo_inicio_b1), 1)
	dados.addTempoOcupacao((tempo_fim_b1 - 900), 1)
	
	req_bandeja_3, tempo_fim_b2, tempo_inicio_b3 = yield env.process(rotina_bandeja(env, nome, recurso_bandeja_3, 'bandeja 3', 2, recurso_bandeja_2, req_bandeja_2))
	
	dados.addOcupacao((tempo_fim_b2 - tempo_inicio_b2), 2)
	dados.addTempoOcupacao((tempo_fim_b2 - 900), 2)
	
	req_bandeja_4, tempo_fim_b3, tempo_inicio_b4 = yield env.process(rotina_bandeja(env, nome, recurso_bandeja_4, 'bandeja 4', 3, recurso_bandeja_3, req_bandeja_3))
	
	dados.addOcupacao((tempo_fim_b3 - tempo_inicio_b3), 3)
	dados.addTempoOcupacao((tempo_fim_b3 - 900), 3)
	
	req_assento = recurso_assento.request()
	
	yield req_assento
	
	print('%s chegou no assento no tempo %.1f' % (nome, env.now))
	
	recurso_bandeja_4.release(req_bandeja_4)
	
	tempo_fim_b4 = env.now
	
	dados.addOcupacao((tempo_fim_b4 - tempo_inicio_b4), 4)
	dados.addTempoOcupacao((tempo_fim_b4 - 900), 4)
	
	# Media de 10 minutos para almocar
	yield env.timeout(TEMPO_MEDIO_REFEICAO * 60)
	
	recurso_assento.release(req_assento)
	
	print('%s completou seu ciclo e saiu do restaurante no tempo %.1f' % (nome, env.now))
	
	# Adicionando uma saida aos dados
	dados.addSaida()
	
# Fim individuo_furao

def rotina_bandeja(env, nome, recurso_atual, str_recurso_atual, i, recurso_anterior, req_anterior):

	req = recurso_atual.request()
	
	# Requisita recurso atual
	yield req
	
	# Quando consegue o recurso eh que o tempo conta de fato
	tempo_ini = env.now
	
	print('%s chegou na %s no tempo %.1f' % (nome, str_recurso_atual, env.now))
	
	# Libera recurso anterior
	recurso_anterior.release(req_anterior)
	
	# Tempo em que libera o recurso anterior
	tempo_release = env.now
	
	# Pega refeicao e reabastece se for o caso
	yield env.process(get_refeicao(env, i))
	
	return req, tempo_release, tempo_ini
	
# Fim rotina_bandeja

def get_fila(env, nome, fila_principal, fila_secundaria, recurso_talher, recurso_bandeja_1, recurso_bandeja_2, recurso_bandeja_3, recurso_bandeja_4, recurso_assento):
	
	# Escolhe um numero entre 1 e 100
	n = random.randint(1, 100)
	
	if n <= PROBABILIDADE_FURO:
		
		print('Valor de n: %d' % n)
		
		# Incrementa a quantidade de furoes
		dados.addFurao()
		
		print('Furao %d entrou na frente do %s no tempo %d' % (dados.getFurao(), nome, env.now))
		
		# Inicia processo do invididuo furao
		env.process(individuo_furao(env, ('Furao %d' % dados.getFurao()), fila_secundaria, recurso_talher, recurso_bandeja_1, recurso_bandeja_2, recurso_bandeja_3, recurso_bandeja_4, recurso_assento))
		
		# Tempo do furao pegar a fila
		yield env.timeout(1)
	else:
		yield env.timeout(np.random.normal(2, 0.2, size=None)) # Gera um atraso de media 2 variacao 0.2
	
	# Fim if
	
# Fim get_fila

def get_talher(env):
	
	yield env.timeout(np.random.normal(TEMPO_GET_TALHER, 0.7, size=None))
	
# Fim get_talher

def get_refeicao(env, i):
	
	QTD_INICIAIS_BANDEJAS[i] -= 1
	
	if QTD_INICIAIS_BANDEJAS[i] == 0:
		# Tempo medio para troca de bacia de refeicao
		yield env.timeout(25)
		
		QTD_INICIAIS_BANDEJAS[i] = QTD_REFEICOES_BANDEJA[i]
		
		dados.addAbastecimento(i)
		
		dados.addTempoAbastecimento(25)
		
	else:
		yield env.timeout(np.random.normal(TEMPO_GET_REFEICAO, 0.7, size=None))

# Fim get_refeicao
		
def gerador_individuo(env, flag, fila_principal, fila_secundaria, recurso_talher, recurso_bandeja_1, recurso_bandeja_2, recurso_bandeja_3, recurso_bandeja_4, recurso_assento):
	
	request = fila_principal.request()
	yield request
	
	i = 0
	while True:
		
		if env.now <= TEMPO_ALTO_FLUXO:
			tempo_chegada = np.random.normal(CHEGADAS_ALTO_FLUXO, 1.0, size=None)
		else:
			if env.now <= TEMPO_MEDIO_FLUXO:
				tempo_chegada = np.random.normal(CHEGADAS_MEDIO_FLUXO, 2.0, size=None)
			else:
				if env.now <= TEMPO_BAIXO_FLUXO:
					tempo_chegada = np.random.normal(CHEGADAS_BAIXO_FLUXO, 3.0, size=None)
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
		
		# Adicionando mais uma entrada as estatisticas
		dados.addEntrada()
		
		# Incrementa quantidade de pessoas que chegaram
		i += 1
		
		if env.now >= 900 and flag == True:
			flag = False
			fila_principal.release(request)
		# Fim if
	# Fim while

# Fim gerador_individuo


def print_stats(res, nome):
	print('\n\n%s:' % nome)
	print('  %d de %d estao alocados.' % (res.count, res.capacity))
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

# Fim plota_queue_fila

def plota_assentos():
	plt.figure(2)
	plt.plot(lista_tempos, lista_assentos_ocupados, 'go')
	plt.plot(lista_tempos, lista_assentos_ocupados, 'k:', color='orange')
	plt.axhline(y=QTD_ASSENTOS, linewidth=1, color='r') # Desenha limite de quantidade de assentos
	plt.grid(True)
	plt.xlabel('Tempo de Simulacao')
	plt.ylabel('Assentos ocupados')

# Fim plota_assentos

def plota_ocupacao_bandeja():
	plt.figure(3)
	plt.plot(dados.getTempoOcupacao(1), dados.lista_utilizacao(1), 'k:', color='red', label="Bandeja 1")
	plt.plot(dados.getTempoOcupacao(2), dados.lista_utilizacao(2), 'k:', color='orange', label="Bandeja 2")
	plt.plot(dados.getTempoOcupacao(3), dados.lista_utilizacao(3), 'k:', color='green', label="Bandeja 3")
	plt.plot(dados.getTempoOcupacao(4), dados.lista_utilizacao(4), 'k:', color='blue', label="Bandeja 4")
	plt.grid(True)
	plt.legend(loc = 'lower right')
	plt.xlabel('Tempo de Simulacao')
	plt.ylabel('Ocupacao da bandeja')

# Fim plota_ocupacao_bandeja

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
recurso_assento = simpy.Resource(env, QTD_ASSENTOS)

# Flag para uso na rotina de geracao de individuo
flag = True

# Seed do random para numeros aleatorios
random.seed(datetime.datetime.now())

# Processo de geracao de individuos
proc = env.process(gerador_individuo(env, flag, fila_principal, fila_secundaria, recurso_talher, recurso_bandeja_1, recurso_bandeja_2, recurso_bandeja_3, recurso_bandeja_4, recurso_assento))

# Variaveis para obtencao de grafico da queue da fila principal
lista_tempos = []
lista_lotacao = []

# Variavel que controla a quantidade de furoes
qtd_furoes = 0

# Variavel para obtencao de grafico dos assentos
lista_assentos_ocupados = []

# Dados da simulacao para estatistica
dados = ColetaDados()

# Roda a simulacao
env.run(until=TEMPO_SIMULACAO)

# Printa status das filas
print_stats(fila_principal, 'Fila Principal')
print_stats(fila_secundaria, 'Fila Secundaria')
print_stats(recurso_talher, 'Talher')
print_stats(recurso_bandeja_1, 'Bandeja 1')
print_stats(recurso_bandeja_2, 'Bandeja 2')
print_stats(recurso_bandeja_3, 'Bandeja 3')
print_stats(recurso_bandeja_4, 'Bandeja 4')

# Printa os dados coletados
dados.printDados()

#plota_queue_fila()
#plota_assentos()
#plota_ocupacao_bandeja()
plt.show()
plt.close()

#print(dados.getOcupacao(3)[:10])
#print(dados.getTempoOcupacao(3)[:10])

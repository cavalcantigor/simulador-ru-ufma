Trabalho final da disciplina de Processos Estocásticos do curso de Ciência da Computação - UFMA.

1. Objetivo<br />
  O objetivo do trabalho é implementar um modelo de filas utilizando o Simpy para a simulação do Restaurante Universitário da UFMA.
A modelagem levou em consideração os tempos de chegada, escolha de talheres e bandeja, tempo para ser servido ao longo das refeições
e tempo para sentar-se e almoçar.

2. O modelo<br />
  O modelo conta com duas fila, uma principal e uma secundária. A fila secundária é alimentada com indivíduos que saem da principal e furões.
Os furões são indivíduos que tomam o acesso diretamente na fila secundária sem passar pela principal. A fila principal é formada pelos indivíduos
que desejam utilizar o restaurante.
  O serviço do sistema inicia-se ao passar da fila secundária, onde consideramos que o indivíduo já está dentro do restaurante. Uma vez dentro
deverá escolher talher e bandeja, ser servido, sentar, almoçar e finalmente sair do restaurante. Os tempos de cada um desses processos utilizaram
distribuições normais e médias escolhidos arbitrariamente com base em simulações efetuadas.
  As limitações do sistema estã nas quantidade de refeições que são servidas ao longo do tempo de simualação, onde uma vez esgotadas estas deverão
ser reabastecidas e na quantidade de assentos disponíveis.

3. O problema<br />
  O problema proposto está na quantidade de indivíduos na fila ao longo do tempo. A intenção do modelo tem por finalidade testar diferentes
cenários que resulte na quantidade de indivíduos na fila ao final do tempo de simulação igual a zero. Ou seja, reduzir a zero os indivíduos
esperando para serem atendidos assim que a simulação acabar.

4. Dependências<br />
  O modelo está implementado em Python e utiliza o Simpy (https://simpy.readthedocs.io/en/latest/). Também utiliza o Matplotlib para plotar os
gráficos e Numpy como biblioteca de apoio para as distribuições estatísticas.

[![Coverage Status](https://coveralls.io/repos/github/thales-t/balanceamento_carga/badge.svg?branch=master)](https://coveralls.io/github/thales-t/balanceamento_carga?branch=master)

# balanceamento_carga
python 3.7

Input (Entrada):
    Deve ser um arquivo texto com o nome 'input.txt' no mesmo diretório do arquivo python que esta
    sendo executado ('balanceamento_carga.py'). 
    input.txt deve ser um arquivo onde:
    a primeira linha possui o valor de ttask ;
    a segunda linha possui o valor de umax ;
    as demais linhas contém o número de novos usuários para cada tick


Limites:

    1 ≤ ttask ≤ 10
    
    1 ≤ umax ≤ 10


Output (Saída):
    Um arquivo ('output.txt') onde cada linha contém uma lista de servidores disponíveis no final de cada tick,
representado pelo número de usuários em cada servidor separados por vírgula e, ao final, o
custo total por utilização dos servidores
   

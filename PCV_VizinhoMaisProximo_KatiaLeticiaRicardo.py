import csv                                                                  #adiciona biblioteca para ler o csv
import sys                                                                  #adiciona biblioteca para passar o nome de arquivo no terminal, caso nao seja o arquivo cidades.csv

def ler_distancias_csv(caminho_arquivo):                                    # define uma função que recebe o caminho do arquivo CSV e le as distancias entre as cidades
    distancias = {}                                                         # cria um dicionário vazio para guardar as distâncias entre cidades

    with open(caminho_arquivo, newline='', encoding='utf-8-sig') as f:      # abre o arquivo CSV  # newline='' evita problemas de quebra de linha # encoding='utf-8-sig' se o arquivo foi crado no excel
        reader = csv.reader(f, delimiter=',')                               # cria um leitor CSV usando vírgula como separador
        cabecalho = next(reader)                                            # lê a primeira linha do arquivo (cabeçalho)
        cidades = [c.strip() for c in cabecalho[1:] if c.strip()]           # cria uma lista de cidades ignorando a primeira linha, removendo os espaços e filtrando valores vazios

        for linha in reader:                                                # percorre cada linha do CSV
            if not linha or not linha[0].strip():                           # ignora linhas vazias ou sem cidade de origem
                continue                                            
            cidade_origem = linha[0].strip()                                # pega o nome da cidade de origem (primeira coluna)
            distancias[cidade_origem] = {}                                  # grava as distâncias dessa cidade no dicionario de distancias
            for i, cidade_destino in enumerate(cidades):                    # percorre cada cidade de destino
                valor = linha[i + 1].strip().replace(',', '.')              # pega o valor da distancia da cidade removendo espaco e trocando o decimal
                distancias[cidade_origem][cidade_destino] = float(valor)    # converte o valor para float e armazena no dicionário

    return cidades, distancias                                              # retorna a lista de cidades e o dicionário de distâncias


def vizinho_mais_proximo(cidades, distancias, cidade_inicio):               # função que implementa a heurística do vizinho mais próximo
    nao_visitadas = set(cidades)                                            # cria um conjunto com todas as cidades ainda não visitada
    trajeto = [cidade_inicio]                                               # inicia o trajeto com a cidade inicial
    nao_visitadas.remove(cidade_inicio)                                     # remove a cidade das não visitadas
    custo_total = 0                                                         # inicializa o custo total do trajeto
    cidade_atual = cidade_inicio                                            # define a cidade atual como a inicial

    while nao_visitadas:                                                                           # enquanto ainda houver cidades para visitar
        mais_proxima = min(nao_visitadas, key=lambda cidade: distancias[cidade_atual][cidade])     # encontra a cidade mais próxima da atual, usando a função min com base na menor distância e a funcao lambda pra buscar as distancias no dicionario
        distancia = distancias[cidade_atual][mais_proxima]                                         # pega a distância da cidade atual até a cidade com menor distancia encontrada antes
        custo_total += distancia                                                                   # soma essa distância ao custo total
																																																		
        trajeto.append(mais_proxima)                                                               # adiciona a cidade ao trajeto
        nao_visitadas.remove(mais_proxima)                                                         # remove a cidade das não visitadas 
        cidade_atual = mais_proxima                                                                # atualiza a cidade atual

    distancia_retorno = distancias[cidade_atual][cidade_inicio]             # pega a distância da última cidade de volta à inicial
    custo_total += distancia_retorno                                        # soma essa distância ao custo total
    trajeto.append(cidade_inicio)                                           # adiciona o retorno ao início
																																  

    return trajeto, custo_total                                             # retorna o caminho completo e o custo total


def testar_todas_origens(cidades, distancias):                              # função que testa o algoritmo partindo de cada cidade e retorna a melhor rota encontrada
    melhor_trajeto = None                                                   # variável para guardar o melhor trajeto encontrado (começa vazia)
    melhor_custo = float('inf')                                             # variável para guardar o menor custo encontrado (começa com infinito para garantir que qualquer custo real seja menor)
    melhor_origem = None                                                    # variável para guardar qual cidade de origem gerou o melhor resultado

    print("Testando todas as cidades como ponto de partida...\n")          # avisa o usuário que o teste está começando

    for cidade in cidades:                                                  # percorre cada cidade da lista como possível ponto de partida
        trajeto, custo = vizinho_mais_proximo(cidades, distancias, cidade)  # executa o algoritmo do vizinho mais próximo partindo dessa cidade
        print(f"  Origem: {cidade:<20} Custo: {custo:.0f} km")             # imprime o resultado para essa origem (nome alinhado em 20 caracteres)

        if custo < melhor_custo:                                            # se o custo desta rota for menor que o melhor até agora
            melhor_custo = custo                                            # atualiza o melhor custo
            melhor_trajeto = trajeto                                        # atualiza o melhor trajeto
            melhor_origem = cidade                                          # atualiza a melhor cidade de origem

    return melhor_trajeto, melhor_custo, melhor_origem                      # retorna o melhor trajeto, seu custo e a cidade de origem


caminho_csv = sys.argv[1] if len(sys.argv) > 1 else "cidades.csv"  # define o caminho do CSV, ou pelo informado ou pelo nome cidades.csv
print("=" * 50)                                                    # imprime frufru pro titulo do trabalho hehehhe
print("  PCV — Heurística do Vizinho Mais Próximo")                # imprime titulo do trabalho hehehhe
print("=" * 50)                                                    # imprime frufru pro titulo do trabalho hehehhe

cidades, distancias = ler_distancias_csv(caminho_csv)              # chama a função para ler o CSV e obter dados

print(f"Cidades ({len(cidades)}): {', '.join(cidades)}\n")         # imprime a lista de cidades

melhor_trajeto, melhor_custo, melhor_origem = testar_todas_origens(cidades, distancias)  # testa todas as origens e pega a melhor rota

print("\n" + "=" * 50)                                                      # imprime frufru
print(f"  MELHOR RESULTADO")                                                # título da melhor rota
print("=" * 50)                                                             # imprime frufru
print(f"Cidade de início: {melhor_origem}")                                 # imprime a cidade de origem que gerou a melhor rota
print(f"Trajeto: {' → '.join(melhor_trajeto)}")                             # imprime o caminho completo da melhor rota
print(f"Custo total: {melhor_custo:.0f} km")                                # imprime o custo total da melhor rota
print("=" * 50 + "\n")                                                      # imprime frufru
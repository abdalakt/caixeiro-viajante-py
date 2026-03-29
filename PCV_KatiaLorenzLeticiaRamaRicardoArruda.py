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
        print(f"  {cidade_atual} → {mais_proxima}  ({distancia:.0f} km)")                          # imprime o passo do trajeto ex.: "CIDADE A -> CIDADE B (xx km)" -- assumi que a distancia é em km
        trajeto.append(mais_proxima)                                                               # adiciona a cidade ao trajeto
        nao_visitadas.remove(mais_proxima)                                                         # remove a cidade das não visitadas 
        cidade_atual = mais_proxima                                                                # atualiza a cidade atual

    distancia_retorno = distancias[cidade_atual][cidade_inicio]                             # pega a distância da última cidade de volta à inicial
    custo_total += distancia_retorno                                                        # soma essa distância ao custo total
    trajeto.append(cidade_inicio)                                                           # adiciona o retorno ao início
    print(f"  {cidade_atual} → {cidade_inicio}  ({distancia_retorno:.0f} km)  [retorno]")   # imprime o retorno ao ponto inicial

    return trajeto, custo_total                                                             # retorna o caminho completo e o custo total


caminho_csv = sys.argv[1] if len(sys.argv) > 1 else "cidades.csv"  # define o caminho do CSV, ou pelo informado ou pelo nome cidades.csv
print("=" * 50)                                                    # imprime frufru pro titulo do trabalho hehehhe
print("  PCV — Heurística do Vizinho Mais Próximo")                # imprime titulo do trabalho hehehhe
print("=" * 50)                                                    # imprime frufru pro titulo do trabalho hehehhe

cidades, distancias = ler_distancias_csv(caminho_csv)              # chama a função para ler o CSV e obter dados                       
cidade_inicio = cidades[0]                                         # define a primeira cidade como ponto inicial

print(f"Cidades ({len(cidades)}): {', '.join(cidades)}")           # imprime a lista de cidades
print(f"Cidade de início: {cidade_inicio}")                        # imprime a cidade inicial
print("Percurso:")                                                 # título da saída do percurso

trajeto, custo_total = vizinho_mais_proximo(cidades, distancias, cidade_inicio)   # executa o algoritmo do vizinho mais próximo

print("=" * 50)                                     # imprime frufru  
print(f"Trajeto: {' → '.join(trajeto)}")            # imprime o caminho completo
print(f"Custo total: {custo_total:.0f} km")         # imprime o custo total arredondado
print("=" * 50 + "\n")                              # imprime frufru  
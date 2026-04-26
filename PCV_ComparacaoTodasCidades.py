import csv                                                                   # biblioteca para leitura de arquivos csv
import sys                                                                   # biblioteca para permitir passar o nome do arquivo via terminal


def ler_distancias_csv(caminho_arquivo):                                     # função para ler o csv e montar a estrutura de dados
    distancias = {}                                                          # dicionário que armazenará as distâncias entre as cidades

    with open(caminho_arquivo, newline='', encoding='utf-8-sig') as f:       # abre o arquivo csv
        leitor = csv.reader(f, delimiter=',')                                # define o leitor csv com separador vírgula
        cabecalho = next(leitor)                                             # lê a primeira linha do arquivo

        cidades = [c.strip() for c in cabecalho[1:] if c.strip()]             # cria lista de cidades removendo espaços

        for linha in leitor:                                                  # percorre cada linha do arquivo
            if not linha or not linha[0].strip():                             # ignora linhas vazias
                continue

            origem = linha[0].strip()                                         # pega a cidade de origem
            distancias[origem] = {}                                           # cria entrada no dicionário

            for i, destino in enumerate(cidades):                             # percorre cada cidade de destino
                valor = linha[i + 1].strip().replace(',', '.')                # trata o valor da distância
                distancias[origem][destino] = float(valor)                    # armazena como número

    return cidades, distancias                                                # retorna cidades e distâncias


def vizinho_mais_proximo(cidades, distancias, cidade_inicio, mostrar_passos=False):  # implementação da heurística
    nao_visitadas = set(cidades)                                              # conjunto de cidades não visitadas
    trajeto = [cidade_inicio]                                                 # inicia trajeto pela cidade inicial
    nao_visitadas.remove(cidade_inicio)                                       # remove a cidade inicial das não visitadas

    cidade_atual = cidade_inicio                                              # define cidade atual
    custo_total = 0                                                           # inicia custo total

    while nao_visitadas:                                                      # enquanto houver cidades a visitar
        mais_proxima = min(
            nao_visitadas,
            key=lambda cidade: distancias[cidade_atual][cidade]               # escolhe a cidade mais próxima
        )

        distancia = distancias[cidade_atual][mais_proxima]                    # pega a distância até a cidade escolhida
        custo_total += distancia                                              # soma ao custo total

        if mostrar_passos:                                                    # imprime o passo se solicitado
            print(f"  {cidade_atual} → {mais_proxima} ({distancia:.0f} km)")

        trajeto.append(mais_proxima)                                          # adiciona cidade ao trajeto
        nao_visitadas.remove(mais_proxima)                                    # remove cidade das não visitadas
        cidade_atual = mais_proxima                                           # atualiza cidade atual

    distancia_retorno = distancias[cidade_atual][cidade_inicio]               # calcula retorno à origem
    custo_total += distancia_retorno                                          # soma retorno ao custo total
    trajeto.append(cidade_inicio)                                             # fecha o ciclo

    if mostrar_passos:                                                        # imprime retorno se solicitado
        print(f"  {cidade_atual} → {cidade_inicio} ({distancia_retorno:.0f} km) [retorno]")

    return trajeto, custo_total                                               # retorna caminho e custo


def testar_todas_as_origens(cidades, distancias):                             # testa todas as cidades como origem
    resultados = []                                                           # lista para armazenar resultados

    for cidade_inicio in cidades:                                             # percorre todas as cidades
        trajeto, custo = vizinho_mais_proximo(
            cidades,
            distancias,
            cidade_inicio,
            mostrar_passos=False
        )

        resultados.append({
            "origem": cidade_inicio,
            "trajeto": trajeto,
            "custo": custo
        })

    melhor = min(resultados, key=lambda item: item["custo"])                  # encontra o menor custo

    return resultados, melhor                                                 # retorna todos os resultados e o melhor


def imprimir_resultados(resultados, melhor):                                  # imprime resultados principais
    print("=" * 70)
    print("comparação da heurística saindo de todas as cidades")
    print("=" * 70)

    print("\nresultados por cidade inicial:\n")

    resultados_ordenados = sorted(resultados, key=lambda item: item["custo"]) # ordena do menor para o maior custo

    for item in resultados_ordenados:
        print(f"origem: {item['origem']:<20} | custo: {item['custo']:.0f} km")

    print("\n" + "=" * 70)
    print("melhor resultado encontrado")
    print("=" * 70)

    print(f"cidade inicial: {melhor['origem']}")
    print(f"custo total: {melhor['custo']:.0f} km")
    print("trajeto:")
    print(" → ".join(melhor["trajeto"]))
    print("=" * 70)


def imprimir_diferencas(resultados, melhor):                                  # mostra diferença em relação ao melhor custo
    melhor_custo = melhor["custo"]                                            # pega o menor custo encontrado

    print("\n" + "=" * 70)
    print("diferença de custo em relação ao melhor resultado")
    print("=" * 70)

    resultados_ordenados = sorted(resultados, key=lambda item: item["custo"]) # ordena os resultados

    for item in resultados_ordenados:
        diferenca = item["custo"] - melhor_custo                              # calcula diferença absoluta
        percentual = (diferenca / melhor_custo) * 100                         # calcula diferença percentual

        print(
            f"origem: {item['origem']:<20} | "
            f"custo: {item['custo']:.0f} km | "
            f"diferença: +{diferenca:.0f} km | "
            f"{percentual:.2f}% acima do melhor"
        )


def salvar_resultados_csv(resultados, nome_arquivo="resultado_comparacao_origens.csv"):  # salva resultados em csv
    with open(nome_arquivo, mode="w", newline="", encoding="utf-8-sig") as f:
        escritor = csv.writer(f)

        escritor.writerow(["origem", "custo_km", "trajeto"])                 # cabeçalho do arquivo

        for item in resultados:
            escritor.writerow([
                item["origem"],
                round(item["custo"], 0),
                " -> ".join(item["trajeto"])
            ])

    print(f"\narquivo gerado: {nome_arquivo}")


def gerar_grafico_comparativo(resultados):                                   # função para gerar gráfico comparativo
    import matplotlib.pyplot as plt                                           # biblioteca para criação de gráficos

    resultados_ordenados = sorted(resultados, key=lambda item: item["custo"]) # ordena do menor para o maior custo

    origens = [item["origem"] for item in resultados_ordenados]               # nomes das cidades
    custos = [item["custo"] for item in resultados_ordenados]                 # custos totais

    plt.figure(figsize=(12, 6))                                               # tamanho da figura
    plt.bar(origens, custos)                                                  # cria gráfico de barras

    plt.title("comparação do custo por cidade inicial")                       # título do gráfico
    plt.xlabel("cidade inicial")                                              # eixo x
    plt.ylabel("custo total (km)")                                            # eixo y

    plt.xticks(rotation=45, ha="right")                                       # gira nomes das cidades
    plt.tight_layout()                                                        # ajusta espaçamento

    plt.savefig("grafico_comparacao_origens.png", dpi=300)                   # salva gráfico
    plt.show()                                                                # exibe gráfico


def main():                                                                   # função principal
    caminho_csv = sys.argv[1] if len(sys.argv) > 1 else "cidades2.csv"        # define arquivo de entrada

    print("=" * 70)
    print("pcv — comparação da heurística do vizinho mais próximo")
    print("=" * 70)

    cidades, distancias = ler_distancias_csv(caminho_csv)                     # lê os dados do csv

    print(f"\narquivo utilizado: {caminho_csv}")
    print(f"quantidade de cidades: {len(cidades)}")
    print(f"cidades: {', '.join(cidades)}\n")

    resultados, melhor = testar_todas_as_origens(cidades, distancias)         # executa análise

    imprimir_resultados(resultados, melhor)                                   # mostra resultados
    imprimir_diferencas(resultados, melhor)                                   # mostra diferenças
    salvar_resultados_csv(resultados)                                         # salva csv
    gerar_grafico_comparativo(resultados)                                     # gera gráfico


main()                                                                        # executa o programa
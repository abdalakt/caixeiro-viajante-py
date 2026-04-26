import csv                                                                   # biblioteca para leitura de arquivos csv
import sys                                                                   # biblioteca para permitir passar o nome do arquivo via terminal
import time                                                                  # biblioteca para medir tempo de execução


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

            for i, destino in enumerate(cidades):                             # percorre cada cidade destino
                valor = linha[i + 1].strip().replace(',', '.')                # trata o valor da distância
                distancias[origem][destino] = float(valor)                    # converte para número

    return cidades, distancias                                                # retorna cidades e distâncias


def calcular_custo_trajeto(trajeto, distancias):                              # calcula o custo total de um trajeto
    custo = 0                                                                 # inicia custo

    for i in range(len(trajeto) - 1):                                          # percorre pares consecutivos da rota
        origem = trajeto[i]                                                   # cidade de origem
        destino = trajeto[i + 1]                                               # cidade destino
        custo += distancias[origem][destino]                                  # soma distância

    return custo                                                              # retorna custo total


def vizinho_mais_proximo(cidades, distancias, cidade_inicio):                 # heurística do vizinho mais próximo
    nao_visitadas = set(cidades)                                              # conjunto de cidades não visitadas
    trajeto = [cidade_inicio]                                                 # inicia trajeto pela cidade inicial
    nao_visitadas.remove(cidade_inicio)                                       # remove cidade inicial

    cidade_atual = cidade_inicio                                              # define cidade atual

    while nao_visitadas:                                                      # enquanto houver cidade não visitada
        mais_proxima = min(
            nao_visitadas,
            key=lambda cidade: distancias[cidade_atual][cidade]               # escolhe cidade com menor distância
        )

        trajeto.append(mais_proxima)                                          # adiciona ao trajeto
        nao_visitadas.remove(mais_proxima)                                    # remove das não visitadas
        cidade_atual = mais_proxima                                           # atualiza cidade atual

    trajeto.append(cidade_inicio)                                             # retorna à cidade inicial

    custo_total = calcular_custo_trajeto(trajeto, distancias)                 # calcula custo total

    return trajeto, custo_total                                               # retorna trajeto e custo


def aplicar_2opt(trajeto, distancias):                                        # aplica melhoria local 2-opt
    melhor_trajeto = trajeto[:]                                               # copia o trajeto inicial
    melhor_custo = calcular_custo_trajeto(melhor_trajeto, distancias)         # calcula custo inicial
    melhorou = True                                                           # controla se houve melhoria
    trocas = 0                                                                # conta quantas trocas foram aceitas
    avaliacoes = 0                                                            # conta quantas rotas foram avaliadas

    while melhorou:                                                           # repete enquanto houver melhoria
        melhorou = False                                                      # assume que não melhorou nesta rodada

        for i in range(1, len(melhor_trajeto) - 2):                            # evita alterar a primeira cidade
            for j in range(i + 1, len(melhor_trajeto) - 1):                    # evita alterar o retorno final
                if j - i == 1:                                                # ignora cidades vizinhas imediatas
                    continue

                novo_trajeto = (
                    melhor_trajeto[:i] +
                    melhor_trajeto[i:j][::-1] +
                    melhor_trajeto[j:]
                )                                                             # inverte um trecho da rota

                novo_custo = calcular_custo_trajeto(novo_trajeto, distancias) # calcula custo da nova rota
                avaliacoes += 1                                               # conta avaliação feita

                if novo_custo < melhor_custo:                                 # se melhorou, aceita a troca
                    melhor_trajeto = novo_trajeto                              # atualiza trajeto
                    melhor_custo = novo_custo                                  # atualiza custo
                    melhorou = True                                           # marca que houve melhoria
                    trocas += 1                                               # conta troca aceita

    return melhor_trajeto, melhor_custo, trocas, avaliacoes                   # retorna resultado melhorado


def testar_todas_as_origens(cidades, distancias):                             # testa todas as cidades como origem
    resultados = []                                                           # lista de resultados

    for cidade_inicio in cidades:                                             # percorre cada cidade inicial
        inicio_tempo = time.perf_counter()                                    # inicia medição de tempo

        trajeto_inicial, custo_inicial = vizinho_mais_proximo(
            cidades,
            distancias,
            cidade_inicio
        )                                                                     # roda vizinho mais próximo

        trajeto_2opt, custo_2opt, trocas, avaliacoes = aplicar_2opt(
            trajeto_inicial,
            distancias
        )                                                                     # aplica melhoria 2-opt

        fim_tempo = time.perf_counter()                                       # finaliza medição
        tempo_execucao = fim_tempo - inicio_tempo                             # calcula tempo total

        melhoria_km = custo_inicial - custo_2opt                              # calcula ganho absoluto
        melhoria_percentual = (melhoria_km / custo_inicial) * 100             # calcula ganho percentual

        resultados.append({
            "origem": cidade_inicio,
            "trajeto_inicial": trajeto_inicial,
            "custo_inicial": custo_inicial,
            "trajeto_2opt": trajeto_2opt,
            "custo_2opt": custo_2opt,
            "melhoria_km": melhoria_km,
            "melhoria_percentual": melhoria_percentual,
            "tempo": tempo_execucao,
            "trocas": trocas,
            "avaliacoes": avaliacoes
        })                                                                    # armazena resultado

    melhor = min(resultados, key=lambda item: item["custo_2opt"])             # melhor resultado após 2-opt

    return resultados, melhor                                                 # retorna todos e o melhor


def imprimir_resultados(resultados, melhor):                                  # imprime resultados no terminal
    print("=" * 100)
    print("comparação da heurística do vizinho mais próximo com melhoria 2-opt")
    print("=" * 100)

    print("\nresultados por cidade inicial:\n")

    resultados_ordenados = sorted(resultados, key=lambda item: item["custo_2opt"])

    for item in resultados_ordenados:
        print(
            f"origem: {item['origem']:<20} | "
            f"heurística: {item['custo_inicial']:.0f} km | "
            f"2-opt: {item['custo_2opt']:.0f} km | "
            f"melhoria: {item['melhoria_km']:.0f} km "
            f"({item['melhoria_percentual']:.2f}%) | "
            f"tempo: {item['tempo']:.6f} s"
        )

    print("\n" + "=" * 100)
    print("melhor resultado encontrado")
    print("=" * 100)

    print(f"cidade inicial: {melhor['origem']}")
    print(f"custo pela heurística: {melhor['custo_inicial']:.0f} km")
    print(f"custo após 2-opt: {melhor['custo_2opt']:.0f} km")
    print(f"melhoria obtida: {melhor['melhoria_km']:.0f} km ({melhor['melhoria_percentual']:.2f}%)")
    print(f"tempo de execução: {melhor['tempo']:.6f} s")
    print(f"trocas aceitas pelo 2-opt: {melhor['trocas']}")
    print(f"rotas avaliadas pelo 2-opt: {melhor['avaliacoes']}")

    print("\ntrajeto inicial:")
    print(" → ".join(melhor["trajeto_inicial"]))

    print("\ntrajeto após 2-opt:")
    print(" → ".join(melhor["trajeto_2opt"]))

    print("=" * 100)


def salvar_resultados_csv(resultados, nome_arquivo="resultado_comparacao_origens_2opt.csv"):  # salva resultados em csv
    with open(nome_arquivo, mode="w", newline="", encoding="utf-8-sig") as f:
        escritor = csv.writer(f)

        escritor.writerow([
            "origem",
            "custo_heuristica_km",
            "custo_2opt_km",
            "melhoria_km",
            "melhoria_percentual",
            "tempo_segundos",
            "trocas_2opt",
            "avaliacoes_2opt",
            "trajeto_heuristica",
            "trajeto_2opt"
        ])                                                                    # cabeçalho

        for item in resultados:
            escritor.writerow([
                item["origem"],
                round(item["custo_inicial"], 0),
                round(item["custo_2opt"], 0),
                round(item["melhoria_km"], 0),
                round(item["melhoria_percentual"], 2),
                round(item["tempo"], 6),
                item["trocas"],
                item["avaliacoes"],
                " -> ".join(item["trajeto_inicial"]),
                " -> ".join(item["trajeto_2opt"])
            ])                                                                # grava linha

    print(f"\narquivo gerado: {nome_arquivo}")


def gerar_grafico_comparativo(resultados):                                   # gera gráfico comparando heurística e 2-opt
    import matplotlib.pyplot as plt                                           # biblioteca para gráficos

    resultados_ordenados = sorted(resultados, key=lambda item: item["custo_2opt"])

    origens = [item["origem"] for item in resultados_ordenados]               # cidades
    custos_iniciais = [item["custo_inicial"] for item in resultados_ordenados] # custos antes do 2-opt
    custos_2opt = [item["custo_2opt"] for item in resultados_ordenados]       # custos após 2-opt

    x = range(len(origens))                                                    # posições no eixo x
    largura = 0.35                                                             # largura das barras

    plt.figure(figsize=(14, 6))

    plt.bar([p - largura / 2 for p in x], custos_iniciais, width=largura, label="vizinho mais próximo")
    plt.bar([p + largura / 2 for p in x], custos_2opt, width=largura, label="após 2-opt")

    plt.title("comparação de custo por cidade inicial")
    plt.xlabel("cidade inicial")
    plt.ylabel("custo total (km)")
    plt.xticks(list(x), origens, rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()

    plt.savefig("grafico_comparacao_heuristica_2opt.png", dpi=300)
    plt.show()


def gerar_grafico_melhoria(resultados):                                      # gera gráfico apenas com a melhoria obtida
    import matplotlib.pyplot as plt                                           # biblioteca para gráficos

    resultados_ordenados = sorted(resultados, key=lambda item: item["melhoria_km"], reverse=True)

    origens = [item["origem"] for item in resultados_ordenados]
    melhorias = [item["melhoria_km"] for item in resultados_ordenados]

    plt.figure(figsize=(12, 6))
    plt.bar(origens, melhorias)

    plt.title("melhoria obtida com 2-opt por cidade inicial")
    plt.xlabel("cidade inicial")
    plt.ylabel("redução de custo (km)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.savefig("grafico_melhoria_2opt.png", dpi=300)
    plt.show()


def main():                                                                  # função principal
    caminho_csv = sys.argv[1] if len(sys.argv) > 1 else "cidades2.csv"       # define arquivo padrão

    print("=" * 100)
    print("pcv — vizinho mais próximo testando todas as origens com melhoria 2-opt")
    print("=" * 100)

    cidades, distancias = ler_distancias_csv(caminho_csv)                    # lê dados

    print(f"\narquivo utilizado: {caminho_csv}")
    print(f"quantidade de cidades: {len(cidades)}")
    print(f"cidades: {', '.join(cidades)}\n")

    resultados, melhor = testar_todas_as_origens(cidades, distancias)        # executa testes

    imprimir_resultados(resultados, melhor)                                  # mostra terminal
    salvar_resultados_csv(resultados)                                        # salva tabela
    gerar_grafico_comparativo(resultados)                                    # gráfico comparação
    gerar_grafico_melhoria(resultados)                                       # gráfico melhoria


main()                                                                       # executa o programa
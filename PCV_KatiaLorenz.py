import csv
import sys

def ler_distancias_csv(caminho_arquivo):
    distancias = {}

    with open(caminho_arquivo, newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f, delimiter=',') 
        cabecalho = next(reader)
        cidades = [c.strip() for c in cabecalho[1:] if c.strip()]

        for linha in reader:
            if not linha or not linha[0].strip():
                continue

            cidade_origem = linha[0].strip()
            distancias[cidade_origem] = {}

            for i, cidade_destino in enumerate(cidades):
                valor = linha[i + 1].strip().replace(',', '.')
                distancias[cidade_origem][cidade_destino] = float(valor)

    return cidades, distancias


def vizinho_mais_proximo(cidades, distancias, cidade_inicio):
    nao_visitadas = set(cidades)
    tour = [cidade_inicio]
    nao_visitadas.remove(cidade_inicio)
    custo_total = 0
    cidade_atual = cidade_inicio

    while nao_visitadas:
        mais_proxima = min(nao_visitadas, key=lambda cidade: distancias[cidade_atual][cidade])
        distancia = distancias[cidade_atual][mais_proxima]
        custo_total += distancia
        print(f"  {cidade_atual} → {mais_proxima}  ({distancia:.0f} km)")
        tour.append(mais_proxima)
        nao_visitadas.remove(mais_proxima)
        cidade_atual = mais_proxima

    distancia_retorno = distancias[cidade_atual][cidade_inicio]
    custo_total += distancia_retorno
    tour.append(cidade_inicio)
    print(f"  {cidade_atual} → {cidade_inicio}  ({distancia_retorno:.0f} km)  [retorno]")

    return tour, custo_total


caminho_csv = sys.argv[1] if len(sys.argv) > 1 else "cidades.csv" 

print("=" * 50)
print("  PCV — Heurística do Vizinho Mais Próximo")
print("=" * 50)

cidades, distancias = ler_distancias_csv(caminho_csv)
cidade_inicio = cidades[0]

print(f"\nCidades ({len(cidades)}): {', '.join(cidades)}")
print(f"\nCidade de início: {cidade_inicio}")
print("\nPercurso:\n")

tour, custo_total = vizinho_mais_proximo(cidades, distancias, cidade_inicio)

print("\n" + "=" * 50)
print(f"Tour: {' → '.join(tour)}")
print(f"Custo total: {custo_total:.0f} km")
print("=" * 50)
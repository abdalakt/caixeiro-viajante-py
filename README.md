# Algoritmos Heurísticos aplicados ao Problema do Caixeiro Viajante (TSP)

## Descrição

Este repositório apresenta a implementação de um algoritmo heurístico para a resolução do Problema do Caixeiro Viajante (Travelling Salesman Problem – TSP). O trabalho foi desenvolvido como atividade avaliativa da disciplina **Análise de Algoritmos**, no âmbito do Mestrado em Computação Aplicada da Universidade do Vale do Itajaí (UNIVALI), no período letivo 2026/01.

## Autores

- Katia Lorenz  
- Letícia Zorzi Rama  
- Ricardo Arruda Júnior

## Orientação

Prof. Dr. Rudimar Luís Scaranto Dazzi

## Objetivo

O objetivo da atividade consiste na implementação de uma abordagem heurística para a solução do Problema do Caixeiro Viajante, conforme proposto em aula, visando explorar estratégias aproximadas para problemas de otimização combinatória.

## Metodologia

A heurística adotada foi o **método do vizinho mais próximo** (Nearest Neighbor), que consiste em selecionar iterativamente o vértice adjacente não visitado com menor distância em relação ao vértice atual.

## Funcionamento

O algoritmo desenvolvido realiza as seguintes etapas:

1. Leitura de uma matriz de distâncias a partir de um arquivo no formato `.csv`;  
2. Execução da heurística do vizinho mais próximo;  
3. Determinação do trajeto percorrido entre as cidades;  
4. Cálculo das distâncias individuais entre os vértices visitados;  
5. Cálculo do custo total do percurso.

## Código-fonte

O código-fonte da implementação está disponível no repositório:

https://github.com/abdalakt/caixeiro-viajante-py/blob/master/PCV_KatiaLorenzLeticiaRamaRicardoArruda.py


## Visualização Interativa

Como complemento à implementação do algoritmo heurístico, foi desenvolvida uma interface web interativa para visualização do percurso gerado.

A visualização foi implementada utilizando **HTML, CSS e JavaScript**, com apoio da biblioteca **Leaflet**, permitindo a exibição geográfica das cidades e a animação do trajeto calculado pelo algoritmo.

### Funcionalidades da visualização

- Exibição das cidades em um mapa interativo do Brasil;  
- Animação passo a passo do percurso gerado pela heurística do vizinho mais próximo;  
- Destaque visual das cidades visitadas e da cidade atual;  
- Exibição do caminho percorrido em tempo real;  
- Cálculo e apresentação do custo acumulado do trajeto;  
- Apresentação da matriz de distâncias utilizada no problema.

### Arquivo da visualização

A interface pode ser acessada através do arquivo: [Visualização interativa (HTML)](./pcv_cidades2_mapa.html)



### Objetivo da visualização

A inclusão da interface visual tem como finalidade facilitar a compreensão do comportamento do algoritmo, permitindo uma análise mais intuitiva da construção do trajeto e das decisões tomadas a cada etapa da heurística.

Essa abordagem contribui para a interpretação dos resultados e para a apresentação didática do problema no contexto acadêmico.
# =============================================================================
# ROTAS REGIC 2021 BRASIL - IBGE

# Fonte:
# https://www.ibge.gov.br/apps/regic/#/mapa/regic-distancias

# Caminho para chegar no dataset:
# Consultar rede urbana > Distâncias > CSV  - Base de ligações completa

# Isso baixa um .csv com todas as ligações aéres, rodoviárias, hidroviárias e hidro-rodoviárias entre todos os municípios do Brasil
# O script abaixo filtra esse dataset e cria um subset apenas das distâncias rodoviárias entre as capitais
# =============================================================================
 
# --- 1. PACOTES --------------------------------------------------------------
library(dplyr)
library(ggplot2)
library(skimr)
library(tidyr)
library(tibble)
 
# --- 2. LEITURA DOS DADOS ----------------------------------------------------
D <- read.csv("rotas_regic2021_brasil.csv", stringsAsFactors = FALSE, encoding = "UTF-8")
 
# --- 3. VISÃO GERAL ----------------------------------------------------------
cat("====== DIMENSÕES ======\n")
cat("Linhas:", nrow(D), "| Colunas:", ncol(D), "\n\n")
 
cat("====== NOMES DAS VARIÁVEIS ======\n")
print(names(D))
 
cat("\n====== TIPOS DE VARIÁVEIS ======\n")
print(str(D))
 
cat("\n====== PRIMEIRAS LINHAS ======\n")
print(head(D, 10))
 
cat("\n====== RESUMO ESTATÍSTICO ======\n")
print(summary(D))
 
# Resumo detalhado com skimr (opcional, mas recomendado)
cat("\n====== RESUMO DETALHADO (skimr) ======\n")
print(skim(D))
 
# --- 4. QUALIDADE DOS DADOS --------------------------------------------------
cat("\n====== VALORES AUSENTES (NA) POR VARIÁVEL ======\n")
na_counts <- colSums(is.na(D))
print(na_counts[na_counts > 0])
 
cat("\n====== PROPORÇÃO DE NAs (%) ======\n")
na_pct <- round(colMeans(is.na(D)) * 100, 2)
print(na_pct[na_pct > 0])
 
cat("\n====== LINHAS COMPLETAMENTE DUPLICADAS ======\n")
cat("Total de duplicatas:", sum(duplicated(D)), "\n")
 
# --- 5. ANÁLISE DE VARIÁVEIS NUMÉRICAS ---------------------------------------
num_vars <- names(D)[sapply(D, is.numeric)]
cat("\n====== VARIÁVEIS NUMÉRICAS ======\n")
print(num_vars)
 
if (length(num_vars) > 0) {
  cat("\n-- Estatísticas descritivas --\n")
  print(D %>% select(all_of(num_vars)) %>% summary())
}
 
# --- 6. ANÁLISE DE VARIÁVEIS CATEGÓRICAS ------------------------------------
cat_vars <- names(D)[sapply(D, function(x) is.character(x) | is.factor(x))]
cat("\n====== VARIÁVEIS CATEGÓRICAS ======\n")
print(cat_vars)
 
for (v in cat_vars) {
  cat("\n--", v, "(top 10 categorias) --\n")
  print(sort(table(D[[v]], useNA = "ifany"), decreasing = TRUE)[1:min(10, length(unique(D[[v]])))])
}

# --- 7. FILTRAR DATASET PARA DISTÂNCIAS RODOVIÁRIAS ENTRE AS CAPITAIS -------

# Listar todas as capitais brasileiras
capitais <- c(
  "Rio Branco", "Maceió", "Macapá", "Manaus", "Salvador",
  "Fortaleza", "Brasília", "Vitória", "Goiânia", "São Luís",
  "Cuiabá", "Campo Grande", "Belo Horizonte", "Belém",
  "João Pessoa", "Curitiba", "Recife", "Teresina",
  "Rio de Janeiro", "Natal", "Porto Alegre", "Porto Velho",
  "Boa Vista", "Florianópolis", "São Paulo", "Aracaju", "Palmas"
)

# Filtrar e selecionar
D_capitais <- D %>%
  filter(
    modal == "Rodoviário",
    nome_o %in% capitais,
    nome_d %in% capitais
  ) %>%
  select(modal, nome_o, nome_d, km, minutos, kmh)

# Checar capitais que aparecem como origens
unique(D_capitais$nome_o)

# Checar capitais que aparecem como destinos
unique(D_capitais$nome_d)

# Checar capitais faltantes
setdiff(capitais, unique(c(D_capitais$nome_o, D_capitais$nome_d)))

# Checar se Macapá aparece em outros tipos de via que não Rodoviária
D %>% filter(nome_o == capitais, nome_d == "Macapá")
D %>% filter(nome_o == "Macapá", nome_d == capitais)

# Exportar dataset
#write.csv(D_capitais, "subset_distancias_capitais_br.csv", row.names = FALSE)

# Importar dataset
#C <- read.csv("subset_distancias_capitais_br.csv")

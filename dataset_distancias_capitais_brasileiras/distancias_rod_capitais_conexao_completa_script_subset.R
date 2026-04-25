# =============================================================================
# Matriz de Distâncias Mínimas entre Capitais Brasileiras
# Método: Algoritmo de Dijkstra via pacote igraph
# Escopo: modal Rodoviário
# =============================================================================

# install.packages("igraph")
# install.packages("jsonlite")
library(igraph)
library(jsonlite)

# -----------------------------------------------------------------------------
# 1. CARREGAR DADOS
# -----------------------------------------------------------------------------
C <- read.csv("distancias_rod_capitais_subset.csv")

dim(C)
names(C)
head(C)

# -----------------------------------------------------------------------------
# 2. REMOVER ERROS GEOGRÁFICOS
# -----------------------------------------------------------------------------
# Coordenadas das capitais para cálculo da distância em linha reta (Haversine)
coords <- list(
  "Aracaju"        = c(-10.9472, -37.0731),
  "Belém"          = c(-1.4558,  -48.5044),
  "Belo Horizonte" = c(-19.9167, -43.9345),
  "Boa Vista"      = c(2.8235,   -60.6758),
  "Brasília"       = c(-15.7797, -47.9297),
  "Campo Grande"   = c(-20.4697, -54.6201),
  "Cuiabá"         = c(-15.5961, -56.0967),
  "Curitiba"       = c(-25.4297, -49.2711),
  "Florianópolis"  = c(-27.5954, -48.5480),
  "Fortaleza"      = c(-3.7172,  -38.5433),
  "Goiânia"        = c(-16.6864, -49.2643),
  "João Pessoa"    = c(-7.1195,  -34.8450),
  "Maceió"         = c(-9.6658,  -35.7350),
  "Manaus"         = c(-3.1190,  -60.0217),
  "Natal"          = c(-5.7945,  -35.2110),
  "Palmas"         = c(-10.2491, -48.3243),
  "Porto Alegre"   = c(-30.0346, -51.2177),
  "Porto Velho"    = c(-8.7612,  -63.9004),
  "Recife"         = c(-8.0539,  -34.8811),
  "Rio Branco"     = c(-9.9754,  -67.8249),
  "Rio de Janeiro" = c(-22.9068, -43.1729),
  "Salvador"       = c(-12.9714, -38.5014),
  "São Luís"       = c(-2.5297,  -44.3028),
  "São Paulo"      = c(-23.5505, -46.6333),
  "Teresina"       = c(-5.0892,  -42.8019),
  "Vitória"        = c(-20.3155, -40.3128)
)

haversine <- function(c1, c2) {
  R <- 6371
  lat1 <- c1[1] * pi / 180; lon1 <- c1[2] * pi / 180
  lat2 <- c2[1] * pi / 180; lon2 <- c2[2] * pi / 180
  dlat <- lat2 - lat1; dlon <- lon2 - lon1
  a <- sin(dlat/2)^2 + cos(lat1) * cos(lat2) * sin(dlon/2)^2
  R * 2 * asin(sqrt(a))
}

# Calcular razão km_dataset / km_linha_reta para cada registro
C$km_reta <- mapply(function(o, d) {
  if (o %in% names(coords) && d %in% names(coords))
    haversine(coords[[o]], coords[[d]])
  else NA
}, C$nome_o, C$nome_d)

C$razao <- C$km / C$km_reta

# Registros com razão < 0.5 são geograficamente impossíveis
erros <- C[!is.na(C$razao) & C$razao < 0.5, c("nome_o","nome_d","km","km_reta","razao")]
cat("Registros com erro geográfico removidos:\n")
print(erros)

C_limpo <- C[is.na(C$razao) | C$razao >= 0.5, ]
cat(sprintf("\nRegistros após remoção: %d\n", nrow(C_limpo)))

# -----------------------------------------------------------------------------
# 3. ADICIONAR CONEXÃO DE REFERÊNCIA: Manaus → Porto Velho
# -----------------------------------------------------------------------------
# Após a remoção dos erros, Manaus e Boa Vista ficam isoladas do grafo.
# A única ligação rodoviária existente é a BR-319 (Manaus–Porto Velho).
# Valores de referência: 885 km, 608 minutos, 87 kmh (fonte: distanciascidades.com)
# Boa Vista se reconecta via Manaus (BR-174, 745 km, já presente no dataset).

nova_conexao <- data.frame(
  modal   = "Rodoviário",
  nome_o  = "Manaus",
  nome_d  = "Porto Velho",
  km      = 885.0,
  minutos = 608,
  kmh     = 87,
  km_reta = NA,
  razao   = NA
)

C_limpo <- rbind(C_limpo, nova_conexao)
cat(sprintf("Após adicionar Manaus → Porto Velho: %d registros\n", nrow(C_limpo)))

# -----------------------------------------------------------------------------
# 4. PRÉ-PROCESSAR ARESTAS
# -----------------------------------------------------------------------------
# Normalizar sentido (par_o = menor nome alfabético) e manter menor km por par.
# Isso elimina assimetrias e duplicatas multimodais.

edges <- C_limpo[, c("nome_o", "nome_d", "km")]
edges$par_o <- pmin(edges$nome_o, edges$nome_d)
edges$par_d <- pmax(edges$nome_o, edges$nome_d)

edges_clean <- aggregate(km ~ par_o + par_d, data = edges, FUN = min)
names(edges_clean) <- c("nome_o", "nome_d", "km")
cat(sprintf("Arestas após deduplicação: %d\n", nrow(edges_clean)))

# -----------------------------------------------------------------------------
# 5. CONSTRUIR O GRAFO
# -----------------------------------------------------------------------------
g <- graph_from_data_frame(d = edges_clean, directed = FALSE)

vcount(g)    # deve ser 26
ecount(g)    # arestas limpas
is_simple(g) # deve ser TRUE
components(g)$no  # deve ser 1 (grafo totalmente conectado)

# -----------------------------------------------------------------------------
# 6. CALCULAR DISTÂNCIAS MÍNIMAS (DIJKSTRA)
# -----------------------------------------------------------------------------
mat_dist <- distances(graph = g, weights = E(g)$km)

sum(is.infinite(mat_dist))  # deve ser 0

# -----------------------------------------------------------------------------
# 7. INSPECIONAR
# -----------------------------------------------------------------------------
dim(mat_dist)
mat_dist[1:5, 1:5]

# Exemplos com intermediários
mat_dist["Manaus", "São Paulo"]
mat_dist["Boa Vista", "Brasília"]
mat_dist["Rio Branco", "Fortaleza"]

# -----------------------------------------------------------------------------
# 8. CONVERTER PARA FORMATO LONGO
# -----------------------------------------------------------------------------
mat_largo <- as.data.frame(mat_dist)
mat_largo$capital_origem <- rownames(mat_largo)

mat_longo <- reshape(
  data      = mat_largo,
  varying   = rownames(mat_dist),
  v.names   = "km_minimo",
  timevar   = "capital_destino",
  times     = rownames(mat_dist),
  direction = "long",
  idvar     = "capital_origem"
)

rownames(mat_longo) <- NULL
mat_longo <- mat_longo[, c("capital_origem", "capital_destino", "km_minimo")]
mat_longo <- mat_longo[order(mat_longo$capital_origem, mat_longo$capital_destino), ]

# -----------------------------------------------------------------------------
# 9. EXPORTAR
# -----------------------------------------------------------------------------
#write.csv(mat_largo, "distancia_rod_capitais_matriz_larga.csv", row.names = TRUE)
#write.csv(mat_longo, "distancia_rod_capitais_matriz_longa.csv",  row.names = FALSE)

json_largo <- toJSON(mat_dist,  pretty = TRUE)
json_longo  <- toJSON(mat_longo, pretty = TRUE)
#write(json_largo, "distancia_rod_capitais_json_largo.json")
#write(json_longo, "distancia_rod_capitais_json_longo.json")
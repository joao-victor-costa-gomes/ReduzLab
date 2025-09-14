# PROJETO - INTERFACE PARA ALGORITMOS DE REDUÇÃO DE REDIMENSIONALIDADE DA BIBLIOTECA SCIKIT-LEARN

--- 

## GERAL

- [ ] A aplicação só será estilizada quando todas as funcionalidades principais estiverem prontas.

- [X] Usar um sistema de template inheritance para compartilhar a estrutura HTML (header, footer, etc.) entre as páginas.

- [X] A aplicação deve ter um .env para configurações.

- [ ] A aplicação deve ser estruturada para deploy (usar requirements.txt, caminhos relativos).

- [X] A aplicação deve ter páginas de erro padrão (404, 500).

--- 

## PÁGINA DE ENVIO DE DATASET

- [X] Página de envio de arquivos .csv e .xlsx.

- [X] Definir um nome seguro e único para os arquivos upados.

- [X] Lidar com erros de envio (formato, tamanho, corrupção).

- [X] Mostrar um preview dos 10 primeiros itens.

- [X] Lidar com erros no carregamento do preview.

- [X] Botões de seleção de algoritmo de redução após o dataset ser carregado

- [X] Para evitar erros futuros, logo nessa página deve ter uma verificação se o dataset tem alguma coluna com tipos não númericos ou nulos e alertar quais colunas são. 

---

## PÁGINA DE PROCESSAMENTO DE ALGORITMO

- [X] Mostrar novamente o preview do dataset.

- [X] Bloquear acesso se nenhum dataset foi enviado (gerenciamento de sessão).

- [X] Salvar os valores dos campos no localStorage do navegador como sugestão.

- [X] Validação de formulário no frontend (mensagem de aviso padrão) e backend (mensagem de erro).

### SEÇÃO DE PRÉ-PROCESSAMENTO E PARÂMETROS

- [X] Campo para selecionar a porcentagem que será usada no algoritmo (amostragem). `parâmetro do algoritmo`

- [X] Campo para selecionar a coluna target. Deve ter uma validação para caso essa coluna ter valores não numéricos.  `parâmetro do algoritmo`

- [X] Campo para selecionar dimensão do gráfico. `parâmetro do algoritmo`

- [X] Campo para selecionar tipo do gráfico (.png ou .html). `parâmetro do gráfico`

- [X] Campo para selecionar um scaler (Nenhum, StandardScaler ou MinMaxScaler). `parâmetro do algoritmo`

- [X] Campo para inserir título do gráfico. `parâmetro do gráfico`

- [X] Campo para inserir dimensões do gráfico. `parâmetro do gráfico`

- [X] Botão para rodar o algoritmo com os parâmetros e carregar gráfico resultante. 

### SEÇÃO DO GRÁFICO E RESULTADOS

- [X] Exibir o gráfico gerado abaixo da seção de parâmetros.

- [X] Lidar com erros de processamento/geração do gráfico.

- [X] Exibir tempo de execução.

- [X] Exibir métricas específicas de cada algoritmo se houver (PCA tem variância explicada acumulada, t-SNE tem KL divergence, etc.).

- [X] Botão de download do gráfico.

- [X] Botão para baixar o .csv com os dados reduzidos.

---

## OUTROS 

- [ ] **Header** para navegação entre algoritmos de redução de dimensionalidade. Caso o usuário já tenha enviado um dataset e esteja na página de algum algoritmo, se ele navegar para outra página de algoritmo as informações do dataset enviado serão carregados novamente nessa página nova. `componente reutilizável`

- [ ] **Footer** com informações sobre o projeto e sobre o autor. `componente reutilizável`

- [ ] **Página "Sobre" ou "Ajuda"** explicando o que é redução de dimensionalidade e uma breve descrição de cada algoritmo implementado. 

- [ ] **Seção de parâmetros avançados** que irá aparecer quando o usuário clicar no botão "Parâmetros avançados" localizado na seção de parâmetros do algoritmo. Essa seção deve exibir parâmetros específicos do algoritmo. 

---

## TEXTO SOBRE ALGORITMOS

Com certeza! É uma ótima ideia ter uma visão geral do que a biblioteca oferece. O `scikit-learn` é extremamente rico em algoritmos de redução de dimensionalidade, e eles podem ser agrupados em categorias com base em como funcionam.

Você já tem uma excelente lista inicial (PCA, T-SNE, etc.). Abaixo está uma visão mais ampla, categorizada, dos principais métodos disponíveis.

---
### 1. Métodos Lineares (Projeções Lineares)

Estes métodos assumem que os dados podem ser projetados em um subespaço linear de dimensão inferior. Geralmente são rápidos e ótimos para entender a estrutura global dos dados.

* **Principal Component Analysis (PCA)**
    * **O que faz:** Encontra os eixos (componentes principais) que maximizam a variância nos dados. Ele projeta os dados nesses novos eixos, mantendo a maior quantidade de "informação" possível.
    * **Ideal para:** Visualização geral de dados, remoção de ruído, compressão de dados e pré-processamento para outros algoritmos de machine learning.

* **KernelPCA (KPCA)**
    * **O que faz:** Uma versão "não-linear" do PCA. Usando o "truque do kernel", ele primeiro mapeia os dados para um espaço de dimensão muito alta onde as relações (esperançosamente) se tornam lineares, e então aplica o PCA nesse espaço.
    * **Ideal para:** Capturar relações complexas e não-lineares que o PCA padrão não consegue ver.

* **TruncatedSVD (também conhecido como Latent Semantic Analysis - LSA)**
    * **O que faz:** Muito similar ao PCA, mas funciona diretamente em matrizes esparsas (matrizes com muitos zeros), como as que são geradas a partir de dados de texto (ex: contagens de palavras).
    * **Ideal para:** Redução de dimensionalidade em dados de texto (NLP), sistemas de recomendação.

---
### 2. Aprendizado de Manifold (Métodos Não-Lineares)

Esses métodos assumem que seus dados de alta dimensão na verdade residem em uma "superfície" curva de baixa dimensão (um "manifold"). O objetivo é "desenrolar" essa superfície para visualizá-la.

* **t-Distributed Stochastic Neighbor Embedding (t-SNE)**
    * **O que faz:** Mapeia os pontos de dados de alta dimensão para 2D ou 3D de forma a preservar as "vizinhanças". Pontos que são próximos no espaço original tendem a permanecer próximos no espaço reduzido.
    * **Ideal para:** **Visualização de clusters**. É um dos melhores algoritmos para criar mapas 2D/3D visualmente atraentes que revelam a estrutura de agrupamento dos dados.
    * **Ponto a considerar:** O T-SNE é computacionalmente caro e as distâncias entre os clusters no gráfico final não são necessariamente significativas; o foco está na estrutura local.

* **Locally Linear Embedding (LLE)**
    * **O que faz:** Assume que cada ponto de dado pode ser representado como uma combinação linear de seus vizinhos mais próximos. O objetivo é preservar esses "pesos" de reconstrução local no espaço de baixa dimensão.
    * **Ideal para:** "Desenrolar" manifolds bem definidos, como o famoso exemplo do "swiss roll" (rolo suíço).

* **Isomap**
    * **O que faz:** Tenta preservar a "distância geodésica" (o caminho mais curto ao longo da superfície do manifold) entre os pontos, em vez da distância em linha reta. Ele constrói um grafo de vizinhança e calcula as distâncias através desse grafo.
    * **Ideal para:** Entender a estrutura global de um manifold não-linear.

---
### 3. Métodos Supervisionados (Usam a Coluna Target)

Estes métodos são fundamentalmente diferentes dos outros, pois eles usam as informações da sua **coluna target (`y`)** para encontrar a melhor projeção.

* **Linear Discriminant Analysis (LDA)**
    * **O que faz:** Encontra uma projeção que **maximiza a separação entre as diferentes classes** do seu target.
    * **Diferença crucial do PCA:** O PCA maximiza a variância dos dados *no geral*, ignorando as classes. O LDA maximiza a distância *entre as médias das classes* e minimiza a variância *dentro de cada classe*.
    * **Ideal para:** Redução de dimensionalidade focada em **classificação**.

* **Neighborhood Components Analysis (NCA)**
    * **O que faz:** Também é supervisionado. Ele aprende uma projeção de tal forma que a acurácia de um classificador de vizinhos mais próximos (k-NN) seja maximizada no espaço de baixa dimensão.
    * **Ideal para:** Redução de dimensionalidade para melhorar a performance de classificadores baseados em distância.

---
### Resumo

* **Para exploração e visualização geral:** **PCA** (rápido, linear), **KPCA** (não-linear), **t-SNE** (ótimo para clusters).
* **Para dados de texto:** **TruncatedSVD**.
* **Se o seu objetivo é melhorar um modelo de CLASSIFICAÇÃO:** **LDA** e **NCA** são as escolhas corretas, pois usam o target para guiar a redução.

Sua lista original já cobre os algoritmos mais importantes e representativos de cada categoria!
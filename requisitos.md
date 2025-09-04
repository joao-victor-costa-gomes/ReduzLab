# PROJETO - INTERFACE PARA ALGORITMOS DE REDUÇÃO DE REDIMENSIONALIDADE DA BIBLIOTECA SCIKIT-LEARN

--- 

## GERAL

- [ ] A aplicação só será estilizada quando todas as funcionalidades principais estiverem prontas.

- [ ] Usar um sistema de template inheritance para compartilhar a estrutura HTML (header, footer, etc.) entre as páginas.

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

- [ ] Salvar os valores dos campos no localStorage do navegador como sugestão.

- [X] Validação de formulário no frontend (mensagem de aviso padrão) e backend (mensagem de erro).

### SEÇÃO DE PRÉ-PROCESSAMENTO E PARÂMETROS

- [X] Campo para selecionar a porcentagem que será usada no algoritmo (amostragem). `parâmetro do algoritmo`

- [X] Campo para selecionar a coluna target. Deve ter uma validação para caso essa coluna ter valores não numéricos.  `parâmetro do algoritmo`

- [X] Campo para selecionar dimensão do gráfico. `parâmetro do algoritmo`

- [X] Campo para selecionar tipo do gráfico (.png ou .html). `parâmetro do gráfico`

- [X] Campo para selecionar um scaler (Nenhum, StandardScaler ou MinMaxScaler). `parâmetro do algoritmo`

- [X] Campo para inserir título do gráfico. `parâmetro do gráfico`

- [ ] Campo para inserir dimensões do gráfico. `parâmetro do gráfico`

- [X] Botão para rodar o algoritmo com os parâmetros e carregar gráfico resultante. 

### SEÇÃO DO GRÁFICO E RESULTADOS

- [ ] Exibir o gráfico gerado abaixo da seção de parâmetros.

- [ ] Lidar com erros de processamento/geração do gráfico.

- [ ] Exibir tempo de execução.

- [ ] Exibir métricas específicas de cada algoritmo se houver (PCA tem variância explicada acumulada, t-SNE tem KL divergence, etc.).

- [ ] Botão de download do gráfico.

- [ ] Botão para baixar o .csv com os dados reduzidos.

---

## OUTROS 

- [ ] **Header** para navegação entre algoritmos de redução de dimensionalidade. Caso o usuário já tenha enviado um dataset e esteja na página de algum algoritmo, se ele navegar para outra página de algoritmo as informações do dataset enviado serão carregados novamente nessa página nova. `compoenete reutilizável`

- [ ] **Footer** com informações sobre o projeto e sobre o autor. `compoenete reutilizável`

- [ ] **Página "Sobre" ou "Ajuda"** explicando o que é redução de dimensionalidade e uma breve descrição de cada algoritmo implementado. 

- [ ] **Seção de parâmetros avançados** que irá aparecer quando o usuário clicar no botão "Parâmetros avançados" localizado na seção de parâmetros do algoritmo. Essa seção deve exibir parâmetros específicos do algoritmo. 
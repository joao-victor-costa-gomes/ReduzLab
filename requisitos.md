# INTERFACE PARA ALGORITMOS DE REDUÇÃO DE REDIMENSIONALIDADE DA BIBLIOTECA SCIKIT-LEARN

--- 

## GERAL
- [ ] A aplicação só será estilizada quando todas as funcionalidades principais estiverem prontas 

- [ ] Se não for muito difícil de emplementar, seria interessante se toda página de algoritmos compartilhassem a mesma estrutura HTML, para evitar repetição de código

- [ ] A aplicação deve ter um .env para definir configurações importantes (chave secreta, tamanho máximo de arquivo, etc.)

- [ ] A aplicação deve ser estruturada de modo que seja possível fazer o deploy dela na Internet, seja agora ou em planos futuros (não é prioridade, mas tentar)

- [ ] A aplicação deve ter página de erros padrões por precaução (404, 500, etc.)

--- 

## PÁGINA DE ENVIO DE DATASET

### SEÇÃO DE ENVIO
- [ ] Terá uma página de envio de arquivos .csv

- [ ] A aplicação deve definir um nome seguro e único para os arquivos upados

- [ ] Essa página deve saber lidar com todos os possíveis erros gerados pelo envio desses arquivos (arquivos de outros formatos, arquivos corrompidos, arquivo de tamanho muito elevado) e deve exibir esses erros

### SEÇÃO DE PREVIEW
- [ ] Em seguida, a página deverá mostrar um preview dos 10 primeiros itens do dataset enviado pelo usuário 

- [ ] A página também deve saber lidar caso acontece algo no carregamento do preview do dataset (registros corrompidos, nenhum dado a ser exebido, etc.)

### SEÇÃO DE BOTÕES DOS ALGORITMOS
- [ ] Por fim, após o preview, deve ser possível escolher o método de redução de dimensionalidade que será aplicado no dataset, isso levará para sua respectiva página do algoritmo

---

## PÁGINA DE PROCESSAMENTO DO DATASET

- [ ] Essa será a página onde o usuário irá inserir os parâmetros para em seguida rodar o algoritmo selecionado 

### SEÇÃO DE PREVIEW
- [ ] A página deve mostrar novamente o preview do dataset assim como na página de envio 

- [ ] Caso o usuário acessar essa página sem ter enviado um dataset, o restante que será descrito abaixo não deve ser carregado e uma mensagem de erro deve aparecer 

### SEÇÃO DE PARÂMETROS
- [ ] Abaixo do preview do dataset, terá a seção de inserir os parâmetros principais, que são esses: amostragem, coluna do target, tamanho da dimensão, tipo do gráfico (.png ou .html), scaler (standard ou minmax), título do gráfico, tamanho do título,  tamanho da fonte de cada lado do gráfico, tamanho do gráfico em si

- [ ] Esses dados acima devem ficar salvos como sugestão para toda vez que o usuário recarregar a página não precisar colocar tudo de novo

- [ ] O processo não deve rodar caso faltar algum dado a ser informado, isso tanto no frontend como no backend (no caso do backend, irá exebir uma mensagem de erro, para caso o usuário consiga fazer isso com um postman por exemplo)

- [ ] Por fim um botão para rodar o algoritmo e carregar o gráfico abaixo

### SEÇÃO DO GRÁFICO
- [ ] Abaixo da seção de parâmetros, deve ser mostrado o gráfico gerado a partir dos parâmetros fornecidos pelo usuário

- [ ] Ele também deve poder lidar com erros caso o gráfico não seja processado corretamente e exibir esses erros

- [ ] Além do gráfico, também deve ser mostrado algumas coisas importantes como: tempo de execução, botão de download do gráfico, baixar arquivo .csv com os dados reduzidos

---

## HEADER 

- [ ] A partir da próxima página, terá um header onde o usuário poderá acessar outros algoritmos de redução de dimensionalidade. O motivo de ser a partir da próxima página é para que ela seja carregada com os dados que ele enviou 

--- 

## FOOTER

- [ ] Um footer simples com as informações do projeto e github do criador 

--- 

## SEÇÃO DE PARÂMETROS AVANÇADOS
- [ ] Essa seção será feita por último quando as coisas acimas estiverem prontas, ela ficará entre a seção do gráfico e a seção de parâmetros e só aparecerá quando o usuário clicar no botão "avançado". Nela terá vários espaços para o usuário colocar parâmetros avançados específicos do próprio algoritmo (mas isso deve ser visto com calma para saber a melhor forma de implementar) 
# Deep Learning Crawler for InsurUP
### Python3 é necessário para este projeto.

 Crawler alternativo para o InsurUP, um projeto de pesquisa qualificada para processos de subscrição de riscos, abordando um conceito de Tree Data Structure (estrutura de dados em árvore) com a biblioteca anytree.

Este é rastreador construído em python implementa a Pesquisa Aprofundada iterativa (Deepening Depth Search) para rastrear todos os
os "links filhos" (childrens) a partir de uma URL de base específica (parent) até uma profundidade especificada. Durante o scraping, o programa salva o HTML de cada página encontrada em um arquivo de texto e executa um N-gram Feature Extractor nesses arquivos. N-grama é uma sequência contígua N itens de uma determinada amostra de texto, esses itens podem ser palavras, sílabas, fonemas, letras ou pares de base de acordo com a aplicação. 

Exemplificando:

![Unigram-example](https://uploaddeimagens.com.br/images/002/817/379/original/Unigram-example.png?1596815821)

Os N-gramas poderão ser processados por um algoritmo de classificação posteriormente, sendo considerados para:
* atribuição de valores;
* modelo de Markov;
* Correção ortográfica e
* Tradução automática de textos. 

#
## Instale as pendências:
~~~
> pip install -r requirements.txt
~~~

#
## Execução: 
  ```commandprompt
> python index.py -u <url> -d <depth>  
  ```
 #   
## Exemplo:
  ```commandprompt
  > python index.py -u "http://www.google.com" -d 2  
  ```

#
  
### Profundidade (Depht) especificada com valor acima de 2 provavelmente levarão muito tempo para o término da execução do código.

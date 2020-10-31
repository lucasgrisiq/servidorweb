# servidorweb


Nesta tarefa, a equipe desenvolverá um servidor Web simples, capaz de processar apenas
uma requisição. O servidor Web:
(i) criará um socket de conexão quando contatado por cliente (navegador);
(ii) receberá a requisição HTTP dessa conexão;
(iii) analisará a requisição para determinar o arquivo específico sendo
requisitado;
(iv) obterá o arquivo requisitado do sistema de arquivo do servidor;
(v) criará uma mensagem de resposta HTTP consistindo no arquivo requisitado
precedido por linhas de cabeçalho; e
(vi) enviará a resposta pela conexão TCP ao navegador requisitante.
Caso o navegador requisite um arquivo que não esteja presente no servidor, ele deverá
retornar uma mensagem de erro “404 Not Found”.

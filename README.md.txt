!copie esta pasta para um diretorio local em sua maquina

instale o python e o tesseract, ambos est�o na pasta Cpd$\instaladores
de preferencia estas vers�es:
python-3.7.3
tesseract-ocr-w64-setup-v5.0.0-alpha.20190623


obs:
>python: n�o deixe de setar as variaveis de ambiente (no inicio marque a op��o SET python to PATH) ou fa�a isso manualmente
>tesseract-ocr: n�o deixe de instalar o pacote de idioma portuguese em additional language data e setar a variavel de ambiente 

para saber se a instala��o deu certo abra o cmd e execute os comandos:
python --version
pip --version
tesseract --version

se sim prosseguir

execute o .bat instalar_dependencias.bat 


//configure seu putty com
consolas bold 11-point
e pronto XD


O BatchSlave tem o intuito de facilitar a execu��o mecanica (S e enter 4ever)
do batch e n�o exclui de maneira alguma a necessidade da presen�a de um cpd.


para utilizar da primeira vez siga primeiro os passos de instala��o
feita a instala��o abra o putty dentro da tela '02' 

1) primeiro passo � posicionar a tela, use o script BatchSlave2/print.py para verificar a posi��o
at� que esteja no lugar certo.

2) depois inicie um job, e execute o script BatchSlave2/executajob.py
esse script vai seguir a execu��o do job at� que alguma informa��o que precise ser anotada
apare�a na tela neste caso o script ser� pausado at� que o cpd de continuidade
ao fim de cada job o cpd deve finalizar e iniciar um novo

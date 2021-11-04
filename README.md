
O BatchSlave tem o intuito de facilitar a execução mecanica de processamentos em lote


Instalação
!copie esta pasta para um diretorio local em sua maquina

instale o python e o tesseract, ambos estão na pasta Cpd$\instaladores
de preferencia estas versões:
python-3.7.3
tesseract-ocr-w64-setup-v5.0.0-alpha.20190623


obs:
>python: não deixe de setar as variaveis de ambiente (no inicio marque a opção SET python to PATH) ou faça isso manualmente
>tesseract-ocr: não deixe de instalar o pacote de idioma portuguese em additional language data e setar a variavel de ambiente 

para saber se a instalação deu certo abra o cmd e execute os comandos:
python --version
pip --version
tesseract --version

se sim prosseguir

execute o .bat instalar_dependencias.bat 


//configure seu putty com
consolas bold 11-point

para utilizar da primeira vez siga primeiro os passos de instalação
feita a instalação abra o putty dentro da tela '02' 

1) primeiro passo é posicionar a tela, use o script BatchSlave2/print.py para verificar a posição
até que esteja no lugar certo.

2) depois inicie um job, e execute o script BatchSlave2/executajob.py
esse script vai seguir a execução do job até que alguma informação que precise ser anotada
apareça na tela neste caso o script será pausado até que o cpd de continuidade
ao fim de cada job o cpd deve finalizar e iniciar um novo

# DOCs: http://docs.paramiko.org/en/2.6/api/sftp.html
#str.replace(stt,cng)
#DEPENDENCIAS PARA EXECUÇÃO
import paramiko 
from datetime import datetime, timedelta
import pyscreenshot as ImageGrab
import os
import configparser
from Acionador import Acionador
import pytesseract
import time
import cv2 
try:
    from PIL import Image
except ImportError:
    import Image

#Credenciais para acessar o servidor e listar os arquivos
URL   =  '#####'
User  =  '####'
Pass  =  '####'
ssh = paramiko.SSHClient()
#data
dt = datetime.today() - timedelta(hours=8)
data = dt.strftime("%d%m%y")
data_dm = dt.strftime("%d%m")
#TAMANHO DA JANELA/Monitor
cmd = 'mode 50,20'
os.system(cmd)
config = configparser.ConfigParser()
config.read('files/configuracoes.ini')
x1 = int(config['print']['X1'])
x2 = int(config['print']['X2'])
x3 = int(config['print']['X3'])
x4 = int(config['print']['X4'])

acionador = Acionador(int(config['mouse']['X']),int(config['mouse']['Y']))

def baixa_arquivos(filial, arquivos):

    if( len(arquivos) == 0):
        return False
    print("\n\nBaixando Arquivos de",filial  )
    print("arquivos:",arquivos) 
    acionador.pressionarF()    
    acionador.prosseguirT(filial)   
    acionador.pressionarR()     
    acionador.prosseguirT(' '.join(arquivos))
    time.sleep(1)
    

    espera = True
    while(espera):   
        print('em espera...')
        im=ImageGrab.grab(bbox=(x1, x2, x3, x4)) 
        im.save('files/temp2.png')       

        img = cv2.imread(r'files/temp2.png')
        imagem = cv2.bitwise_not(img)

        text = pytesseract.image_to_string(Image.fromarray(imagem),lang='por', config="--user-words files/words.txt")
        text = text.lower()

        if text.rfind('enter') != -1 :
           # print('enter')
            acionador.prosseguirE()

        if(text.rfind('nao') != -1 and text.rfind('existe') != -1 ):
            #print('nao existe')
            acionador.prosseguirE()


        if text.rfind('[f]servidor') != -1 or text.rfind('[r]receber') != -1:
            print('pronto...')
            espera = False

 
if __name__ ==  '__main__':


    s = ''
    while(s.upper() != "S"):  
        im=ImageGrab.grab(bbox=(x1, x2, x3, x4))         
        im.show()
        s = input('\nConsegue ver o Putty por inteiro no print ? \n <S>Sim - Prosseguir \n >') 

    #busca arquivos
    prosseguir = True
    while(prosseguir):
        print("\n\nVerificando Arquivos Faltantes...")
        #Uma string com todos os arquivos para listagem
        Arquivos_receber = "agenda."+ data_dm + "*" + " ba241111" + data + "*" + " cm241111" + data + "*" + " ms030" + data + "*" + " sc241111" + data + "*" + " cpr111" + data + "*" + " fn" + data + "*" + " it241111" + data + "*" + " it241008" + data + "*" + " it241180" + data + "*" + " it241181" + data + "*" + " it241183" + data + "*" + " me000" + data + "*" + " pa241" + data + "*" + " pc241111" + data + "*" + " pc241030" + data + "*" + " pc241180" + data + "*" + " pc241181" + data + "*" + " prf241180" + data + "*" + " lms030" + data + "*" + " lbm111" + data + "*" + " pd241111" + data + "*" + " pd241030" + data + "*" + " pd241180" + data + "*" + " pd241181" + data + "*" + " ca111" + data + "*" + " tb030" + data + "*" + " pf000" + data + "*" + " ef000" + data + "*" + " set111" + data + "*" + " ucl111" + data + ".txt* cmc241111_" + data + "_" + data + "*" + ""

        # Um vetor para cada filial
        Arquivos_Matriz_vet = ("agenda."+ data_dm +  " ba241111" + data +  " cm241111" + data +  " sc241111" + data +  " cpr111" + data +  " fn" + data +  " it241111" + data +  " it241008" + data +  " me000" + data +  " pa241" + data +  " pc241111" + data +  " lbm111" + data + ".dat" +" pd241111" + data + " ca111" + data +  " pf000" + data +  " ef000" + data +  " set111" + data + ".txt"+ " ucl111" + data + ".txt cmc241111_" + data + "_" + data + ".txt").split(" ")
        Arquivos_030_vet = ("ms030" + data + " lms030" + data + ".dat"+  " pc241030" + data +  " pd241030" + data +   " tb030" + data).split(" ")
        Arquivos_180_vet = ("it241180" + data +  " pc241180" + data +  " prf241180" + data +  " pd241180" + data).split(" ")
        Arquivos_181_vet = ("it241181" + data +  " pc241181" + data +  " pd241181" + data).split(" ") 
        Arquivos_183_vet = ("it241183" + data).split(" ")


        #Adiciona chaves automaticamente, brabo d+ 
        ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy() )

        #Abre a conexao
        ssh.connect(URL, username=User, password=Pass)
        ftp = ssh.open_sftp()
        
        # Retorna somente os arquivos já Baixados 
        command = 'cd /fs1/integra/ ; ls ' + Arquivos_receber
        (stdin, stdout, stderr) = ssh.exec_command(command)
        
        #Aqui itera nos arquivos baixados e remove os já baixados de cada vetor
        for line in stdout.readlines():
            line = line.replace('\n', '') 
            if( line in Arquivos_Matriz_vet):
                Arquivos_Matriz_vet.remove(line)

            if( line in Arquivos_030_vet):
                Arquivos_030_vet.remove(line)

            if( line in Arquivos_180_vet):
                Arquivos_180_vet.remove(line)

            if( line in Arquivos_181_vet):
                Arquivos_181_vet.remove(line)
            
            if( line in Arquivos_183_vet):
                Arquivos_183_vet.remove(line)

            #print(line)

        #Fecha Conexão   
        ssh.close()
            

        #Se todos vetores estiverem vazios = se não restar nenhum arquivo para baixar
        if(len(Arquivos_Matriz_vet) == 0 and len(Arquivos_030_vet) == 0 and len(Arquivos_180_vet) == 0 and len(Arquivos_181_vet) == 0 and len(Arquivos_183_vet) == 0):
            print("Todos Arquivos Baixados Bom batch !")
            prosseguir = False
        else:
        #
            print("\n\n")
            print("Arquivos Faltantes da Matriz:",Arquivos_Matriz_vet)
            print("Arquivos Faltantes da 030:",Arquivos_030_vet)
            print("Arquivos Faltantes da 180:",Arquivos_180_vet)
            print("Arquivos Faltantes da 181:",Arquivos_181_vet)
            print("Arquivos Faltantes da 183:",Arquivos_183_vet)
            print("\n\n")
            time.sleep(2)
            #
            baixa_arquivos("srvsave",Arquivos_Matriz_vet)
            baixa_arquivos("srvsave030",Arquivos_030_vet)
            baixa_arquivos("srvsave180",Arquivos_180_vet)
            baixa_arquivos("srvsave181",Arquivos_181_vet)
            baixa_arquivos("srvsave183",Arquivos_183_vet)

    os.system("pause")
        


    
    


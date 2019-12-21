#from PIL import Image
try:
    from PIL import Image
except ImportError:
     import Image
#import Pillow
import pytesseract
import sys
import os
import configparser
from configparser import ConfigParser
from Acionador import Acionador
import cv2
#-- include('examples/showgrabfullscreen.py') --#
import pyscreenshot as ImageGrab

def tesseract(x1,x2,x3,x4):     
    im = ImageGrab.grab()#objeto que tira print    
    im=ImageGrab.grab(bbox=(x1, x2, x3, x4))#define a posição e tamanho da região de leitura (putty)   
    im.save('files/temp.jpg') # salvar imagem
    img = cv2.imread(r'files/temp.jpg')
    imagem = cv2.bitwise_not(img)  
    #extrai texto da imagem
    text = pytesseract.image_to_string(Image.fromarray(imagem),lang='por', config="--user-words files/words.txt")
    return text.lower()

if __name__ == '__main__':

    
    
    #INICIALIZAÇÃO DAS VARIAVEIS GLOBAIS
    config = configparser.ConfigParser()
    config.read('files/configuracoes.ini')
    parser = ConfigParser()
    parser.read('files/configuracoes.ini')
    x1 = int(config['print']['X1'])
    x2 = int(config['print']['X2'])
    x3 = int(config['print']['X3'])
    x4 = int(config['print']['X4'])

    filial = str(config['filial']['codigo'])
    cmd = 'mode 50,20'
     
    #os.system(cmd)
    # job = ""
    # job = sys.argv[1:]
    # job = 1 if str(job) == '[]' else int(sys.argv[1:][0])
    acionador = Acionador(int(config['mouse']['X']),int(config['mouse']['Y']))
    
    intervalo_valido_jobs = range(1,5)

    #NESTE BLOCO O PROGRAMA RECEBE OS VALORES OS MESMOS SÃO VALIDADOS
    continuar_perguntando = True
    job_executar_agora = -1
    while(continuar_perguntando): # loop 1
        valor_inserido = input("Escolha um modo de execucao: \n <1> -Executar jobs em sequencia \n <2> -Executar um unico job\n <3> - Executar um job qualquer, inicio antes \n opcao:")
        if(valor_inserido.lower() == '1'):
            continuar_perguntando = False # encerra loop 1
            p_valor_inserido = -1
            s_valor_inserido = -1


            continuar_perguntando2 = True

            while(continuar_perguntando2): #loop 2
                while(int(p_valor_inserido) not in intervalo_valido_jobs):
                    p_valor_inserido = int(input("numero do primeiro job a se executar [1-4] :"))

                while(int(s_valor_inserido) not in intervalo_valido_jobs):
                    s_valor_inserido = int(input("numero do ultimo job a se executar [" + str(p_valor_inserido) + "-4] :"))
                
                if(s_valor_inserido > p_valor_inserido):                
                    continuar_perguntando2 = False #encerra loop 2
                    #modelo parser de conf em memoria
                    parser.set('job','ini',str(p_valor_inserido))
                    parser.set('job','atual',str(p_valor_inserido))
                    parser.set('job','fim',str(s_valor_inserido))
                    job_executar_agora = p_valor_inserido
                    #print('flag')
                else:
                    print("\n [erro]segundo numero deve ser maior doque o primeiro \n")
                    p_valor_inserido = -1
                    s_valor_inserido = -1
                  
        else:
            if (valor_inserido.lower() == '2'):
                continuar_perguntando = False # encerra loop 1
                valor_inserido = -1

                while(int(valor_inserido) not in intervalo_valido_jobs):
                    valor_inserido = int(input("Insira o numero do job a se executar [1-4] :"))

                #modelo parser de conf em memoria
                parser.set('job','ini',str(valor_inserido))
                parser.set('job','atual',str(valor_inserido))
                parser.set('job','fim',str(valor_inserido))
                job_executar_agora = valor_inserido
            else:
                if(valor_inserido.lower() == '3'):
                    continuar_perguntando = False # encerra loop 1
                    os.startfile('executajob.py') #inicia programa executajob
                    os._exit(1) # encerra este programa


    #Valores Para realizar Checagens
    if(job_executar_agora == 1 ):
        print("\n\nCHECAGENS")

        repetir = True

        while(repetir):
            try:   
                svdoi70_total = float(input("Svdoi70 Total:").replace(' ','').replace(',','.'))
                svdoi70_devolucoes = float(input("Svdoi70 Devolucoes:").replace(' ','').replace(',','.'))
                sasoi60 = sas24 = sas08 = float(input("Sasoi60:").replace(' ','').replace(',','.'))
                subtotal = svdoi70_total - svdoi70_devolucoes
                srtbi01 = subtotal + sasoi60
                repetir = False
            except ValueError:
                print('Valor inserido invalido tente algo assim: xxxxxx.xx ou assim xxxxxx,xx ')
        print('\n')
        print('svdoi70_total:',svdoi70_total)
        print('svdoi70_devolucoes:',svdoi70_devolucoes)
        print('sasoi60:',sasoi60)
        print('sas24 esperado:',sas24)
        print('sas08 esperado:',sas08)
        print('subtotal (T - D):',subtotal)
        print('srtbi01 esperado (subtotal + sasoi60):',srtbi01)
        
        os.system("pause")

        parser.set('checagens', 'sas24', str(sas24))
        parser.set('checagens', 'sas08', str(sas08))
        parser.set('checagens', 'srtbi01', str(srtbi01))

       
    
    text = tesseract(x1,x2,x3,x4)
    #print(text.replace('\n',''))
    #os.system("pause")


    if text.rfind('executando') == -1  and  text.rfind('processar') == -1 and text.rfind('impressora') == -1 and text.rfind('class') == -1  and ((text.rfind('s=sim') == -1) and (text.rfind('n=nao') == -1)):
        acionador.mover_e_clicar()
       #acionador.limpar() #Pressiona F9
       #time.sleep(3)
        acionador.prosseguirT(filial)
        acionador.prosseguirT("sjbdd0"+str(job_executar_agora))            
       
        

    #Abre escreve e fecha arquivo
    file = open('files/configuracoes.ini','w')
    parser.write(file)
    file.close()

    os.startfile('executajob2.py')#inicia programa executajob
    os._exit(1)#encerra este programa


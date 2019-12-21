try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from playsound import playsound
import cv2 
import pyscreenshot as ImageGrab

import time
from threading import Thread
import os
import sys
from datetime import datetime
import re

from Acionador import Acionador
import configparser
from configparser import ConfigParser

def contem(texto, busca):
    if texto.rfind(busca) != -1:
        return True
    else:
        return False

def data_atual():
    now = datetime.now()
    return str(now.strftime(" %d %m %Y %H-%M-%S"))              


if __name__ == '__main__':
    
    #Tamanho da Tela
    cmd = 'mode 50,20'
    os.system(cmd)  

    #Carrega Arquivo de configurações
    config = configparser.ConfigParser()
    config.read('files/configuracoes.ini')
    parser = ConfigParser()
    parser.read('files/configuracoes.ini')

    #Configurações para printar a tela
    x1 = int(config['print']['X1'])
    x2 = int(config['print']['X2'])
    x3 = int(config['print']['X3'])
    x4 = int(config['print']['X4'])
    y1 = int(config['print']['Y1'])
    y2 = int(config['print']['Y2'])
    y3 = int(config['print']['Y3'])
    y4 = int(config['print']['Y4'])

    #Configuraçoes para executar o batch
    filial = str(config['filial']['codigo'])
    ini = int(config['job']['ini'])
    fim = int(config['job']['fim'])
    atual = int(config['job']['atual'])  

    #Configurações para checagens
    sas24 = str(config['checagens']['sas24'])
    sas08 = str(config['checagens']['sas08'])
    srtbi01 = str(config['checagens']['srtbi01'])

    #Variação do tipo de execução
    execucao_multipla = ini != fim
    ainda_falta = fim - atual > 0  
    proceguir = True    
    erros = 0
    index = 0

    acionador = Acionador(int(config['mouse']['X']),int(config['mouse']['Y']))

    print('Hurra !!')

    while(proceguir):
        #objeto que tira
        im = ImageGrab.grab()
        #posição e tamanho da região de leitura (putty)
        if(erros > 1):
           im=ImageGrab.grab(bbox=(y1, y2, y3, y4))
        else:            
           im=ImageGrab.grab(bbox=(x1,x2,x3,x4))    # X1,Y1,X2,Y2 to grab fullscreenull:(0,0,2000,900)   
        # # salvar imagem
        im.save('files/temp/temp.png')
        # mostrar imagem
        #im.show()        
        
        #pre processar imagem
        img = cv2.imread(r'files/temp/temp.png')
        imagem = cv2.bitwise_not(img)

        #extrai texto da imagem        
        text = pytesseract.image_to_string(Image.fromarray(imagem),lang='por', config="--user-words files/words.txt")
        text = text.lower()
        #print(text)    

        #Procura palavras chave
        #Se estiver executando
        if contem(text,'executando'):
            erros = 0
            print('EXECUTANDO |(' +  str(index)+')')           
            
        #Condições em que o slave deve prosseguir
        elif contem(text,'checagem') and ( int(atual) > 1 ) or contem(text,'processar') or contem(text, 'impressora')  or contem(text,'class') or ( contem(text, 's=sim') and contem(text, 'n=nao')):
            index = erros = 0
            print('Processar >')
            acionador.prosseguirS()            
 
        #Checagem Sas24
        elif atual == 1 and contem(text, '675 - sasbu24'):
            os.rename(r'files/temp/temp.png',r'files/temp/SAS24' + data_atual() + '.png')
            print('\nSAS24\n')
            #Extrai valor do sas24 do texto
            text = text.replace(".","")
            text = text.replace(",",".")
            sas24_print = re.findall("\d+\.\d+",  text)[0]

            if(sas24_print == sas24):
                print('Checagem Válida !')
                print('sas24:', sas24_print)
                time.sleep(3)
                acionador.prosseguirS()
            else:
                print("Checagem Invalida !")
                print("sas24 esperado:", sas24)
                print("sas24 identificado:", sas24_print)
                erros = erros + 3 #forçar parada

        #Checagem sas08
        elif atual == 1 and contem(text, '700 - sasbi'): 
            os.rename(r'files/temp/temp.png',r'files/temp/SAS08' + data_atual() + '.png')
            print('\nSAS08\n')
            #Extrai valor do sas08 do texto
            text = text.replace(".","")
            text = text.replace(",",".")
            sas08_print = re.findall("\d+\.\d+",  text)[0]

            if(sas08_print == sas08):
                print('Checagem Válida !')
                print('sas08:', sas08_print)
                time.sleep(3)
                acionador.prosseguirS()
            else:
                print("Checagem Invalida !")
                print("sas08 esperado:", sas08)
                print("sas08 identificado:", sas08_print)    
                erros = erros + 3 #forçar parada            
                
        #Checagem Srtbi01
        elif atual == 1 and contem(text, '1125 - srtbi'):         
            os.rename(r'files/temp/temp.png',r'files/temp/Srtbi01' + data_atual() + '.png')
            print('\Srtbi01\n')
            #Extrai valor do Srtbi01 do texto
            text = text.replace(".","")
            text = text.replace(",",".")
            srtbi01_print = re.findall("\d+\.\d+",  text)[0]
            rentabilidade = float(re.findall("\d+\.\d+",  text)[1])

            if(srtbi01_print == srtbi01 and rentabilidade > 0 ):
                print('Checagem Válida !')
                print('srtbi01:', srtbi01_print)
                print('rentabilidade:', rentabilidade)
                time.sleep(3)
                acionador.prosseguirS()
            else:
                print("Checagem Invalida !")
                print("srtbi01 esperado:", srtbi01)
                print("srtbi01 identificado:", srtbi01_print)   
                print('rentabilidade:', rentabilidade)
                erros = erros + 3 #forçar parada             

        #Checagem saebi05
        elif atual == 1 and contem(text, '1450 - saebi'):
            os.rename(r'files/temp/temp.png',r'files/temp/saebi05' + data_atual() + '.png')

            print('\nsaebi05\n')
            #Extrai valor do saebi05 do texto
            text = text.replace(".","")
            text = text.replace(",",".")
            saebi05_print = float(re.findall("\d+\.\d+",  text)[0]) 

            if(saebi05_print < 500 ):
                print('Checagem Válida !')
                print('saebi05:', saebi05_print)
                time.sleep(3)
                acionador.prosseguirS()
            else:
                print("Checagem Invalida !")                
                print("saebi05 identificado:", saebi05_print)                
                erros = erros + 3 #forçar parada 

        #Quando um job é concluido e for uma execução multipla e ainda não tiver terminado
        elif contem(text, 'concluido') and execucao_multipla and ainda_falta:           
           # acionador.limpar() #Pressiona F9
            os.rename(r'files/temp/temp.png',r'files/temp/sjbdd' + str(atual) + data_atual() + '.png')
            acionador.prosseguirE()
            time.sleep(3)
            acionador.prosseguirT(filial)
            atual = int(atual) + 1
            acionador.prosseguirT("sjbdd0"+str(atual)) 
            ainda_falta = fim - atual > 0
            parser.set('job','atual',str(atual))
            file = open('files/configuracoes.ini','w')
            parser.write(file)
            file.close()
            
        #Quando um job é concluido e for uma execução multipla e não houver mais jobs para executar
        elif contem(text, 'concluido') and execucao_multipla and not ainda_falta:
            os.rename(r'files/temp/temp.png',r'files/temp/sjbdd' + str(atual) + data_atual() + '.png')
            playsound('files/alarm01.wav')
            print("execucao concluida !! 1")
            if(atual > 2):
                os.startfile(os.path.realpath("../../../../relatorios/scripts_de_download/baixarrelatorioss.bat"))
            os.system("pause")
            break

        #Quando um job é concluido e não for uma execução multipla
        elif contem(text, 'concluido') and  not execucao_multipla :
            os.rename(r'files/temp/temp.png',r'files/temp/sjbdd' + str(atual) + data_atual() + '.png')
            playsound('files/alarm01.wav')
            print("execucao concluida !! 2")
            #if(atual > 2):
             #   os.startfile(os.path.realpath("../../../relatorios/scripts_de_download/copiarMapa2.bat"))
            #     os.startfile("../../../relatorios/scripts_de_download/baixarRelatorios2.bat")
            os.system("pause")
            break

        #Quando houver um erro ;/
        elif text.rfind('erro') != -1:
            os.rename(r'files/temp/temp.png',r'files/temp/erro ' + data_atual() + '.png')
            print("Atencao ERRO")
            erros = erros + 3
            index = 0
        #Quando nenhuma das condições forem identificadas default
        else:
            print("o Putty precisa de atenção  (Ó__Ò) ")
            erros = erros + 1
            index = 0                    

        if(erros > 2):
            txt = None
            if(atual == 1):            
                playsound('files/alarm01.wav')            

            #Reiniciar app após x segundos se nenhuma opção for escolhida em x segundos
            def check():
                time.sleep(8)
                if erros < 2:
                    return
                print("reiniciando...")
                os.startfile(__file__)
                os._exit(1)

            if(erros > 1):
                Thread(target = check).start()

            while(erros >= 3):
                txt = input("Devo continuar? <C>CONTINUAR <P> Parar :")
                if(txt.lower() == 'c'):
                    erros = 0
                elif txt.lower() == 'p': 
                    erros = 0                   
                    proceguir = False #interromper programa

        index = index + 1
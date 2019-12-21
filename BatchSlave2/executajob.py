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
from Acionador import Acionador
import configparser


if __name__ == '__main__':

    
    proceguir = True    
    erros = 0
    index = 0
    cmd = 'mode 50,20'
    os.system(cmd)
    print('Olá')

    config = configparser.ConfigParser()
    config.read('files/configuracoes.ini')
    x1 = int(config['print']['X1'])
    x2 = int(config['print']['X2'])
    x3 = int(config['print']['X3'])
    x4 = int(config['print']['X4'])
    y1 = int(config['print']['Y1'])
    y2 = int(config['print']['Y2'])
    y3 = int(config['print']['Y3'])
    y4 = int(config['print']['Y4'])

    acionador = Acionador(int(config['mouse']['X']),int(config['mouse']['Y']))

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
    
        #procura palavras chave


        if text.rfind('executando') != -1 :
            print('EXECUTANDO > (' + str(index) + ')')
            erros = 0
        elif text.rfind('processar') != -1 or text.rfind('impressora') != -1 or text.rfind('class') != -1  or ((text.rfind('s=sim') != -1) and (text.rfind('n=nao') != -1)):
            print('Processar >')
            acionador.prosseguirS()
            erros = 0
            index = 0
        else:
            print("o Putty precisa de atenção  (Ó__Ò) ")
            erros = erros + 1
            index = 0
        

        if(erros > 2):            
            playsound('files/alarm01.wav')
            txt = None

            #Reiniciar app após x segundos se nenhuma opção for escolhida em x segundos

            def check():
                time.sleep(15)
                if erros == 0:
                    return
                print("reiniciando...")
                os.startfile(__file__)
                os._exit(1)

            Thread(target = check).start()


            while(erros >= 3):
                txt = input("Devo continuar? <C>CONTINUAR <P> Parar :")
                if(txt.lower() == 'c'):
                    erros = 0
                elif txt.lower() == 'p': 
                    erros = 0                   
                    proceguir = False #interromper programa

        index = index + 1

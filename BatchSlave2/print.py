 

#-- include('examples/showgrabfullscreen.py') --#

import pyscreenshot as ImageGrab
import sys
import os
import configparser

if __name__ == '__main__':

    job = ""
    job = sys.argv[1:]
    job = 1 if str(job) == '[]' else int(sys.argv[1:][0])
    proceguir = True
    cmd = 'mode 50,20'
    os.system(cmd)

    config = configparser.ConfigParser()


    print('')
    print('Posicione o putty na parte superior direita da tela')
    print('')
    print('')


    while (proceguir):    

        config.read('files/configuracoes.ini')
        x1 = int(config['print']['X1'])
        x2 = int(config['print']['X2'])
        x3 = int(config['print']['X3'])
        x4 = int(config['print']['X4'])
        y1 = int(config['print']['Y1'])
        y2 = int(config['print']['Y2'])
        y3 = int(config['print']['Y3'])
        y4 = int(config['print']['Y4'])

        # grab fullscreen
        im = ImageGrab.grab()
        # im=ImageGrab.grab(bbox=(850,95,1510,550))  # X1,X2,X3,X4 full:(0,0,2000,900)
        # im=ImageGrab.grab(bbox=(850,400,1310,550)) # Y1, Y2,Y3,Y4
        if(job == 1):
            im=ImageGrab.grab(bbox=(x1, x2, x3, x4))       
        else:            
            im=ImageGrab.grab(bbox=(y1, y2, y3, y4)) 
    # save image file
        im.save('files/temp.jpg')

        # show image in a window
        im.show()

        txt = input("Consegue ver o Putty por inteiro no print ? \n <S>Sim - Prosseguir\n <N> Nao - novo print \n opcao:")
        if(txt.lower() == 's'):
            proceguir = False
      

    os.startfile('bootstrap.py')
    os._exit(1)



#-#
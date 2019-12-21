 
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import sys
import configparser
import os

import cv2
#-- include('examples/showgrabfullscreen.py') --#
import pyscreenshot as ImageGrab

if __name__ == '__main__':

    job = ""
    job = sys.argv[1:]
    job = 1 if str(job) == '[]' else int(sys.argv[1:][0])
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


    # grab fullscreen
    im = ImageGrab.grab()
    if(job == 1):
        im=ImageGrab.grab(bbox=(x1, x2, x3, x4))       
    else:            
        im=ImageGrab.grab(bbox=(y1, y2, y3, y4)) 
    im.save('files/temp.jpg')

    # show image in a window
   # im.show()


    
    img = cv2.imread(r'files/temp.jpg')
    imagem = cv2.bitwise_not(img)     
   

    text = pytesseract.image_to_string(Image.fromarray(imagem),lang='por', config="--user-words files/words.txt")
    print(text)
    print()
    text = text.lower()
    print (text.rfind('processar') != -1 ) 

    #print(pytesseract.image_to_string(Image.fromarray(imagem), lang='port'))

#-#
    os.system("pause")
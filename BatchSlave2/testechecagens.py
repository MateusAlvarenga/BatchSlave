 
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import sys
import configparser
import os
import cv2

import re
#-- include('examples/showgrabfullscreen.py') --#
import pyscreenshot as ImageGrab

import configparser
from configparser import ConfigParser

def contem(texto, busca):
    if texto.rfind(busca) != -1:
        return True
    else:
        return False
 

config = configparser.ConfigParser()
config.read('files/configuracoes.ini')
parser = ConfigParser()
parser.read('files/configuracoes.ini') 

img = cv2.imread(r'files/temp/saebi05.png')
imagem = cv2.bitwise_not(img)     

sas24 = str(config['checagens']['sas24'])
sas08 = str(config['checagens']['sas08'])
srtbi01 = str(config['checagens']['srtbi01'])


text = pytesseract.image_to_string(Image.fromarray(imagem),lang='por', config="--user-words files/words.txt")

text = text.replace("\n","")
text = text.lower()
print(text)
print('\n\n\n>\n\n\n')

#Checagem Sas24
if contem(text, '675 - sasbu24'):
    print('SAS24')             

#Checagem sas08
elif contem(text, '700 - sasbi'):           
    print('SAS08')            

#Checagem Srtbi01
elif contem(text, '1125 - srtbi'):         
    print('SRTBI01')            

#Checagem saebi05
elif contem(text, '1450 - saebi'):
    print('saebi05')
print("\n\n numeros:")

text = text.replace(".","")
text = text.replace(",",".")
print(text)
print('\n\n\n>\n\n\n')

saebi05 = float(re.findall("\d+\.\d+",  text)[0])

print('saebi05 :',saebi05)
 

if(saebi05  < 500):
    print("checagem Valida !")
else:
    print("checagem invalida")


os.system("pause")
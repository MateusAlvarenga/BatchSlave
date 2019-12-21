import pynput
from pynput.keyboard import Key
from pynput.mouse import Button
import time
 

class Acionador:

    def __init__(self,positionX,positionY):
        self.x = positionX
        self.y = positionY
        self.keyboard = pynput.keyboard.Controller()
        self.mouse = pynput.mouse.Controller() 

    def prosseguirE(self):
        self.mouse.position = (self.x, self.y)
        self.clicar()     
        self.pressionar(Key.enter)
        time.sleep( 1 )

    def prosseguirS(self):
        self.mouse.position = (self.x, self.y)
        self.clicar()
        self.pressionar('S')     
        self.pressionar(Key.enter)
        time.sleep( 1 )

    def prosseguirN(self):
        self.mouse.position = (self.x, self.y)
        self.clicar()
        self.pressionar('N')     
        self.pressionar(Key.enter)
        time.sleep( 1 )
    
    def pressionarF(self):
        self.mouse.position = (self.x, self.y)
        self.clicar()
         
        self.pressionar('f')         
        time.sleep( 1 )
    
    def pressionarR(self):
        self.mouse.position = (self.x, self.y)
        self.clicar()
        self.pressionar('r')      
        time.sleep( 1 )

    def prosseguirT(self, texto):
        self.mouse.position = (self.x, self.y)
        self.clicar()
        self.escrever(texto)  
        self.pressionar(Key.enter)
        time.sleep( 1 )

    def mover_e_clicar(self):
        self.mouse.position = (self.x, self.y)
        self.clicar()

    def escrever(self,texto):
        self.keyboard.type(texto)

    def limpar(self):
        self.pressionar(Key.f9)

    def pressionar(self,alvo):
        self.keyboard.press(alvo)
        self.keyboard.release(alvo)    

    def clicar(self):
        self.mouse.click(Button.left,1)


    def setPosition(self, positionX, positionY):
        self.mouse.position = (positionX, positionY)
        
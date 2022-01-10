import os
import pygame, sys

##############  Class Button  ##############################################################################################
class button:
    x = 0
    y = 0
    width = 0
    height = 0
    btn_name = ""
    btn_caption = ""
    def __init__(self, x, y, width, height, btn_name):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.btn_name = btn_name
    def isClicked(self, Maus_x, Maus_y):
        if Maus_y > self.y + self.height:
            return False
        if Maus_y < self.y:
            return False
        if Maus_x > self.x + self.width:
            return False
        if Maus_x < self.x:
            return False
        return True



##############  Start  #####################################################################################################

##############  PyGame  
pygame.init()
pygame.display.set_caption('Mine Sweeper')
##############  Variable  
Farben={"Background":(192,192,192),"Screen":(0, 0, 0),"input":(0, 0, 0),"fehler":(255,255,0),"fehlerbg":(0,0,0)}
Screen={"width":400,"height":300,"left":10,"right":10}
##############  Font  
font = pygame.font.SysFont("Arial", 28)

##############  Eingabe Felder  ############################################################################################
button_INPUTNAME = button(10, 100, 380, 50, "InputName")
button_INPUTNAME.btn_caption = "Player1"
button_INPUTX = button(10, 20, 100, 50, "InputX")
button_INPUTX.btn_caption = "X=12"
button_INPUTY = button(150, 20, 100, 50, "InputY")
button_INPUTY.btn_caption = "Y=12"
button_INPUTM = button(290, 20, 100, 50, "InputM")
button_INPUTM.btn_caption = "Mines"

##############  Tasten  ####################################################################################################
button_EXIT = button(10, 160, 380, 50, "Spiel")
button_SPIEL = button(10, 220, 380, 50, "End")

##############  Button List  ###############################################################################################
button_list = []
button_list.append(button_INPUTNAME)
button_list.append(button_INPUTX)
button_list.append(button_INPUTY)
button_list.append(button_INPUTM)
button_list.append(button_SPIEL)
button_list.append(button_EXIT)

index =0
Error_MinesZahl = False
schrift = pygame.font.SysFont('Arial', 32)


##############  PYGAME loop  ###############################################################################################
screen = pygame.display.set_mode((Screen['width'], Screen['height']))

while True:
    ##############  Events  ####################################################################################################
    #############################################  Beneden  ####################################################################
        #####  mit "Close" beenden  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:     # Exit mit X
            sys.exit()
        #####  mit "q" beenden  
        if event.type == pygame.KEYDOWN:  # Exit mit Q
            if event.key == pygame.K_q:
                sys.exit()

    #############################################  Mouse Links  ################################################################               
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1: 
            pos = pygame.mouse.get_pos()
            for b in button_list:
                if b.isClicked(pos[0], pos[1]):
                    ##############  beenden  
                    if b.btn_name == "End":
                        sys.exit()
                    ##############  Spielen  
                    elif b.btn_name == "Spiel":
                    #####  Prüfen : Spieler Name nicht leer  
                        Spielername = button_list[0].btn_caption
                        if Spielername =="":
                            button_list[0].btn_caption="Player1"
                            Spielername="Player1"
                    #####  Prüfen : X , Y und Mines     
                        try:
                            x =int(button_list[1].btn_caption)
                        except:
                            x=12
                        try:
                            y =int(button_list[2].btn_caption)
                        except:
                            y=12
                        try:
                            m =int(button_list[3].btn_caption)
                        except:
                            m = int(x * y /10)
                        #####  Prüfen : X , Y und Mines kleiner als X * Y  
                        if m > x * y:
                            Error_MinesZahl = True
                            sound = pygame.mixer.Sound('rec/alert.mp3')
                            pygame.mixer.Sound.play(sound)
                        else:
                        #####  Minesweeper ausführen  
                            sound = pygame.mixer.Sound('rec/menu.mp3')
                            pygame.mixer.Sound.play(sound)
                            arg = "{} {} {} {}".format(Spielername , x, y,m )
                            os.system("minesweeper.py "+ arg)                      
                    #####  Welche Input Feld ist gedrückt  
                    elif b.btn_name == "InputName":
                        index = 0 
                    elif b.btn_name == "InputX":
                        index = 1 
                    elif b.btn_name == "InputY":
                        index = 2 
                    elif b.btn_name == "InputM":
                        index = 3
                        Error_MinesZahl = False
                    else:
                        index = 100
                    #####  Eingabefeld löschen mit Klick     
                    button_list[index].btn_caption = ''

    #############################################  Key Down  ###################################################################               
        if event.type == pygame.KEYDOWN:
            #####  Stop bearbeitung von Eingabefeld  
            if event.key == pygame.K_RETURN:
                index = 100
            #####  Letzte char löschen  
            elif event.key == pygame.K_BACKSPACE:
                if index != 100:
                    button_list[index].btn_caption = button_list[index].btn_caption[:-1]
            #####  zu eingabefeld hinzufügen  
            else:
                #####  keine leer Zeichen erlaubt  
                # leer zeichen verursacht fehler beim  Spiel
                if index != 100 and event.unicode !=" ":
                    #####  Nur Nummern eralubt im X , Y und Mineszahl  
                        if index!=0:
                            erlaubtezeichen = "0123456789"
                            if event.unicode in erlaubtezeichen:
                                button_list[index].btn_caption += event.unicode
                        elif index == 0 :
                            button_list[0].btn_caption += event.unicode



    ##############  Zeichen  ###################################################################################################
    screen.fill(Farben['Background'])
    #############################################  Tasten und Eingabefeld zeichnen  ############################################
    for b in button_list:
        img = pygame.image.load('rec/'+b.btn_name + '.png')
        screen.blit(img, (b.x, b.y))
        pygame.draw.rect(screen, Farben['Screen'], pygame.Rect(b.x, b.y, b.width, b.height),  2)
    
    #############################################  Werte im Eingabefelder zeichnen  ############################################
    for i in range(0,5):
        nametext = schrift.render(button_list[i].btn_caption, True, Farben['input'])          
        screen.blit(nametext, (button_list[i].x+15, button_list[i].y+5))
    #############################################  Fehler Bildschirm  ##########################################################
    if Error_MinesZahl:
        font1 = pygame.font.SysFont('Arial', 40)
        surface = schrift.render('Falsche MINES ZAHL', True,Farben['fehler'],Farben['fehlerbg'])
        rect = surface.get_rect(center=(200, 150))
        screen.blit(surface,rect)
    
    ##############  FPS und Update  ############################################################################################   
    pygame.time.Clock().tick(60)
    pygame.display.update()


import pygame
import random
import sys
from Spiellist import Spiellist
from Spiellist import Cell

##############  Spiel Eingaben  ########################################################################################
##############  Vom Parameter einlesen  
try:
    Spiel_Spielername = sys.argv[1]
    X_total = int(sys.argv[2])
    Y_total = int(sys.argv[3])
    Mine_Zahl = int(sys.argv[4])
##############  Eingegeben Werte  
except:
    Spiel_Spielername = "Sipan"
    X_total = 10
    Y_total = 10
    Mine_Zahl = 20


Mine_ZahlOriginal = Mine_Zahl
clock = pygame.time.Clock()


##############  Start  #####################################################################################################

##############  PyGame  
pygame.init()
pygame.display.set_caption('Mine Sweeper')
##############  Variable  
Lost = {"animation":1 ,"clickanimation":1 , "gameover":False }
Farben ={"screen":(192,192,192) , "Stats":(0,0,0) ,"gameover":(255,255,0) , "Continue":(255,0,0)}
Spiel ={"Cellwidth":32 , "Cellheight":32 ,"Topbar":50 ,"Bottombar":50 ,
"leftbar":10 ,"rightbar":10 ,"drawW":0 ,"drawH":0 ,"totalW":0 ,"totalH":0,
"Result":"","isFertig":False,"timer":0,"starttick":0}
##############  Font  
font = pygame.font.SysFont('Arial', 24)

##############  Fenster Eigenschaften  #####################################################################################
Spiel['starttick'] = pygame.time.get_ticks()
Spiel['drawW'] = Spiel['Cellwidth'] * X_total
Spiel['drawH'] = Spiel['Cellwidth'] * Y_total
totalW = Spiel['drawW'] + Spiel['leftbar'] + Spiel['rightbar']
totalH = Spiel['drawH'] + Spiel['Topbar'] + Spiel['Bottombar']

##############  List von Cells erstellen  ##################################################################################
CellList = Spiellist(Y_total, X_total, Mine_Zahl)

##############  Calculiere X , Y für jede Cell  ############################################################################
for Cell in CellList.Cell_list:
    x = Cell.pos % X_total
    if x == 0:
        x = X_total
    x -= 1
    Cell.x = Spiel['leftbar']+x * Spiel['Cellwidth']
    y = int((Cell.pos-1)/X_total)
    Cell.y = Spiel['Topbar']+y * Spiel['Cellheight']
    Cell.width = Spiel['Cellwidth']
    Cell.height = Spiel['Cellheight']


##############  Funktionen  ################################################################################################
############################################################################################################################
##############  Alle Nachbarn Cells mit 0 öffnen  
def Value_0_Offnen(tmp_Cell):
    clist = []
    clist = tmp_Cell.nc_list.copy()
    global Mine_Zahl
    for nc in clist:
        ##############  Cells Wert ist 0 und nicht geklickt  
        if CellList.Cell_list[nc-1].value == 0 and CellList.Cell_list[nc-1].mark != 2:
            clist.extend(CellList.Cell_list[nc-1].nc_list)
            #####  Zahl von Minen recalculieren für Statistik  
            if CellList.Cell_list[nc-1].mark == 1:
                Mine_Zahl += 1
        ##############  Cells Wert ist nicht 0 und nicht geklickt  
        if CellList.Cell_list[nc-1].value != 9 and CellList.Cell_list[nc-1].mark != 2:
            CellList.Cell_list[nc-1].mark = 2
            #####  Zahl von Minen recalculieren für Statistik  
            if CellList.Cell_list[nc-1].mark == 1:
                Mine_Zahl += 1

##############  Cell Markieren mit Recht Klick
def Cell_Flag(tmp_Cell):
    global Mine_Zahl
    if tmp_Cell.mark == 1:
    #####  unmarkieren 
        tmp_Cell.mark = 0
        Mine_Zahl += 1
    else:
    #####  markieren  
        if Mine_Zahl <= 0:
            return
        tmp_Cell.mark = 1
        Mine_Zahl -= 1


##############  PYGAME loop  ###############################################################################################
screen = pygame.display.set_mode((totalW, totalH))
while True:
    ##############  Gewinn Überprüfen  #########################################################################################
    x = 0
    for Cell in CellList.Cell_list:
        #####  Count alle geöffneten Cells  
        if Cell.mark == 2:
            x += 1
    if x == X_total*Y_total-Mine_ZahlOriginal:
        Spiel['isFertig'] = True
        Spiel['Result'] = "YOU WON"

    ##############  Events  ####################################################################################################
    for event in pygame.event.get():
    #############################################  Beneden  ####################################################################
        #####  mit "Close" beenden  
        if event.type == pygame.QUIT:
            sys.exit()
        #####  mit "q" beenden  
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                sys.exit()

    #############################################  Mouse Links  ################################################################
        ##############  Nach Gewinn beenden  
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and Spiel['isFertig']:  
            sys.exit()
        ##############  Cell öffnen  
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and not Spiel['isFertig']:
            for Cell in CellList.Cell_list:
                pos = pygame.mouse.get_pos()
                if Cell.isClicked(pos[0], pos[1]) and Cell.mark == 0:
                    Cell.mark = 2
                    sound = pygame.mixer.Sound('rec/click.mp3')
                    pygame.mixer.Sound.play(sound)
        #####  Verloren : Cell hat Mine  
                    if Cell.value == 9:  
                        Spiel['Result'] = "GAME OVER"
                        Spiel['isFertig'] = True
                        sound = pygame.mixer.Sound('rec/mine.mp3')
                        pygame.mixer.Sound.play(sound)
                        for Cell in CellList.Cell_list:
                            if Cell.value ==9 :
                                Cell.mark = 2                           
        #####  Andere Cell öffnen wenn Value ist 0  
                    if Cell.value == 0:
                        Value_0_Offnen(Cell)
                        sound = pygame.mixer.Sound('rec/0value.mp3')
                        pygame.mixer.Sound.play(sound)
    #############################################  Mouse Rechts  ###############################################################
        ##############  Cell Markieren  
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3 and not Spiel['isFertig']:  # Right Click
            for Cell in CellList.Cell_list:
                pos = pygame.mouse.get_pos()
                if Cell.isClicked(pos[0], pos[1]) and Cell.mark != 2:  # Flag
                    Cell_Flag(Cell)



    ##############  Zeichen  ###################################################################################################
    screen.fill(Farben['screen'])

    #############################################  Statistik  ##################################################################
    ##############  Zahl von Mines  
    surface = font.render("Mines: " + str(Mine_Zahl), True, Farben['Stats'])
    rect = surface.get_rect(center=(55, Spiel['Topbar']/2))
    screen.blit(surface, rect)
    ##############  Spieler Name  
    surface = font.render(Spiel_Spielername, True, Farben['Stats'])
    rect = surface.get_rect(center=(totalW/2, Spiel['Topbar']/2))
    screen.blit(surface, rect)
    ##############  Timer  
    if not Spiel['isFertig']:
        Spiel['timer'] = int((pygame.time.get_ticks()-Spiel['timer'])/1000)
    surface = font.render("Time " + str(Spiel['timer']).zfill(3), True, Farben['Stats'])
    rect = surface.get_rect(center=(totalW - 52, Spiel['Topbar']/2))
    screen.blit(surface, rect)
    
    #############################################  Cell Zeichnen  ##############################################################
    for Cell in CellList.Cell_list:
        ##############  Cell im Anfangs Status  
        if Cell.mark == 0:  
            img = pygame.image.load('rec/none.png')
            img = pygame.transform.scale(img, (Cell.width, Cell.height))
            screen.blit(img, (Cell.x, Cell.y,Cell.width, Cell.height))
            #####  Ränder Zeichnen  
            #pygame.draw.rect(surface, (192,192,192), pygame.Rect(tmp_Cell.x, tmp_Cell.y, tmp_Cell.width, tmp_Cell.height),  1)
        ##############  Cells mit Fahne anschauen  
        if Cell.mark == 1:  
            img = pygame.image.load('rec/flag.png')
            img = pygame.transform.scale(img, (Cell.width, Cell.height))
            screen.blit(img, (Cell.x, Cell.y,Cell.width, Cell.height))
        ##############  Cells mit Werte anschauen  
        if Cell.mark == 2:  
            img = pygame.image.load('rec/' + str(Cell.value)+'.png').convert_alpha()
            img = pygame.transform.scale(img, (Cell.width, Cell.height))
            screen.blit(img, (Cell.x, Cell.y, Cell.width, Cell.height))
            #####  Ränder Zeichnen 
            #pygame.draw.rect(screen, (0, 255, 255), pygame.Rect(Cell.x, Cell.y, Cell.width, Cell.height),  1)
    
    #############################################  Ende Bildschirm  ############################################################
    if Spiel['isFertig']:
        ##############  Animation Geschwindigkeit
        if Lost['animation'] < 40:
            Lost['animation'] += 2
        else:
            Lost['gameover'] = True

        ##############  Game Over  
        font1 = pygame.font.SysFont('Arial', Lost['animation'], True)
        surface = font1.render(Spiel['Result'], True, Farben["gameover"],True)
        rect = surface.get_rect(center=(totalW/2, totalH/2))
        screen.blit(surface, rect)
        ##############  Click to Continue  
        if Lost['gameover']:
            if Lost['clickanimation'] < 20:
                Lost['clickanimation'] += 1
            font2 = pygame.font.SysFont('Arial', Lost['clickanimation'])
            surface = font2.render("Click to Continue", True, Farben["Continue"],True)
            rect = surface.get_rect(center=(totalW/2, totalH/2+50))
            screen.blit(surface, rect)
    ##############  FPS und Update  ############################################################################################   
    pygame.time.Clock().tick(80)
    pygame.display.flip()

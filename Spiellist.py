import random

class Cell:
    mark = 0   # 0 Null    1 Flag    2 Shown
    value = 0  # 0-8       9 Bomb
    pos = 0
    nc_list = []
    x=0 
    y=0
    width =0 
    height = 0
    def __init__(self, pos, X_total,Y_total):
        self.pos = pos
        ##############  Nachbar finden  
        nc_list = []
        #####  Auf Seite  
        nc_list.append(pos+X_total)
        nc_list.append(pos-X_total)
        #####  Unten  
        if pos % X_total !=0:
            nc_list.append(pos-X_total+1)   
            nc_list.append(pos+1)
            nc_list.append(pos+X_total+1)
        #####  Oben  
        if (pos - 1) % X_total !=0:
            nc_list.append(pos+X_total-1)
            nc_list.append(pos-X_total-1)
            nc_list.append(pos-1)
        #####  Ungültige nachbarn entfernen  
        temp = []
        for Nachbar in nc_list:
            if Nachbar <= 0:
                continue
            if Nachbar > Y_total * X_total:
                continue
            temp.append(Nachbar)
        self.nc_list= temp
    ##############  Click prüfen  
    def isClicked(self,Maus_x,Maus_y):
        if Maus_y > self.y + self.height:
            return False
        if Maus_y < self.y:
            return False
        if Maus_x > self.x + self.width:
            return False
        if Maus_x < self.x:
            return False
        return True
        
class Spiellist:
    Cell_list=[]
    def __init__(self,X_total, Y_total,Mine_Zahl):
        ##############  Cells Erstellen  
        Cell_list = []
        temp_pos = 0
        for x in range(1, X_total+1):
            for y in range(1, Y_total+1):
                temp_pos += 1
                temp_Cell = Cell(temp_pos, X_total, Y_total)
                self.Cell_list.append(temp_Cell)

        ##############  Mines random legen  
        temp_mines = Mine_Zahl
        while temp_mines > 0:
            for temp_Cell in self.Cell_list:
                if temp_mines <= 0:
                    break
                if temp_Cell.value != 9:
                    temp_random = random.randint(0, 10)
                    if temp_random == 5:
                        temp_Cell.value = 9
                        temp_mines -= 1
                    else:
                        continue
        ##############  Mines werte rechnen  
        for temp_Cell in self.Cell_list:
            if temp_Cell.value == 9:
                continue
            temp_value = 0
            for temp_nc in temp_Cell.nc_list:
                if self.Cell_list[temp_nc-1].value == 9:
                    temp_value += 1
            temp_Cell.value = temp_value

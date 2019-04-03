from ship import Ship
import pygame
from utils import setTextbox

#various color definitions
white = (255,255,255)
dark_white = (220,220,220)
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)
ready_but_color = (204,204,0)
ready_but_active_color = (255,255,0)

class Map:
#constructor and attribute declaration
    def __init__(self,dim,x,y,tile_size,bgImg,total_ships=4):
        self.dim = dim
        self.x = x
        self.y = y
        self.ts = tile_size
        self.x_max = self.x + self.dim*self.ts
        self.y_max = self.y + self.dim*self.ts
        self.bgImg = bgImg
        self.coo_mapper = self.idx2coord()
        self.total_ships = total_ships
        self.ships = []
        self.tries = []
        self.map = self.createEmptyMap()
        self.letters = ()
        self.nums = ()
        self.images = {}

    def createEmptyMap(self):
        mapArray = []
        for j in range(self.dim):
            mapArray.append([])
            for i in range(self.dim):
                mapArray[j].append('O')
        return mapArray

    def idx2coord(self):
        coo_map = {}
        for i in range(self.dim):
            for j in range(self.dim):
                # define top-left & bottom-right coord
                coo_map[(i,j)] = (self.x + i*self.ts, self.y + j*self.ts),(self.x + (i+1)*self.ts, self.y + (j+1)*self.ts)
        return coo_map

    def coord2idx(self,tar):
        tar_x,tar_y = tar
        tar_x = tar_x - self.x
        tar_y = tar_y - self.y
        i,j = tar_x//self.ts,tar_y//self.ts
        return i,j

    def hit_xy(self,xy):
        x,y = xy
        # Ensure hit target is within bounds
        print(self.x,self.y)
        print(x,y)
        print(self.x_max,self.y_max)
        if(self.x<=x<=self.x_max and self.y<y<=self.y_max):
            ij = self.coord2idx(xy)
            return self.hit(ij)
        else:
            return -1

    def hit(self,ij):
        didHit = 0
        if ij not in self.tries:
            #create hit points
            print('Points hit: ',end='')
            hitPoints = self.genHitPoints(ij)
            for hitPoint in hitPoints:
                self.tries.append(hitPoint)
                for ship in self.ships:
                    didHit = didHit | ship.hit(hitPoint)
            return didHit #hit any = 1, nohit = 0
        else:
            # invalid selection
            return -1

    def genHitPoints(self,ij):
        i,j = ij
        # Generate 9 hitpoints
        hitPoints = [(i-1,j-1),(i,j-1),(i+1,j-1),(i-1,j),(i,j),(i+1,j),(i-1,j+1),(i,j+1),(i+1,j+1)]
        hitPoints_valid = []
        # remove invalid hitpoints
        for hitPoint in hitPoints:
            if(not (hitPoint[0]<0 or hitPoint[0]>=self.dim or hitPoint[1]<0 or hitPoint[1]>=self.dim)):
                hitPoints_valid.append(hitPoint)
        return hitPoints_valid

    def addShip(self,head_xy,shipType,rot,img):
        # head is in (x,y) coordinates
        head_ij = self.coord2idx(head_xy)
        newShip = Ship(len=shipType,img=img,rot=rot,head=head_ij)
        #check for valid placement (within bounds)
        for idx in newShip.body:
            if(idx[0]<0 or idx[1]<0 or idx[0]>=self.dim or idx[1]>=self.dim):
                print('Add failed! Illegal idx: {}; out of map bounds.'.format(idx))
                setTextbox('Add failed! Illegal idx: {}; out of map bounds.'.format(idx))
                return False

        #check for ship collision; shipType is the length of ship
        for ship in self.ships:
            for idx in newShip.body:
                if(idx in ship.body):
                    print('Add failed! Illegal idx: {}; another ship has already been placed here.'.format(idx))
                    setTextbox('Add failed! Illegal idx: {}; another ship has already been placed here.'.format(idx))
                    return False

        #if all else passes, successfully add new ship
        self.ships.append(newShip)
        print('Ship added at {}.'.format(newShip.body))
        setTextbox('Ship added at {}.'.format(newShip.body))
        self.getMapState()
        return True

    def dropShip(self,xy):
        x,y = xy
        idx = self.coord2idx((x,y))
        #match coordinate to ship
        for ship in self.ships:
            if(idx in ship.body):
                self.ships.remove(ship)
                print('Ship removed!')
                break

    def getMapState(self):
        self.map = self.createEmptyMap() #refresh map
        print(self.tries)
        for i,j in self.tries: #returns set of coordinates of each prev made attempt
            self.map[j][i] = 'X'

        #successful attempts
        for ship in self.ships:
            for i,j in ship.body:
                if((i,j) in ship.damaged):
                    self.map[j][i] = 'D'
                else:
                    self.map[j][i] = 'S'

        for row in self.map:
            print(row)
        return self.map

    def getAliveShips(self):
        aliveShips = []
        for ship in self.ships:
            if(ship.life>0):
                aliveShips.append(ship)
        return aliveShips

    def drawMap(self,display_surface):
        #starting x and y coordinate
        x = self.x
        y = self.y

        nums = self.nums
        letters = self.letters

        #margin size and board legend x location for player board are both 50
        delta_margin = 50
        player_letter_ref_x = x

        #max y location for board legend
        y_max = self.y_max

        #max x location for board legend of player and enemy board
        x_player_max = self.x_max

        display_surface.blit(self.bgImg,(x,y))

        #draw individual tile outlies
        #410 is max y coordinate
        #410 and 860 are max x coordinates for respective boards
        #left board (player board)
        curr_num = 0
        curr_letter = 0
        while (x < x_player_max):
        	#draw number legend with slight location offsets
            display_surface.blit(nums[curr_num],(x+10,y-30))
            curr_num += 1
            while (y < y_max):#draw tiles and only draw letter legend only once
                pygame.draw.rect(display_surface,green,(x,y,self.ts,self.ts),1)
                if x == player_letter_ref_x:
                    display_surface.blit(letters[curr_letter],(x-30,y+5))
                    curr_letter += 1
                y += self.ts
            x += self.ts
            y = delta_margin

        # curr_num = 0
        # curr_letter = 0
        #
        # #account for middle barrier of 50 pixels
        # x += delta_margin
        #
        # #draw enemy side backrgound of board
        # display_surface.blit(self.images['battle_waterIMG'],(x,y))
        #
        # #right board(enemy/attacking board)
        # while (x < x_enemy_max):
        #     display_surface.blit(nums[curr_num],(x+10,y-30))
        #     curr_num += 1
        #     while (y < y_max):
        #         pygame.draw.rect(display_surface,green,(x,y,self.ts,self.ts),1)
        #         if x == enemy_letter_ref_x:
        #             display_surface.blit(letters[curr_letter],(x-30,y+5))
        #             curr_letter += 1
        #         y += self.ts
        #     x += self.ts
        #     y = delta_margin

    def drawTries(self,display_surface):
        for row in range(self.dim):
            for col in range(self.dim):
                x,y = self.coo_mapper[(col,row)][0]
                if(self.map[row][col] == 'D'):
                    display_surface.blit(self.images['hitIMG'],(x,y))
                elif(self.map[row][col] == 'X'):
                    display_surface.blit(self.images['missIMG'],(x,y))

    def drawShips(self,display_surface):
        for ship in self.ships:
            shipHead_xy = self.coo_mapper[ship.head]
            if ship.rot == 'V':
                display_surface.blit(pygame.transform.rotate(ship.img,90),shipHead_xy)
            else:
                display_surface.blit(ship.img,shipHead_xy)

    # def pickupShip(self,(mouse_x,mouse_y)):
    #     for ship in self.ships:
    #         if(ship.init_Pos = (mouse_x,mouse_y)):
    #             ship.isPickedUp = 1
    #             return ship.image

    def drawReset(self):
        self.drawMap()
        for ship in self.ships():
            ship.drawReset()

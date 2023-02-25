######################################################
# implementation of wave function collapse in python #
######################################################

import pygame
import numpy as np
import copy
import time
import random

pygame.init()

class tile:
    def __init__(self, conf) -> None:
        self.conf = conf
        self.start_pos = [(-1, 3), (3, -1), (6, 3), (3, 6)]
        self.tile = pygame.Surface((7, 7))
        self.init_tile()
        
    def init_tile(self):
        self.tile.fill((255, 255, 255))
        for i in range(4):
            if self.conf[i]:
                pygame.draw.line(self.tile, (200, 0, 0), self.start_pos[i], (3, 3))

possible_tiles = [
    [0, 0, 0, 0],
    [0, 0, 1, 1],
    [0, 1, 0, 1],
    [0, 1, 1, 0],
    [0, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 0, 1, 0],
    [1, 0, 1, 1],
    [1, 1, 0, 0],
    [1, 1, 0, 1],
    [1, 1, 1, 0],
    [1, 1, 1, 1]
]

tileList = [tile(possible_tile) for possible_tile in possible_tiles]

class possibleTile:
    def __init__(self, x, y) -> None:

        self.x = x
        self.y = y
        
        self.possibility = list(range(len(possible_tiles)))
        
        self.collapsed = False
        self.tile:tile
        
    def remove_pos(self, pos, value):
        for i in copy.copy(self.possibility):
            if possible_tiles[i][(pos+2)%4] != value:
                self.possibility.remove(i)
                
    def collapse(self):
        self.collapsed = True
        self.tile = copy.copy(tileList[random.choice(self.possibility)])
        
    def getpos(self):
        return self.possibility
        
class mainWindow:
    def __init__(self) -> None:
        self.size = 100
        self.zoom = 1000//self.size
        
        self.screen = pygame.display.set_mode((1000, 1000))
        self.screen.fill((0, 0, 0))
        
        self.table = np.zeros((self.size, self.size), dtype=possibleTile)
        self.init_table()
        self.dir = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        self.collapsing = set()
        
    def init_table(self):
        for i in range(self.size):
            for j in range(self.size):
                self.table[i, j] = possibleTile(j, i)
        
    def collapse(self):
        self.collapsing.add(self.table[self.size//2, self.size//2])
        self.col_single_cell(self.size//2, self.size//2)
        self.draw_tile(self.table[self.size//2, self.size//2])

        while len(self.collapsing) != 0:
            cell = sorted(self.collapsing, key=lambda x: len(x.possibility))[0]
            self.col_single_cell(cell.x, cell.y)
            
        time.sleep(1000)
        
            
            
    def col_single_cell(self, x, y):
        
        self.table[y, x].collapse()
        self.collapsing.remove(self.table[y, x])
        self.draw_tile(self.table[y, x])
        for i in range(4):
            nx = x+self.dir[i][1]
            ny = y+self.dir[i][0]
            
            if nx < 0 or nx >= self.size or ny < 0 or ny >= self.size or self.table[ny, nx].collapsed: 
                continue
           
            self.table[ny, nx].remove_pos(i, self.table[y, x].tile.conf[i])
            self.collapsing.add(self.table[ny, nx])
            
    def draw_tile(self, tile):
        self.screen.blit(pygame.transform.scale(tile.tile.tile, (self.zoom, self.zoom)), (tile.x*self.zoom, tile.y*self.zoom))
        pygame.display.flip()

            
main = mainWindow()
main.collapse()




            
            
            
            
        
        
        
        
        
        
        
        
        
        
        
        

            
        
        
    
        
        
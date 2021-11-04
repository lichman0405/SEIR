# import modules
from pylab import *
import random
import pygame
import sys
import matplotlib.pyplot as plt

# The simulation is based on Mole neighborhood
# definition:
"""
There are for stages of individuals:
1. S0 = susceptible individuals, the infected probability by neighbors p, which equals K1 * (number of directly neighboring) * 0.25 
        + K2 * (number of diagnose neighboring) * 0.25. The probability of transfer to infectious is C1. The probability of transfer to carriers is 1-C1
2. S1 = infectious individuals, who are able to infect S0. After time t1, S1 will transfer to S2, and t1 returns to 0
3. S2 = recovered individuals. They have temporary capabilities of immunity. After time T, S2 will transfer to S0, T returns to 0.
        In this simulation, we will not take permenant immunity into consideration.
4. S3 = carrier individuals. They will transfer to S1 after time t2. They can also infect S0
5. S4 = death. Nothing left.

p: The probability of being infected
K1: the parameter of direct neighborhood
K2: the parameter of diagnose neighborhood
p_aged_death: the probability of death rate for elders

C1: the probability of S0 transfer to S1
1-C1: the probability of S0 transfer to S3

t1: the period of S1 transfer to S2, which will return 0 after the transfering
T: the period of S2 transfer to S0, which will return 0 after the transfering
t2: the period of S3 transfer to S1, which will return 0 after the transfering
"""
"""
How to find out an appropriate rule of death for age and low immu-system is another issue which should be double check carefully.
In this piece of simulation, I do not find it.
Maybe in Cell class, adding another feature of age following the normal distribution is the key.
"""
# initialization the parameters
# Smallpox simulation
population = 100*100
K1 = 0.8
K2 = 0.8 
C1 = 0.5
p_death = 0.3
age_indicator = 3 # determine the age. Higher with high danger of death

t1 = 17
t_old_long = 16
T = 999999
t2 = 12

# Color setting
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GREY = (192, 192, 192)

# The cell-class
class Cell:
    stage = 0
    def __init__(self, ix, iy, stage):
        # ix and iy here means the position of the cell in the xy metrics
        self.ix = ix
        self.iy = iy
        self.stage = stage            # initialize the stage as susceptible
        self.neighbour_count = 0      # the number of cells around the cell

        self.s0_A = 0       # top bottom left right            
        self.s0_B = 0       # diagnose         
        self.t1_ = 0                  # period being infected
        self.T_ = 0                  # period of recovering
        self.t2_= 0
        self.age = int(random.random()*100)

    # count the number of infectious
    def source_count(self):
        count_0 = 0
        count_1 = 0
        x_before = self.ix - 1 if self.ix > 0 else 0
        for i in range(x_before, self.ix+1+1):
            y_before = self.iy - 1 if self.iy > 0 else 0
            for j in range(y_before, self.iy+1+1):
                if i == self.ix and j == self.iy:   # check if the cell itself
                    continue
                if self.boundary(i, j):           # check if outof classnet
                    continue
                if CellNet.cells[i][j].stage == 1 or CellNet.cells[i][j].stage == 3 :  # direct neighbour
                    # check diagnose
                    if (i==self.ix and j==self.iy-1) or (i==self.ix and j==self.iy+1) or (i==self.ix-1 and j==self.iy) or (i==self.ix+1 and j==self.iy):
                        count_0+=1
                    else:
                        count_1+=1
        self.s0_A = count_0
        self.s0_B = count_1

    # check the boundary
    def boundary(self, x, y):
        if x >= CellNet.cell_x or y >= CellNet.cell_y:
            return True
        if x < 0 or y < 0:
            return True
        return False
    
    # CA rules
    def next_step(self):
        # S0 rules
        if self.stage==0:
            probability=random.random()
            p = self.s0_A * K1/4 + self.s0_B * K2/4

            if (p>probability) and (p!=0):
                p1 = random.random()
                if p1>C1:
                    self.stage=1
                else:
                    self.stage=3
            else:
                self.stage = 0
        # S1 rules
        elif self.stage == 1:
            p2 = random.random()
            if self.t1_ >= t_old_long and self.age >= 8:
                if p2 < p_death: 
                    self.stage = 4
                else:
                    self.t1_ = self.t1_ + 1
            else:
                if self.t1_ >= t1:
                    self.stage = 2
                else:
                    self.t1_ = self.t1_ + 1
        # S2 rules
        elif self.stage == 2:
            if self.T_ >= T:
                self.stage = 0
            else:
                self.T_ = self.T_ + 1
        # S3 rules
        elif self.stage == 3:
            if self.t2_ >= t2:
                self.stage = 1  
            else:
                self.t2_ += 1
        # S4 ruls
        elif self.stage == 4:
            None


# Generate the area node net
class CellNet:
    cells = []
    cell_x = 0
    cell_y = 0
    # Initialize Net:
    def __init__(self, cx, cy):
        CellNet.cell_x = cx
        CellNet.cell_y = cy
        # starting point
        # if wanna have more start point, please generate random int
        x_start1 = random.randint(0,cx+1)
        y_start1 = random.randint(0,cy+1)
        x_start2 = random.randint(0,cx+1)
        y_start2 = random.randint(0,cy+1)
        x_start3 = random.randint(0,cx+1)
        y_start3 = random.randint(0,cy+1)
        for i in range(cx):
            cell_list = []
            for j in range(cy):
                cell = Cell(i, j, 0)            #setting all to S0
                if (i == x_start1 and j ==y_start1) or (i==x_start2 and j==y_start2) or (i==x_start3 and j==y_start3):
                    cell_list.append(Cell(i,j,1))
                else:
                    cell_list.append(cell)
            CellNet.cells.append(cell_list)

    def next_step(self):
        for cell_list in CellNet.cells:
            for item in cell_list:
                item.next_step()

    def source_count(self):
        for cell_list in CellNet.cells:
            for item in cell_list:
                item.source_count()


    def num_of_nonstage(self):
        count0 = 0 # susceptible
        count1 = 0 # infectious
        count2 = 0 # recovered
        count3 = 0 # carrier
        count4 = 0 # death
        for i in range(self.cell_x):
            for j in range(self.cell_y):
                # count all cells
                cell = self.cells[i][j].stage
                if cell == 0:
                    count0 += 1
                elif cell == 1:
                    count1 += 1
                elif cell == 2:
                    count2 += 1
                elif cell == 3:
                    count3 += 1
                elif cell == 4:
                    count4 += 1
        return count0, count1, count2, count3, count4
    
# Interface, 
class Game:
    screen = None
    count0 = 0
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    def __init__(self, width, height, cx, cy): #size of windows, the size of cell
        self.width = width
        self.height = height
        self.cx_rate = int(width / cx)
        self.cy_rate = int(height / cy)
        self.screen = pygame.display.set_mode([width, height])#
        self.cells = CellNet(cx, cy)

    def show_life(self):
        for cell_list in self.cells.cells:
            for item in cell_list:
                x = item.ix
                y = item.iy
                if item.stage == 0:
                    pygame.draw.rect(self.screen, YELLOW,
                                     [x * self.cx_rate, y * self.cy_rate, self.cx_rate, self.cy_rate])
                elif item.stage == 1:
                    pygame.draw.rect(self.screen, RED,
                                     [x * self.cx_rate, y * self.cy_rate, self.cx_rate, self.cy_rate])
                elif item.stage == 2:
                    pygame.draw.rect(self.screen, GREEN,
                                     [x * self.cx_rate, y * self.cy_rate, self.cx_rate, self.cy_rate])
                elif item.stage == 3:
                    pygame.draw.rect(self.screen, BLACK,
                                     [x * self.cx_rate, y * self.cy_rate, self.cx_rate, self.cy_rate])
                elif item.stage == 4:
                    pygame.draw.rect(self.screen, GREY, 
                                     [x * self.cx_rate, y * self.cy_rate, self.cx_rate, self.cy_rate])


if __name__ == '__main__':
    count0_ = []
    count1_ = []
    count2_ = []
    count3_ = []
    count4_ = []
    pygame.init()
    pygame.display.set_caption("SEIR Simulation")
    # the parameter of Game class:
    # the 1st and 2nd are the size of the window
    # the rest of them determine the population in simulation
    game = Game(800, 800, 100, 100)

    clock = pygame.time.Clock()
    k1 = 0
    while True:
        k1 += 1
        print(k1)

        clock.tick(10000) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        game.cells.source_count()
        count0, count1, count2,count3, count4 = game.cells.num_of_nonstage()
        count0_.append(count0)
        count1_.append(count1)
        count2_.append(count2)
        count3_.append(count3)
        count4_.append(count4)

        plt.plot(count0_, color='y', label='susceptible')
        plt.plot(count3_, color='black', label='carrier')
        plt.plot(count1_, color='r', label='infectious')
        plt.plot(count2_, color='g', label='recovered')
        plt.plot(count4_, color='grey', label = 'death')
        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Population')
        plt.pause(1e-4)
        plt.clf()

        game.show_life()
        pygame.display.flip()
        game.cells.next_step()

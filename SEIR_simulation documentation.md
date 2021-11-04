# SEIR_simulation documentation

Shibo Li

*new feature:* 

- death stage, 
- random start points
- Cellular Automata description

----

## **What is Cellular Automata**

A **cellular automaton** (pl. **cellular automata**, abbrev. **CA**) is a discrete [model of computation](https://en.wikipedia.org/wiki/Model_of_computation) studied in [automata theory](https://en.wikipedia.org/wiki/Automata_theory). Cellular automata are also called **cellular spaces**, **tessellation automata**, **homogeneous structures**, **cellular structures**, **tessellation structures**, and **iterative arrays**.[[2\]](https://en.wikipedia.org/wiki/Cellular_automaton#cite_note-reviews-2) Cellular automata have found application in various areas, including [physics](https://en.wikipedia.org/wiki/Physics), [theoretical biology](https://en.wikipedia.org/wiki/Theoretical_biology) and [microstructure](https://en.wikipedia.org/wiki/Microstructure) modeling.

A cellular automaton consists of a regular grid of *cells*, each in one of a finite number of *[states](https://en.wikipedia.org/wiki/State_(computer_science))*, such as *on* and *off* (in contrast to a [coupled map lattice](https://en.wikipedia.org/wiki/Coupled_map_lattice)). The grid can be in any finite number of dimensions. For each cell, a set of cells called its *neighborhood* is defined relative to the specified cell. An initial state (time *t* = 0) is selected by assigning a state for each cell. A new *generation* is created (advancing *t* by 1), according to some fixed *rule* (generally, a mathematical function)[[3\]](https://en.wikipedia.org/wiki/Cellular_automaton#cite_note-3) that determines the new state of each cell in terms of the current state of the cell and the states of the cells in its neighborhood. Typically, the rule for updating the state of cells is the same for each cell and does not change over time, and is applied to the whole grid simultaneously,[[4\]](https://en.wikipedia.org/wiki/Cellular_automaton#cite_note-4) though exceptions are known, such as the [stochastic cellular automaton](https://en.wikipedia.org/wiki/Stochastic_cellular_automaton) and [asynchronous cellular automaton](https://en.wikipedia.org/wiki/Asynchronous_cellular_automaton).

The concept was originally discovered in the 1940s by [Stanislaw Ulam](https://en.wikipedia.org/wiki/Stanislaw_Ulam) and [John von Neumann](https://en.wikipedia.org/wiki/John_von_Neumann) while they were contemporaries at [Los Alamos National Laboratory](https://en.wikipedia.org/wiki/Los_Alamos_National_Laboratory). While studied by some throughout the 1950s and 1960s, it was not until the 1970s and [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway's_Game_of_Life), a two-dimensional cellular automaton, that interest in the subject expanded beyond academia. In the 1980s, [Stephen Wolfram](https://en.wikipedia.org/wiki/Stephen_Wolfram) engaged in a systematic study of one-dimensional cellular automata, or what he calls [elementary cellular automata](https://en.wikipedia.org/wiki/Elementary_cellular_automaton); his research assistant [Matthew Cook](https://en.wikipedia.org/wiki/Matthew_Cook) showed that [one of these rules](https://en.wikipedia.org/wiki/Rule_110) is [Turing-complete](https://en.wikipedia.org/wiki/Turing-complete).

The primary classifications of cellular automata, as outlined by Wolfram, are numbered one to four. They are, in order, automata in which patterns generally stabilize into [homogeneity](https://en.wikipedia.org/wiki/Homogeneity), automata in which patterns evolve into mostly stable or oscillating structures, automata in which patterns evolve in a seemingly chaotic fashion, and automata in which patterns become extremely complex and may last for a long time, with stable local structures. This last class is thought to be [computationally universal](https://en.wikipedia.org/wiki/Computationally_universal), or capable of simulating a [Turing machine](https://en.wikipedia.org/wiki/Turing_machine). Special types of cellular automata are *reversible*, where only a single configuration leads directly to a subsequent one, and *totalistic*, in which the future value of individual cells only depends on the total value of a group of neighboring cells. Cellular automata can simulate a variety of real-world systems, including biological and chemical ones.

Check the link to find out more.

https://en.wikipedia.org/wiki/Cellular_automaton

----

- CA Rules

  1. There are for stages of individuals:

     1. S0 = susceptible individuals, the infected probability by neighbors p, which equals K1 * (number of directly neighboring) * 0.25 

     ​        \+ K2 * (number of diagnose neighboring) * 0.25. The probability of transfer to infectious is C1. The probability of transfer to carriers is 1-C1

     2. S1 = infectious individuals, who are able to infect S0. After time t1, S1 will transfer to S2, and t1 returns to 0

     3. S2 = recovered individuals. They have temporary capabilities of immunity. After time T, S2 will transfer to S0, T returns to 0.

     ​        In this simulation, we will not take permenant immunity into consideration.

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

- Game class parameters:

  - Game(A, B, a, b)

  - A, B determine the size of the view

  - a*b determine the population

    ```python
    game = Game(800, 800, 400, 400)
    # here means the window of simulation is 800*800
    # the population involved in the simulation is 400*400
    ```

    

Improving:

- The function next_step():

  - If to add new stage of Sx, please add elif here.

  - *line from 92 to 123*

  - Users can modify the part of code to setting rules

    ```python
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
    ```
    
    

- The *\_init\_* function in Cell class:

  - If to add new features of a single cell, please add self.xxx here

  - *line 51 to 60*

    ```python
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
            self.t2_= 0                 # period of carrier to infectious
            self.age = int(random.random()*100)
    
    ```
    
    

- The *\_init\_* function in CellNet class:

  - Line 139 determines the starting points of spreading

  - The vanila states is starting from the center

    ```python
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
    ```
    
    

# CA Simulation Parameters

1. Simulation one

   1. Parameters:

      1. *# initialization the parameters*

         population = 100*100

         K1 = 0.8

         K2 = 0.4 

         C1 = 0.4

         p_death = 0.02

         age_indicator = 80 *# determine the age. Higher with high danger of death*

         

         t1 = 15 

         t_old_long = 10

         T = 28

         t2 = 4.7 

2. Simulation two

   1. Parameters:

      1. Diphtheria simulation

      2. population = 100*100

         K1 = 0.6

         K2 = 0.4 

         C1 = 0.4

         p_death = 0.3

         age_indicator = 8 *# determine the age. Higher with high danger of death*

         

         t1 = 28

         t_old_long = 20

         T = 180

         t2 = 3 

3. Simulation two

   1. Parameters:

      1. *# initialization the parameters*

         *# Smallpox simulation*

         population = 100*100

         K1 = 0.8

         K2 = 0.8 

         C1 = 0.5

         p_death = 0.3

         age_indicator = 3 *# determine the age. Higher with high danger of death*

         

         t1 = 17

         t_old_long = 16

         T = 999999

         t2 = 12

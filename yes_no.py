import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
from matplotlib.colors import ListedColormap
from random import randint

'''
One of the applications of a two-dimensional non-deterministic cellular automaton is the simulation of changes in the "state of views or beliefs" of people under 
the influence of their "neighbors". For the purposes of the simulation, members of society live in the nodes of a two-dimensional geometric network and have radical 
(such as yes, no or for and against) views, depicted in the colors: yellow and purple (eight-neighborhood).
'''

# Board size
height = 250
width = 250

# Initialize the board as a numpy array (0 - for, 1 - against)
board = np.random.choice([0, 1], size=(height, width), p=[0.5, 0.5])

# Variable to store animation state (pause/continue)
animation_active = True

# Function to perform one step of the simulation
def simulation_step(board):
    new_board = np.copy(board)
    for i in range(height):
        for j in range(width):
            neighbors = board[max(0, i-1):min(height, i+2),
                             max(0, j-1):min(width, j+2)]
            sum_of_neighbors = np.sum(neighbors) - board[i, j]

            if sum_of_neighbors == 0:
                sum_of_anti_neighbors = 8

            elif sum_of_neighbors == 1:
                sum_of_anti_neighbors = 7

            elif sum_of_neighbors == 2:
                sum_of_anti_neighbors = 6

            elif sum_of_neighbors == 3:
                sum_of_anti_neighbors = 5

            elif sum_of_neighbors == 4:
                sum_of_anti_neighbors = 4

            elif sum_of_neighbors == 5:
                sum_of_anti_neighbors = 3

            elif sum_of_neighbors == 6:
                sum_of_anti_neighbors = 2

            elif sum_of_neighbors == 7:
                sum_of_anti_neighbors = 1

            elif sum_of_neighbors == 8:
                sum_of_anti_neighbors = 0

            if board[i, j] == 1:

                if sum_of_anti_neighbors == 1:
                    b = randint(1, 100)
                    if b <= 4:
                        new_board[i, j] = 0

                elif sum_of_anti_neighbors == 2:
                    b = randint(1, 100)
                    if b <= 20:
                        new_board[i, j] = 0

                elif sum_of_anti_neighbors == 3:
                    b = randint(1, 100)
                    if b <= 50:
                        new_board[i, j] = 0

                elif sum_of_anti_neighbors == 4:
                    b = randint(1, 100)
                    if b <= 80:
                        new_board[i, j] = 0

                elif sum_of_anti_neighbors == 5:
                    b = randint(1, 100)
                    if b <= 90:
                        new_board[i, j] = 0

                elif sum_of_anti_neighbors == 6:
                    b = randint(1, 100)
                    if b <= 95:
                        new_board[i, j] = 0

                elif sum_of_anti_neighbors == 7:
                    b = randint(1, 100)
                    if b <= 98:
                        new_board[i, j] = 0

                elif sum_of_anti_neighbors == 8:
                    new_board[i, j] = 0

            elif board[i, j] == 0:

                if sum_of_neighbors == 1:
                    b = randint(1, 100)
                    if b <= 4:
                        new_board[i, j] = 1

                elif sum_of_neighbors == 2:
                    b = randint(1, 100)
                    if b <= 20:
                        new_board[i, j] = 1

                elif sum_of_neighbors == 3:
                    b = randint(1, 100)
                    if b <= 50:
                        new_board[i, j] = 1

                elif sum_of_neighbors == 4:
                    b = randint(1, 100)
                    if b <= 80:
                        new_board[i, j] = 1

                elif sum_of_neighbors == 5:
                    b = randint(1, 100)
                    if b <= 90:
                        new_board[i, j] = 1

                elif sum_of_neighbors == 6:
                    b = randint(1, 100)
                    if b <= 95:
                        new_board[i, j] = 1

                elif sum_of_neighbors == 7:
                    b = randint(1, 100)
                    if b <= 98:
                        new_board[i, j] = 1

                elif sum_of_neighbors == 8:
                    new_board[i, j] = 1

    return new_board

# Function to handle the "Pause" button
def pause(event):
    global animation_active
    animation_active = False

# Function to handle the "Continue" button
def continue_simulation(event):
    global animation_active
    animation_active = True

# Define a custom RGB color map (using purple and yellow colors)
colors = [(0.4, 0, 1), (1, 1, 0)]
cmap = ListedColormap(colors)

# Initialize the animation
fig, ax = plt.subplots()

matrix = ax.matshow(board, cmap=cmap)  

# Create "Pause" and "Continue" buttons
ax_pause = plt.axes([0.7, 0.01, 0.1, 0.04])
ax_continue = plt.axes([0.81, 0.01, 0.1, 0.04])
button_pause = Button(ax_pause, 'Pause')
button_continue = Button(ax_continue, 'Continue')

# Function to update the board in the animation
def update(frame):
    global board, animation_active
    if animation_active:
        board = simulation_step(board)
        matrix.set_data(board)
    return [matrix]

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=100, interval=200, blit=True)

# Assign functions to the buttons
button_pause.on_clicked(pause)
button_continue.on_clicked(continue_simulation)

plt.show()
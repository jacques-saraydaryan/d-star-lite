import heapq
import pygame

from graph import Node, Graph
from grid import GridWorld
from utils import *
from d_star_lite import *

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY1 = (145, 145, 102)
GRAY2 = (77, 77, 51)
BLUE = (0, 0, 80)

colors = {
    0: WHITE,
    1: GREEN,
    -1: GRAY1,
    -2: GRAY2
}

# This sets the WIDTH and HEIGHT of each grid location

# This sets the margin between each cell
MARGIN = 5


GRID_SIZE = 10
# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(GRID_SIZE):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(GRID_SIZE):
        grid[row].append(0)  # Append a cell

# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)
grid[1][5] = 1

# Initialize pygame
pygame.init()

X_DIM = 12
Y_DIM = 12
#VIEWING_RANGE = 3


# Set the HEIGHT and WIDTH of the screen


# Set title of screen
pygame.display.set_caption("D* Lite Path Planning")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

d_s_obj=d_star_obj()

if __name__ == "__main__":
    graph = GridWorld(X_DIM, Y_DIM)
    s_start = 'x3y1'
    s_goal = 'x0y6'
    graph.goal = s_goal
    goal_coords = stateNameToCoords(s_goal)
    graph.goal_coords = goal_coords
    graph.setStart(s_start)
    graph.setGoal(s_goal)

    for i in range(len(graph.cells)):
            row = graph.cells[i]
            for j in range(len(row)):
                graph.cells[i][j]=-2

    
    #graph.cells[2][2]=-2
    #graph.cells[3][0]=-2
    #graph.cells[3][2]=-2
    #graph.cells[4][0]=-2
    #graph.cells[4][2]=-2
    #graph.cells[5][0]=-2
    #graph.cells[5][2]=-2


    graph.cells[1][0]=0
    graph.cells[1][1]=0
    graph.cells[1][2]=0
    graph.cells[1][3]=0

    graph.cells[6][0]=0
    graph.cells[6][1]=0
    graph.cells[6][2]=0
    graph.cells[6][3]=0

    graph.cells[5][1]=0
    graph.cells[4][1]=0
    graph.cells[3][1]=0
    graph.cells[2][1]=0

    graph.cells[5][3]=0
    graph.cells[4][3]=0
    graph.cells[3][3]=0
    graph.cells[2][3]=0

    
    #Remove obstacle from graphn nodes children and parents list
    for node in graph.graph:
        coords = stateNameToCoords(node)
        if graph.cells[coords[1]][coords[0]] == -2:
             for graph_node in graph.graph:
                if node in graph.graph[graph_node].children:
                    del graph.graph[graph_node].children[node]
                if node in graph.graph[graph_node].parents:
                    del graph.graph[graph_node].parents[node]

    k_m = 0
    s_last = s_start
    queue = []
    s_current = s_start
    pos_coords = stateNameToCoords(s_current)
    graph.pos_coords = pos_coords
    graph, queue, k_m = d_s_obj.initDStarLite(graph, queue, s_start, s_goal, k_m)




    basicfont = pygame.font.SysFont('Comic Sans MS', 36)
    #global STEP_ALGO 
    #lock_A.acquire()
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                d_s_obj.step_is_on=True
            elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                d_s_obj.step_is_on=False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # print('space bar! call next action')
                s_new, k_m = d_s_obj.moveAndRescan(
                    graph, queue, s_current, VIEWING_RANGE, k_m)
                if s_new == 'goal':
                    print('Goal Reached!')
                    done = True
                else:
                    # print('setting s_current to ', s_new)
                    s_current = s_new
                    pos_coords = stateNameToCoords(s_current)
                    graph.pos_coords = pos_coords
                    # print('got pos coords: ', pos_coords)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                # Set that location to one
                if column >0 and  column <= GRID_SIZE and row >0 and  row <= GRID_SIZE:
                    if(graph.cells[row][column] in [0,2,3]):
                        graph.cells[row][column] = -1

        # Set the screen background
        render_all(graph)
        '''
        screen.fill(BLACK)

        # Draw the grid
        for row in range(Y_DIM):
            for column in range(X_DIM):
                color = WHITE
                # if grid[row][column] == 1:
                #     color = GREEN
                pygame.draw.rect(screen, colors[graph.cells[row][column]],
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
                node_name = 'x' + str(column) + 'y' + str(row)
                if(graph.graph[node_name].g != float('inf')):
                    # text = basicfont.render(
                    # str(graph.graph[node_name].g), True, (0, 0, 200), (255,
                    # 255, 255))
                    text = basicfont.render(
                        str(graph.graph[node_name].g), True, (0, 0, 200))
                    textrect = text.get_rect()
                    textrect.centerx = int(
                        column * (WIDTH + MARGIN) + WIDTH / 2) + MARGIN
                    textrect.centery = int(
                        row * (HEIGHT + MARGIN) + HEIGHT / 2) + MARGIN
                    screen.blit(text, textrect)

        # fill in goal cell with GREEN
        pygame.draw.rect(screen, GREEN, [(MARGIN + WIDTH) * goal_coords[0] + MARGIN,
                                         (MARGIN + HEIGHT) * goal_coords[1] + MARGIN, WIDTH, HEIGHT])
        # print('drawing robot pos_coords: ', pos_coords)
        # draw moving robot, based on pos_coords
        robot_center = [int(pos_coords[0] * (WIDTH + MARGIN) + WIDTH / 2) +
                        MARGIN, int(pos_coords[1] * (HEIGHT + MARGIN) + HEIGHT / 2) + MARGIN]
        pygame.draw.circle(screen, RED, robot_center, int(WIDTH / 2) - 2)

        # draw robot viewing range
        pygame.draw.rect(
            screen, BLUE, [robot_center[0] - VIEWING_RANGE * (WIDTH + MARGIN), robot_center[1] - VIEWING_RANGE * (HEIGHT + MARGIN), 2 * VIEWING_RANGE * (WIDTH + MARGIN), 2 * VIEWING_RANGE * (HEIGHT + MARGIN)], 2)

        # Limit to 60 frames per second
        clock.tick(20)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    '''
    pygame.quit()

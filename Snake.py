import pygame
import random
import threading
import sys


# Initializes the screen and all variables
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Sets the screen to full screen
screen.fill((200, 200, 200))
screen_font = pygame.font.SysFont("arial", 22)
done = False
directions = ["UP", "DOWN", "LEFT", "RIGHT"]
start = False
ai_run = False
game_width = 40
game_height = 40
update_time = 0.065
ai_bool = True
iteration = 1
max_length = 0
block_colours = [(255, 255, 255), (0, 0, 0), (255, 255, 0), (200, 200, 200)]
length = 2


# Displays the time in the upper left corner
def display_time(hour, minute, second):
    try:
        screen.fill((200, 200, 200), (0, 0, 100, 30))
        if int(second) < 59:
            second = str(int(second)+1)
            if len(second) == 1:
                second = "0" + second
        else:
            if int(minute) < 59:
                minute = str(int(minute)+1)
                if len(minute) == 1:
                    minute = "0" + minute
            else:
                if int(hour) < 59:
                    hour = str(int(hour)+1)
                    if len(hour) == 1:
                        hour = "0" + hour
                    minute = "00"
            second = "00"
        time = screen_font.render(f"{hour}:{minute}:{second}", True, (0, 0, 0))
        screen.blit(time, (0, 0))
        threading.Timer(1, display_time, args=[hour, minute, second]).start()

    except pygame.error:
        print("\nEnd of Program")


# Displays the current length in the upper right corner
def display_value():
    global length
    screen.fill((200, 200, 200), (screen.get_width()-175, 0, screen.get_width(), 30))
    iteration_text = screen_font.render("Current Length: " + str(length), True, (0, 0, 0))
    screen.blit(iteration_text, (screen.get_width()-175, 0))


# Displays the max score reached in the bottom left corner
def max_score(snek_length):
    global max_length
    if snek_length > max_length:
        max_length = snek_length

    screen.fill((200, 200, 200), (0, screen.get_height()-30, 150, screen.get_height()))
    max_length_text = screen_font.render(f"Max Length: {max_length}", True, (0, 0, 0))
    screen.blit(max_length_text, (0, screen.get_height()-30))


# Returns a random position within the map that isn't already occupied by the snake
def randPos(snek_pos):
    rand_pos = [random.randint(1, 38), random.randint(1, 38)]
    while rand_pos in snek_pos:
        rand_pos = [random.randint(1, 38), random.randint(1, 38)]
    return rand_pos


# It's the map it's the map it's the map it's the map it's the maaaaaaap
class Map:
    def __init__(self, snek, goal):
        self.map = []
        self.reset()
        self.snek = snek
        self.goal = goal

    # Resets the map to its initial state
    def reset(self):
        self.map = []
        temp = []
        for i in range(game_height):
            for j in range(game_width):
                if i == 0 or i == game_width-1 or j == 0 or j == game_height-1:
                    temp.append(3)
                else:
                    temp.append(0)
            self.map.append(temp)
            temp = []

    # Updates the map to contain both the snake and the goal
    def update(self):
        map.snek = snake.positions

        # If the snake has reached a goal then run the function again to ensure that it doesn't look janky
        if map.snek[0] == map.goal:
            snake.length += 2
            map.goal = randPos(map.snek)
            global length
            length += 2
            display_value()
            return 1

        # Places the snake and goal within the map
        for i in self.snek:
            exec(f"self.map[{i[0]}][{i[1]}] = 1")
        exec(f"self.map[{self.goal[0]}][{self.goal[1]}] = 2")

        # Determines the screen size and how large the individual blocks need to be
        surface = pygame.display.get_surface()
        surface_width = surface.get_width()
        surface_height = surface.get_height()
        block_x = 0
        block_y = 0
        if surface_height < surface_width:
            block_width = (surface_width * 0.55) / 40
            block_height = block_width
        else:
            block_height = (surface_height * 0.55) / 40
            block_width = block_height

        # Draws the map onto the screen
        global block_colours
        for i in range(0, game_width):
            for j in range(0, game_height):
                pygame.draw.rect(screen, block_colours[map.map[i][j]], (
                    surface_width * 0.2 + (block_width * i), surface_height * 0.01 + (block_height * j), block_width,
                    block_height), 0)

                block_x += 1
                block_y += 1
        return 0


# Snek will eat
class Snek:
    def __init__(self, direction, ai=False):
        self.positions = [[20, 20]]
        self.direction = direction
        self.length = 2
        self.ai = ai

    # Updates the position of the snake
    def update(self):
        self.t = threading.Timer(update_time, self.update)
        self.t.start()

        # Extends the snake if needed
        if len(self.positions) < self.length:
            self.positions.append([])

        # Moves the snake forward
        i = len(self.positions)-1
        while i >= 1:
            self.positions[i] = list(self.positions[i-1])
            i -= 1

        # Moves the head of the snake based on the direction entered by the user
        if self.direction == "LEFT":
            self.positions[0][0] -= 1
        elif self.direction == "RIGHT":
            self.positions[0][0] += 1
        elif self.direction == "UP":
            self.positions[0][1] -= 1
        elif self.direction == "DOWN":
            self.positions[0][1] += 1

        global map

        # Checks whether the snake has died or not
        if self.positions[0][0] in (0, 39) or self.positions[0][1] in (0, 39) or self.positions[0] in self.positions[1:]:
            global length
            length += 2
            display_value()
            max_score(self.length)
            self.length = 2
            self.positions = [[20, 20]]
            self.direction = randElement(directions)
            map.goal = randPos(map.snek)

        # Resets and updates the map to account for the new snake position
        map.reset()
        m = map.update()
        if m:
            map.update()


# Returns a random element within an array (I'm going to be honest I have no idea why the fuck I needed this)
def randElement(arr):
    return arr[random.randint(0, len(arr)-1)]


display_time("00", "00", "00")

# Runs the main portion of the code
while not done:

    # Initializes the snake and map
    if not start:
        snake = Snek(randElement(directions), ai=ai_bool)
        map = Map(snake.positions, randPos(snake.positions))
        snake.update()
        display_value()
        start = True

    # Determines whether the user has entered a key that corresponds to a direction or wants to close the screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and snake.direction != "DOWN":
                snake.direction = "UP"
            elif event.key == pygame.K_s and snake.direction != "UP":
                snake.direction = "DOWN"
            elif event.key == pygame.K_a and snake.direction != "RIGHT":
                snake.direction = "LEFT"
            elif event.key == pygame.K_d and snake.direction != "LEFT":
                snake.direction = "RIGHT"

    # Updates the screen
    pygame.display.flip()


# Closes the window and exits the game once the program ends
snake.t.cancel()
pygame.quit()
sys.exit()

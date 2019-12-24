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
game_width = 40
game_height = 40
update_time = 0.065
ai_bool = True
iteration = 1
max_length = 0
start_length = 3
block_colours = [(255, 255, 255), (0, 0, 0), (255, 255, 0), (200, 200, 200), (0, 0, 210)]
length = 3
last_right = False


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
    global snake_one
    global snake_two
    screen.fill((200, 200, 200), (screen.get_width()-250, 0, screen.get_width(), 90))
    iteration_text_one = screen_font.render(f"Your (Black) Length: {snake_one.length}", True, (0, 0, 0))
    iteration_text_two = screen_font.render(f"H.A.N.S. (Blue) Length: {snake_two.length}", True, (0, 0, 0))
    screen.blit(iteration_text_one, (screen.get_width() - 226, 0))
    screen.blit(iteration_text_two, (screen.get_width() - 250, 30))


# Displays the max score reached in the bottom left corner
def max_score(snek_length):
    global max_length
    if snek_length > max_length:
        max_length = snek_length

    screen.fill((200, 200, 200), (0, screen.get_height()-30, 150, screen.get_height()))
    max_length_text = screen_font.render(f"Max Length: {max_length}", True, (0, 0, 0))
    screen.blit(max_length_text, (0, screen.get_height()-30))


# Returns a random position within the map that isn't already occupied by the snake
def randPos(first=False):
    global snake_one
    global snake_two
    rand_pos = [random.randint(1, 38), random.randint(1, 38)]
    if not first:
        while rand_pos in snake_one.positions or rand_pos in snake_two.positions:
            rand_pos = [random.randint(1, 38), random.randint(1, 38)]
    return rand_pos


# Holding the spot as one of the worst functions I've ever created, this function returns a specific direction for the
# snake to follow to allow to it to follow a specific path I've created to win
def returnDirection(snek_pos):
    x = snek_pos[0][0]
    y = snek_pos[0][1]
    if 1 < x < game_width-2:
        if y == game_height-3 or y == 2:
            if y == game_height-3:
                return "RIGHT" if x % 2 == 1 else "UP"
            else:
                return "RIGHT" if x % 2 == 0 else "DOWN"
        elif y == 1:
            return "LEFT"
        else:
            return "UP" if x % 2 == 0 else "DOWN"
    elif x == game_width - 2:
        return "UP" if y != 1 else "LEFT"
    elif x == 1:
        return "DOWN" if y != game_height-3 else "RIGHT"


# Evaluates whether or not the path to the goal is safe for the snake to take
def checkPath(snek_pos, goal_pos):
    increment_x = 1 if goal_pos[0] < snek_pos[0][0] else -1
    increment_y = 1 if goal_pos[1] < snek_pos[0][1] else -1
    global map
    for i in range(goal_pos[0], snek_pos[0][0], increment_x):
        if map.map[i][snek_pos[0][1]] in (1, 3, 4):
            return False
    for i in range(goal_pos[1], snek_pos[0][1], increment_y):
        if map.map[goal_pos[0]][i] in (1, 3, 4):
            return False
    return True


def checkDirection(snek_pos, direction):
    global map
    x = snek_pos[0][0]
    y = snek_pos[0][1]
    if direction == "LEFT":
        if map.map[x-1][y] in (1, 3, 4):
            return False
    elif direction == "RIGHT":
        if map.map[x+1][y] in (1, 3, 4):
            return False
    elif direction == "UP":
        if map.map[x][y-1] in (1, 3, 4):
            return False
    elif direction == "DOWN":
        if map.map[x][y+1] in (1, 3, 4):
            return False
    return True


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
        display_value()
        global snake_positions
        global snake_one
        global snake_two
        map.snek = snake_positions

        # If the snake has reached a goal then run the function again to ensure that it doesn't look janky
        if snake_one.positions[0] == map.goal:
            snake_one.length += 2
            map.goal = randPos()
            return 1
        if snake_two.positions[0] == map.goal:
            snake_two.length += 2
            map.goal = randPos()
            return 1

        # Places the snake and goal within the map
        for i in snake_one.positions:
            exec(f"self.map[{i[0]}][{i[1]}] = 1")
        for i in snake_two.positions:
            exec(f"self.map[{i[0]}][{i[1]}] = 4")
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
    def __init__(self, start, direction, ai=False):
        self.start, self.positions = start, start
        self.direction = direction
        global start_length
        self.length = start_length
        self.ai = ai

    # Updates the position of the snake
    def update(self):
        global map
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

        global last_right

        if self.ai:
            if not checkPath(self.positions, map.goal):
                newDirection = returnDirection(self.positions)
                if checkDirection(self.positions, newDirection):
                    self.direction = newDirection
                else:
                    x = self.positions[0][0]
                    y = self.positions[0][1]
                    if not last_right:
                        if map.map[x-1][y] in (0, 2):
                            self.direction = "LEFT"
                        elif map.map[x+1][y] in (0, 2):
                            self.direction = "RIGHT"
                        elif map.map[x][y-1] in (0, 2):
                            self.direction = "UP"
                        elif map.map[x][y+1] in (0, 2):
                            self.direction = "DOWN"
                    else:
                        if map.map[x+1][y] in (0, 2):
                            self.direction = "RIGHT"
                        elif map.map[x-1][y] in (0, 2):
                            self.direction = "LEFT"
                        elif map.map[x][y-1] in (0, 2):
                            self.direction = "UP"
                        elif map.map[x][y+1] in (0, 2):
                            self.direction = "DOWN"
            else:
                if self.positions[0][0] != map.goal[0]:
                    self.direction = "RIGHT" if self.positions[0][0] < map.goal[0] else "LEFT"
                elif self.positions[0][1] != map.goal[1]:
                    self.direction = "DOWN" if self.positions[0][1] < map.goal[1] else "UP"

        # Moves the head of the snake based on the direction entered by the user
        if self.direction == "LEFT":
            self.positions[0][0] -= 1
            last_right = False
        elif self.direction == "RIGHT":
            self.positions[0][0] += 1
            last_right = True
        elif self.direction == "UP":
            self.positions[0][1] -= 1
        elif self.direction == "DOWN":
            self.positions[0][1] += 1

        # Checks whether the snake has died or not
        if self.positions[0][0] in (0, 39) or self.positions[0][1] in (0, 39) or map.map[self.positions[0][0]][self.positions[0][1]] in (1, 4):
            global start_length
            self.length = start_length
            self.positions = [randPos()]
            self.direction = randElement(directions)

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
        snake_one = Snek([[10, 10]], randElement(directions), ai=False)
        snake_two = Snek([[30, 30]], randElement(directions), ai=True)
        snake_positions = [snake_one.positions, snake_two.positions]
        map = Map(snake_positions, randPos(True))
        snake_one.update()
        snake_two.update()
        display_value()
        start = True

    # Determines whether the user has entered a key that corresponds to a direction or wants to close the screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and snake_one.direction != "DOWN":
                snake_one.direction = "UP"
            elif event.key == pygame.K_s and snake_one.direction != "UP":
                snake_one.direction = "DOWN"
            elif event.key == pygame.K_a and snake_one.direction != "RIGHT":
                snake_one.direction = "LEFT"
            elif event.key == pygame.K_d and snake_one.direction != "LEFT":
                snake_one.direction = "RIGHT"

    # Updates the screen
    pygame.display.flip()


# Closes the window and exits the game once the program ends
snake_one.t.cancel()
snake_two.t.cancel()
pygame.quit()
sys.exit()

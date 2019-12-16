import pygame
import os
import math
import random

"""
CLASSES AND FUNCTIONS
"""

class player(pygame.sprite.Sprite):  # player class
    def __init__(self):  # initialisation function
        pygame.sprite.Sprite.__init__(self)  # calls to the init class
        self.move_x = 0  # defines move_x
        self.move_y = 0  # defines move_y
        self.frame = 0  # defines frame variable
        self.images = []  # puts player sprites inside of a list

        for i in range(1, 17):  # loading images loop
            character = pygame.image.load(
                os.path.join("images", "player" + str(i) + ".png")).convert_alpha()  # convert alpha for transparancy
            self.images.append(
                pygame.transform.scale(character, (player_x, player_y)))  # scales image size to character
            self.image = self.images[0]        # sets variable to first in images list
            self.rect = self.image.get_rect()  # rectangle for hitbox

        self.jumping = 0  # jumping defined

    def control(self, x, y):  # movement control function
        self.move_x += x  # adds to the x-coordinate
        self.move_y += y  # adds to the y-coordinate

    def update(self):  # this is called by mainloop to update player
        self.rect.x = int(self.rect.x + self.move_x)  # the hit box rectangle moves with the player x
        self.rect.y = int(self.rect.y + self.move_y)  # the hit box rectangle moves with the player x

        if self.move_x < 0:  # moving left
            self.frame += 1  # adds frames

            if self.frame > 7 * player_animation_cycles:  # if all frames has been looped
                self.frame = 0  # reset frames

            self.image = self.images[(
                                                 self.frame // player_animation_cycles) + 8]  # finds the images, adds 8 for the mirrored ones, when moving left

        if self.move_x > 0:  # moving right
            self.frame += 1  # adds frames

            if self.frame > 7 * player_animation_cycles:  # if all frames has been looped
                self.frame = 0  # restarts frames

            self.image = self.images[
                self.frame // player_animation_cycles]  # gets the image for each frame when moving right

        """if self.move_x == 0:     # if player is standing still
            self.image = self.images[0]     # display still image"""

        if self.rect.x > window_x - player_x:  # if the player is at the boundary of the left side
            self.rect.x = window_x - player_x  # set his position to the boundary of the left side

        if self.rect.x < 0 - player_x:  # if the player is right outside of the map on the right side
            self.rect.x = 0 - player_x  # set the player position to right outside the map on the right side

    def gravity(self):
        self.move_y += acceleration  # how fast player falls

        if self.move_y > 0:  # if moving downwards in the y-direction

            if self.rect.colliderect(ground):  # if player collides with the ground rectangle
                self.move_y = 0  # stops moving in the y-direction
                self.rect.y = ground_y + 1 - player_y  # sets position to 1 pixel inside the ground rectangle
                self.jumping = 0  # reset jump

    def jump(self):
        global test

        if self.jumping == 0:
            self.move_y -= jump_speed  # a big jump
            self.jumping = 1  # change jumping status

        elif self.jumping == 1 and self.move_y <= 0:
            self.move_y -= jump_speed / 2  # a small one
            self.jumping = 2  # change jumping status

            if test == 1:
                self.rect.x += 40
                test = 0

    """def crouch(self):

    def jetpack(self):
        self.move_y -= 1"""

class enemy(pygame.sprite.Sprite):
    global enemy_sprites        # global list for images for each enemy

    def __init__(self, x, y):       # function for initialising
        pygame.sprite.Sprite.__init__(self)     # calls to the init super class
        self.frame = 0      # defining frame
        self.direction_x = 0        # movement x_direction
        self.direction_y = 0        # movement y_direction
        self.images = enemy_sprites     # puts enemy sprites list as images
        self.image = enemy_sprites[0]       # sets variable to first in images list
        self.rect = self.image.get_rect()       # hitbox
        self.rect.x = x     # rectangle x
        self.rect.y = y     # rectangle y

    def move(self, player):     # enemy movement function, called by mainloop to player
        sound_moo.play()        # play loaded moo sound
        self.direction_x = player.rect.x - self.rect.x  # find direction vector (direction_x, direction_y) between enemy and player
        self.direction_y = (player.rect.y + (player_y - enemy_y)) - self.rect.y  # adding the difference between the player height and the enemy height so it looks like they are proportional to each other, othervise the enemy would have been trying to get to the head of the player instead of the legs
        distance = math.hypot(self.direction_x, self.direction_y)  # use math to calculate the hypotenuse between the direction_x and direction_y (the cathetuses)

        if distance > 10:  # by having the distance to be higher than 10, preventing glitching when teh enemy is on the player
            self.direction_x = self.direction_x / distance  # normalise x
            self.direction_y = self.direction_y / distance  # normalise y
            self.rect.x += int(self.direction_x * enemy_steps)  # move along this normalised vector towards the player at current speed along the x-axis
            self.rect.y += int(self.direction_y * enemy_steps)  # along the y-axis

        self.direction_y += acceleration  # how fast enemy falls

        if self.direction_y > 0:        # if enemy is falling (y-coordinate bigger than 0)
            if self.rect.colliderect(ground):       # if colliding with ground
                self.direction_y = 0        # y-coordinate movement equals to 0

    def update(self):       # called by mainloop, updates enemy animation
        self.rect.x = int(self.rect.x + self.direction_x)       # the hit box rectangle moves with the player x
        self.rect.y = int(self.rect.y + self.direction_y)       # the hit box rectangle moves with the player y

        if self.direction_x < 0:  # moving left
            self.frame += 1     # adds frames

            if self.frame > 7 * enemy_animation_cycles:     # if all frames has been looped
                self.frame = 0      # reset frames

            self.image = self.images[(self.frame // enemy_animation_cycles) + 8]      # finds the images, adds 8 for the mirrored ones, when moving left

        if self.direction_x > 0:  # moving right
            self.frame += 1     # adds frames

            if self.frame > 7 * enemy_animation_cycles:     # if all frames has been looped
                self.frame = 0      # reset frames

            self.image = self.images[self.frame // enemy_animation_cycles]      # gets the image for each frame when moving right

        """if self.rect.colliderect(player.rect):      # if enemy rectangle collides with player
            enemy_death.play()      # play loaded enemy death sound"""

class platform(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.position = 0
        self.y = 0
        self.x = 0
        self.type = 0
        self.image = 0

    def load_type(self):
        if level == 1:
            self.type = random.randint(0, len(platformSpritesSky))
            self.image = platformSpritesSky[self.type - 1]

        if level == 2:
            self.type = random.randint(0, len(platformSpritesSky))
            self.image = platformSpritesDesert[self.type - 1]

        return self.image

    def random_position(self):
        self.position = random.randint(1, 2)
        platform_height1 = ground_y - 2 * meter
        platform_height2 = ground_y - 3 * meter
        platform_height3 = ground_y - 4 * meter
        platform_height4 = ground_y - 5 * meter


        if self.position == 0:
            self.y = platform_height1

        elif self.position == 1:
            self.y = platform_height2

        elif self.position == 2:
            self.y = platform_height3

        elif self.position == 3:
            self.y = platform_height4

        return self.y

class projectile(object):  # projectile class

    def __init__(self, x, y, radius, colour, facing):  # initialising function
        self.x = x  # defining x
        self.y = y  # defining y
        self.rect = pygame.rect.Rect(x, y, 20, 20)  # rectangle hitbox
        self.radius = radius  # defining radius
        self.colour = colour  # defining colour
        self.facing = facing  # which direction facing
        self.velocity = bullet_speed * facing  # speed is the facing direction times variable

    def draw(self, window):  # draw function
        pygame.draw.circle(window, self.colour, (self.x, self.y), self.radius)  # circle

    def move(self):  # called by main loop
        self.x += self.velocity  # movement per frame
        self.rect.x = self.x  # rectangle x

def instantiate_platforms():  # this function creates platforms at the start of the game
    global platformList

    for variable in range(1, 15):
        platformList.append(platform())

    previousPlatformPosition = random.randint(500, 600)

    for platformObject in platformList:
        platformObject.random_position()  # assigns random y position
        platformObject.x = random.randint(100, 200) + previousPlatformPosition  # assings a random x position
        previousPlatformPosition += random.randint(200, 500)  # makes sure the next platform's x position isn't exactly the same as the old one

def bullet_collision():  # this function allows you to check for bullet collisions
    global bullets

    for bullet in bullets:
        for enemyObject in enemies:
            if enemyObject in enemies:
                if bullet.rect.colliderect(enemyObject.rect):
                    global score
                    bullets.remove(bullet)
                    enemies.remove(enemyObject)
                    score += 1
                    return

def draw_moving_background():  # draw game background
    global moving_background1, moving_background2  # global variables for the 2 moving backgrounds

    window.blit(pygame.transform.scale(background, (window_x, window_y)), (int(moving_background1), 0), window.get_rect())  # draws our first moving background image
    window.blit(pygame.transform.scale(background, (window_x, window_y)), (int(moving_background2), 0), window.get_rect())  # draws the second moving background image
    moving_background1 -= moving_background_speed  # sets the speed for the backgrounds
    moving_background2 -= moving_background_speed  # speed for the other background

    if moving_background1 < window_x * -1:  # if background 1 is outside of the window
        moving_background1 = window_x  # sets its x position to the other side of the window moving in again

    if moving_background2 < window_x * -1:  # if background 2 is outside of the window
        moving_background2 = window_x  # sets the x position to the other side of the window

def draw_player():  # drawing player
    player.gravity()  # check gravity
    player.rect.x -= moving_background_speed  # moves back with background
    player.update()  # updates player position and animation
    pygame.sprite.Group(player).draw(window)  # draws the player group to the window

    for bullet in bullets:  # draw bullet loop for all bullets
        bullet.draw(window)  # draw to the window

def draw_enemy():  # drawing enemies
    global enemies  # global enemies list

    for enemy in enemies:  # for all enemies in the list
        enemy.rect.x -= moving_background_speed  # move with background
        enemy.move(player)  # follow player
        enemy.update()  # update movement and frames
        pygame.sprite.Group(enemy).draw(window)  # draw to window

def draw_platform():  # drawing all platforms fun
    for platformObject in platformList:

        if platformObject.x < - 5 * meter:  # if it is out of the screen (only on the left side)
            platformList.remove(platformObject)  # removes platform from game

        if platformObject.image == 0:
            platformObject.load_type()

        else:
            window.blit(platformObject.image, (platformObject.x, platformObject.y))
            platformObject.x -= moving_background_speed

def draw_score():  # draw score to window
    score_text = font.render("Score: " + str(score), 1, (0, 0, 0))  # using font, render the score variable
    window.blit(score_text, (line_spacing, line_spacing))  # blit to screen in the right corner
    highscore_text = font.render("Highscore: " + str(highscore), 1, (0, 0, 0))      # highscore rendering
    window.blit(highscore_text, (line_spacing, 2 * line_spacing + font_size))  # blit to screen in the right corner under the score

"""
SETUP
"""

pygame.init()       # Initialises pygame
pygame.mixer.init()     # Initialises pygame mixer
main = True     # main-loop variable set to true

pygame.display.set_caption("Nuclear Cow Bomber")      # sets a title
pygame.mixer.music.load(os.path.join("songs", "ussr_anthem.ogg"))      # loads a song
pygame.mixer.music.play(-1)       # plays whats loaded on repeat
sound_moo = pygame.mixer.Sound(os.path.join("songs", "moo.ogg"))     # sets enemy suicide sound

frames_per_second = 60        # frame rate
moving_background_speed = 2     # how fast the background moves
meter = 64      # 1 meter equals 64 pixels
line_spacing = 10       # spacing in pixels between text
font_size = 30      # size of letters
font = pygame.font.Font(pygame.font.get_default_font(), font_size)       # gets a font
window_x = 1000     # window length
window_y = 707      # window height
window = pygame.display.set_mode((window_x, window_y))        # sets a surface window

background = pygame.image.load(os.path.join("images", "menu.png")).convert()        # sets the menu background picture to the background variable
window.blit(pygame.transform.scale(background, (window_x, window_y)), (0, 0))       # adjusts the background to the window

player_animation_cycles = 4        # animation cycles per
player_x = 49      # player length
player_y = 110      # player height
player_steps = 4      # how fast to move

enemy_animation_cycles = 1      # animation cycles for enemy
enemy_x = 108       # enemy length
enemy_y = 79        # enemy height
enemy_steps = 6     # enemy speed
enemy_spawn_rate = 150      # rate of which enemies spawn, lower equals more frequent
enemies = []        # list of every enemy entity for drawing to the window
enemy_sprites = []       # will fetch all enemy sprites images and slap them into one list
for x in range(1, 17):      # for-loop for every cow image
    character = pygame.image.load(os.path.join("images", "enemy" + str(x) + ".png")).convert_alpha()        # load the image and make the transparent parts transparent
    enemy_sprites.append(pygame.transform.scale(character, (enemy_x, enemy_y)))      # add and scale the images into the list

ground_y = 530      # floor level
acceleration = 1        # downwards acceleration (gravity)
jump_speed = 16     # startspeed of the jump

bullet_size = 6     # diameter of the bullet
bullet_speed = 8        # speed
ammo = 3        # how many bullets can be on the screen at once
shoot_cooldown = 5      # time between shoots
bullets = []  # makes a bullet list for each entity

platformSpritesSky = []     # adds all sky platforms to list

for x in range(1, 5):
    character = pygame.image.load(os.path.join("images", "sky_platform" + str(x) + ".png")).convert_alpha()
    platformSpritesSky.append(pygame.transform.scale(character, (x * meter, meter)))

platformSpritesDesert = []

for x in range(1, 5):
    character = pygame.image.load(os.path.join("images", "desert_platform" + str(x) + ".png")).convert_alpha()
    platformSpritesDesert.append(pygame.transform.scale(character, (x * meter, meter)))

platformList = []

highscore = 569

level = 2
test = 0

if level != 0:
    player = player()      # spawn player
    player.rect.x = 400     # player spawning x coordinate
    player.rect.y = ground_y     # player spawning y coordinate

    moving_background1 = 0      # sets the x position of the first game background to be in frame
    moving_background2 = window_x       # sets the x position of the second game background to be right outside of frame at the x coordinate of the window
    ground = pygame.Rect(0 - player_x, ground_y, window_x + player_x, window_y - ground_y)      # sets the ground rectangle

    facing = 1      # sets facing direction
    shoot_loop = 0      # makes a bullet cooldown variable
    score = 0       # score variable

    instantiate_platforms()     # Instantiates platforms

    if level == 1:
        background = pygame.image.load(os.path.join("images", "sky.png")).convert()     # level 1 wallpaper

    elif level == 2:
        background = pygame.image.load(os.path.join("images", "desert.png")).convert()      # level 2 wallpaper

"""
MAIN LOOP
"""

while main == True:     # if main is true, which it is
    for event in pygame.event.get():        # loop through a list of events from mouse and keyboard
        if event.type == pygame.QUIT:       # check if the user clicking the red x event
            main = False        # end main loop
            pygame.quit(); quit()       # if it has, end the program, end python

        if event.type == pygame.KEYDOWN:        # if keys are pressed down
            if event.key == ord("a"):       # if a key
                player.control(-player_steps, 0)        # player moves left
                facing = -1

            if event.key == ord("d"):       # if d key
                player.control(player_steps, 0)     # player moves right
                facing = 1

            if event.key == ord("w"):       # if w key
                player.jump()       # player jump with the jump function

            """if event.key == ord("s"):       # if s key
                player.crouch()     # crouch function"""

        if event.type == pygame.KEYUP:      # if keys are released
            if event.key == ord("a"):       # if a key
                player.control(player_steps, 0)     # player moves left

            if event.key == ord("d"):       # if d key
                player.control(-player_steps, 0)        # player moves right

            if pygame.key.get_mods() and pygame.KMOD_CTRL:      # if modifier key is ctrl
                if event.key == ord("q"):       # if q key
                    main = False        # end main loop
                    pygame.quit(); quit()       # if it is, end the program, end python

    if pygame.key.get_pressed()[pygame.K_d]:
        if player.jumping == 1:
            test = 1

    if shoot_loop > 0:      # if shooting is on cooldown
        shoot_loop += 1     # add 1 for each mainloop run

    if shoot_loop > shoot_cooldown:     # until shoot_loop is bigger than the cooldown
        shoot_loop = 0      # reset cooldown

    if pygame.key.get_pressed()[pygame.K_SPACE] and shoot_loop == 0:        # if pressing space and shoot cooldown has passed
        if len(bullets) < ammo:     # if amount of bullets on screen is less than ammo
            if facing < 0:      # if facing left
                bullet_x = player.rect.x        # shoot from players left side

            if facing > 0:      # if facing right
                bullet_x = player.rect.x + player_x     # shoot from players right side

            bullets.append(projectile(bullet_x, player.rect.y + player_y // 2 + 20, bullet_size, (0, 0, 0), facing))        # add a bullet projectile from the middle of the player as a circle in black
        shoot_loop = 1      # start the shoot cooldown

    for bullet in bullets:      # for all bullets
        if window_x > bullet.x > 0 - player_x:      # if inside of the window
            bullet.move()       # move function

        else:       # if not
            bullets.pop(bullets.index(bullet))      # remove from list

    bullet_collision()      # checks for bullet rectangle collisions using this function

    if random.randrange(0, enemy_spawn_rate) < 1:       # for every mainloop run get a random number between 0 and the enemy_spawn_rate variable, if the number is less than 1 which its cna only be a single time
        enemies.append(enemy(window_x, ground_y - enemy_y)) or enemies.append(enemy(0 - enemy_x, ground_y - enemy_y))       # add an enemy outside the window on the right or the left side

        if len(enemies) < ammo:     # if there are less enemies than the player has ammo
            if enemy_spawn_rate > 1:        # if the enemy spawn rate is bigger than 1 per run
                enemy_spawn_rate -= 1       # increase the chance of enemy spawns

    if level != 0:      # if a level has been selected
        draw_moving_background()        # function that draws the game background
        draw_platform()     # function that draws platforms
        draw_enemy()        # function that draws enemies
        draw_player()       # function that draws the player
        draw_score()        # function that draws the score

    pygame.display.update()     # updates the screen
    pygame.time.Clock().tick(frames_per_second)     # sets the runtime speed of the game to number of times the screen updates per second
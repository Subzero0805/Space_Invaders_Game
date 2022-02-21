#Importing the relevant libaires that will be used through the game

import pygame
import os
import random
#intiating fonts
pygame.font.init()

#Creating a window for the game
WIDTH, HEIGHT = 750 , 750
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Invader Game")

#Loading in the enemy's
#Using caps for variables as these be constant
BASIC_ALIEN = pygame.transform.scale(
    pygame.image.load(os.path.join("Space_Invaders_Game\Assets","Alien_sprite.png")), (75,75))
FAST_ALIEN = pygame.transform.scale(
    pygame.image.load(os.path.join("Space_Invaders_Game\Assets","fast_alien_sprite.png")),(75,75))
GUNNER_ALIEN = pygame.transform.scale(
    pygame.image.load(os.path.join("Space_Invaders_Game\Assets","gunner_alien_sprite.png")),(75,75))

#Player ship
PLAYER_SHIP = pygame.transform.scale(
    pygame.image.load(os.path.join("Space_Invaders_Game\Assets","player_ship.png")), (100, 100))

#Loading in Bullets/Lasers
#Basic Alien Bullet
BASIC_BULLET = pygame.image.load(os.path.join("Space_Invaders_Game\Assets", "basic_bullet.png"))
#Fast alien Bullet
FAST_BULLET = pygame.image.load(os.path.join("Space_Invaders_Game\Assets","fast_bullet.png"))
#Gunner Bullet
GUNNER_BULLET = pygame.image.load(os.path.join("Space_Invaders_Game\Assets","gunner_bullet.png"))
#Player bullet
PLAYER_BULLET = pygame.image.load(os.path.join("Space_Invaders_Game\Assets","ship_bullet.png"))

#Load in background
BG = pygame.image.load(os.path.join("Space_Invaders_Game\Assets","background.png"))

#Creating a bullet class
class Bullet:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        #Creating a mask to use for collision dectection
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        #enabling the bullet to be drawn in the window
        window.blit(self.img, (self.x, self.y))


    def move(self, vel):
        #Giving the bullet a velocity (ability to move)
        self.y += vel

    def off_screen(self, height):
        #Checking that the bullet is still within the window
        return not(self.y <= height and self.y >= 0)
    
    def collision(self, obj):
        #Collision detection by return the value of the collide function.
        #the 'self' will check if the object is colliding with itself 
        return collide(obj, self)


#Creating a ship class
class Ship:
    #Half a second as our FPS is 60
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x 
        self.y = y
        self.health = health
        self.ship_img = None
        self.bullet_img = None
        self.bullets = []
        self.cool_down_counter = 0

    def draw(self, window):
        #Testing ship class and movement
        #pygame.draw.rect(window, (255,255,255), (self.x,self.y,50,50))
        window.blit(self.ship_img, (self.x,self.y))
        for bullet in self.bullets:
            bullet.draw(window)
    
    def move_bullets(self, vel, obj): #vel gives velocity, obj is used to check for collision
        #Checking that cooldown is 0
        self.cooldown()
        #for each bullet that is in the list
        for bullet in self.bullets:
            #Move the bullet by velocity
            bullet.move(vel)
            #If the bullet is offscreen remove it
            if bullet.off_screen(HEIGHT):
                self.bullets.remove(bullet)
            #If the bullet is colliding, reduce the health of the object and remove the bullet
            elif bullet.collision(obj):
                obj.health -= 10
                self.bullets.remove(bullet)

    def cooldown(self):
        #if the cooldown is at the time limit, reset the cooldown
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        #If the cooldown counter is greater than 0, increment it by 1 up to 30 (half a second)
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        #Chekcing that the cooldown is 0
        #Creating a laser object
        if self.cool_down_counter == 0:
            bullet = Bullet(self.x + self.x/8, self.y, self.bullet_img)
            self.bullets.append(bullet)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_width()

#Creating a player class that inherits the Ship class
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = PLAYER_SHIP
        self.bullet_img = PLAYER_BULLET
        #Using masks to enable pixel perfect collision
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

        #Player's ability to shoot
    def move_bullets(self, vel, objs): #objs as the laser can hit different enemies
        #Checking that cooldown is 0
        self.cooldown()
        #for each bullet that is in the list
        for bullet in self.bullets:
            #Move the bullet by velocity
            bullet.move(vel)
            if bullet.off_screen(HEIGHT):
                self.bullets.remove(bullet)
            #If the bullet is colliding.
            else:
                #for each object in the objects list (enemies)
                for obj in objs:
                    #if the bullet has collided with an object
                    if bullet.collision(obj):
                        #remove the object
                        objs.remove(obj)
                        #remove the bullet
                        self.bullets.remove(bullet)
    
    def draw(self,window):
        super().draw(window)
        self.health_bar(window)

    def health_bar(self, window):
        #Creating a red rectangle for "lost" health
        pygame.draw.rect(window, (255,0,0), (self.x, 
        self.y + self.ship_img.get_height() + 10,
        self.ship_img.get_width(), 10))

        #Creating a green rectangle for current health
        pygame.draw.rect(window, (0,255,0), (self.x, 
        self.y + self.ship_img.get_height() + 10,
        self.ship_img.get_width() * (self.health/self.max_health), 10))


#Creating an Enemy
class Enemy(Ship):
    ENEMY_MAP = {
                "basic": (BASIC_ALIEN, BASIC_BULLET),
                "fast" : (FAST_ALIEN, FAST_BULLET),
                "gunner": (GUNNER_ALIEN,GUNNER_BULLET)
                }
    def __init__(self, x, y, enemy, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.bullet_img = self.ENEMY_MAP[enemy]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel
    #Overriding the shoot function to aline bullets with centre of enemy 
    def shoot(self):
        #Chekcing that the cooldown is 0
        #Creating a laser object
        if self.cool_down_counter == 0:
            bullet = Bullet(self.x + self.x/14, self.y, self.bullet_img)
            self.bullets.append(bullet)
            self.cool_down_counter = 1

#Collision function
def collide(obj1, obj2):
    #Masks works by checking if pixels within two sprites overlap. 
    #Usually sprites are loaded in as rectangles/squares, therefore mask allows for 
    #the game to check where the actual pixels collide.
    offset_x = obj2.x - obj1.x  #Distance between object 1 and object 2
    offset_y = obj2.y - obj1.y  #As above but for y
    #Given two objects, if they are overlapping based on their offset, then we return True.
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    run = True
    FPS = 60
    level = 0
    lives = 3
    #Setting the main text font and size
    main_font = pygame.font.SysFont("comicsans", 20)
    #Font for when User loses
    lost_font = pygame.font.SysFont("comicsans", 30)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    #player move speed
    player_vel = 5

    #Bullet velocity
    bullet_vel = 5

    #Making a ship
    player = Player(300,630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0,0))
        #Drawing text
        lives_label = main_font.render(f"Lives : {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
        #Adding lives and level counter to window
        WIN.blit(lives_label, (10, 10))
        #Ensuring that the Level label will sit 10 pixels from the right edge of the screen
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        #Drawing Enemy
        for enemy in enemies:
            enemy.draw(WIN)
        #Drawing Player
        player.draw(WIN)
        
        #If the player loses, show a loss statement.
        if lost:
            lost_label = lost_font.render("You Lost!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    
    while run:
        #Setting the FPS to 60
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
        #showing the lost message for 3 seconds
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue


        #Checking that there are no more enemies and increasing level
        if len(enemies) == 0:
            level += 1
            #Increasing the amount of enemies by 5
            wave_length += 3
            #Spawning in Enemies
            for i in range(wave_length):
                #Randomly spawning in Enemies
                enemy = Enemy(random.randrange(100, WIDTH - 100),
                 random.randrange(-1500, -100),
                 random.choice(["basic","fast","gunner"]))
                enemies.append(enemy)

        #Checking for possible events in the game
        for event in pygame.event.get():
            #Checking for the quit event, enabling the game to stop running
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0: #Left
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH: #Right
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0: #Up
            player.y -= player_vel
        #Account for health bar.
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < HEIGHT: #Down
            player.y += player_vel
        if keys[pygame.K_SPACE]: #Allowing the player to shoot.
            player.shoot()


        for enemy in enemies[:]:
            #giving enemies the ability to move
            enemy.move(enemy_vel)
            #giving enemies the ability to shoot
            enemy.move_bullets(bullet_vel, player)
            #Enemies will shoot, assigning a random value to the shots per second
            if random.randrange(0, 4* 6) == 1:
                enemy.shoot()
            #Checking for collision
            if collide(enemy, player):
                player.health -= 20
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

            


        player.move_bullets(-bullet_vel, enemies)

#Creating a main menu
def main_menu():
    title_font = pygame.font.SysFont("comicsans",50)
    run = True
    while run:
        WIN.blit(BG, (0,0))
        title_label = title_font.render("Press the mouse to begin...",
        1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #If any mouse buttons are pressed, start the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()

main_menu()

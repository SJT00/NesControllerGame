'''
Author:Saad Jahanzeb
Revision Date:14/6/2017
Program Name:Final Project-Space Invaders
Program Description:My Space Invader Game,which uses Left and Right Keys for movement aswell as spacebar for shooting Laser.
       Table of Variables:
width:width of screen
height:height of screen
FPS:Frames per second variable can be changes to provide smoother control, but performance would suffer aswell as vice versa.
screen: variable for screen display, ie the python window that opens up holds property like length and width.
clock: used to hold a inbuilt pygame time.clock value this will be used to keep track of the fps as said above.
pspritegroup: a sprite group(a pygame builtin type that holds multiple or singular sprites and has inbuilt attributes and functions) holding the player sprite/class instance.
lspritegroup: a sprite group holding all player laser sprites/class instances.
espritegroup: a sprite group holding all enemy sprites/class instances.
elspritegroup: a sprite group holding all enemy laser sprites/class instances.
Dir: a variable holding the directory of my pygame path this is so i can access my sprite folder on any pc by just changing this small value and adding the new file path.
font: a font variable that holds and loads my font file from my sprites folder.
cellw: cell width variable.
cellh: cell height variable.(both cell variables are used for enemy placement at beginning of game).
dir: a directional value which if +1 means enemies all go right, while if left they go left.
score: a score variable holding the points player has gained by killing enemies.
lives: a lives variable holding the number of lives player has left, this is to check if player has lost the game.
winorlose: a win or lose variable to store if player won or lost the game, used to print this on screen at end game.
calculatedonce: a boolean too tell if winning or losing has been calculated or not, as once screen is cleared player will have lost even if they actually won, this will be further explained.
pressed: a variable that eases calling key press events.
self.speed: a speed variable in all classes it controls speed of said sprite whether vertical speed for the laser or horizontal for player and enemies.
self.Spaceisup: a boolean checking if space is not being pressed, to prevent space spamming by just holding it down.
l: a temporary laser class instance called when either player or enemy has shot a laser.
lx: initial x location of laser class instance/ laser sprite.
ly: initial y location of laser class instance/ laser sprite.
ydir: dictates whether laser sprite is moving towards bottom or top of screen for enemy/player respectively.
p: player class instance which will be added, to be displayed in a spritegroup.
e: enemy class instance which will be added, to be displayed in a spritegroup.
ex: initial enemy x location.
ey: initial enemy y location.
self.anim: enemy classes inbuilt variable to check what animation sprite enemy is on, so i can flip through them.
self.clock: enemy clock variable that increases every second so i can change enemy animation at regular intervals, to create the illusion of change.
self.etype: enemy type variable, that decides what enemy type the initial enemy instance will be (out of 3 possible enemy types).
label: a temporary variable holding what text is to be rendered on screen.
label1: a temporary variable holding what text is to be rendered on screen.
Note:instance and sprite are pretty much used interchangeably.
'''
import pygame  # imports pygame library to access its functions and event handling
import sys  # imports system library as well used later to exit program
import os
import random  # imports random method aswell for later use.
import serial
ser = serial.Serial('com3', 9600)
width = 800  # Width-Dimension of Window
height = 600  # Height-Dimension of Window
FPS = 60  # Fps of Game
pygame.init()  # running pygame init function
screen = pygame.display.set_mode((width, height))  # sets up display screen resolution ie:Game Window
pygame.display.set_caption("Space Invaders")  # Title of Window
clock = pygame.time.Clock()  # sets up fps clock
# Note:instead of using one pygame sprite group as is traditionally used, i used multiple sprite groups, this was due to the certain collision detection features that are available group vs group but not sprite vs sprite.
pspritegroup = pygame.sprite.Group()  # holds player sprite, to be drawn on screen
lspritegroup = pygame.sprite.Group()  # holds all player shot laser sprites, to be drawn on screen, see note above.
espritegroup = pygame.sprite.Group()  # holds all enemy sprites, to be drawn on screen, see note above.
elspritegroup = pygame.sprite.Group()  # holds all enemy laser sprites, to be drawn on screen, see note above.
Dir = os.getcwd()+"\\"  # Used for ease of access, in terms of finding the location/directory of my game sprites.
font = pygame.font.Font(Dir + "Sprites\Font.ttf",
                       25)  # variable to store my imported font file, it first imports it from directory then places it within this variable.
cellw = 60  # size of a grid cells width, this is used to place enemy sprites approprite grid/cell spaces away from each other.
cellh = 40  # size of a grid cells height, this is used to place enemy sprites approprite grid/cell spaces away from each other.
dir = random.choice((-1,
                    1))  # direction variable for all enemy sprites, randomly chooses either -1 or 1, ie left or right direction initial movement for all enemies.
score = 0  # score variable to give player some immersion and fun.
lives = 3  # lives variable will decrease by one everytime player gets hit.
winorlose = "Lost"  # win or lose variable, holds a string value to see if player lost or won(ie killed all enemies or has no lives left) this will be printed on end game screen.
calculatedonce = False  # a Boolean to check only once if player has lost or won, as after player has lost he can't win unless replaying game and vice versa


class Player(pygame.sprite.Sprite):  # Class for player, holds all attributes and variables, to be called later.
   def __init__(self):  # init function that runs when instance of class occurs
       super(Player,
             self).__init__()  # calls init function to initialize base class in this case pygame.sprite.Sprite class, this is required in every pygame sprite class.
       self.image = pygame.image.load(
           Dir + "Sprites\Player.png").convert()  # loads image of player(and sets it to sprite image) from Directory then converts it into faster to render format, for effeciency amd optimization
       self.image.set_colorkey((0, 0,
                                0))  # sets black as color key to make any part of the picture that is black, transparent to avoid bad paint backgrounds and ugly overlapping of sprites.
       self.image = pygame.transform.scale(self.image, (39,
                                                        24))  # changes dimensions of sprite to my one specifications, as the file image size was too big for my screen size.
       self.rect = self.image.get_rect()  # creates a rectangle around image and gives it properties and values, like x and y values, etc.
       self.rect.center = (
           width / 2,
           height * 9 / 10)  # puts center of image rather than top left corner at said location, ie middle bottom of screen.
       self.speed = 3  # player speed variable, this will determine player velocity when directional key is pressed.
       self.Spaceisup = True  # a variable to check if spacebar key is down, this is essential as if this wasn't present user could just hold space ke and make a laser blob, instead of singular laser shots.

   def update(
           self):  # a update function, this is something inbuilt into pygame sprite classes and i will call it every frame to update player position and shoot laser.
       pressed = pygame.key.get_pressed()  # Handles Key Presses, for ease of access later
       if (pressed[
           pygame.K_RIGHT]or ser.readline()[3]==49)and self.rect.right < width: self.rect.centerx += self.speed  # if right arrow key is pressed and player is not in danger of going off screen then move player by player speed.
       if (pressed[
           pygame.K_LEFT]or ser.readline()[1]==49)and self.rect.left > 0: self.rect.centerx -= self.speed  # if left arrow key is pressed and player is not in danger of going off screen then move player by player speed.
       if (pressed[
           pygame.K_SPACE]or ser.readline()[4]==49)and self.Spaceisup:  # if Spacebar is pressed and Spacebar is not being held down(to avoid just holding the key until a laser blob is created) then
           l = Laser(self.rect.centerx, self.rect.y, 1)  # create a instance of laser class at players location and going towards screen top.
           lspritegroup.add(l)  # add this instance of laser class to laser sprite group so it can be rendered.
           self.Spaceisup = False  # makes this boolean false as Space is down, or is being pressed, hence this if will only run once, when space is pressed.


class Laser(pygame.sprite.Sprite):# My laser class, used for both enemy and player laser instances.
   def __init__(self, lx, ly, ydir):# init function that runs when instance of class occurs
       super(Laser, self).__init__()# calls init function to initialize base class in this case pygame.sprite.Sprite class, this is required in every pygame sprite class.
       self.image = pygame.Surface((3, 6))#creates a 3 by six rectangle.
       self.image.fill((255, 255, 255))#fills said rectangle with white, to create iconic white laser shot.
       self.rect = self.image.get_rect()# creates a rectangle around image and gives it properties and values, like x and y values, etc.
       self.rect.center = (lx, ly)#sets up this new rectangle/sprite x and y values at given location/argument (center is used as base and y are at left corner of images).
       self.speed = 5#vertical speed at which laser will travel.
       self.ydir = ydir#declares ydir as a private class variable, this stops problems with altering ydir resulting in all laser sprites moving in different direction rather than just the once instance.

   def update(self):# a update function, this is something inbuilt into pygame sprite classes and i will call it every frame to update laser position.
       self.rect.centery -= self.speed * self.ydir#changes y location every frame by decreasing/inceasing it by speed towards/away from player depending on given direction (enemies shoot towards player, player shoots towards enemy etc).
       if (self.rect.bottom <= 0 or self.rect.top>=height): lspritegroup.remove(self)#if laser instance is outside of screen delete it as it missed its target and is just wasting performance.


class Enemy(pygame.sprite.Sprite):# Enemy class for instances of all enemy, whether different type or not.
   def __init__(self, ex, ey, etype):#init function with certain parameter, which will be explained as they come.
       super(Enemy, self).__init__()# calls init function to initialize base class in this case pygame.sprite.Sprite class, this is required in every pygame sprite class.
       self.image = pygame.image.load(Dir + "Sprites\e" + str(etype) + "_0.png").convert()#loads base image of enemy, with given enemy type(out of 3 possible enemy types) parameter, then converts it for an efficent to render file type.
       self.image.set_colorkey((0, 0, 0)) # sets black as color key to make any part of the picture that is black, transparent to avoid bad paint backgrounds and ugly overlapping of sprites.
       self.image = pygame.transform.scale(self.image, (36, 24))#changes image dimensions as original file was to big or small for my screen dimensions.
       self.rect = self.image.get_rect()#gives image rect properties which will give me access to its x and y as well as other properties.
       self.rect.center = (ex, ey)#puts image center at given location, which was called in init function.
       self.speed = 1#speed at which enemys move horizontally.
       self.anim = 0#animation frame that the enemy instance is on, initial is 0 as player is on 1st frame as start point is 0 then next frame is frame 1.
       self.clock = 0#every enemy instance has a clock which i use to determine if it should change its animation frame.
       self.etype = etype#enemy type variable that takes value that was called in the initial function and makes it private within class .

   def update(self):# a update function, this is something inbuilt into pygame sprite classes and i will call it every frame to update enemy position, animation and shoot laser.
       self.animate()#calls animation function to update enemy animation frame.
       self.move()#calls move function to move enemy sprite horizontally.
       if ((random.randint(1, 500)) == 1): self.shoot()#every 1/500 chance enemy should shoot, ie call shoot function.

   def animate(self):#animation function for enemy sprite.
       self.clock += 1#add time to enemy clock.
       if self.clock % 25 == 0:# every time clock is evenly divisbile by 25 update enemy's animation(which i found to be not too fast or slow).
           if self.anim == 0:#if player was on frame 0 goto frame 1.
               self.anim = 1
           elif self.anim == 1:#vice versa.
               self.anim = 0
       self.image = pygame.image.load(Dir + "Sprites\e" + str(self.etype) + "_" + str(self.anim) + ".png").convert()# loads image with newly updated animation and preset enemy type and then converts it for optimization.
       self.image.set_colorkey((0, 0, 0))#sets black as color key to make black parts of new image transparent.
       self.image = pygame.transform.scale(self.image, (36, 24))#changes new images dimensions to look more visually appealing and coherant.

   def move(self):#move function for all enemies.
       global dir# calls global variables as it will be modified
       self.rect.centerx += dir * self.speed# changes enemy location by enemies speed and given direction.
       if (self.rect.left <= 0 + self.speed or self.rect.right >= width - self.speed):#if enemy hits left or right edge of screen change all enemies direction and move them one cell down screen.
           dir *= -1#changes direction to opposite way.
           for i in espritegroup.sprites():#all instances of enemy
               i.rect.centery += cellh#will move down one cell aswell

   def shoot(self):#enemy shooting laser function.
       l = Laser(self.rect.centerx, self.rect.bottom, -1)# calls instance of laser at enemy location and gives it direction to go down screen.
       elspritegroup.add(l)# adds this instance to enemy laser sprite group.


def Scoring():#scoring function that handles score increase and display.
   global score# calls global variable score as this will be changed through out function.
   if (pygame.sprite.groupcollide(lspritegroup, espritegroup, True, True)):# if players laser hits enemy, then kill/unrender laser sprite aswell as enemy sprite that got hit.
       score += 10#increase player score every kill.
   label = font.render("Score: " + str(score), 1, (255, 255, 255))# temporary variable holding what is to be rendered on player score in previously loaded font type and white colour.
   screen.blit(label, (5, 0))#displays player score at top left corner.


def Lives():#lives function that changes/decreases and displays lives as is appropriate.
   global lives#calls global variable to be changed.
   if (pygame.sprite.groupcollide(elspritegroup, pspritegroup, True, False)):#if player collides with enemy's laser then kill the laser and.....
       lives -= 1#decrease player lives by 1.
       p.rect.centerx = width / 2#change player center x (explained above) value to middle of screen, to "respawn".
   label = font.render("Lives: " + str(lives), 1, (255, 255, 255))#temporary variable holding text to be rendered.
   screen.blit(label, (width - 125, 0))#displays said lives at left corner of screen.


def EndGame():#End Game function that runs when a win or loss is triggered.
   global winorlose, calculatedonce#calls global variables to be changed later.
   if calculatedonce == False:#if win or loss hasn't already been calculated (look  in table of values for more info).
       if len(espritegroup) == 0:#if no enemies remain.
           winorlose = "Won"#Youve won.
       else:
           winorlose = "Lost"#else you lost
       calculatedonce = True#Calculation has been done and can't be done again.
   pspritegroup.empty()#delete/unrender player sprite.
   lspritegroup.empty()#delete/unrender player laser sprites.
   espritegroup.empty()#delete/unrender enemy sprites.
   elspritegroup.empty()#delete/unrender enemy laser sprite.
   label = font.render("Game Over, " + "You " + winorlose, 1, (255, 255, 255))# temporary variable that creates text (curtaining to whether player lost or won) with given font in white colour.
   screen.blit(label, (width / 2, height / 2 - 30))#displays said text in upper middle of screen
   label1 = font.render("Score:" + str(score), 1, (255, 255, 255))# temporary variable that creates text (players end score in this case) with given font in white colour.
   screen.blit(label1, (width / 2, height / 2))#displays said text below previously displayed text.


def spritegrouper():#just a function that renders and updates all sprite groups, made mostly for aesthetic purposes, to clean up my main game loop.
   pspritegroup.update()#calls up date function for all sprites within said class so in this case player.
   lspritegroup.update()#same as above for player lasers.
   espritegroup.update()#for enemies.
   elspritegroup.update()#for enemy lasers.
   pspritegroup.draw(screen)#draws updated sprites on screen.
   lspritegroup.draw(screen)#same as above.
   espritegroup.draw(screen)#same as above.
   elspritegroup.draw(screen)#same as above.


p = Player()#instance of player class called.
pspritegroup.add(p)#this instance is then displayed on screen.
for ey in range(height // 10, height // 2, cellh):#a for loop going through creating a grid basically, from half of screen height to a tenth of screen height dividing by cell size
   for ex in range(width * 2 // 10, width * 8 // 10, cellw):#same as above but with screen width instead
       if ey // cellh == 1: e = Enemy(ex, ey, 1)#places enemy instance at this grid location and by row gives it  a enemy type in this case 1 enemy type if row 1
       if ey // cellh == 2: e = Enemy(ex, ey, 1)
       if ey // cellh == 3: e = Enemy(ex, ey, 2)
       if ey // cellh == 4: e = Enemy(ex, ey, 2)
       if ey // cellh == 5: e = Enemy(ex, ey, 3)
       if ey // cellh == 6: e = Enemy(ex, ey, 3)
       espritegroup.add(e)#adds newly made enemy instance to enemy sprite group to render it.
while True:#infinite loop unless window is closed (will be discussed later).
   clock.tick(FPS)  # Sets up Fps to 60 to give smooth animated feel and appearence
   for event in pygame.event.get():  # creates iterator called event that goes through all events triggered by user
       if event.type == pygame.QUIT:  # When user click on X button to close window (my loop end condition)
           sys.exit()  # Exit  the program
       #if event.type == pygame.KEYUP:
        #   if event.key == pygame.K_SPACE: p.Spaceisup = True#sets my Space is up variable to True if space is not being held down.
   if (ser.readline()[4] == 48):
       p.Spaceisup = True
   screen.fill((0, 0, 0))  # re-colour the screen to black to clear it
   if lives <= 0 or len(espritegroup) == 0 or pygame.sprite.groupcollide(espritegroup, pspritegroup, False, True):#if player has no lives left or no more enemies exist or enemies are low enough on the screen to hit player Kill/unrender player and....
       EndGame()#run End game function
   else:# if game is still running and not ended then
       spritegrouper()#update and draw all sprites
       Scoring()#record and display score
       Lives()#record and display lives
   pygame.display.flip()  # update screen with all changes made

pygame.quit()  # end pygame if game loop is over
quit()  # end window if game is over



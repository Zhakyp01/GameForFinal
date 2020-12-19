import math
import pygame

#define some colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)

#size of break out blocks
block_width = 23
block_height = 15


class Block(pygame.sprite.Sprite):
    """this class respresents each block that will get knocked out by the ball
    It derives from the "Sprite" class in pygame """

    def __init__(self, color, x, y):
        ''' constructor. pass in the color of the block,
        and its x and y position '''

        #Call the parent class (Sprite) canstructor
        super().__init__()

        #Create the image of the block of appropriate size
        #the width and height are sent as a list for the first parameter
        self.image = pygame.Surface([block_width, block_height])

        #fill the image with the appropriate color
        self.image.fill(color)

        #fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

        #move the top left of the rectangle th x, y
        #this is where our block will appear..
        self.rect.x = x
        self.rect.y = y


class Ball(pygame.sprite.Sprite):
    ''' this class represents the ball
    It derives from the "Sprite" class in pygame '''

    #speed in pixels per cycle
    speed = 10.0

    # floating point representation of where the ball is
    x = 0.0
    y = 180.0

    # direction of ball (in degrees)
    direction = 200

    width = 10
    height = 10

    # constructor. pass in the color of the block, and its x and y position
    def __init__(self):
        #call the parent class (Sprite) constructor
        super().__init__()

        #creat the image of the ball
        self.image = pygame.Surface([self.width, self.height])

        #color the ball
        self.image.fill(white)

        # get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()

        # get attributes for the height/width of the screen
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

    def bounce(self, diff):
        ''' this function will bounce the ball
        of a horizontal surface (not a vertical one)'''

        self.direction = (180 - self.direction) % 360
        self.direction -= diff

    def update(self):
        ''' update the position of the ball.'''
        # sine and cosine work in degrees, so we have to convert them
        direction_radians = math.radians(self.direction)

        # change the position (x and y) according to the speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)

        # move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y

        # do we bounce off the top of the screen?
        if self.y <= 0:
            self.bounce(0)
            self.y = 1

        # do we bounce off the left of the screen?
        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1

        # do we bounce off the right side of the screen?
        if self.x > self.screenwidth - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = self.screenwidth - self.width - 1

        # did we fall off the bottom edge of the screen?
        if self.y > 600:
            return True
        else:
            return False


class Player(pygame.sprite.Sprite):
    ''' this class represents the bar at the bottom that the
    player controls. '''

    def __init__(self):
        ''' constructor for Player.'''
        # call the parent's constructor
        super().__init__()

        self.width = 75
        self.height = 15
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((white))

        # make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        self.rect.x = 0
        self.rect.y = self.screenheight-self.height

    def update(self):
        ''' update the player position. '''
        # Get where the mouse is
        pos = pygame.mouse.get_pos()
        # set the left side of the player bar to the mouse position
        self.rect.x = pos[0]
        # make sure we don't push the player paddle
        # off the right side of thr screen
        if self.rect.x > self.screenwidth - self.width:
            self.rect.x = self.screenwidth - self.width

# call this function so the pygame library can initialize itself
pygame.init()

# create an 800x600 sized screen
screen = pygame.display.set_mode([800, 600])

# set the title of the window
pygame.display.set_caption('breakout')

# enable this to make the mouse disappear when over our window
pygame.mouse.set_visible(0)

# this is a font we use to draw text on the screen (size 36)
font = pygame.font.Font(None, 36)

# create a surface we can draw on
background = pygame.Surface(screen.get_size())

# create sprite lists
blocks = pygame.sprite.Group()
balls = pygame.sprite.Group()
allsprites = pygame.sprite.Group()

# create the player paddle object
player = Player()
allsprites.add(player)

# create the ball
ball = Ball()
allsprites.add(ball)
balls.add(ball)

# the top of the block (y position)
top = 80

# number of blocks to create
blockcount = 32

# --- create blocks

# five rows of blocks
for row in range(5):
    # 32 columbs of blocks
    for column in range(0, blockcount):
        # create a block (color, x, y)
        block = Block(blue, column * (block_width + 2) + 1, top)
        blocks.add(block)
        allsprites.add(block)
    # move the top of the next row down
    top += block_height + 2

# clock to limit speed
clock = pygame.time.Clock()

# is the game over?
game_over = False

# exit the program?
exit_program = False

# main program loop
while not exit_program:

    # limit to 30 fps
    clock.tick(30)

    # clear the screen
    screen.fill(black)

    # process the events in the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_program = True

    # update the ball and player position as long
    # as the game is  not over
    if not game_over:
        # update the player and ball positions
        player.update()
        game_over = ball.update()

    # if we are done, print game over
    if game_over:
        text = font.render('Game Over', True, white)
        textpos = text.get_rect(centerx=background.get_width()/2)
        textpos.top = 300
        screen.blit(text, textpos)

    # see if the ball hits the player paddle
    if pygame.sprite.spritecollide(player, balls, False):
        # the "diff" lets you try to bounce the ball left or right
        # depending where on the  paddle you hit it
        diff = (player.rect.x + player.width/2) - (ball.rect.x+ball.width/2)

        # set the ball's y position in case
        # we hit the ball on the edge of the paddle
        ball.rect.y = screen.get_height() - player.rect.height - ball.rect.height - 1
        ball.bounce(diff)

    # check for collisions between the ball and the blocks
    deadblocks = pygame.sprite.spritecollide(ball, blocks, True)

    # if we actually hit a block, bounce the ball
    if len(deadblocks) > 0:
        ball.bounce(0)

        # game ends if all the blocks are gone
        if len(blocks) == 0:
            game_over = True

    # draw everything
    allsprites.draw(screen)

    # flip the screen and show what we've drawn
    pygame.display.flip()

pygame.quit()

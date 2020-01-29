import pygame
from pygame import mixer
import random
import math

#Params
acel = 0.05 #Player's acceleration
fps = 60 #The number of frames per seconds the game runs on
sSpeed =2 #bullet speed
speed = 1.2 #Enemy speed

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 0, 255)


#HighScore Tracking
f = open('score.txt', 'r') #Open file for reading
highScore = int(f.read()) 
f.close()
f = open('champion.txt', 'r')
champion = f.read()
f.close()
score = 0
#High score and champion name read from external text files and stored in variables

#Background Music
mixer.init()
mixer.music.load("BMusic.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(-1)

#dimensions
WORLD_WIDTH = 5000
WORLD_HEIGHT = 5000
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size) #creates the window and sets it's size

#int to change between menu and gameplay
menu = 1 #0: HighScore Screen 1:Menu 2:Gameplay
dead = False #Is The Player Dead?


class GameObject(pygame.Rect): #Class based on a rect and base tod all objects in the game
    allObj = [] #list of all GameObjects
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hp = 1000
        self._xf = self.x
        self._yf = self.y
        GameObject.allObj.append(self)
    
    def takeDamage(self, dam):
        self.hp-= dam
        if self.hp <= 0: 
            self.destroy()

    #x and y are integers, so, for calculation purposes, float versions of them are set as properties
    @property
    def xf(self):
        return self._xf

    @xf.setter
    def xf(self, value):
        self._xf=value
        self.x = int(value)-self.width/2

    @property
    def yf(self):
        return self._yf
    @yf.setter
    def yf(self, value):
        self._yf=value
        self.y = int(value)-self.height/2

    def destroy(self): 
        GameObject.allObj.remove(self)

    def draw(self, position):
        pygame.draw.rect(screen, (50,50,50), (position,self.size))
    

    def update(self): #Method called every frame to update objects
        for g in GameObject.allObj:
            if g is not self and self.colliderect(g) and type(g) is not Bullet and type(g) is not Star:
                h = self.hp
                self.takeDamage(g.hp/2)
                g.takeDamage(h/2)



class Enemy(GameObject): #Base to all enemy ships
    allEnemies = []
    def __init__(self, hp, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hp = hp
        Enemy.allEnemies.append(self)

    def update(self):
        if self.hp<=0:
            self.destroy()

    def destroy(self):
        bSound = mixer.Sound('Explosion.wav')
        bSound.play()
        bSound.set_volume(200)
        LeftOver((self.xf,self.yf))
        Enemy.allEnemies.remove(self)
        super().destroy()
        global score
        score += 200



def pointTo(a, b):
    o = (b[0]-a[0], a[1]-b[1])
    return math.atan2(o[1], o[0])

class LeftOver(GameObject): #The "Explosion". destroys itself one second after the enemy dies
    def __init__(self, pos):
        super().__init__(pos, (60, 60))
        self.time = 0
        self.coolDown = 60

    def update(self):
        if self.time>=self.coolDown:
            self.destroy()
        self.time += 1

    def draw(self, position):
        r = int(self.width/2)
        position = (int(position[0]-self.width/2), int(position[1]-self.height/2))
        pygame.draw.circle(screen, (200,200,0), position, r)


class Ship(Enemy):
    def __init__(self, pos):
        super().__init__(10, pos, (40, 40))
        self.vx = 0
        self.vy = 0
        self.v = 0
        self.ac = 0.2
        self.ang = 0
        self.time = 0
        self.coolDown = fps*2

    def shoot(self):
        Bullet(self.ang, self, 1.6, self.xf,self.yf,5,5)

    def update(self):
        super().update()
        self.ang = pointTo((self.xf, self.yf), (player.xf, player.yf)) 
        a = self.ang
        if self.time>=self.coolDown:
            self.shoot()
            self.time = 0
        self.time += 1
        a = pointTo((self.x, self.y), (player.xf, player.yf))
        self.xf += speed*math.cos(a)
        self.yf -= speed*math.sin(a)
        a += math.radians(90)
        if self.v > 4:
            self.v = 4
        if self.v < -4:
            self.v = -4
        self.v += random.randint(-1,1)*self.ac
        d = ((self.xf-player.xf)**2+(self.yf-player.yf)**2)**(1/2)
        d /= 600
        self.xf += speed*math.cos(a)*self.v *d
        self.yf -= speed*math.sin(a)*self.v *d

    def draw(self, position):
        a = self.ang
        r = int(self.width/2)
        position = (int(position[0]-self.width/2), int(position[1]-self.height/2))
        pygame.draw.circle(screen, (200,50,50), position, r)
        pygame.draw.line(screen, (100,100,100), position, (position[0]+math.cos(a)*(r+5), position[1]-math.sin(a)*(r+5)), 10)

class MachineGun(Enemy):
    def __init__(self, pos):
        super().__init__(10, pos, (40, 40))
        bSound = mixer.Sound('MachineGun.wav')
        self.vx = 0
        self.vy = 0
        self.v = 0
        self.ac = 0.2
        self.ang = 0
        self.time = 0
        self.coolDown = fps*0.3

    def shoot(self):
        b =Bullet(self.ang+math.radians(random.randint(-30,30)), self, 1.3,  self.xf,self.yf,15,15)


    def update(self):
        super().update()
        self.ang = pointTo((self.xf, self.yf), (player.xf, player.yf)) 
        a = self.ang
        if self.time>=self.coolDown:
            self.shoot()
            self.time = 0
        self.time += 1
        a = pointTo((self.x, self.y), (player.xf, player.yf))
        self.xf += speed*math.cos(a)
        self.yf -= speed*math.sin(a)
        a += math.radians(90)
        if self.v > 4:
            self.v = 4
        if self.v < -4:
            self.v = -4
        self.v += random.randint(-1,1)*self.ac
        self.v += random.randint(-1,1)*self.ac
        d = ((self.xf-player.xf)**2+(self.yf-player.yf)**2)**(1/2)
        d /= 600
        self.xf += speed*math.cos(a)*self.v *d
        self.yf -= speed*math.sin(a)*self.v *d

    def draw(self, position):
        a = self.ang
        r = int(self.width/2)
        position = (int(position[0]-self.width/2), int(position[1]-self.height/2))
        p1 = position
        b = a+math.radians(30)
        p2 = (position[0]+math.cos(b)*(r+5), position[1]-math.sin(b)*(r+5))
        b = a-math.radians(30)
        p3 = (position[0]+math.cos(b)*(r+5), position[1]-math.sin(b)*(r+5))

        pygame.draw.polygon(screen, (100,100,100), [p1,p2,p3])
        pygame.draw.circle(screen, (200,50,50), position, r)




class Star(): #Stars are randomly generated objects that are not gameObjects yet can be seen
    allStar = []
    def __init__(self, x, y):
        self.x = x
        self.y = y
        Star.allStar.append(self)

    def draw(self):
        x = player.x%2000
        y = player.y%2000
        pos = (int((self.x - x)%2000), int((self.y - y)%2000))
        pygame.draw.circle(screen, WHITE, pos, 5)

    def genesis(a=160, w=2000, h=2000):
        for i in range(a):
            Star(random.randint(0,w), random.randint(0,h))

class Bullet(GameObject): #Base to all bullets. Are Instantiated with a direction to go and a speed and do damage to everything but who shot it
    allB = []
    def __init__(self, angle, owner, sp, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bSound = mixer.Sound('Blast.wav')
        bSound.play()
        bSound.set_volume(0.1)
        self.owner = owner
        self.hp = 3
        self.vx = sSpeed*math.cos(angle)*sp + owner.vx
        self.vy = -sSpeed*math.sin(angle)*sp + owner.vy
        Bullet.allB.append(self)

    def destroy(self):
        Bullet.allB.remove(self)
        super().destroy()

    def update(self):
        self.xf += self.vx
        self.yf += self.vy
        
        self.takeDamage(0.007)
        for g in GameObject.allObj:
            if self.hp<=0:
                return
            if g is not self and g is not self.owner and g.colliderect(self) and type(g) is not Star:
                g.takeDamage(self.hp)
                self.takeDamage(1)
    def draw(self, position):
        pygame.draw.circle(screen, (0,250,50), position, int(self.width/2))


def alert(): #Function called when the player goes too far away from the center of the map
    sound = mixer.Sound('wave.wav')
    sound.play()            

class Player(GameObject): #Class that holds all player cappabilities and funcions that calculate how objects are rendered in the screen based on player's position
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hp = 10
        self.ang = 0
        self.vx = 0
        self.vy = 0
        self.xf = self.centerx
        self.yf = self.centery

    def move(self):
        self.xf+=self.vx
        self.yf+=self.vy
        if(abs(self.xf)>3000):
            self.vx -= self.xf / 50000
            self.xf -= self.xf / 500
            alert()
        if(abs(self.yf)>5000):
            self.yf -= self.yf / 500
            self.vy -= self.yf / 50000
            alert()

    def drawAll(self):
        for g in GameObject.allObj:
                w = SCREEN_WIDTH/2
                h = SCREEN_HEIGHT/2
                if not (g.left>self.xf+w and g.right<self.xf-w and g.top>self.yf+h and g.bottom<self.yf-h):
                    g.draw((int(g.xf - self.xf + w), int(g.yf - self.yf + h)))
    def destroy(self):
        global dead
        dead = True

    def boost(self): #The player can only accelerate himself in the direction it is pointing at
        self.vx += acel*math.cos(self.ang)
        self.vy -= acel*math.sin(self.ang)
        if self.vx > 15:
            self.vx = 15
        if self.vx < -15:
            self.vx = -15
        if self.vy > 15:
            self.vy = 15
        if self.vy < -15:
            self.vy = -15
        

    def shoot(self):

        b = Bullet(self.ang, self, 1.7, self.xf,self.yf,5,5)

    def draw(self, position):
        a = self.ang
        r = int(self.width/2)


player = Player((0,0, 30,30)) #Instantiates the lpayer in the center of the map

Star.genesis()

def spawnEnemy(): #Spanws a random enemy in a random position arround the player and out of it's field of view
    n = random.randint(0,1)
    a = random.randint(0,360)
    a = math.radians(a)
    position = (player.x+math.cos(a)*400, player.y-math.sin(a)*400)
    if n == 0:
        Ship(position)
    else: 
        MachineGun(position)

def main():
    pygame.init() #Initiate pygame
    
    #Display details
    pygame.display.set_caption("Balanced as everything should be")
    a = pygame.image.load("Infinito.png")
    pygame.display.set_icon(a)


    
    global menu
    global score
    global highScore
    global dead

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    

    tempo = 2000
    menu = 1

    #HighScore naming variables
    l1 = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    l2 = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    l3 = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    l4 = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    i1 = 0
    i2 = 0
    i3 = 0
    i4 = 0
    sw = 0


    # Loop until the user clicks the close button.
    done = False
        # -------- Main Program Loop -----------
    while not done:
        clock.tick(fps)#Lock the fps
        if menu == 0:#HighScore screen
            #BackGround image
            image = pygame.image.load('space.jpg')
            image = pygame.transform.scale(image, (700, 500))
            screen.blit(image, (0,0))

            font = pygame.font.SysFont("consolas", 40)
            text = font.render("What is your name, traveler?", True, (200, 100, 50))
            screen.blit(text,(360 - text.get_width() // 2, 200 - text.get_height() // 2))
            
            name = l1[i1]+l2[i2]+l3[i3]+l4[i4] #Put 4 chars in a string

            #Display the name string
            font = pygame.font.SysFont("consolas", 72)
            text = font.render(name, True, (0, 100, 200))
            screen.blit(text,(360 - text.get_width() // 2, 295 - text.get_height() // 2))
            
            font = pygame.font.SysFont("consolas", 55)
            text = font.render("New HighScore! {}".format(highScore), True, (180, 100, 0))
            screen.blit(text,(50, 30))

            #Square cursor
            xPos = [295,335,375,415]
            pygame.draw.rect(screen, (200,100, 0), ((xPos[sw], 320),(10,10)))

            pygame.display.flip()#Update screen

            for event in pygame.event.get(): #Check for input
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        f = open('champion.txt','w')
                        f.write(name)
                        f.close()
                        global champion
                        champion = name
                        menu = 1
                    if event.key == pygame.K_RIGHT:
                        sw += 1
                        sw = sw%4
                    if event.key == pygame.K_LEFT:
                        sw -= 1
                        sw = sw%4
                    if event.key == pygame.K_UP:
                        am = 1
                        if sw == 0:
                            i1+=am
                            i1 = i1%26
                        if sw == 1:
                            i2+=am      
                            i2 = i2%26  
                        if sw == 2:
                            i3+=am
                            i3 = i3%26            
                        if sw == 3:
                            i4+=am
                            i4 = i4%26
                    if event.key == pygame.K_DOWN:
                        am = -1
                        if sw == 0:
                            i1+=am
                            i1 = i1%26
                        if sw == 1:
                            i2+=am      
                            i2 = i2%26  
                        if sw == 2:
                            i3+=am
                            i3 = i3%26            
                        if sw == 3:
                            i4+=am
                            i4 = i4%26

        elif menu == 1: #Menu screen
            #background
            image = pygame.image.load('space.jpg')
            image = pygame.transform.scale(image, (700, 500))
            screen.blit(image, (0,0))

            font = pygame.font.SysFont("consolas", 72)
            text = font.render("Press Enter", True, (0, 100, 200))
            screen.blit(text,(360 - text.get_width() // 2, 285 - text.get_height() // 2))
            font = pygame.font.SysFont("consolas", 110)
            text = font.render("Solar", True, (200, 50, 0))
            screen.blit(text,(360 - text.get_width() // 2, 430 - text.get_height() // 2))

            #Display current HighScore
            font = pygame.font.SysFont("consolas", 40)
            text = font.render("HighScore: {}".format(highScore), True, (180, 100, 0))
            screen.blit(text,(50, 30))
            text = font.render("{}".format(champion), True, (180, 140, 0))
            screen.blit(text,(210 - text.get_width() // 2, 80))


            pygame.display.flip()#Screen update

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        menu = 2 #Go to Gameplay
        else:
            if dead:#Routine aplyied when the player dies
                print('Dead')
                menu = 1
                GameObject.allObj.clear()
                global player
                player = Player((0,0,30,30))
                bSound = mixer.Sound('Explosion.wav')
                bSound.play()
                if score > highScore:
                    highScore = score
                    menu = 0
                    f = open('score.txt','w')
                    f.write(str(highScore))
                    f.close()
                score = 0
                dead = False

            else: #Gameplay
                # --- Event Processing
                tempo += 1
                score += 1 #Each second you survive if worth 60 points

                if tempo>= 5*fps: # Loop to spawn enemies every 5 seconds
                    spawnEnemy()
                    tempo= 0

                screen.fill(BLACK) #paint the screen black
                keys=pygame.key.get_pressed()
                #player spinning
                if keys[pygame.K_RIGHT]:
                    player.ang -= math.radians(3)
                if keys[pygame.K_LEFT]:
                    player.ang += math.radians(3)

                #General Input
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True #Close the game

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            player.shoot()

                # --- Drawing
                for g in Star.allStar: #Star loop
                    g.draw()

                for g in GameObject.allObj: #GameObject loop
                    g.update()

                player.drawAll()
                w=int(SCREEN_WIDTH/2)
                h=int(SCREEN_HEIGHT/2)
                
                #Player drawing
                p1 = (w+math.cos(player.ang)*20.0, h-math.sin(player.ang)*20.0)
                p2 = (w+20 * math.cos(player.ang+math.radians(120)), h-20*math.sin(player.ang+math.radians(120)))
                p4 = (w+20 * math.cos(player.ang+math.radians(240)), h-20*math.sin(player.ang+math.radians(240)))
                p3 = (w+0* math.cos(player.ang+math.radians(180)), h-0*math.sin(player.ang+math.radians(180)))
                pygame.draw.polygon(screen, (55,0,200), [p1, p2, p3, p4])

                #Score display
                font = pygame.font.SysFont("consolas", 50)
                text = font.render("Score {}".format(score), True, (0, 128, 0))
                screen.blit(text,(160 - text.get_width() // 2, 50 - text.get_height() // 2))
                
                player.move()#player movement     

                if keys[pygame.K_UP]: #Check input for player boost and draw the booster
                    player.boost()
                    pygame.draw.line(screen, (255,255,0), (int(w-math.cos(player.ang)*15.0), int(h+math.sin(player.ang)*15.0)), (int(w-math.cos(player.ang)*36),int(h+math.sin(player.ang)*36)), 10)

                #draw the hp bar
                pygame.draw.rect(screen, RED, ((450,35), (int(180*player.hp/10),24)))
                
                pygame.display.flip() #Update the screen
    

    pygame.quit() #Close pygame
 
if __name__ == "__main__":
    main()
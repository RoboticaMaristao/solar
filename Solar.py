import pygame
import random
import math
#Params
acel = 0.05
fps = 60
sSpeed =2 #shoot speed
speed = 1.2

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 0, 255)

WORLD_WIDTH = 5000
WORLD_HEIGHT = 5000
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)

menu = True

class GameObject(pygame.Rect):
    allObj = []
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hp = 2
        self._xf = self.x
        self._yf = self.y
        GameObject.allObj.append(self)
    
    def takeDamage(self, dam, noisy=True):
        self.hp-= dam
        if self.hp <= 0: 
            self.destroy()

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
    
    def update(self): 
        for g in GameObject.allObj:
            if g is not self and self.colliderect(g) and type(g) is not Bullet and type(g) is not Star:
                h = self.hp
                self.takeDamage(g.hp/2)
                g.takeDamage(h/2)

class Enemy(GameObject):
    allEnemies = []
    def __init__(self, hp, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hp = hp
        Enemy.allEnemies.append(self)
    def update(self):
        if self.hp<=0:
            self.destroy()
    def destroy(self):
        Enemy.allEnemies.remove(self)
        super().destroy()

def pointTo(a, b):
    o = (b[0]-a[0], a[1]-b[1])
    return math.atan2(o[1], o[0])

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
       Bullet(self.ang, self, 1, self.xf,self.yf,5,5)

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
        self.vx = 0
        self.vy = 0
        self.v = 0
        self.ac = 0.2
        self.ang = 0
        self.time = 0
        self.coolDown = fps*0.3

    def shoot(self):
       b =Bullet(self.ang+math.radians(random.randint(-30,30)), self, 0.7,  self.xf,self.yf,15,15)


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




class Star():
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

class Bullet(GameObject):
    allB = []
    def __init__(self, angle, owner, sp, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        
        self.takeDamage(0.007, False)
        for g in GameObject.allObj:
            if self.hp<=0:
                return
            if g is not self and g is not self.owner and g.colliderect(self) and type(g) is not Star:
                g.takeDamage(self.hp)
                self.takeDamage(1)
    def draw(self, position):
        pygame.draw.circle(screen, (0,250,50), position, int(self.width/2))

    
                

class Player(GameObject):
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
    def drawAll(self):
        for g in GameObject.allObj:
                w = SCREEN_WIDTH/2
                h = SCREEN_HEIGHT/2
                if not (g.left>self.xf+w and g.right<self.xf-w and g.top>self.yf+h and g.bottom<self.yf-h):
                    g.draw((int(g.xf - self.xf + w), int(g.yf - self.yf + h)))
    def destroy(self):
        print('died')
        global menu
        self.hp = 10 
        for g in Enemy.allEnemies:
            g.destroy()
        menu = True
    def boost(self):
        self.vx+=acel*math.cos(self.ang)
        self.vy-=acel*math.sin(self.ang)
    def shoot(self):
        b = Bullet(self.ang, self, 1.7, self.xf,self.yf,5,5)

    def draw(self, position):
        a = self.ang
        r = int(self.width/2)

        return self._xf

player = Player((0,0, 30,30))

Star.genesis()

def spawnEnemy():
    n = random.randint(0,1)
    a = random.randint(0,360)
    a = math.radians(a)
    position = (player.x+math.cos(a)*400, player.y-math.sin(a)*400)
    if n == 0:
        Ship(position)
    else: 
        MachineGun(position)

def main():

    pygame.init()
    
    pygame.display.set_caption("Balanced as everything should be")
 
    # Loop until the user clicks the close button.
    done = False
    global menu
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    

    tempo = 2000
    # -------- Main Program Loop -----------
    while not done:
        if menu:
            screen.fill((100,0,150))
            clock.tick(fps)
            font = pygame.font.SysFont("comicsansms", 72)
            text = font.render("Press Space", True, (0, 128, 0))
            screen.blit(text,(280 - text.get_width() // 2, 240 - text.get_height() // 2))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        menu = False
        else:
            # --- Event Processing
            tempo += 1
            print(tempo)
            if tempo>= 5*fps:
                spawnEnemy()
                print('Spawn')
                tempo= 0
            screen.fill(BLACK)
            keys=pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                player.ang -= math.radians(3)
            if keys[pygame.K_LEFT]:
                player.ang += math.radians(3)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.shoot()
    

            # --- Drawing
            for g in Star.allStar:
                g.draw()
            for g in GameObject.allObj:
                g.update()
            player.drawAll()
            w=int(SCREEN_WIDTH/2)
            h=int(SCREEN_HEIGHT/2)
            # pygame.draw.circle(screen,(0,0,255),(w,h), 20)
            p1 = (w+math.cos(player.ang)*20.0, h-math.sin(player.ang)*20.0)
            p2 = (w+20 * math.cos(player.ang+math.radians(120)), h-20*math.sin(player.ang+math.radians(120)))
            p4 = (w+20 * math.cos(player.ang+math.radians(240)), h-20*math.sin(player.ang+math.radians(240)))
            p3 = (w+0* math.cos(player.ang+math.radians(180)), h-0*math.sin(player.ang+math.radians(180)))
            pygame.draw.polygon(screen, (55,0,200), [p1, p2, p3, p4])
            # pygame.draw.line(screen, (100,0,20), (w, h), (int(w+math.cos(player.ang)*20.0), int(h-math.sin(player.ang)*20)), 2)
            player.move()     

            for b in Bullet.allB:
                b.update()

            # Set the screen background
    
            if keys[pygame.K_UP]:
                player.boost()
                pygame.draw.line(screen, (255,255,0), (int(w-math.cos(player.ang)*15.0), int(h+math.sin(player.ang)*15.0)), (int(w-math.cos(player.ang)*36),int(h+math.sin(player.ang)*36)), 10)

            pygame.draw.rect(screen, RED, ((50,50), (int(150*player.hp/10),10)))
            clock.tick(fps)
            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
 
    # Close everything down
    pygame.quit()
 
if __name__ == "__main__":
    main()

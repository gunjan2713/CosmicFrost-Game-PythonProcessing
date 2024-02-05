import random
import os
import time
add_library('minim')
player=Minim(this)
path = os.getcwd()
RESOLUTION_W = 1000
RESOLUTION_H = 600
score=0
game_started=False
# strating time here
start_time = time.time()

# Adding Instructions for the player, Initial Screen 
def Start():
    global game_started
    img=loadImage(path+"/StartGame.png")
    image(img,0,0,1000,600)

# on the initial screen, start game button defined, if pressed in that area game will start 
    if mousePressed and RESOLUTION_W/2-100<mouseX < RESOLUTION_W/2+100 and RESOLUTION_H/2-100<mouseY<RESOLUTION_H +100:
        game_started=True
        
# Creating Parent class for other space objects
class Space_Objects():
    def __init__(self):
        self.radius = random.randint(20,40)
        self.x = RESOLUTION_W
        self.y = random.randint(self.radius , RESOLUTION_H - self.radius)
        self.vx = random.uniform(10,20)
        self.vy= random.uniform(-0.5 , 0.5)
        self.img1=loadImage("Asteroid.png")
        
# Displaying Space_Objects as circles and using graphics as well to make it easy for collision detection   
    def display(self):
        noFill()
        noStroke() 
        circle(self.x , self.y , self.radius*2)
        image(self.img1, self.x - self.radius-2, self.y-self.radius-2 , self.radius*2+4, self.radius*2 + 4)
 
# Updating velocities, moving objects from right to left    
    def update(self):
        self.x -= self.vx
        self.y -= self.vy
        
# Collision detectin method
    def collision_detection(self , other):
        Centre_distance = dist(self.x , self.y , other.x , other.y)
        return Centre_distance < self.radius + other.radius
    
# checking if object is Off_Screen    
    def Off_Screen(self):
        return self.x < 0
    
# Creating coin class inheriting from asteroid class
class Coin(Space_Objects):
    def __init__(self):
        Space_Objects.__init__(self)
        self.radius = 23
        self.img2=loadImage("C.png")

# Method to display coin    
    def display(self):
        noStroke() 
        noFill()
        circle(self.x,self.y, self.radius*2)
        image(self.img2, self.x-self.radius , self.y-self.radius , self.radius*2 , self.radius*2 )

# Resetting position when it goes off screen        
    def Reset(self):
        if self.x < - self.radius:
            self.y = random.randint(0, RESOLUTION_H)
            self.x = RESOLUTION_W + self.radius
            
# Creating booster class interiting form asteroid class
class Booster(Space_Objects):
    def __init__(self):
        Space_Objects.__init__(self)
        self.radius = 23
        self.img3= loadImage("coin2.png")

# Method to display booster        
    def display(self):
        noStroke() 
        noFill()
        circle(self.x,self.y,self.radius*2)
        image(self.img3, self.x-self.radius , self.y-self.radius , self.radius*2 , self.radius*2 )

# Resetting position when it goes off screen          
    def Reset(self):
        if self.x < -self.radius:
            self.y = random.randint(0, RESOLUTION_H)
            self.x = RESOLUTION_W+self.radius
        
# Creating bullet class 
class Bullet:
    def __init__(self, x,y ):
        self.y = y
        self.x = x
        self.speed = 40
        self.radius = 8
        self.img4=loadImage("Bullet.png")

# Method to display bullet 
    def display(self):
        noFill()
        noStroke() 
        circle(self.x, self.y+27, self.radius*2) # display a circle at its positiong6
        image(self.img4, self.x-27,self.y+10 ,35,35)

# As it deosn not inherit form asteroid class, give it some velocity        
    def update(self):
        self.x += self.speed
    
    def Off_Screen(self):
        return self.x > RESOLUTION_W
    
# Creating Enemy bullet class 
class Ebullet:
    def __init__(self,x,y):
        self.x=x 
        self.y = y
        self.speed = 45
        self.radius = 5
        self.img5=loadImage("Ebullet.png")

# Method to display bullet     
    def  display(self):
        noStroke() 
        noFill()
        circle(self.x, self.y+8, self.radius * 2)
        image(self.img5, self.x-5,self.y-15, 35,35)

# As it deosn not inherit form asteroid class, give it some velocity   
    def update(self):
          self.x -= self.speed
          
    def Off_Screen(self):
        return self.x < -self.radius*2
 
# Creating class of enemy spacehisp
class EnemySpaceship:
    def __init__(self):
        self.radius = 35
        self.x = RESOLUTION_W
        self.y = random.randint(0+self.radius, RESOLUTION_H-self.radius) 
        self.speed = random.uniform(20, 35)
        self.Off_Screen = False
        self.bullets = []       #creating list of bullets 
        self.last_bulletfired_time = 0
        self.img6 = loadImage("Enemy.png")

# if bullet offscreen reset it's position        
    def Reset(self):
        self.x -= self.speed
        
        for i, bullet in enumerate(self.bullets):
            bullet.update()
            if bullet.Off_Screen():
                self.bullets.pop(i)
        
        if random.random()< 0.01: # probability
            self.shoot()

# displaying enemyspaceship and bullets          
    def display(self):
        noStroke() 
        noFill()
        circle(self.x,self.y,self.radius*2)
        image(self.img6, self.x-self.radius*2 , self.y-self.radius , self.radius*2 , self.radius*2 )
        
        for bullet in self.bullets:
            bullet.display()
            
# if spacehisp off screen retunr true
    def is_Off_Screen(self):
        if self.x < -self.radius*2:
            self.Off_Screen = True
        return self.Off_Screen

# collision detection method    
    def collision_detection(self,other):
        Centre_distance = dist(self.x, self.y, other.x, other.y)
        return Centre_distance < self.radius + other.radius

# defining shoot function by using millis    
    def shoot(self):
       # Shoot after a specific time after a shot has been fireed
        if millis() - self.last_bulletfired_time > 500:
           # Add new bullet to the list
            bullet = Ebullet(self.x- self.radius ,self.y)
            self.bullets.append(bullet)
        # Time update
            self.last_bulletfired_time = millis()
 
# Players spacehisp class        
class Spaceship():
    def __init__(self):
        self.x = RESOLUTION_W/4 
        self.y = RESOLUTION_H /2
        self.speed = 30
        self.bullets = []  # bullet list for player
        self.radius=35
        self.img5=loadImage(path + "/Player.png")
        self.game_over=False
        self.keycode= {UP:False ,DOWN:False}
        self.bulletfired_sound=player.loadFile(path + "/Bulletfired.mp3")

# displaying it        
    def display(self):
        noFill()
        noStroke() 
        circle(self.x , self.y , self.radius*2) 
        image(self.img5, self.x-38, self.y-40, self.radius*2+10, self.radius*2+10)
        for bullet in self.bullets: 
            bullet.display()

# updating its position based on keys pressed
    def update(self):
        
        if key==CODED:
            if self.keycode[UP] == True:
                self.y -= self.speed 
            if self.keycode[DOWN] == True:
                self.y += self.speed
        
# restricting spacehisp to a perticular area        
        # self.x = constrain(self.x, 0, RESOLUTION_W)
        self.y = constrain(self.y, self.radius, RESOLUTION_H-self.radius)

# updating bulet here    
        for bullet in self.bullets: 
            bullet.update()
            if bullet.Off_Screen(): 
                self.bullets.remove(bullet)

    # checking for collision detection    
    def collision_detection(self, other):
            Centre_distance = dist(self.x, self.y, other.x, other.y)
            return Centre_distance < self.radius +other.radius
        
   # creating shoot function  and using sound when fired
    def shoot(self):
            bullet = Bullet(self.x , self.y-25)
            self.bulletfired_sound.play()
            self.bulletfired_sound.rewind()
            self.bullets.append(bullet)
            
# Creating Gamelass with all the methods to run code inside            
class Game:
    def __init__(self):
        self.spaceship=Spaceship()     #instantiating Spacehsip classs
        self.Game = []           #list to record coin,asteroid,booster
        self.enemies = []        # list to record enemies
        self.score=0
        self.collision_sound=player.loadFile(path + "/collision.mp3")
        self.Gameover_sound=player.loadFile(path +"/Gameover.mp3")
        self.coincollision=player.loadFile(path + "/coin_collision.mp3")
        self.Booster_collision=player.loadFile(path + "/Booster_collision.mp3")
        self.enemykilled=0 
        self.booster=0
        self.lives=0
        self.bg_music=player.loadFile(path + "/music.mp3")
        self.bg_music.loop()
        self.game_over=False
        # self.update_lives()
        
# Updating lives if 4 boosters collected         
    def update_lives(self):
            self.lives = self.booster // 4
            if self.lives<0:
                self.lives=0
                
# keeoing track of score, enemy killed,livess and time and displaying it                
    def Score(self):
        textSize(30) 
        fill(255) 
        text("Score: " + str(self.score), 50, 50)
        text("Enemy Killed:" + str(self.enemykilled), 250,50)
        text("Lives:" + str(self.lives) , 500,50)
        text("Time:" + str(int(time.time() - start_time)), 650 , 50)
        if self.score<0:
            self.score=0
            
# adding objects to the screen        
    def Add_objects(self):
        # adding enemies to the screen 
            if len(self.enemies)<4:
                if random.random() < 0.1:    # probability
                    enemy = EnemySpaceship()
                    self.enemies.append(enemy)
        # adding Game to the screen
            if len(self.Game)<3:
                if random.random()<0.01:      # probability
                    booster=Booster()
                    self.Game.append(booster)
        # adding coin to the screen
                if random.random()<0.7:  # probability
                    coin=Coin()
                    self.Game.append(coin)
        # adding asteroid ro the screen
                else:
                    asteroid = Space_Objects()
                    self.Game.append(asteroid)

# updating     
    def update(self):
        if self.game_over:
            self.Gameover_sound.play()
            self.Gameover_sound.rewind()
            textSize(60) 
            fill(255) 
            text("GAME OVER" , 300,200)
            text("  Score: " + str(self.score), 300, 300)
            text("Enemies Killed:" + str(self.enemykilled), 260,400)
            fill(255,0,0)
            textSize(40)
            text("Play Again", 355,500)
            return
 
#   Terminating condiiton, time limit of 5 minutes      
        time_taken = time.time() - start_time 
        if time_taken > 300:  
            self.game_over = True  
            return
            
        self.spaceship.update() 
          
        for j in self.Game:
            j.update()
            if isinstance(j, Booster):
                j.Reset()
            if isinstance(j,Coin):
                j.Reset()
        
        for i, j in enumerate(self.Game):
            j.update()
            
# if object goes off screen remove them from the list
            if j.Off_Screen():
                self.Game.pop(i)
                continue
            for other in self.Game[i+1:]:
                if j.collision_detection(other):
                    if j.radius > other.radius:
                        self.Game.pop(self.Game.index(other))
                    else:
                        self.Game.pop(i)
                    break
# Instance method to keep track of difffrent space objects in the list, detecting collision            
            if isinstance(j,Coin) and self.spaceship.collision_detection(j):
                self.score += 100
                self.Score()
# Playing audio if collided
                self.coincollision.play()
                self.coincollision.rewind()
                self.Game.remove(j)

    # detcting collision betweene booster and spacehsip             
            elif isinstance(j,Booster) and self.spaceship.collision_detection(j):                    
                self.score += 100        
                self.Score()
                self.Booster_collision.play()
                self.Booster_collision.rewind()
                self.booster+=1
                self.update_lives()
                self.Game.remove(j)

#detecting collision between asteroid and spacehsip        
            elif self.spaceship.collision_detection(j):
                self.collision_sound.play()
                self.collision_sound.rewind()
                self.Game.remove(j)
                self.Score()
                self.score -= 100
            
#detecting collision between  spacehsip  and enemyspacehisp    
        for enemy in self.enemies:
            enemy.Reset()
            if self.spaceship.collision_detection(enemy):
                self.enemies.remove(enemy)
                self.update_lives()
                self.booster-=4
        # if player has life in his account, continue game
                if self.lives>0:
                    self.game_over= False
                else:
                    self.game_over = True
                self.Score()
                break

# #detecting collision between enemybullet and spacehsip  
            for bullet in enemy.bullets:
                if self.spaceship.collision_detection(bullet):
                    self.update_lives()
                    if self.lives>0:
                        self.game_over= False
                    else:
                        self.game_over = True
                    enemy.bullets.remove(bullet)
                    break
                    
            if enemy.is_Off_Screen():
                self.enemies.remove(enemy)
 
 #detecting collision between bullet.spaceship.bullets:
            for bullet in self.spaceship.bullets:
                if enemy.collision_detection(bullet):
                    self.score += 100 
                    self.enemies.remove(enemy)
                    self.spaceship.bullets.remove(bullet)
                    self.enemykilled+=1
                    self.Score()
                    break
                
 #detecting collision of enemy to other enemies                 
        for i, enemy in enumerate(self.enemies):
            for other in self.enemies[i+1:]:
                if enemy.collision_detection(other):
                    self.enemies.remove(other)  
            break

# displaying everything by this    function             
    def display(self):
        for asteroid in self.Game:
            asteroid.display()
            
        for enemy in self.enemies:
            enemy.display()
            
        self.spaceship.display()
        self.Score()

# instantiating main class
game = Game()

def setup():
    size(RESOLUTION_W, RESOLUTION_H)
    
#creating background scrolling effect 
    global img10 , img11 , img12
    img10=loadImage("background.jpg")
    img11=loadImage("background.jpg")
    img12 =loadImage("background.jpg")
    global img10_x , img11_x, img12_x ,speed
    img10_x=0
    img11_x=1200
    img12_x=-1200
    speed= 5

def draw():
    global game_started
    if not game_started:
        Start()
    else:
        global game, img10_x , img11_x , img12_x ,speed
        background(255)
        image(img10, img10_x, 0, 1200, 700)
        image(img11, img11_x, 0, 1200, 700)
        image(img12, img12_x, 0, 1200, 700)
    
        # Move the images to the left or right based on the scroll speed
        img10_x -= speed
        img11_x -= speed
        img12_x -= speed
    
        
        # If the first image goes off the screen to the left, move it to the right of the second image
        if img10_x < -1200:
            img10_x = img11_x+1190
        if img11_x < -1200:
            img11_x = img10_x+ 1190
    
        game.Add_objects()    
        game.display()
        game.update()
        
# Defining a function to handle keyboard events
def keyPressed():
    global speed
    if key == ' ': # Check if the spacebar is pressed
        if len(game.spaceship.bullets) < 4: # Check if the number of bullets is less than 4
            game.spaceship.shoot()  
    if keyCode == LEFT:
        speed= -20
    elif keyCode == RIGHT:
        speed= 20
        
    elif keyCode == UP:
        game.spaceship.keycode[UP] = True  
    
    elif keyCode == DOWN:
        game.spaceship.keycode[DOWN] = True  

def keyReleased():
    global speed
    speed=10
    if keyCode == UP:
        game.spaceship.keycode[UP] = False
    elif keyCode == DOWN:
        game.spaceship.keycode[DOWN] = False

# restart the gane when mouse is clicked 
def mouseClicked():
    global start_time
    global game
    game= Game()
    start_time=time.time()

    

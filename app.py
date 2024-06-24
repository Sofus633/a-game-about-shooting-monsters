# Pyxel S

import pyxel
import random

spritebank = {
    "caracter": {
        "player1" : [[[0, 24], [16, 16]],  [[16, 24], [16, 16]]]
        },
    
    "mob" : {
        "spider" : [[[0, 136], [-16, 16]], [[0+16, 136], [-16, 16]], [[0+16+16, 136], [-16, 16]], [[0+16+16+16, 136], [-16, 16]]],
        "bug"  : [[[128, 8], [-16, 16]], [[128+16, 8], [-16, 16]], [[128+16+16, 8], [-16, 16]], [[128+16+16+16, 8], [-16, 16]], [[128+16+16+16+16, 8], [-16, 16]], [[128+16+16+16+16+16, 8], [-16, 16]], [[128+16+16+16+16+16+16, 8], [-16, 16]], ]
        },
    
    "projectile": {
        "ammo" : [[[32, 56], [16, 16]], [[32+16, 56], [16, 16]], [[32+16, 56], [16, 16]], ]
        },
    "icon": {
        "icon" : [[48, 216], [16, 16]]
        }
    
}

mobslist = []
d_frame = 0 
score = 5000
life = 5
difficulty = 50
killcount = 0
objectif = 10
vague = 0
game = True

class Ball :
    def __init__(self, pos, sprite, bulletlist):
        self.position = pos
        self.sprite = sprite
        self.speed = 3
        self.bulletlist = bulletlist
        self.d_frame = pyxel.frame_count
        self.state = 0
    def show(self):
        pyxel.blt(self.position[0], self.position[1], 0, self.sprite[self.state][0][0], self.sprite[self.state][0][1], self.sprite[self.state][1][0], self.sprite[self.state][1][1], 5)
         
    def update(self):
        if pyxel.frame_count - self.d_frame >= 5:
            self.d_frame = pyxel.frame_count
            if self.state <= 1:
                self.state += 1
            else:
                self.state = 0
        if self.position[0] > 256 :
            self.bulletlist.remove(self)
        self.position[0] += self.speed
        


class Mob:
    def __init__(self, mobslist, mobtype):
        self.position = [256, random.randint(0, 220 - 16)]
        self.sprite = spritebank["mob"][mobtype]
        self.mobtype = mobtype
        self.list = mobslist
        self.speed = 1 if mobtype == "spider" else 2
        self.state = 0
        
    def show(self):
        pyxel.blt(self.position[0], self.position[1], 0, self.sprite[self.state][0][0], self.sprite[self.state][0][1], self.sprite[self.state][1][0], self.sprite[self.state][1][1], 5)

    def update(self):
        global life
        if self.position[0] < 0 :
            mobslist.remove(self)
            life -= 1
        self.position[0] -= self.speed
        
        nb_sprites = len(spritebank["mob"][self.mobtype])
        self.state = (pyxel.frame_count // 2) % nb_sprites





class Player:
    def __init__(self, pos):
        self.position = pos
        self.sprite = spritebank["caracter"]["player1"]
        self.ballsprite = spritebank["projectile"]["ammo"]
        self.alive = True
        self.projlist = []
        self.state = 0
        self.d_frame = pyxel.frame_count
        self.speed = 2
    
    def movements(self):
        if pyxel.btn(pyxel.KEY_Z):
            player.position[1] -= self.speed
            player.walk()

        if pyxel.btn(pyxel.KEY_D):
            player.position[0] += self.speed
            player.walk()

        if pyxel.btn(pyxel.KEY_S):
            player.position[1] += self.speed
            player.walk()

        if pyxel.btn(pyxel.KEY_Q):
            player.position[0] -= self.speed
            player.walk()

    def shoot(self):

        newball = Ball([self.position[0] + 5, self.position[1] + 5], self.ballsprite, self.projlist)
        self.projlist.append(newball)

    def walk(self):
        if pyxel.frame_count - self.d_frame >= 5:
            self.d_frame = pyxel.frame_count
            if self.state < 1:
                self.state += 1
            else:
                self.state = 0

    def draw(self):
        pyxel.blt(self.position[0], self.position[1], 0, self.sprite[self.state][0][0], self.sprite[self.state][0][1], self.sprite[self.state][1][0], self.sprite[self.state][1][1], 5)


class Menu:
    def __init__(): 
        






pyxel.init(256, 256)
player = Player([5, 50])




def main():
    pyxel.load("3_2.pyxres")
    
    
    
    
    
    pyxel.run(update, draw)
    



def update():
    global game
    if game == True:
        global d_frame
        global score
        global killcount
        global objectif
        global difficulty
        global life
        global mobslist
        global vague
        
        for mob in mobslist:
            for tir in player.projlist:
                if mob.position[0] <= tir.position[0]+1 and mob.position[0]+16 >= tir.position[0] and mob.position[1]+16 >= tir.position[1] and mob.position[1]<= tir.position[1]+8 :
                    try:
                        score += 25
                        killcount += 1 
                        mob.list.remove(mob)
                        tir.bulletlist.remove(tir)
                    except:
                        pass

        
        if life <= 0:
            life = 5
            game = False
            mobslist = []
            difficulty = 50
            killcount = 0
            objectif = 10

        if killcount == objectif:
            objectif += 10
            killcount = 0
            if difficulty > 0:
                print("WAVE", difficulty)
                difficulty -= 10
                vague += 1
        
        if pyxel.btn(pyxel.KEY_1):
            if score > 500:
                score -= 500
                player.speed += 0.2



        if random.randint(0,difficulty) == difficulty:
            newmob = Mob(mobslist,"spider" if random.randint(0, 1) or (vague < 2) else "bug")
            print(objectif, killcount)
            mobslist.append(newmob)
        


        player.movements()
        

        if player.position[0] >= 138:
            player.position[0] -= 4
        if player.position[0] <= 0:
            player.position[0] += 4
        if player.position[1] >= 248: 
            player.position[1] -= 4
        if player.position[1] <= 0:
            player.position[1] += 4

        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and pyxel.frame_count - d_frame >= 5 :
            score -= 5
            player.shoot()
            d_frame = pyxel.frame_count

        for proj in player.projlist:
            proj.update()

        for mob in mobslist:
            mob.update()




    if game == False:
        if pyxel.btn(pyxel.KEY_E):
            game = True



def draw():
    global game
    if game == True:
        pyxel.cls(0)
        y = 0
        pyxel.bltm(0, 0, 0, 0, 0, 256, 220)
        player.draw()
        for proj in player.projlist:
            proj.show()
        for mob in mobslist:
            mob.show()
        x = 20
        for i in range(life):
            x += 10
            pyxel.blt(x, 5, 0, 48, 216, 15, 15, 5)
        
        pyxel.text(10,10, str(score),0)
        pyxel.text(200,10, "vague : " + str(vague),0)
    if game == False:
        pyxel.text(256//2 - 60,256//2, "GameOver Press E to restart",0)
    

main()
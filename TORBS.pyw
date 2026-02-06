"""
Totally
Obligatory
Rectal
Battle
Simulator
------ controls
up/down arrow to select
space to play
e to stop
click to place
numbers to quick select


"""
import random
import math
import pygame
import copy
pygame.init()
import pygame.freetype
import os
directory = os.path.dirname(os.path.abspath(__file__))
files = os.listdir(os.path.join(directory, "campaigns"))
campaignsList = []
for i in files:
    thing = ""
    found = False
    for i2 in i:
        if i2 == ".":
            found = True
        if not found:
            thing += i2
    
    campaignsList.append(thing)
campaignsList.remove("__pycache__")
exec("import campaigns."+campaignsList[0]+" as levels")
levelsMax = len(campaignsList)
levelsIt = 0
campaignStorage = copy.deepcopy(levels.levels)

saveFile = open(os.path.join(directory,"saveData.txt"), "r")
saveData = []
for i in saveFile.readlines():
    if i[-1] == "\n":
        saveData.append(i[:-1])
    else:
        saveData.append(i)
#default save data
#0 1

#lists
keys = []
askee = ["SPACE","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
askeeVal = [32,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122]
colors = [(0,150,255), (255,0,0), (0,200,0), (255,175,100), (150,150,150), (150,100,0), (100, 0, 150), (255,255,255),(0,255,255)]
death = []
people = [] #[player, type, [hp,max hp], [x, y], timer, [extra]]
peopleStorage = []
peopleTemp = [
    [0, 0, [10,10], [0, 0], 0, [2, 2, 0, 0, 0,0,0,0]], #guy
    [0, 1, [10,10], [0, 0], 0, [2, 6, 0, 0, 0,0,0,0]], #sword
    [0, 2, [35,35], [0, 0], 0, [1, 2, 0, 0, 0,0,0,0]], #giant
    [0, 3, [10,10], [0, 0], 0, [2, 3, 10, 0, 0,0,0,0]], #bow
    [0, 4, [15,15], [0, 0], 0, [2, 2, 10, 0, 0,0,0,0]], #necromacer
    [0, 5, [15,15], [0, 0], 0, [2, 3, 25, 0, 0,0,0,0]], #angel
    [0, 6, [25,25], [0, 0], 0, [2, 2, 0, 0, 0,0,0,0]], #sheild
    [0, 7, [25,25], [0, 0], 0, [2, 6, 0, 0, 0,0,0,0]], #knight
    [0, 8, [12,12], [0, 0], 0, [2, 0, 0, 0, 0,0,0,0]], #wizard
    [0, 9, [5,5], [0, 0], 0, [4, 2, 0, 0, 0,0,0,0]], #halfing
    [0, 10, [10,10], [0, 0], 0, [1, 1, 0, 0, 0,0,0,0]], #minigun
    [0, 11, [10,10], [0, 0], 0, [1, 16, 10, 0, 0,0,0,0]],#sniper
    [0, 12, [50,50], [0, 0], 0, [5, 4, 10, 0, 0,0,0,0]],#john
    [0, 13, [35,35], [0, 0], 0, [1, 3, 0, 0, 0,0,0,0]],#ogre
    [0, 14, [15,15], [0, 0], 0, [2, 2, 25, 0, 0,0,0,0]],#fallen angel
    [0, 15, [10,10], [0, 0], 0, [1, 5, 0, 0, 0,0,0,0]],#canon
    [0, 16, [35,35], [0, 0], 0, [1, 2, 0, 0, 0,0,0,0]],#thorn giant
    [0, 17, [5,5], [0, 0], 0, [4, 1, 0, 0, 0,0,0,0]],#bomb
    [0, 18, [15,15], [0, 0], 0, [2, 0, 0, 0, 0,0,0,0]],#alchemist
    [0, 19, [12,12], [0, 0], 0, [1, 2, 10, 0, 0,0,0,0]],#morter
    [0, 20, [35,35], [0, 0], 0, [1, 0, 0, 0, 0,0,0,0]], #mother necromacer
    [0, 21, [10,10], [0, 0], 0, [1, 0, 0, 0, 0,0,0,0]], #chronomancer
    [0, 22, [12,12], [0, 0], 0, [2, 0, 0, 0, 0,0,0,0]], #ice wizard
    [0, 23, [20,20], [0, 0], 0, [2, 6, 0, 0, 0,0,0,0]], #crusader
    [0, 24, [10,10], [0, 0], 0, [2, 2, 0, 0, 0,0,0,0]], #lasso
    [0, 25, [35,35], [0, 0], 0, [1, 2, 0, 0, 0,0,0,0]], #giant rider
    [0, 26, [35,35], [0, 0], 0, [1, 1, 0, 0, 0,0,0,0]], #golem
    [0, 27, [10,10], [0, 0], 0, [2, 2, 10, 0, 0,0,0,0]], #engineer
    [0, 28, [10,10], [0, 0], 0, [2, 2, 10, 0, 0,0,0,0]], #cupid
    [0, 29, [10,10], [0, 0], 0, [3, 7, 0, 0, 0,0,0,0]], #spy
    [0, 30, [10,10], [0, 0], 0, [0, 0, 0, 0, 0,0,0,0]], #fan
    [0, 31, [250,250], [0, 0], 0, [1, 2, 0, 0, 0,0,0,0]], #fake knight
    [0, 32, [10,10], [0, 0], 0, [2, 3, 0, 0, 0,0,0,0]], #witch

]
peopleCost = [
    5,
    8,
    14,
    10,
    15,
    10,
    10,
    18,
    14,
    5,
    20,
    18,
    589384802,
    22,
    24,
    16,
    20,
    10,
    15,
    16,
    50,
    50,
    12,
    16,
    10,
    20,
    26,
    16,
    50,
    8,
    49,
    50,
    15,
]
peopleName = [
    "Guy", #0
    "Sword", #1
    "Giant", #2
    "Bow", #3
    "Necromacer", #4
    "Angel", #5
    "Sheild", #6
    "Knight", #7
    "Wizard", #8
    "Halfing", #9
    "Minigun", #10
    "Sniper", #11
    "John", #12
    "Ogre", #13
    "Fallen Angel", #14
    "Canon", #15
    "Thorn Giant", #16
    "Bomb", #17
    "Alchemist", #18
    "Morter", #19
    "Mother Necromancer", #20
    "Chronomancer", #21
    "Ice Wizard", #22
    "Crusader", #23
    "Lasso", #24
    "Giant Rider", #25
    "Golem", #26
    "Engineer", #27
    "Cupid", #28
    "Spy", #29
    "Fan", #30
    "Fake Knight Smoking A Blunt", #31
    "Witch", #32
]
peopleDesc = [
    ["Basic guy that runs at enemies","health - 10","damage - 2"], #0
    ["Guy with sword that slices enemies","health - 10","damage - 6"], #1
    ["Large brute that can tank heavy hits","health - 35","damage - 2"], #2
    ["Shoots from a range","health - 10","damage - 3"], #3
    ["Summons skeletons to fight for them","health - 15","damage - 0","skeleton health - 5","skeleton damage - 2"], #4
    ["Heals troops on your side","health - 15","heal - 3"], #5
    ["Guy with a sheild to tank damage","health - 25","damage - 2"], #6
    ["Guy with a sword and sheild to take hits and deal them too","health - 25","damage - 6"], #7
    ["Casts fireballs that damage multiple enemies","health - 12","splash damage - 2"], #8
    ["Small but agile guy, useful in swarms","health - 5","damage - 2"], #9
    ["Weilds a fast firing short range weapon","health - 10","damage - 1"], #10
    ["Long range weapon that packs a punch","health - 10","damage - 16"], #11
    ["j","health - 25","damage - 4","splash damage - 2","plinkaju health - 5","plinkaju damage - 5"], #12
    ["Launches enemies with its club","health - 35","damage - 3","knockback - 20"], #13
    ["Fires bouncing orbs and casts dark magic","health - 15","damage - 2","orb lifetime - 160","orb splash damage - 1"], #14
    ["Weilds a powerful canon that knocks enemies back","health - 10","damage - 5","giant damage - 7","knockback - 20"], #15
    ["Giant covered in thorns that stab attackers","health - 35","damage - 2","thorn damage - 2"], #16
    ["Runs and explodes on death","health - 5","damage - 1","death damage - 8"], #17
    ["Buffs troops on your team","health - 15","damage buff - 1"], #18
    ["Targets the farthest thing away from itself","health - 12","damage - 2","splash damage - 2"], #19
    ["Mega necromacer","health - 35","damage - 0"], #20
    ["Freezes everybody periodically","health - 10","damage - 2"], #21
    ["Freezes enemies it attacks","health - 12","splash damage - 1"], #22
    ["Heals itself when it kills an enemy","health - 10","damage - 6"], #23
    ["pulls enemies closer to itself","health - 10","damage - 2"], #24
    ["Giant with a sword on its back","health - 35","damage - 2","sword health - 10","sword damage - 6"], #25
    ["Large rock beast that splits on death","health - 35","damage - 1"], #26
    ["Large rock beast that splits on death","health - 10","damage - 0","sentry health - 10","sentry damage - 1"], #27
    ["Shoots from a range and hypnotizes","health - 10","damage - 2"], #28
    ["Sneaks into enemy lines","health - 10","damage - 2","sneak damage - 7"], #29
    ["It blows","health - 10","blow job - 5"], #30
    ["he","health - 250","head - 5"], #31
    ["Turns people into frogs","health - 10","damage - 3","frog health - 5","frog damage - 2"], #32
]
sprite_table = {
    0: "guy.png", #0
    1: "sword.png", #1
    2: "giant.png", #2
    3: "bow.png",
    4: "necromacer.png",
    4.1: "skeleton.png",
    5: "angel.png",
    6:"sheild.png",
    7: "knight.png",
    8:"wizard.png",
    9:"halfing.png",
    10: "minigun.png",
    11: "sniper.png",
    12: "john.png",
    12.1: "plinkaju.png",
    13: "ogre.png",
    14: "fallen_angel.png",
    14.1: "blank.png",
    15: "canon.png",
    16: "thorn_giant.png",
    17: "bomb.png",
    18: "alchemist.png",
    19: "morter.png",
    20: "mother_necromacer.png",
    21: "chronomancer.png",
    22: "ice_wizard.png",
    23: "crusader.png",
    24: "lasso.png",
    25: "sword_giant.png",
    26: "golem_big.png",
    26.1: "golem_med.png",
    26.2: "golem_small.png",
    27: "engineer.png",
    27.1: "sentry.png",
    28: "cupid.png",
    29.1: "spy.png",
    29: "spy_hidden.png",
    30: "fan.png",
    31: "fake_knight.png",
    32: "witch.png",
    32.1: "frog.png",
}
peopleMelee = [0,1,2,4.1,6,7,9,12.1,13,16,17,23,25,26,26.1,26.2,29.1,31,32.1]
peopleGiant = [2,13,16,20,25]
peopleSupport = [5, 18]
peopleCheat = [20,21,28,30,31]
peopleRedundant = [14.1,27.1]
unlocked = copy.deepcopy(levels.unlocked)
peopleAllowed = unlocked
#vars

goodfont = "Acme-Regular.ttf"
badfont = "devious-font.ttf"
font = pygame.freetype.Font(os.path.join(directory, goodfont), 30)

moneyList = [50,100,150,200,500,999999999]
startMoneyIt = 1
campaign = True

#sounds
exec(f"isMute = {saveData[9]}")
sfx = os.path.join(directory, "sfx")
pygame.mixer.music.load(f"{sfx}\\music.mp3")

Shit1 = pygame.mixer.Sound(f"{sfx}\\hit1.wav")
Shit2 = pygame.mixer.Sound(f"{sfx}\\hit2.wav")
Shit3 = pygame.mixer.Sound(f"{sfx}\\hit3.wav")
Sbow = pygame.mixer.Sound(f"{sfx}\\bow1.wav")
Sdeath1 = pygame.mixer.Sound(f"{sfx}\\death1.wav")
Sdeath2 = pygame.mixer.Sound(f"{sfx}\\death2.wav")
Sdeath3 = pygame.mixer.Sound(f"{sfx}\\death3.wav")
Sfireball = pygame.mixer.Sound(f"{sfx}\\fireball.wav")
Siceball = pygame.mixer.Sound(f"{sfx}\\iceball.wav")
SfallenAngelDeath = pygame.mixer.Sound(f"{sfx}\\fallenAngelDeath.wav")
SorbDeath = pygame.mixer.Sound(f"{sfx}\\orbDeath.wav")
Splace = pygame.mixer.Sound(f"{sfx}\\place.wav")
Sdelete = pygame.mixer.Sound(f"{sfx}\\delete.wav")

sounds = [Shit1,Shit2,Shit3,Sbow,Sdeath1,Sdeath2,Sdeath3,Splace,Sdelete,Sfireball,Siceball,SorbDeath,SfallenAngelDeath]
for i in sounds:
    i.set_volume(0.25 * int(isMute))

pygame.mixer.music.play(-1,0)
pygame.mixer.music.set_volume(0.5 * int(isMute))


pygame.mouse.set_visible(0)
startMoney = 100
money1 = startMoney
money2 = startMoney

Cgreen = 2
Cskin = 3
Cgrey = 4
Cbrown = 5
Cpurple = 6
Cwhite = 7
Cteal = 8
exec(f"level = {saveData[1]}[levels.name]")
exec(f"levelData = {saveData[1]}")
exec(f"frameRate = {saveData[8]}")
menu = 0
submenu = 2
team = 0
playing = True
cheat = int(saveData[0])
exec(f"healthNums = {saveData[10]}")
exec(f"deathNums = {saveData[11]}")
numList = []
selecting = 0
#controls
exec(f"Kstart = {saveData[2]}")
exec(f"Kend = {saveData[3]}")
exec(f"Kleave = {saveData[4]}")
exec(f"Kdelete = {saveData[5]}")
exec(f"Kwipe = {saveData[6]}")
exec(f"Kmute = {saveData[7]}")

#buttons
startButton = pygame.Rect(300,300,400,300)

button1 = pygame.Rect(100,100,300,200)
button1b = pygame.Rect(100,350,300,150)


button2 = pygame.Rect(600,100,300,200)
button2b = pygame.Rect(600,350,300,150)

cheatButton = pygame.Rect(400,550,200,125)
settingsButton = pygame.Rect(0,600,100,100)
textureButton = pygame.Rect(900,600,100,100)

window = pygame.display.set_mode([1000,700],pygame.RESIZABLE)
w = pygame.Surface([1000,700])
c = pygame.time.Clock()
#cache
#sprite = pygame.image.load(os.path.join(directory, "sprites\\"+name))
sprite_cache = {}
spritePacks = os.listdir(os.path.join(directory, "sprites"))
spritePack = "vanilla"
exec(f"import sprites.{spritePack}.data as spriteData")
spritePackIt = 1

sprites = os.listdir(os.path.join(directory, f"sprites\\{spritePack}"))
for i in sprites:
    if i != "data.py" and i != "__pycache__":
        sprite_cache[i] = pygame.image.load(os.path.join(directory, f"sprites\\{spritePack}\\{i}")).convert_alpha()
pygame.display.set_icon(sprite_cache["icon.png"])
pygame.display.set_caption("TORBS")
#functions
def Mousepos():
    Mx, My = pygame.mouse.get_pos()
    Mx *= 1000/nwid
    My *= 700/nhei
    return (Mx,My)
def save(file):
    text = ""
    text += str(cheat) + "\n"
    text += str(levelData) + "\n"
    text += str(Kstart) + "\n"
    text += str(Kend) + "\n"
    text += str(Kleave) + "\n"
    text += str(Kdelete) + "\n"
    text += str(Kwipe) + "\n"
    text += str(Kmute) + "\n"
    text += str(frameRate) + "\n"
    text += str(pygame.mixer.music.get_volume() > 0) + "\n"
    text += str(healthNums) + "\n"
    text += str(deathNums) + "\n"
    file.write(text)
def printPpl():
    toPrint = '["Level # - desc",\n20,\n[\n'
    for i in people:
        toPrint += str(i)+",\n"
    toPrint += '],\n[], #unlocks\n[], #restrictions\n],\n'
    print(toPrint)
def getDistance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
def drawSprite(name, pos, adjust,tint=False,red=0,alpha=255):
    x, y = pos
    sprite = sprite_cache[name].copy()
    if tint:
        sprite.fill((0, 50, 100), special_flags=pygame.BLEND_RGB_ADD)
    stren = max(1, 255 - red)
    sprite.fill((255, stren, stren), special_flags=pygame.BLEND_MULT)
    if adjust:
        w.blit(sprite, (x-125,y-125))
    else:
        w.blit(sprite, (x,y))
def drawChar(typ, pos, bonus):
    x, y = pos
    pygame.draw.circle(w, (255,175,0), pos, int(bonus[3])*((typ in peopleGiant) +1) )
    pygame.draw.circle(w, colors[Cteal], pos, int(bonus[5])*((typ in peopleGiant) +1) )

    tint = False
    if bonus[6] > 0:
        drawSprite("snowflake.png", (x,y),True)
        tint = True

    match typ:
        case 3:
            pygame.draw.circle(w, colors[Cwhite], pos, int(bonus[2]*2), 10)
        case 4:
            pygame.draw.circle(w, colors[Cteal], (x+35, y-25), int(bonus[2]))
        case 5:
            pygame.draw.circle(w, colors[Cwhite], pos, int(bonus[2]))
        case 10:
            pygame.draw.circle(w, colors[Cwhite], pos, int(bonus[2]*2), 10)
        case 11:
            pygame.draw.circle(w, colors[Cwhite], pos, int(bonus[2]*2), 10)
        case 12:
            pygame.draw.circle(w, colors[Cwhite], pos, int(bonus[2]), 10)
        case 14:
            pygame.draw.circle(w, (255,0,0), pos, int(bonus[2]))
        case 14.1:
            drawSprite(random.choice(["orb1.png","orb2.png","orb3.png"]), (x,y),True)
        case 15:
            pygame.draw.circle(w, colors[Cwhite], pos, int(bonus[2]*2), 10)
        case 19:
            pygame.draw.circle(w, colors[Cwhite], pos, int(bonus[2]*2), 10)
        case 20:
            pygame.draw.circle(w, colors[Cteal], (x+65, y-35), int(bonus[2]))
        case 23:
            pygame.draw.circle(w, colors[Cwhite], pos, int(bonus[2]))
        case 24:
            pygame.draw.circle(w, colors[Cwhite], pos, int(bonus[2]*2), 10)
        case 27:
            pygame.draw.circle(w, colors[Cwhite], pos, int(bonus[2]*2), 10)
        case 27.1:
            pygame.draw.circle(w, colors[Cwhite], pos, int(bonus[2]*2), 10)
        case 28:
            pygame.draw.circle(w, colors[Cwhite], pos, int(bonus[2]*2), 10)
        case 32:
            pygame.draw.circle(w, colors[Cwhite], pos, int(bonus[2]*2), 10)
        case default:
            pass
    drawSprite(sprite_table[typ], (x,y),True,tint,bonus[7])
def draw():
    Mx, My = Mousepos()
    if menu == 0:
        pygame.display.set_caption("TORBS - Menu")
        drawSprite("menu.png", (0,0), False)
        font.size = 60
        if submenu == 0:
            
            color = (200,200,200)#button 1
            if button1.collidepoint(Mx,My):
                color = (220,220,220)
            pygame.draw.rect(w, color, button1)
            font.render_to(w, (200,175), "PvP")
            
            color = (200,200,200)
            if button1b.collidepoint(Mx,My):
                color = (220,220,220)
            pygame.draw.rect(w, color, button1b)
            font.render_to(w, (200,400), str(startMoney)+"$")
            
            
            color = (200,200,200)#button 2
            if button2.collidepoint(Mx,My):
                color = (220,220,220)
            pygame.draw.rect(w, color, button2)
            font.render_to(w, (625,175), "Campaign")
            
            color = (200,200,200)
            if button2b.collidepoint(Mx,My):
                color = (220,220,220)
            pygame.draw.rect(w, color, button2b)
            font.render_to(w, (625,400), levels.name)
            
            color = (200,200,200)
            if cheatButton.collidepoint(Mx,My):
                color = (220,220,220)
            pygame.draw.rect(w, color, cheatButton)
            font.render_to(w, (400,600), "Save")
            
            font.fgcolor = (0,0,0)
            
            color = (200,200,200)
            if settingsButton.collidepoint(Mx,My):
                color = (220,220,220)
            pygame.draw.rect(w, color, settingsButton)

            color = (200,200,200)
            if textureButton.collidepoint(Mx,My):
                color = (220,220,220)
            pygame.draw.rect(w, color, textureButton)
            font.size = 15
            font.render_to(w, (920,620), spriteData.name)
            font.size = 60
        elif submenu == 1:
            
            color = (200,200,200)
            nowrect = pygame.Rect(900,0,100,100) #exit
            if nowrect.collidepoint(Mx,My):
                color = (220,220,220)
            pygame.draw.rect(w, color, nowrect)
            
            if deathNums:
                color = (0,200,0)
            else:
                color = (200,200,200)
            nowrect = pygame.Rect(800,0,100,100) #death nums
            if nowrect.collidepoint(Mx,My):
                if deathNums:
                    color = (20,220,20)
                else:
                    color = (220,220,220)
            pygame.draw.rect(w, color, nowrect)
            font.size = 12
            font.render_to(w, (800,50), "Damage Numbers")

            if healthNums:
                color = (0,200,0)
            else:
                color = (200,200,200)
            nowrect = pygame.Rect(700,0,100,100) #health nums
            if nowrect.collidepoint(Mx,My):
                if healthNums:
                    color = (20,220,20)
                else:
                    color = (220,220,220)
            pygame.draw.rect(w, color, nowrect)
            font.size = 12
            font.render_to(w, (700,50), "Detailed Health")

            font.size = 30
            font.render_to(w, (0,0), "Click a button while holding down new keybind")
            
            color = (200,200,200)#--------------------------------------------------------------------
            nowrect = pygame.Rect(0,100,1000,100) #start game
            if nowrect.collidepoint(Mx,My):
                color = (220,220,220)
            pygame.draw.rect(w, color, nowrect)
            font.render_to(w, (0,150),"start game")
            font.render_to(w, (900,150),askee[askeeVal.index(Kstart)])
            color = (200,200,200)#--------------------------------------------------------------------
            nowrect = pygame.Rect(0,200,1000,100) #end game
            if nowrect.collidepoint(Mx,My):
                color = (220,220,220)
            pygame.draw.rect(w, color, nowrect)
            font.render_to(w, (0,250),"end game")
            font.render_to(w, (900,250),askee[askeeVal.index(Kend)])
            color = (200,200,200)#--------------------------------------------------------------------
            nowrect = pygame.Rect(0,300,1000,100) #quit menu
            if nowrect.collidepoint(Mx,My):
                color = (220,220,220)
            pygame.draw.rect(w, color, nowrect)
            font.render_to(w, (0,350),"quit to menu")
            font.render_to(w, (900,350),askee[askeeVal.index(Kleave)])
            color = (200,200,200)#--------------------------------------------------------------------
            nowrect = pygame.Rect(0,400,1000,100) #delete
            if nowrect.collidepoint(Mx,My):
                color = (220,220,220)
            pygame.draw.rect(w, color, nowrect)
            font.render_to(w, (0,450),"delete troop")
            font.render_to(w, (900,450),askee[askeeVal.index(Kdelete)])
            color = (200,200,200)#--------------------------------------------------------------------
            nowrect = pygame.Rect(0,500,1000,100) #wipe
            if nowrect.collidepoint(Mx,My):
                color = (220,220,220)
            pygame.draw.rect(w, color, nowrect)
            font.render_to(w, (0,550),"delete all")
            font.render_to(w, (900,550),askee[askeeVal.index(Kwipe)])
            color = (200,200,200)#--------------------------------------------------------------------
            nowrect = pygame.Rect(0,600,1000,100) #delete
            if nowrect.collidepoint(Mx,My):
                color = (220,220,220)
            pygame.draw.rect(w, color, nowrect)
            font.render_to(w, (0,650),"mute")
            font.render_to(w, (900,650),askee[askeeVal.index(Kmute)])
        elif submenu == 2:
            color = (200,200,200)#start
            if startButton.collidepoint(Mx,My):
                color = (220,220,220)
            pygame.draw.rect(w, color, startButton)
            font.render_to(w, (445,425), "Play!")
        drawSprite("mouse.png",(Mx,My),False)

    else:
        Mx, My = Mousepos()
        drawSprite("ground.png", (0,0), False)
        if menu == 1:
            pygame.display.set_caption("TORBS - Preperation")
            pygame.draw.line(w, colors[0], (495,0),(495,700), 10)
            pygame.draw.line(w, colors[1], (505,0),(505,700), 10)
        if menu == 2:
            pygame.display.set_caption("TORBS - Battle")
            surface = pygame.Surface((1000,700), pygame.SRCALPHA)
            for i in death:
                if i[0] == "boom":
                    pygame.draw.circle(w, (255,150,0), (i[1][0],i[1][1]), i[2] )
                else:
                    if i[3] == 4.1:
                        pygame.draw.circle(surface, (0,0,255,i[2]), (i[0][0],i[0][1]), i[1] )
                    elif i[3] == 14 or i[3] == 26 or i[3] == 26.1 or i[3] == 26.2:
                        pygame.draw.circle(surface, (0,0,0,i[2]), (i[0][0],i[0][1]), i[1] )
                    else:
                        pygame.draw.circle(surface, (255,0,0,i[2]), (i[0][0],i[0][1]), i[1] )
            w.blit(surface, (0,0))
        
        money1Spent = 0
        money2Spent = 0
        for i in people:
            drawChar(i[1], i[3], i[5])
            healthPerc = (i[2][0]/i[2][1])
            if i[0] == 0:
                if i[1] == int(i[1]):
                    money1Spent += peopleCost[i[1]]
                pygame.draw.line(w, (0,100,200), (i[3][0]-35,i[3][1]-35), (i[3][0]+35,i[3][1]-35), 5)
                pygame.draw.line(w, colors[0], (i[3][0]-35,i[3][1]-35), (i[3][0]+round(70*healthPerc)-35,i[3][1]-35), 5)
            else:
                if i[1] == int(i[1]):
                    money2Spent += peopleCost[i[1]]
                pygame.draw.line(w, (150,0,0), (i[3][0]-35,i[3][1]-35), (i[3][0]+35,i[3][1]-35), 5)
                pygame.draw.line(w, colors[1], (i[3][0]-35,i[3][1]-35), (i[3][0]+round(70*healthPerc)-35,i[3][1]-35), 5)
            if menu == 2 and healthNums:
                font.fgcolor = (0,0,0)
                font.size = 15
                font.render_to(w, (i[3][0]-15,i[3][1]-50),f"{i[2][0]}/{i[2][1]}")
        totalSpent = money1Spent + money2Spent
        if menu == 2:
            pygame.draw.line(w,colors[1],(0,0),(1000,0),10)
            if money2Spent == 0:
                pygame.draw.line(w,colors[0],(0,0),(1000,0),10)
            else:
                pygame.draw.line(w,colors[0],(0,0),(  int( (money1Spent/totalSpent) *1000)  ,0),10)
                drawSprite("combat.png",(  int( (money1Spent/totalSpent) *1000)-25  ,0),False)
            if deathNums:
                for i in numList:
                    if i[3] < 7:
                        font.fgcolor = (0,0,0)
                        font.size = 15
                    elif i[3] < 12:
                        font.fgcolor = (150,0,0)
                        font.size = 15
                    elif i[3] >= 12:
                        font.fgcolor = (255,0,0)
                        font.size = 30
                    font.render_to(w, i[1], i[0])
        if menu == 1:
            if not Kdelete in keys:
                drawChar(selecting, (Mx, My), [2, 2, 10, 0, 0, 0, 0,0])
            
            #text
            font.fgcolor = (0,0,0)
            font.size = 30
            font.render_to(w, (0,0), str(money1)+"$")
            font.render_to(w, (0,30), "costs "+str(peopleCost[selecting])+"$")
            font.render_to(w, (0,60), str(peopleName[selecting]))
            if campaign:
                font.render_to(w, (520,0), levels.levels[level-1][0])
                if len(levels.levels[level-2][3]) > 0:
                    font.render_to(w, (590,670), "You have new troops!")
            else:
                font.render_to(w, (520,0), str(money2)+"$")
            
            team1amount = 0
            team2amount = 0
            for i in people:
                if i[0] == 1:
                    team2amount += 1
                else:
                    team1amount += 1
            font.render_to(w, (0,670), str(team1amount))
            font.render_to(w, (520,670), str(team2amount))
            
            font.size = 15
            line = 1
            for i in peopleDesc[selecting]:
                font.render_to(w, (520,30*line), str(i))
                line += 1
            if campaign:
                if len(levels.levels[level-1][4]) > 0:
                    font.render_to(w, (0,100), "Troop selection limited")
                    
            if cheat:
                font.render_to(w,(400,0),"Cheats enabled!")
            if Kdelete in keys:
                drawSprite("mouse_delete.png",(Mx,My),False)
            else:
                drawSprite("mouse_grab.png",(Mx-15,My-25),False)
    window.blit(pygame.transform.scale(w, (nwid,nhei)), (0,0))
    pygame.display.flip()

#GAMEPLAY LOOP------------------------------------------------------------------------------------------------------------------
while playing:
    timePass = c.get_time()/1000
    deltaTime = timePass * 30
    nwid, nhei = window.get_size()
    
    Mx, My = Mousepos()
    mouse = False
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            playing = False
        elif i.type == pygame.KEYDOWN:
            keys.append(i.key)
            
            if submenu == 0:
                if i.key == Kmute:
                    if pygame.mixer.music.get_volume() > 0:
                        pygame.mixer.music.set_volume(0)
                        for i2 in sounds:
                            i2.set_volume(0)
                    else:
                        pygame.mixer.music.set_volume(0.5)
                        for i2 in sounds:
                            i2.set_volume(0.5)
                
                if i.key == pygame.K_UP:# cycle up
                    selecting += 1
    
                    while ((not selecting in peopleAllowed) and campaign) or (selecting in peopleCheat and not cheat): #campaign
                        selecting += 1
                        if selecting >= len(peopleTemp):
                            selecting = 0
                    if selecting >= len(peopleTemp):
                        selecting = 0
                            
                if i.key == pygame.K_DOWN: #cycle down
                    selecting -= 1
                    while ((not selecting in peopleAllowed) and campaign) or (selecting in peopleCheat and not cheat): #campaign
                        selecting -= 1
                        if selecting <= -1:
                            selecting = len(peopleTemp)-1
                    if selecting <= -1:
                        selecting = len(peopleTemp)-1
                        
                if i.key == Kleave:
                    if menu == 0:
                        saveDataW = open(os.path.join(directory,"saveData.txt"), "w")
                        save(saveDataW)
                        saveDataW.close()
                        playing = False
                    elif menu != 2:
                        levels.levels = copy.deepcopy(campaignStorage)
                        menu = 0
                        submenu = 0
                    
                        
                if i.key == pygame.K_o and cheat:
                    for i2 in levels.levels[level-1][3]:
                        unlocked.append(i2)
                    level += 1
                    people = levels.levels[level-1][2]
                    money1 = levels.levels[level-1][1]
                    money2 = 0
                    if len(levels.levels[level-1][4]) == 0:
                        peopleAllowed = unlocked
                    else:
                        peopleAllowed = levels.levels[level-1][4]
                    selecting = copy.deepcopy(peopleAllowed[0])
                        
                if i.key == pygame.K_p and cheat:
                    money1 += 3294572984758
                    money2 += 3294572984758
                if i.key == pygame.K_l:
                    printPpl()
                if i.key == Kwipe:
                    remove = []
                    team = Mx > 500
                    if team == 0 or not campaign:
                        if menu == 1:
                            for i in people:
                                if ((i[1] in peopleAllowed and campaign and team == 0) or (not campaign)) and i[0] == team:
                                    remove.append(i)
                        for i in remove:
                            if i[0] == 0:
                                money1 += peopleCost[i[1]]
                            else:
                                money2 += peopleCost[i[1]]
                            people.remove(i)
            elif submenu == 2 and i.key == Kleave:
                playing = False
            elif i.key == pygame.K_LEFTBRACKET:
                window = pygame.display.set_mode((1000,700),pygame.RESIZABLE)
            elif i.key == pygame.K_RIGHTBRACKET:
                window = pygame.display.set_mode((500,350),pygame.RESIZABLE)
                
                
        elif i.type == pygame.KEYUP:
            if i.key in keys:
                keys.remove(i.key)
        elif i.type == pygame.MOUSEBUTTONDOWN:
            mouse = True
    #menu
    if menu == 0:
        if submenu == 0:
            if button1.collidepoint(Mx,My) and mouse:
                menu = 1
                campaign = False
                money1 = startMoney
                money2 = startMoney
                mouse = False
                people = []
            if button1b.collidepoint(Mx,My) and mouse:
                startMoneyIt += 1
                if startMoneyIt >= len(moneyList):
                    startMoneyIt = 0
                startMoney = moneyList[startMoneyIt]
            if button2.collidepoint(Mx,My) and mouse:
                menu = 1
                campaign = True
                people = levels.levels[level-1][2]
                money1 = levels.levels[level-1][1]
                money2 = 0
                mouse = False
                if len(levels.levels[level-1][4]) == 0:
                    peopleAllowed = unlocked
                else:
                    peopleAllowed = levels.levels[level-1][4]
                selecting = copy.deepcopy(peopleAllowed[0])
            if button2b.collidepoint(Mx,My) and mouse:
                levelsIt += 1
                if levelsIt >= levelsMax:
                    levelsIt = 0
                exec("import campaigns."+campaignsList[levelsIt]+" as levels")
                exec(f"allow = levels.name in {saveData[1]}")
                if not allow:
                    saveDataW = open(os.path.join(directory,"saveData.txt"), "w")
                    exec("levelData["+"'"+levels.name+"'"+"] = 1")
                    save(saveDataW)
                    saveDataW.close()
                    saveFile = open(os.path.join(directory,"saveData.txt"), "r")
                    saveData = []
                    for i in saveFile.readlines():
                        if i[-1] == "\n":
                            saveData.append(i[:-1])
                        else:
                            saveData.append(i)
                exec(f"level = {saveData[1]}[levels.name]")

                campaignStorage = copy.deepcopy(levels.levels)
                unlocked = copy.deepcopy(levels.unlocked)
            if cheatButton.collidepoint(Mx,My) and mouse:
                saveDataW = open(os.path.join(directory,"saveData.txt"), "w")
                save(saveDataW)
                saveDataW.close()
            if settingsButton.collidepoint(Mx,My) and mouse:
                submenu = 1
            if textureButton.collidepoint(Mx,My) and mouse:
                spritePackIt += 1
                if spritePackIt >= len(spritePacks):
                    spritePackIt = 0
                #reset to vanilla
                spritePack = "vanilla"
                exec(f"import sprites.{spritePack}.data as spriteData")
                sprites = os.listdir(os.path.join(directory, f"sprites\\{spritePack}"))
                for i in sprites:
                    if i != "data.py" and i != "__pycache__":
                        sprite_cache[i] = pygame.image.load(os.path.join(directory, f"sprites\\{spritePack}\\{i}")).convert_alpha()
                #update
                spritePack = spritePacks[spritePackIt]
                sprites = os.listdir(os.path.join(directory, f"sprites\\{spritePack}"))
                spriteDataName = os.path.join(directory, f"{spritePacks}\\{spritePack}\\data.py")
                exec(f"import sprites.{spritePack}.data as spriteData")
                for i in sprites:
                    if i != "data.py" and i != "__pycache__":
                        sprite_cache[i] = pygame.image.load(os.path.join(directory, f"sprites\\{spritePack}\\{i}")).convert_alpha()
                #end
        elif submenu == 1:
            if pygame.Rect(900,0,100,100).collidepoint(Mx,My) and mouse:
                submenu = 0

            if pygame.Rect(800,0,100,100).collidepoint(Mx,My) and mouse:
                deathNums = not deathNums

            if pygame.Rect(700,0,100,100).collidepoint(Mx,My) and mouse:
                healthNums = not healthNums
                
            if pygame.Rect(0,100,1000,100).collidepoint(Mx,My) and mouse and len(keys) > 0:
                if keys[0] in askeeVal:
                    Kstart = keys[0]
            elif pygame.Rect(0,200,1000,100).collidepoint(Mx,My) and mouse and len(keys) > 0:
                if keys[0] in askeeVal:
                    Kend = keys[0]
            elif pygame.Rect(0,300,1000,100).collidepoint(Mx,My) and mouse and len(keys) > 0:
                if keys[0] in askeeVal:
                    Kleave = keys[0]
            elif pygame.Rect(0,400,1000,100).collidepoint(Mx,My) and mouse and len(keys) > 0:
                if keys[0] in askeeVal:
                    Kdelete = keys[0]
            elif pygame.Rect(0,500,1000,100).collidepoint(Mx,My) and mouse and len(keys) > 0:
                if keys[0] in askeeVal:
                    Kwipe = keys[0]
            elif pygame.Rect(0,600,1000,100).collidepoint(Mx,My) and mouse and len(keys) > 0:
                if keys[0] in askeeVal:
                    Kmute = keys[0]
        elif submenu == 2:
            if startButton.collidepoint(Mx,My) and mouse:
                submenu = 0
        
    #placing
    if menu == 1:
        if mouse:#place
            plr, typ, hp, pos, timer, bonus = peopleTemp[selecting]
            plr = Mx >= 500
            pos = [Mx, My]
            #v place v
            if campaign:
                if (plr == 0 and money1 >= peopleCost[selecting]):
                    people.append([plr, typ, hp, pos, timer, bonus])
                    Splace.play()
                    money1 -= peopleCost[selecting]
            else:
                if (plr == 0 and money1 >= peopleCost[selecting]) or (plr == 1 and money2 >= peopleCost[selecting]):
                    Splace.play()
                    people.append([plr, typ, hp, pos, timer, bonus])
                    if plr == 0:
                        money1 -= peopleCost[selecting]
                    if plr == 1:
                        money2 -= peopleCost[selecting]
            

                    
        if Kdelete in keys:#delete
            for i in people:
                if getDistance(i[3], (Mx,My)) < 25:
                    if i[0] == 0 and (i[1] in peopleAllowed or not campaign):
                        money1 += peopleCost[i[1]]
                        people.remove(i)
                        Sdelete.play()
                    elif i[0] == 1 and not campaign:
                        money2 += peopleCost[i[1]]
                        people.remove(i)
                        Sdelete.play()
        if Kstart in keys:#start
            random.seed(1)
            peopleStorage = copy.deepcopy(people)
            menu = 2
        #better select
        startSelect = selecting
        if pygame.K_0 in keys: #better select
            if pygame.K_1 in keys:
                selecting = 1
            elif pygame.K_2 in keys:
                selecting = 2  
            elif pygame.K_3 in keys:
                selecting = 3
            elif pygame.K_4 in keys:
                selecting = 4
            elif pygame.K_5 in keys:
                selecting = 5
            elif pygame.K_6 in keys:
                selecting = 6
            elif pygame.K_7 in keys:
                selecting = 7
            elif pygame.K_8 in keys:
                selecting = 8
            elif pygame.K_9 in keys:
                selecting = 9
            else:
                selecting = 0
        elif pygame.K_1 in keys: 
            if pygame.K_2 in keys:
                selecting = 12
            elif pygame.K_3 in keys:
                selecting = 13
            elif pygame.K_4 in keys:
                selecting = 14
            elif pygame.K_5 in keys:
                selecting = 15
            elif pygame.K_6 in keys:
                selecting = 16
            elif pygame.K_7 in keys:
                selecting = 17
            elif pygame.K_8 in keys:
                selecting = 18
            elif pygame.K_9 in keys:
                selecting = 19
        elif pygame.K_2 in keys: 
            if pygame.K_3 in keys:
                selecting = 23
            elif pygame.K_4 in keys:
                selecting = 24
            elif pygame.K_5 in keys:
                selecting = 25
            elif pygame.K_6 in keys:
                selecting = 26
            elif pygame.K_7 in keys:
                selecting = 27
            elif pygame.K_8 in keys:
                selecting = 28
            elif pygame.K_9 in keys:
                selecting = 29
        if selecting > len(peopleTemp)-1:
            selecting = len(peopleTemp)-1
        if (not selecting in peopleAllowed) and campaign:
            selecting = startSelect
    #fighting
    elif menu == 2:
        if Kend in keys:
            menu = 1
            win = True
            for i in people:
                if i[0] == 1 and not i[1] in peopleRedundant:
                    win = False
            if win and campaign:
                for i in levels.levels[level-1][3]:
                    unlocked.append(i)
                level += 1
                people = levels.levels[level-1][2]
                money1 = levels.levels[level-1][1]
                money2 = 0
                levelData[levels.name] = level
                if len(levels.levels[level-1][4]) == 0:
                    peopleAllowed = unlocked
                else:
                    peopleAllowed = levels.levels[level-1][4]
                selecting = copy.deepcopy(peopleAllowed[0])
            else:
                people = copy.deepcopy(peopleStorage)
            death = []
            numlist = []
            #money1 = startMoney
            #money2 = startMoney
            
        #code for people
        toRemove = []
        toAdd = []
        for i in people:
            plr, typ, hp, pos, timer, bonus = i
            hitbox = 40
            if bonus[6] <= 0:
                timer += timePass
            bonus[7] -= 20 * deltaTime
            if bonus[7] < 0:
                bonus[7] = 0
            target = [[1,1],[1,1],[1,1],[1,1],[1,1],[1,1,1,1,1,1,1,1,1]]
            tarDist = 1000 - ((i[1]==19)*1000)
            for i2 in people:
                dist = getDistance(pos, i2[3])
                if (( dist < tarDist and i2[0] == (not plr) )) and not i2[1] in [14.1,29] and i[1] != 19:
                    if not i[1] in peopleSupport:
                        tarDist = dist
                        target = i2
                if (( dist > tarDist and i2[0] == (not plr) )) and i[1] == 19:
                    if not i[1] in peopleSupport:
                        tarDist = dist
                        target = i2
                if (( dist < tarDist and i2[0] == (plr) and i[1] in peopleSupport and not i2[1] in peopleSupport)) and not i2[1] in [14.1,29]:
                    tarDist = dist
                    target = i2
            
            #movement
            #range
            if bonus[6] <= 0:
                down = False
                up = False
                if tarDist > 50 + ((i[1] in [2, 13, 16,26]) * 50) + ((i[1] in [3,28,32]) * 200) + ((i[1] in [4,12,18,20,27,27.1]) * 300) + ((i[1] in [5,14.1]) * 125) + ((i[1] == 8 or i[1] == 10 or i[1] == 15) * 150) + ((i[1] == 11 or i[1] == 19 or i[1] == 21 or i[1] == 24) * 550) +  ((i[1] in [14,22]) * 200) + ((i[1] in [30]) * 9999) :
                    if pos[0] <= target[3][0] and abs(pos[0] - target[3][0]) > 15:
                        pos[0] += bonus[0] * deltaTime
                        if i[1] in peopleMelee:
                            for i2 in people:
                                if getDistance(pos, i2[3]) < hitbox and i2 != i and i2[1] in peopleMelee:
                                    pos[0] -= bonus[0] * deltaTime
                                    up = True
                            
                    elif pos[0] >= target[3][0] and abs(pos[0] - target[3][0]) > 15:
                        pos[0] -= bonus[0] * deltaTime
                        if i[1] in peopleMelee:
                            for i2 in people:
                                if getDistance(pos, i2[3]) < hitbox and i2 != i and i2[1] in peopleMelee:
                                    pos[0] += bonus[0] * deltaTime
                                    down = True
                        
                    if pos[1] <= target[3][1] and abs(pos[1] - target[3][1]) > 15 or down:
                        pos[1] += bonus[0] * deltaTime
                        if i[1] in peopleMelee:
                            for i2 in people:
                                if getDistance(pos, i2[3]) < hitbox and i2 != i and i2[1] in peopleMelee:
                                    pos[1] -= bonus[0] * deltaTime
                        
                    elif pos[1] >= target[3][1] and abs(pos[1] - target[3][1]) > 15 or up:
                        pos[1] -= bonus[0] * deltaTime
                        if i[1] in peopleMelee:
                            for i2 in people:
                                if getDistance(pos, i2[3]) < hitbox and i2 != i and i2[1] in peopleMelee:
                                    pos[1] += bonus[0] * deltaTime
                        
                        
                #attack delay
                elif timer > 1 + ((i[1] in [3])) + ((i[1] in [4,5,14,22,24,28]) * 1.5) + ((i[1] in [1,7,8,13,16,23,26,26.1,26.2,32]) * 0.5) - ((i[1] == 9 or i[1] == [12,17]) * 0.4) - ((i[1] in [10,30]) * 0.75) + ((i[1] == 11 or i[1] == 18 or i[1] == 21) * 4) - ((i[1] in [14.1,27.1]) * 0.6) + ((i[1] in [15]) * 2.5) + ((i[1] in [19,27,20]) * 3):
                    if i[1] == 4: #necromace
                        people.append([plr, 4.1, [5,5], [pos[0] + random.randint(-75,75), pos[1] + random.randint(-75,75)], 0, [3, 2, 10, 0, 0, 0, 0,0] ])
                        timer = 0
                        bonus[2] = 25
                    elif i[1] == 20: #mega necromace
                        timer = 0
                        choices = [0,1,2,3,9,13,16,24,25,6,7,8,22]
                        bonus[2] = 40
                        for i3 in range(3):
                            summon = copy.deepcopy(peopleTemp[random.choice(choices)])
                            summon[3] = [pos[0] + random.randint(-125,125), pos[1] + random.randint(-125,125)]
                            summon[0] = plr
                            people.append(summon)
                    elif i[1] == 5: #heal
                        target[2][0] += bonus[1]
                        timer = 0
                        bonus[2] = 75
                    elif i[1] == 18: #buff
                        timer = 0
                        target[5][5] = 100
                        bonus[5] = 50
                        target[5][1] += 1
                    elif i[1] == 8 or i[1] == 12 or i[1] == 14.1 or i[1] == 19 or i[1] == 22: #splash attack
                        target[2][0] -= bonus[1]
                        target[5][7] = 255
                        timer = 0
                        if i[1] in [8,11,12,14,19]:
                            Sfireball.play()
                        elif i[1] in [22]:
                            Siceball.play()
                        #target[5][3] = 50
                        for i3 in people:
                            if getDistance(target[3], i3[3]) <= (75 + ((i[1] == 12) *50 ) - ((i[1] == 14.1) * 35) ) - ((i[1] == 22) * 10) + ((i[1] == 8) * 5) and i3[0] != plr:
                                i3[2][0] -= 2 - (i[1] == 14.1 or i[1] == 22)
                                if i[1] == 22:
                                    i3[5][5] = 50
                                    if i3[5][6] <= 20:
                                        i3[5][6] = 25
                                else:
                                    i3[5][3] = 50 - ((i[1] == 14.1)*10)
                        if i[1] == 19:
                            bonus[2] = 30
                        if i[1] == 12:
                            people.append([plr, 12.1, [5,5], [pos[0] + random.randint(-75,75), pos[1] + random.randint(-75,75)], 0, [10, 5, 10, 0, 0, 0, 0,0] ])
                    elif i[1] == 14: #fallen angel attack
                        target[5][7] = 255
                        timer = 0
                        bonus[2] = 75
                        target[5][3] = 40
                        target[2][0] -= bonus[1]
                        people.append([plr, 14.1, [160,160], [pos[0], pos[1]], 0, [0, 0, (random.randint(0,1)*2)-1, 0, (random.randint(0,1)*2)-1, 0, 0,0] ])
                    elif i[1] == 21:#chronomancer attack
                        for i3 in people:
                            if i3[0] == (not plr):
                                timer = 0
                                i3[5][6] += 75
                                i3[5][5] += 50 
                    elif i[1] == 27: #engineer attack
                        #[0, 27.1, [5,5], [0, 0], 0, [0, 1, 0, 0, 0,0,0,0]]
                        people.append([plr, 27.1, [10,10], [pos[0] + random.randint(-125,125), pos[1] + random.randint(-125,125)], 0, [0, 1, 10, 0, 0, 0, 0,0] ])
                        timer = 0
                        bonus[2] = 25
                    elif i[1] == 30:
                        for i2 in people:
                            if i2[0] != plr:
                                i2[5][4] += 1
                                i2[5][4] *= 1.05
                    else: #basic attack
                        if i[1] in [0,1,2,4.1,6,7,12.1,13,29.1,29]:
                            random.choice([Shit1,Shit2,Shit3]).play()
                        elif i[1] in [3,27.1,28]:
                            Sbow.play()
                        target[5][7] = 255
                        target[2][0] -= bonus[1]
                        damage = bonus[1]
                        timer = 0
                        if i[1] in [3,10,11,15,24,27,27.1,28,32]: #white ring 1
                            bonus[2] = 20 + ((i[1] == 11 or i[1] == 15) * 10)
                        if i[1] in [13,15,24,30]: #knockback
                            target[5][4] += 20 - ((i[1] == 24) * 40) - ((i[1] == 30) * 15)
                        if i[1] == 15 and target[1] in peopleGiant: #bonus giant damage
                            target[2][0] -= 2
                            damage += 2
                        if i[1] in peopleMelee and target[1] == 16:#thorns
                            hp[0] -= 2
                            numList.append( ["-2", (pos[0],pos[1]-50), 40, 2] )#death num
                        if target[2][0] <= 0 and i[1] == 23: #heal self with death
                            bonus[2] = 75
                            hp[0] += 5
                        if i[1] == 27.1:#turret self harm
                            hp[0] -= 0.5
                        if i[1] == 28:#cupid
                            target[0] = plr
                        if i[1] == 29:#spy
                            typ = 29.1
                            bonus[0] = 2
                            bonus[1] = 2
                            pos[0] += -100 * ((plr*2)-1)
                        if target[2][0] <= 0 and i[1] == 32: #witch
                            toAdd.append([plr, 32.1, [5,5], [target[3][0], target[3][1]], 0, [3, 2, 0, 0, 0,0,0,0]]) #guy

                        
                        numList.append( ["-"+str(damage), (target[3][0],target[3][1]-50), 40, damage] )#death num
                #end damage
                
                #more move
                if i[1] in peopleMelee:
                    for i2 in people:
                        if getDistance(pos, i2[3]) < hitbox and i2 != i and i2[1] in peopleMelee:
                            if people.index(i) < people.index(i2):
                                pos[1] -= bonus[0] * ((plr*2)-1) * deltaTime
            #end movement--------------------------------------------
            if i[1] in [3,4,10,11,15,19,20,24,27,27.1,28,32]:#white ring 2
                bonus[2] -= timePass * (5 + ((i[1] == 10) *35 )) + ((i[1] in [15,19,27.1] * 5 ))
                if bonus[2] <= 10:
                    bonus[2] = 10
                    
            if i[1] == 14.1:
                hp[0] -= 1
            
            if bonus[6] > 0:
                bonus[6] -= 1
                    
            if abs(bonus[4]) > 0 and i[1] != 14.1: #knockback
                if plr == 0:
                    pos[0] -= bonus[4]
                else:
                    pos[0] += bonus[4]
                if bonus[4] > 0:
                    bonus[4] -= 1
                else:
                    bonus[4] += 1
                if pos[0] >= 1000 or pos[0] <= 0:
                    bonus[4]*= -1
                    hp[0] -= 2
    
    
            elif i[1] == 14.1:#bounce
                pos[0] += bonus[2]*12
                pos[1] += bonus[4]*12
                if pos[0] >= 1000 or pos[0] <= 0:
                    bonus[2] *= -1
                if pos[1] >= 700 or pos[1] <= 0:
                    bonus[4] *= -1
                           
            if i[1] == 5 or i[1] == 14 or i[1] == 23:
                bonus[2] -= (timePass * (30 + (i[1] == 23) * 25 ))
                if bonus[2] <= 25:
                    bonus[2] = 25
            
            bonus[3] -= timePass * 40
            if bonus[3] <= 0:
                bonus[3] = 0
            bonus[5] -= timePass * 60
            if bonus[5] <= 0:
                bonus[5] = 0
                
            if hp[0] > hp[1]*1.5:
                hp[0] = int(hp[1]*1.5)
                    
                    
            loc = people.index(i)
            if i[1] == 25 and i[2][0] <= 15:
                toRemove.append(i)
                toAdd.append([plr, 1, [10,10], [pos[0], pos[1]], 0, [2, 6, 0, 0, -25,0,0,0]]) #sword
                people[loc] = ([plr, 2, [10,35], [pos[0], pos[1]], 0, [1, 2, 0, 0, 0,0,0,0]] )#giant
                #if not i in toRemove:
            elif i[2][0] > 0 and getDistance(pos, (500,350)) <= 3000:
                people[loc] = [plr, typ, [hp[0], hp[1]], pos, timer, [bonus[0], bonus[1], bonus[2], bonus[3], bonus[4], bonus[5], bonus[6], bonus[7]]]
            elif i in people:
                if i[1] == 17:
                    death.append(["boom", [pos[0],pos[1]], 250])
                else:
                    death.append([[pos[0],pos[1]], 25+((i[1] in peopleGiant)*25), 255, i[1]])
                if i[1] == 17:
                    for i3 in people:
                        if getDistance(target[3], i3[3]) <= 80:
                            i3[2][0] -= 8
                if i[1] == 26:
                    toAdd.append([plr, 26.1, [20,20], [pos[0], pos[1]-25], 0, [1, 2, 0, 0, 0,0,0,0]],)
                    toAdd.append([plr, 26.1, [20,20], [pos[0], pos[1]+25], 0, [1, 2, 0, 0, 0,0,0,0]],)
                    for i3 in people:
                        if getDistance(target[3], i3[3]) <= 60 and i3[0] != plr:
                            i3[2][0] -= 3
                            i3[5][7] = 255
                if i[1] == 26.1:
                    toAdd.append([plr, 26.2, [10,10], [pos[0], pos[1]-25], 0, [1, 2, 0, 0, 0,0,0,0]],)
                    toAdd.append([plr, 26.2, [10,10], [pos[0], pos[1]+25], 0, [1, 2, 0, 0, 0,0,0,0]],)
                    for i3 in people:
                        if getDistance(target[3], i3[3]) <= 35 and i3[0] != plr:
                            i3[2][0] -= 1
                            i3[5][7] = 255
                if i[1] == 31:
                    toAdd.append([plr, 26, [35,35], [pos[0]-25, pos[1]-25], 0, [10, 2, 0, 0, 0,0,0,0]],)
                    toAdd.append([plr, 26, [35,35], [pos[0]-25, pos[1]+25], 0, [10, 2, 0, 0, 0,0,0,0]],)
                    toAdd.append([plr, 26, [35,35], [pos[0]+25, pos[1]-25], 0, [10, 2, 0, 0, 0,0,0,0]],)
                    toAdd.append([plr, 26, [35,35], [pos[0]+25, pos[1]+25], 0, [10, 2, 0, 0, 0,0,0,0]],)
                toRemove.append(i)
        for i in toRemove:
            if not i[1] in [4.1,12.1,14.1,14,17]:
                random.choice([Sdeath1,Sdeath2,Sdeath3]).play()
            if i[1] == 14.1:
                SorbDeath.play()
            if i[1] == 14:
                SfallenAngelDeath.play()
            if i in people:
                people.remove(i)
        toRemove = []
        for i in toAdd:
            people.append(i.copy())
        toAdd = []
        
        for i in death:
            if i[0] == "boom":
                i[2] -= 25 * deltaTime
                if i[2] <= 10:
                    death.remove(i)
            else:
                i[1] += deltaTime
                i[2] -= 5+((i[3]==4.1)*5) * deltaTime
                if i[2] <= 0:
                    death.remove(i)
        for i in numList:
            i[2] -= deltaTime
            i[1] = (i[1][0], i[1][1]-deltaTime)
            if i[2] <= 0 and i in numList:
                numList.remove(i)

            
    c.tick(frameRate)
    draw()
from pygame.locals import *
from threading import Thread
import numpy as np
import pygame, sys
pygame.init()

def getFont(sz):
    return pygame.font.Font(None, sz)

def savefile(name, timeline):
    file = open(logpath, "a")
    file.write(name+"\n")
    for (x, y) in timeline:
        x, y = (x - W//2), (y - W//2)
        x, y = (x / zoom), (y / zoom)
        file.write("%.10f"%x + " " + "%.10f"%y + "\n")
    file.close()

mypath = "../assets/"
logpath = "./pos.txt"

f = open(logpath, "w")
f.close()

from os import listdir
from os.path import isfile, join
infiles = [mypath+f for f in listdir(mypath) if isfile(join(mypath, f))]

W = 500
zoom = 100
running = True
disp = pygame.display.set_mode((W, W))

timeline = []
pos = (0, 0)
cur = 0

while running:
    for e in pygame.event.get():
        if e.type == QUIT:
            running = False

        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                timeline.append(pos)

            elif e.button <= 3:
                if e.button == 2 and len(timeline) > 0:
                    timeline.append(timeline[0])
                savefile(infiles[cur], timeline)
                timeline = []
                cur += 1

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                cur += 1
                timeline = []

    if cur >= len(infiles):
        running = False
        break

    pos = pygame.mouse.get_pos()
    text = getFont(32).render(infiles[cur], True, (255,255,255))

    disp.fill((0,0,0))
    disp.blit(text, ((W - text.get_width())/ 2, 10))

    last = None
    for (x, y) in timeline:
        if last is not None:
            pygame.draw.line(disp, (0,0,255), (x, y), last, 3)
        last = (x, y)
        pygame.draw.circle(disp, (0,0,255), (x, y), 7)

    pygame.draw.circle(disp, (255,0,0), (W//2,W//2), 7)
    pygame.draw.circle(disp, (0,255,0), pos, 5)
    pygame.display.update()

pygame.quit()
sys.exit()

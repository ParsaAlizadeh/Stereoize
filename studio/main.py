from Envir import Env
from listener import Listener
from speaker import Speaker
import numpy as np
import pygame
import time
from pygame.locals import *
pygame.init()

W = 500
zoom = 100  # px / meter
disp = pygame.display.set_mode((W, W))
clock = pygame.time.Clock()

env = Env()
listener = Listener()
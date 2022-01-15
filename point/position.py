from scipy.io import wavfile
import numpy as np
import sounddevice as sd
import pygame
from pygame.locals import *
from threading import Thread

pygame.init()


def process():
    global final

    tmp = np.zeros((dur + fs, 2), dtype=np.int16)
    for i in range(nfile):
        xf = np.arange(len(data[i]))
        dl = np.sum((speaker[i] - left) ** 2) ** .5
        dr = np.sum((speaker[i] - right) ** 2) ** .5

        tl = np.int64(dl * fs / v)
        tr = np.int64(dr * fs / v)

        pl = 1 / (dl ** 2)
        pr = 1 / (dr ** 2)
        pl = min(2, pl)
        pr = min(2, pr)

        tmp[xf + tl, 0] = tmp[xf + tl, 0] + data[i] * pl / nfile
        tmp[xf + tr, 1] = tmp[xf + tr, 1] + data[i] * pr / nfile

    final[:] = tmp


def playing():
    def play():
        stream = sd.OutputStream(samplerate=fs, channels=2, dtype=np.int16)
        stream.start()
        ind = 0
        buff = fs // 10
        while running:
            stream.write(final[ind:ind + buff, :])
            ind = min(ind + buff, dur) % dur

    thr = Thread(target=play)
    return thr.start()


infile = ["../assets/wav/yeki.wav"]
nfile = len(infile)
data = np.empty(nfile, dtype=object)
dur = 0
for i in range(nfile):
    fs, data[i] = wavfile.read(infile[i])
    data[i] = data[i] / 2
    dur = max(dur, len(data[i]))
v = 343
running = True

W = 500
disp = pygame.display.set_mode((W, W))
clock = pygame.time.Clock()

left = np.array([-0.12, 0], dtype=np.float32)
right = np.array([+0.12, 0], dtype=np.float32)
speaker = np.zeros((nfile, 2), dtype=np.float32)
zoom = W / 3

cur = 0
flag = False
speed = np.array([0, 0], dtype=np.float32)
dx = np.array([0, 0, 1, -1], dtype=np.float32) / zoom
dy = np.array([-1, 1, 0, 0], dtype=np.float32) / zoom

final = np.zeros((dur + fs, 2), dtype=np.int16)

process()
playing()

while running:
    for e in pygame.event.get():
        if e.type == QUIT:
            running = False

        if e.type == MOUSEBUTTONDOWN:
            pos = np.array(e.pos)
            pos = (pos - W / 2) / zoom
            speaker[cur, :] = pos

        if e.type == KEYDOWN:
            key = e.key
            if key - 49 < nfile:
                cur = key - 49

    if flag:
        speed[0] += dx[flag - 1]
        speed[1] += dy[flag - 1]
    speaker[cur, :] += speed

    process()

    disp.fill((0, 0, 0))
    pygame.draw.circle(disp, (255, 0, 0), (right * zoom + W / 2).astype(int), 5)
    pygame.draw.circle(disp, (255, 0, 0), (left * zoom + W / 2).astype(int), 5)

    for i in range(nfile):
        col = (0, 255, 255) if i == cur else (0, 255, 0)
        pygame.draw.circle(disp, col, (speaker[i] * zoom + W / 2).astype(int), 7)

    pygame.display.update()

sd.stop()
pygame.quit()

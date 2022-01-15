from scipy.io import wavfile
from pygame.locals import *
from os import system
import time
import numpy as np
import sounddevice as sd
import pygame, sys

# Change to python (instead of python3) for windows
system("python3 choose.py")
pygame.init()

class Speaker:
    def __init__(self, filename, timeline):
        self.name = filename[-filename[::-1].find('/'):]
        self.fs, self.data = wavfile.read(filename)
        if self.data.ndim > 1:
            self.data = np.mean(self.data, axis=-1)
        self.timeline = np.array(timeline, dtype=np.float64)
        self.pos = np.zeros((len(self.data), 2), dtype=np.float64)
        self.prepare()
        self.time = 0

    def getLen(self):
        return len(self.data)

    def getData(self):
        return self.data

    def getPos(self):
        return self.pos

    def getFramePos(self, start):
        curtime = time.time() - start
        curtime *= self.fs
        curtime = int(curtime)
        curtime %= len(self.data)
        return self.pos[curtime]

    def prepare(self):
        xf = np.arange(self.fs) / self.fs
        curtime = 0
        ind = 0
        while curtime + self.fs < len(self.data):
            rel = (self.timeline[ind+1] - self.timeline[ind]).reshape(-1, 2) * xf.reshape(-1, 1)
            self.pos[curtime:curtime+self.fs] = self.timeline[ind] + rel
            ind = (ind + 1) % (len(self.timeline)-1)
            curtime += self.fs
        self.data = self.data[:curtime]
        self.pos = self.pos[:curtime]


def process():
    global final

    tmp = np.zeros((batch + fs, 2), dtype=int)
    cnttmp = np.zeros((batch + fs, 2), dtype=int)

    for i in range(len(speakers)):
        data = speakers[i].getData()
        if data is None:
            continue
        xf = np.arange(len(data))
        spkpos = speakers[i].getPos()

        dl = np.sum((spkpos - left) ** 2, axis=-1) ** .5
        dr = np.sum((spkpos - right) ** 2, axis=-1) ** .5

        tl = np.int64(dl * fs / v)
        tr = np.int64(dr * fs / v)

        pl = 1 / (dl ** 2)
        pr = 1 / (dr ** 2)
        pl = np.clip(pl, None, 1)
        pr = np.clip(pr, None, 1)

        cnttmp[xf + tl, 0] += 1
        cnttmp[xf + tr, 1] += 1
        tmp[xf + tl, 0] = tmp[xf + tl, 0] + data[xf] * pl
        tmp[xf + tr, 1] = tmp[xf + tr, 1] + data[xf] * pr

    final[:] = tmp
    cnt[:] = cnttmp

def load_files():
    file = open(logpath, "r")
    lines = file.readlines()
    speakers = []
    timeline = []
    fname = None
    mxdur = -1

    for line in lines:
        d = line.split()
        if len(d) == 1:
            if fname is not None:
                spk = Speaker(fname, timeline)
                print(fname, spk.data.shape)
                mxdur = max(mxdur, spk.getLen())
                speakers.append(spk)
            fname = d[0]
            timeline = []
        else:
            x, y = list(map(float, d))
            timeline.append((x, y))

    spk = Speaker(fname, timeline)
    print(fname, spk.getLen())
    mxdur = max(mxdur, spk.getLen())
    speakers.append(spk)

    return speakers, mxdur

def getFont(sz):
    return pygame.font.Font(None, sz)


logpath = "./pos.txt"
speakers, batch = load_files()
fs = 44100
FPS = 60

v = 343
running = True

W = 500
zoom = 100
disp = pygame.display.set_mode((W, W))
clock = pygame.time.Clock()

left = np.array([-0.12, 0], dtype=np.float32)
right = np.array([+0.12, 0], dtype=np.float32)

final = np.zeros((batch + fs, 2), dtype=int)
cnt = np.zeros((batch + fs, 2), dtype=int)

process()
cnt[cnt == 0] = 1
chunk = np.int16(final / cnt)

start = time.time()
sd.play(chunk, samplerate=fs)

while running:
    for e in pygame.event.get():
        if e.type == QUIT:
            running = False

    disp.fill((0, 0, 0))
    pygame.draw.circle(disp, (255, 0, 0), (right * zoom + W / 2).astype(int), 5)
    pygame.draw.circle(disp, (255, 0, 0), (left * zoom + W / 2).astype(int), 5)

    for i in range(len(speakers)):
        spkpos = (speakers[i].getFramePos(start) * zoom + W / 2).astype(int)
        pygame.draw.circle(disp, (0,255,0), spkpos, 7)
        text = getFont(24).render(speakers[i].name, True, (255,255,255))
        disp.blit(text, spkpos)

    pygame.display.update()
    clock.tick(FPS)

sd.stop()
pygame.quit()
sys.exit()

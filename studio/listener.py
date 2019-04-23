import numpy as np

class Listener:
    def __init__(self, pos=(0, 0), fs=44100, dur=1, v=343):
        self.pos = np.array(pos, dtype=np.float32)
        self.right = self.pos + [.12, 0]
        self.left = self.pos + [-.12, 0]
        self.v = v
        self.nframe = dur * fs
        self.final = np.zeros((self.nframe, 2), dtype=np.int16)
        self.tmp = np.zeros((self.nframe, 2), dtype=int)
        self.cnt = np.zeros((self.nframe, 2), dtype=int)

    def affect(self, spk):
        dl = np.sum((self.left-spk.pos)**2)**.5
        dr = np.sum((self.right-spk.pos)**2)**.5

        tl = np.int64(dl * self.fs / self.v)
        tr = np.int64(dr * self.fs / self.v)

        pl = 1 / (dl ** 2)
        pr = 1 / (dr ** 2)
        pl[pl > 1] = 1
        pr[pr > 1] = 1

        fr = min(len(spk.data), self.nframe)
        xf = np.arange(fr)
        indl = xf + tl
        indr = xf + tr
        indl = indl[indl < fr]
        indr = indr[indr < fr]

        self.tmp[indl, 0] = self.tmp[indl, 0] + spk.data[:fr] * pl
        self.tmp[indr, 1] = self.tmp[indr, 1] + spk.data[:fr] * pr
        self.cnt[indl, 0] = self.cnt[indl, 0] + 1
        self.cnt[indr, 1] = self.cnt[indr, 1] + 1

    def generate(self):
        self.cnt[self.cnt == 0, :] = 1
        self.final[:] = self.tmp / self.cnt
        self.clean()

    def clean(self):
        self.tmp[:] = 0
        self.cnt[:] = 0




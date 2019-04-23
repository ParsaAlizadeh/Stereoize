import numpy as np

class Speaker:
    def __init__(self, data, timeline):
        self.data = data
        self.timeline = timeline
        self.maxtime = timeline[-1, 0]
        self.pos = np.zeros((2,), dtype=np.float32)

    def update(self, curtime):
        curtime %= self.maxtime
        ind = np.searchsorted(self.timeline, curtime, side="left")
        self.pos[:] = self.timeline[ind, 1:]
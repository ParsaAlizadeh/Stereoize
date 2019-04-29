class Env:
    def __init__(self):
        self.listener = None
        self.speakers = []

    def addListener(self, lis):
        self.listener = lis

    def addSpeaker(self, spk):
        self.speakers.append(spk)

    def update(self, curtime):
        if self.listener is None or len(self.speakers) == 0:
            return

        for spk in self.speakers:
            spk.update(curtime)
            self.listener.affect(spk)

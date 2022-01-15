from scipy.io import wavfile
import numpy as np

infile = "../assets/wav/yeki.wav"
outfile = "./yeki.wav"
v = 343

fs, src = wavfile.read(infile)
dur = len(src)

# Speaker position
speaker = np.zeros((dur, 2))
d = 10 ; rx = 2 ; ry = 2
a = np.linspace(0, d*2*np.pi, dur)
speaker[:, 0] = rx*np.cos(a)
speaker[:, 1] = ry*np.sin(a)

# Listener position
left = np.array([-.12, 0])
right = np.array([.12, 0])

# Distance
dl = np.sum((speaker-left)**2, axis=-1)**.5
dr = np.sum((speaker-right)**2, axis=-1)**.5

# Delta-time
tl = np.int64(dl * fs / v)
tr = np.int64(dr * fs / v)

# Power
pl = 1 / (dl ** 2)
pr = 1 / (dr ** 2)
pl[pl > 1] = 1
pr[pr > 1] = 1

# Final Sound
final = np.zeros((dur+fs, 2), dtype=np.int16)
xf = np.arange(dur)
final[xf+tl, 0] = src * pl
final[xf+tr, 1] = src * pr

# Save
wavfile.write(outfile, fs, final)
print("END :)")

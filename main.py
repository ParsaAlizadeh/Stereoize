from scipy.io import wavfile
import numpy as np

infile = "assets/yeki.wav"
outfile = "out/dist.wav"
v = 343

fs, src = wavfile.read(infile)
dur = len(src)

# Speaker position
speaker = np.zeros((dur, 2))
d = 10
a = np.linspace(0, d*2*np.pi, dur)
speaker[:, 0] = 10*np.cos(a)
speaker[:, 1] = 10*np.sin(a)
#speaker[:, 1] = 10*np.sin(a)

# Listener position
left = np.array([-.12, 0])
right = np.array([.12, 0])

# Distance
dl = np.sum((speaker-left)**2, axis=-1)**.5
dr = np.sum((speaker-right)**2, axis=-1)**.5

# Delta-time
tl = np.int64(dl * fs / v)
tr = np.int64(dr * fs / v)

# Final Sound
final = np.zeros((dur+fs, 2), dtype=float)
cnt = np.zeros((dur+fs, 2), dtype=int)

for i in range(dur):
    final[i+tl[i], 0] += src[i]
    final[i+tr[i], 1] += src[i]
    cnt[i+tl[i], 0] += 1
    cnt[i+tr[i], 1] += 1

mask = (cnt == 0)
cnt[mask] = 1
#print(cnt.min(), cnt.max(), (cnt == 2).sum())
final = final / cnt
final = final.astype(np.int16)
final[np.isnan(final)] = 0

xf = np.arange(0, dur+fs, dtype=np.int64)
ll = xf[~mask[:,0]][0]
lr = xf[~mask[:,1]][0]
for i in range(min(ll, lr), len(final)):
    if mask[i, 0]:
        final[i] = final[ll]
    else:
        ll = i

    if mask[i, 1]:
        final[i] = final[lr]
    else:
        lr = i

wavfile.write(outfile, fs, final)
print("END :)")

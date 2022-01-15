# Stereoize
Transform mono wav files to 3D stereo sound.

## Requirements

```bash
$ pip install -r requirements.txt
```

## Components

### Circle

Generate a simple circular motion.

```bash
$ cd circle
$ python main.py
$ open yeki.wav # play output file with your default audio player
```

### Point

Move the speaker around and play simultaneously.

```bash
$ cd point
$ python position.py
$ # pygame window should be openned
$ # left click on plane to move the selected speaker
$ # press any number to select another speacker
```

### Studio

Move speakers based on predetermined linear motion.

```bash
$ cd 3daudio
$ cp ../assets/wav/yeki.way ./ # copy any file you want
$ python main.py
$ # it first run choose.py, to choose the location of files
$ # left click to create a new path
$ # right click to end the path
$ # press space to ignore that wav file
```
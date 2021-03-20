# KCS Utility V1.0

## Overview
- This python script is built to streamline and simplify KCS08
- It requires DOSBox to be installed to run (but you do not need to open it) due to KCS08 being a dos program
- With this script the encoding and decoding process becomes much easier
- There are auto record and playback features built in so you do not need to use an external program such as audacity
- The script allows you to pick between KCS (300 baud) or CUTS (1200 baud). 300 baud may work better on worse quality recorders
- Please refer to the demonstration video for specific instructions on how to use the script

##  Demonstration Video:

<a href="https://www.youtube.com/watch?v=LhpXfOWhbPY
" target="_blank"><img src="http://img.youtube.com/vi/LhpXfOWhbPY/0.jpg" 
alt="Demonstration video" width="700" height="525" border="0" /></a>


## Installation

You will first need to install [DOSBox](https://www.dosbox.com/download.php?main=1)

Installing `PyAudio` on Windows is a bit tricky. To expedite the process, you should probably use `pipwin` to install it. First, install `pipwin` how you would normally install a Python package (e.g. `pip3 install . . .`), then:

```
pipwin install pyaudio
```

If issues still persist, you may need to install "Microsoft Visual C++ 14.0" which is installed by installing "Microsoft Visual C++ Build Tools".

To install the external dependencies for this project, run:
```
python -m pip install -r requirements.txt
```

## Features
1. Encode file
    
    This simply automates opening of dosbox mounting your current directory and executing an encode command with KCS.

2. Decode file
    
    If you already have a WAV file with encoded date you can use this to decode. Same functionality as 1.
    
3. Play WAV for cassette recording
    
    If you already have a WAV file with encoded data you can use this option to play it through your system for a cassette deck to record.
    (Note set system output to your cassette deck to not blow your ears off)

4. Record cassette to WAV
    
    Record a cassette decks output to the scipt for decoding. Make sure to set your levels so they maz out (around 0 dB).
    This feature should automatically start when the date starts playing and stop when it ends.
    It also trims any dead so only the date recording remains.


5. Change settings (dosbox location, recording device)

6. Exit

## Troubleshooting

- **I keep getting `RuntimeError: Error opening 'output.wav': System error.`**
    - You probably have `output.wav` opened up in another program, which prevents `KCS-Utility` from opening it up for reading. Close whatever's keeping it open and record again.

- **The recording is empty.**
    - There's a chance your audio output might not be loud enough for the program to pick it up. This is also apparent when it doesn't stop the recording automatically (because it will detect noticeable audio, continue recording, and then stop upon silence).

## Known Limitations
- Low quality cassette players may have limited success with this program (this is true with base KCS08 as well).
  To make the most of these low quality recorders you may need to experiment with recording levels. This script detects programs above -7db so thats where you should aim to calibrate your player. This is easier with a higher quality player since the sound will be more crisp at high volumes.
- KCS itself is very outdated and slow. I am looking into making a new encoding format
- Occasionally KCS itself will add a garbage byte at the beginning of a decoded file or remove the first byte of a file.
  I have tried my best to mitigate this issue through the use of this script. If it does happen it can be fixed by editing the decoded file in a text editor.

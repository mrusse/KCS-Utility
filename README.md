# KCS Utility V1.0

Overview
- This python script is built to streamline and simplify KCS08
- It requires DOSBox to run due to KCS08 being a dos program
- With this script the encoding and decoding process becomes much easier
- There are auto record and playback features built in so you do not need to use an external program such as audacity
- The script defaults to CUTS mode when encoding to take full advantage of the KCS08 program
- Please refer to the demonstration video for specific instructions on how to use the script

Demonstration Video:


<a href="https://www.youtube.com/watch?v=LhpXfOWhbPY
" target="_blank"><img src="http://img.youtube.com/vi/LhpXfOWhbPY/0.jpg" 
alt="Demonstration video" width="700" height="525" border="0" /></a>

Features:
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


5. Exit    

Known Limitations
- Low quality cassette players may have limited success with this program (this is true with base KCS08 as well)
- KCS itself is very outdated and slow. I am looking into making a new encoding format
- Occasionally KCS itself will add a garbage byte at the beginning of a decoded file or remove the first byte of a file.
  I have tried my best to mitigate this issue through the use of this script. If it does happen it can be fixed by editing the decoded file in a text editor.

import subprocess
import os
import math 
import wave, sys, pyaudio
import time
import keyboard
import struct
from functools import reduce
import soundfile

#Open dosbox    
def run_dosbox(args):
    return subprocess.call(reduce(lambda x, y: x  + ["-noconsole"] + ["-c"]  + [y], args, ["dosbox"] ))

def truncate_float(value, digits_after_point=2):
    pow_10 = 10 ** digits_after_point
    return (float(int(value * pow_10))) / pow_10

def encode_file():
    print("\nEncode file")
    infile = input("Input filename:")

    print(infile)

    while not os.path.isfile(infile):
        print("File not found. Make sure the file is in the currect directory.")
        infile = input("Input filename:")
    
    os.rename(infile,"toEncode.mjr")
    
    outfile = input("Output WAV filename:")

    KCS = "KCS -M -Y -U -L5 " + "toEncode.mjr" + " " + "encode.wav"
    dosbox_args = [r'mount c ' + cwd,'C:',KCS,'exit']
    run_dosbox(dosbox_args)

    os.rename("toEncode.mjr",infile)
    os.rename("encode.wav",outfile)

    # TODO
    """
    play_audio = input("Would you like to play \"" + outfile +"\"? (Y/N):")

    if play_audio == "Y" or play_audio == "y":
        play_wav(outfile)
    """

def decode_file(infile):

    while not os.path.isfile(infile):
        print("File not found. Make sure the file is in the currect directory.")
        infile = input("Input WAV filename:")
    
    os.rename(infile,"toDecode.wav")
    
    outfile = input("Output filename:")

    KCS = "KCS -Y -U " + "toDecode.wav" + " " + "decode.mjr"

    dosbox_args = [r'mount c ' + cwd,'C:',KCS,'exit']

    run_dosbox(dosbox_args)

    os.rename("toDecode.wav",infile)
    os.rename("decode.mjr",outfile)

    if infile == "output.wav":
        f = open(outfile, 'rb')
        f.seek(1) # skip the first 1 byte
        trim = f.read()
        f.close()
        trimmed = open(outfile, 'wb')
        trimmed.write(trim)
        trimmed.close()

        
    open_decode = input("Would you like to open \"" + outfile +"\"? (Y/N):")

    if open_decode == "Y" or open_decode == "y":
       os.startfile(outfile)

#Play audio
def play_wav(wav_file):

    print("Press space to start playback:")
    sys.stdout.flush()
    while True:
        if keyboard.is_pressed('space'):
            break
    #Count them in
    print("Get ready to record, playing in:")
    count = ["3...","2...","1..."]
    for i in range(3):
        if i == 0:
            print("%s " % (count[0]),end = '\r')
        if i == 1:
            print("%s%s " % (count[0],count[1]),end = '\r')
        if i == 2:
            print("%s%s%s " % (count[0],count[1],count[2]))
        sys.stdout.flush()
        time.sleep(1)
    
    #open wav and get information
    wf = wave.open(wav_file)
    p = pyaudio.PyAudio()
    chunk = 1024
    rate = wf.getframerate()
    channels = wf.getnchannels()
    frames = wf.getnframes()
    stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)

    #get duration and set variables for the progress bar
    duration = frames / float(rate)
    print("Playing: " + wav_file +"\n")
   
    data = wf.readframes(chunk)
    start_time = time.time()
    advance_point = duration / 50 #split the song sections to advance the bar
    progress_bar = [0.00]
    progress_point = advance_point #total acumulated advancements throughout the song
    bar_count = 0 #number of dots on bar
    
    #Print the initial bar
    bar = '█' * bar_count
    line = '-' * int(50 - bar_count)
    print(' |%s%s|       ' % (bar,line),end ='\r')
    bar_count = 1
    
    while True:
        elapsed_time = time.time() - start_time
        in_bar = False
        sys.stdout.flush()
        
        if truncate_float(elapsed_time,1) == truncate_float(progress_point,1):
            for i in range(len(progress_bar)):
                if truncate_float(elapsed_time,1) == progress_bar[i]:
                    in_bar = True
            if not in_bar and bar_count < 51:
                sys.stdout.flush()
                progress_bar.append(truncate_float(elapsed_time,1))
                bar = '█' * bar_count
                line = '-' * int(50 - bar_count)
                print(' |%s%s| %d/%ds ' % (bar,line,elapsed_time,duration),end ='\r')
                progress_point += advance_point
                bar_count += 1
                
            
        if data != '':
            stream.write(data)
            data = wf.readframes(chunk)
        
        if data == b'':
            print('')
            break

    #stop stream  
    stream.stop_stream()  
    stream.close()  

    #close PyAudio  
    p.terminate()
    
    keyboard.press('backspace')
    sys.stdout.flush()
    
def record_wav():

    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)

    print("Press space to start recording:")
    sys.stdout.flush()
    while True:
        if keyboard.is_pressed('space'):
            break
            
    chunk = 1024
    sample_format = pyaudio.paInt16 #16 bit sample
    channels = 1
    fs = 22050
    
    stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True,
                input_device_index=device_id)
    
    frames = []
    recorded = 0
    
    while True:
        sys.stdout.flush()   
        data = stream.read(chunk)
        rms_data = rms(data)
        decibel = 20 * math.log10(rms_data)
        if decibel < -10:
            print("Listening for data... %.2f decibels press esc to abort " % (decibel),end = '\r')
        if decibel > -10:
            print("Recording data... %.2f decibels press esc to abort     " % (decibel),end = '\r')
            #data2 = stream.read(chunk)
            recorded = 1
            frames.append(data)
        if recorded == 1 and decibel < -10:
            break
        if keyboard.is_pressed('esc'):
            break
            
    stream.stop_stream()
    stream.close()
    
    p.terminate()
    
    keyboard.press('backspace')
    
    wf = wave.open("output2.wav", 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    sys.stdout.flush()
    
    #Convert to 8 bit unsigned pcm
    data, samplerate = soundfile.read('output2.wav')
    soundfile.write('output.wav',data, fs, subtype='PCM_U8')
    
    os.remove("output2.wav")

    decode_option = input("Generated \"output.wav\" would you like to decode? (Y/N):")
    if decode_option == "Y" or decode_option == "y":
        decode_file("output.wav")
        

#initize dosbox location and devices
def init_dos():
    #get dosbox location (TODO check its a good filepath)
    if not os.path.isfile("pyKCSconfig.txt"):
        dosbox_location = input("Please input the filepath for DOSBox.exe\n"\
                                "For example C:\\Program Files (x86)\\DOSBox-0.74-3\\DOSBox.exe\n"\
                                "You only have to do this once:")
        while not os.path.isfile(dosbox_location):
            print("File not found.")
            dosbox_location = input("Please input the filepath for DOSBox.exe\n"\
                                "For example C:\\Program Files (x86)\\DOSBox-0.74-3\\DOSBox.exe\n"\
                                "You only have to do this once:")

        location_file = open("pyKCSconfig.txt","w")
        location_file.write(dosbox_location)
        location_file.write("\n")
        location_file.close()
        
        #get device numbers
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        
        print("\nSelect input device to record from (this should be your cassette player)\n")
        
        rec_devices = 0
        
        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
                rec_devices += 1
                
        device_id = int(input("Device ID:"))  
        
        while device_id > rec_devices or device_id < 0:
            print("Cant find that ID")
            device_id = int(input("Device ID:"))
            
        location_file = open("pyKCSconfig.txt","a")
        location_file.write(str(device_id))
        location_file.close()
        
    else:
        location_file = open("pyKCSconfig.txt","r")
        dosbox_location = location_file.readline().rstrip()
        device_id = int(location_file.readline())
        location_file.close()
        
    return dosbox_location, device_id


#Calculate decibels
def rms(data):
    count = len(data)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, data )
    sum_squares = 0.0
    for sample in shorts:
        n = sample * (1.0/32768)
        sum_squares += n*n
    return math.sqrt( sum_squares / count )
 
#Menu options
def menu():

    print("\nMENU\n\
1.Encode file\n\
2.Decode file\n\
3.Play WAV for cassette recording (TODO)\n\
4.Record cassette to WAV (TODO)\n\
5.Change settings (dosbox location, recording device) (TODO)\n\
6.Exit\n")

    menu_option = input("Select option:")

    while not menu_option == '1' and menu_option == '2' and menu_option == '3' and menu_option == '4' and menu_option == '5':
        print("\nNot an option please sellect 1-4\n")
        menu_option = input("Select option:")

    #Call correct function
    if menu_option == '1':
        encode_file()
    
    if menu_option == '2':
        print("\nDecode file")
        infile = input("Input WAV filename:")
        decode_file(infile)
      
    if menu_option == '3':
        print("Not supported on Linux at the moment")
        # TODO
        """
        file_to_play = input("Input WAV filename:")
        while not os.path.isfile(file_to_play):
            print("File not found.")
            file_to_play = input("Input WAV filename:")
        play_wav(file_to_play)
        """
        
    if menu_option == '4':
        print("Not supported on Linux at the moment")
        # TODO
        """
        record_wav()
        """
        
    if menu_option == '5':
        print("Not supported on Linux at the moment")
        # TODO
        """
        os.remove("pyKCSConfig.txt")
        init_dos()
        print ("\nRESTART the script for these changes to take effect.")
        """
        
    if menu_option == '6':
        quit()

# TODO
"""
dosbox_location, device_id = init_dos()
"""
#Working directory
cwd = os.getcwd()

while True:
    menu()

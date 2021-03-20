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
    return subprocess.call(reduce(lambda x, y: x  + ["-noconsole"] + ["-c"]  + [y], args, [dosbox_location] ))

def truncate_float(value, digits_after_point=2):
    pow_10 = 10 ** digits_after_point
    return (float(int(value * pow_10))) / pow_10

def encode_file():
    print("\nEncode file")
    infile = input("Input filename:")

    while not os.path.isfile(infile):
        print("File not found. Make sure the file is in the currect directory.")
        infile = input("Input filename:")

    if os.path.isfile("toEncode.mjr"):
        os.remove("toEncode.mjr")

    os.rename(infile,"toEncode.mjr")
    
    outfile = input("Output WAV filename:")

    if baud == "300":
        KCS = "KCS -M -Y -L5 " + "toEncode.mjr" + " " + "encode.wav"
    if baud == "1200":
        KCS = "KCS -M -Y -U -L5 " + "toEncode.mjr" + " " + "encode.wav"

    dosbox_args = [r'mount c ' + cwd,'C:',KCS,'exit']

    if os.path.isfile(outfile):
        os.remove(outfile)

    run_dosbox(dosbox_args)

    os.rename("toEncode.mjr",infile)
    os.rename("encode.wav",outfile)


    play_audio = input("Would you like to play \"" + outfile +"\"? (Y/N):")

    while play_audio != "y" and play_audio != "Y" and play_audio != "n" and play_audio != "N":
        print("Invalid input.")
        play_audio = input("Would you like to play \"" + outfile +"\"? (Y/N):")

    if play_audio == "Y" or play_audio == "y":
        play_wav(outfile,infile,auto_name)

def decode_file(infile):

    while not os.path.isfile(infile):
        print("File not found. Make sure the file is in the currect directory.")
        infile = input("Input WAV filename:")
    
    if os.path.isfile("toDecode.wav"):
        os.remove("toDecode.wav")

    os.rename(infile,"toDecode.wav")
    
    outfile = input("Output filename:")

    #choose the right baud and make KCS command to send to dosbox
    if baud == "300":
        KCS = "KCS -Y " + "toDecode.wav" + " " + "decode.mjr"
    if baud == "1200":
        KCS = "KCS -Y -U " + "toDecode.wav" + " " + "decode.mjr"

    dosbox_args = [r'mount c ' + cwd,'C:',KCS,'exit']

    #if theres already the file remove it and replace
    if os.path.isfile(outfile):
        os.remove(outfile)

    run_dosbox(dosbox_args)

    os.rename("toDecode.wav",infile)
    os.rename("decode.mjr",outfile)

    #keeping this commented to atone for my sins

    #if infile == "output.wav" and baud == "1200":
        #f = open(outfile, 'rb')
        #f.seek(1) # skip the first 1 byte
        #trim = f.read()
        #f.close()
        #trimmed = open(outfile, 'wb')
        #trimmed.write(trim)
        #trimmed.close()
        
    open_decode = input("Would you like to open \"" + outfile +"\"? (Y/N):")

    while open_decode != "y" and open_decode != "Y" and open_decode != "n" and open_decode != "N":
        print("Invalid input.")
        open_decode = input("Would you like to open \"" + outfile +"\"? (Y/N):")

    #open decoded file 
    if open_decode == "Y" or open_decode == "y":
       os.startfile(outfile)    

#Play audio
def play_wav(wav_file,infile,auto_name):

    if auto_name == "y" or auto_name == "Y":

        print("Encoding file details... ", end = '\r')

        if os.path.isfile("kcs_metadata.tmp"):
            os.remove("kcs_metadata.tmp")

        info_file = open("kcs_metadata.tmp" , "w")
        info_file.write(infile +"\n") 
        info_file.write(str(float(os.path.getsize(infile) / 1000)) + "\n")

        #get wav file duration
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
        info_file.write(str(duration) + "\n")

        info_file.close()

        os.rename("kcs_metadata.tmp","toEncode.mjr")
    
        out_info_file = "kcs_metadata.wav"

        if baud == "300":
            KCS = "KCS -M -Y -L5 " + "toEncode.mjr" + " " + "encode.wav"
        if baud == "1200":
            KCS = "KCS -M -Y -U -L5 " + "toEncode.mjr" + " " + "encode.wav"

        dosbox_args = [r'mount c ' + cwd,'C:',KCS,'exit']

        if os.path.isfile(out_info_file):
            os.remove(out_info_file)

        run_dosbox(dosbox_args)

        os.rename("toEncode.mjr","kcs_metadata.tmp")
        os.rename("encode.wav",out_info_file)
        print("Ready to play!              ")
        auto_name = "N"
        play_wav("kcs_metadata.wav","",auto_name)
        auto_name = "Y"
        os.remove("kcs_metadata.tmp")
        os.remove("kcs_metadata.wav")
        time.sleep(2)

    if auto_name == "N" or auto_name == "n":
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
    print("")
    sys.stdout.flush()  
    stream.stop_stream()  
    stream.close()  

    #close PyAudio  
    p.terminate()
    
    keyboard.press('backspace')
    sys.stdout.flush()
    
def record_wav():

    #stand audio setup
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
    sys.stdout.flush() #why the fuck am i still getting random things printing I DONT WANT THEM
    #detects when incoming audio stream is higher than -7db. It only records then. This should get the data only
    while True:
        sys.stdout.flush()   
        data = stream.read(chunk)
        rms_data = rms(data)
        decibel = 20 * math.log10(rms_data)
        if decibel < -7:
            print("Listening for data... %.2f decibels press esc to abort " % (decibel),end = '\r')
        if decibel > -7:
            print("Recording data... %.2f decibels press esc to abort     " % (decibel),end = '\r')
            #data2 = stream.read(chunk)
            recorded = 1
            frames.append(data)
        if recorded == 1 and decibel < -7: #detects data is done
            break
        if keyboard.is_pressed('esc'): #abort
            break
            
    stream.stop_stream()
    stream.close()
    
    p.terminate()

    keyboard.press('backspace')
    
    #delete blank spots from start (i hope this fixes the garbage byte)
    if len(frames) > 50:
        for i in range(50):
            frames.pop(0)

    wf = wave.open("output2.wav", 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    sys.stdout.flush()
    
    #Convert to 8 bit unsigned pcm (create new file and delete old)
    data, samplerate = soundfile.read('output2.wav')
    soundfile.write('output.wav',data, fs, subtype='PCM_U8')
    
    os.remove("output2.wav")

    decode_option = input("Generated \"output.wav\" would you like to decode? (Y/N):")

    while decode_option != "y" and decode_option != "Y" and decode_option != "n" and decode_option != "N":
        print("Invalid input.")
        decode_option = input("Generated \"output.wav\" would you like to decode? (Y/N):")

    #open decoded file 
    if decode_option == "Y" or decode_option == "y":
        decode_file("output.wav")
        

#initize dosbox location and devices and baud (longer than it has to be could seperate each option into new fcn to revoic repeating)
def init_dos(from_settings):

    if from_settings == True:

        setting_option = input("Select option:")
        
        while setting_option != '1' and setting_option != '2' and setting_option != '3' and setting_option != '4':
            print("\nNot an option please select 1-3\n")
            setting_option = input("Select option:")

        with open("pyKCSconfig.txt", 'r') as settings:
            lines = settings.readlines()

        if setting_option == '1':

            dosbox_location = input("Please input the filepath for DOSBox.exe\n"\
                                "For example C:\\Program Files (x86)\\DOSBox-0.74-3\\DOSBox.exe\n"\
                                "You only have to do this once:")
            while not os.path.isfile(dosbox_location):
                print("File not found.")
                dosbox_location = input("Please input the filepath for DOSBox.exe\n"\
                                "For example C:\\Program Files (x86)\\DOSBox-0.74-3\\DOSBox.exe\n"\
                                "You only have to do this once:")

            lines[0] = dosbox_location + "\n"
            device_id = lines [1]
            baud = lines[2]
            lines[3] = auto_name

        if setting_option == '2':

            #get audio devices
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

            lines[1] = str(device_id) + "\n"
            dosbox_location = lines[0]
            baud = lines[2]
            lines[3] = auto_name

        if setting_option == '3':

            baud = input("\nWould you like to encode at 300 or 1200 baud? (300 is easier for lower quality cassette recorders):")

            while baud != "300" and baud != "1200":
                print("Invalid choice")
                baud = input("\nWould you like to encode at 300 or 1200 baud? (300 is easier for lower quality cassette recorders):")

            lines[2] = baud + "\n"    
            dosbox_location = lines[0]
            device_id = lines[1]
            lines[3] = auto_name

        if setting_option == '4':

            auto_name = input("\nWould you like to automaticly store file names for easier decoding?\nThis setting will encode and store the filename with the file.\nWhen decoding it will automaticly give the file its correct name.\n\nEnable? (Y/N):")
            while auto_name != "y" and auto_name != "Y" and auto_name != "n" and auto_name != "N":
                print("Invalid input.")
                auto_name = input("\nWould you like to automaticly store file names for easier decoding?\nThis setting will encode and store the filename with the file.\nWhen decoding it will automaticly give the file its correct name.\n\nEnable? (Y/N):")
            
            lines[3] = auto_name + "\n"    
            dosbox_location = lines[0]
            device_id = lines[1]
            baud = lines[2]
   
        with open("pyKCSconfig.txt", 'w') as settings:
            settings.writelines( lines )

    if not os.path.isfile("pyKCSconfig.txt") and from_settings == False:
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
        
        
        #get audio devices
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
            

        location_file.write(str(device_id) + "\n")

        baud = input("\nWould you like to encode at 300 or 1200 baud? (300 is easier for lower quality cassette recorders):")

        while baud != "300" and baud != "1200":
            print("Invalid choice")
            baud = input("\nWould you like to encode at 300 or 1200 baud? (300 is easier for lower quality cassette recorders):")

        location_file.write(baud)
        location_file.write("\n")


        auto_name = input("\nWould you like to automaticly store file names for easier decoding?\nThis setting will encode and store the filename with the file.\nWhen decoding it will automaticly give the file its correct name.\n\nEnable? (Y/N):")

        while auto_name != "y" and auto_name != "Y" and auto_name != "n" and auto_name != "N":
            print("Invalid input.")
            auto_name = input("\nWould you like to automaticly store file names for easier decoding?\nThis setting will encode and store the filename with the file.\nWhen decoding it will automaticly give the file its correct name.\n\nEnable? (Y/N):")

        if auto_name == "Y" or auto_name == "y":
            location_file.write(auto_name)
            location_file.write("\n")

        location_file.close()    

    elif from_settings == False:
        location_file = open("pyKCSconfig.txt","r")
        dosbox_location = location_file.readline().rstrip()
        device_id = int(location_file.readline().rstrip())
        baud = location_file.readline().rstrip()
        auto_name = location_file.readline().rstrip()
        location_file.close()

    return dosbox_location, device_id, baud , auto_name


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
def menu(dosbox_location,device_id,baud,auto_name):
    #print(auto_name)
    print("\nMENU\n\
1.Encode file\n\
2.Decode file\n\
3.Play WAV for cassette recording\n\
4.Record cassette to WAV\n\
5.Change settings (dosbox location, recording device, baud rate)\n\
6.Exit\n")

    menu_option = input("Select option:")

    while menu_option != '1' and menu_option != '2' and menu_option != '3' and menu_option != '4' and menu_option != '5' and menu_option != '6':
        print("\nNot an option please select 1-6\n")
        menu_option = input("Select option:")

    #Call correct function
    if menu_option == '1':
        encode_file()
    
    if menu_option == '2':
        print("\nDecode file")
        infile = input("Input WAV filename:")
        decode_file(infile)
      
    if menu_option == '3':

        #default
        infile = ""

        file_to_play = input("Input WAV filename:")
        while not os.path.isfile(file_to_play):
            print("File not found.")
            file_to_play = input("Input WAV filename:")
        
        if(auto_name == "y" or auto_name == "Y"):
            #TODO if this file doesnt exist ask them for its details
            infile = input("Original filename:")
            play_wav(file_to_play,infile,auto_name)    
        else:
            play_wav(file_to_play,infile,"N")
        
    if menu_option == '4':
        record_wav()
        
    if menu_option == '5':
        print("\nSETTINGS\n1.Edit DOSBox location: \"%s\"\n2.Change default recording device: Device #: %s\n3.Select baud rate: %s baud\n4.Automatically encode filenames: %s" % (dosbox_location,device_id,baud,auto_name))
        dosbox_location, device_id, baud, auto_name = init_dos(True)

    if menu_option == '6':
        quit()

dosbox_location, device_id, baud, auto_name = init_dos(False)
#Working directory
cwd = os.getcwd()

while True:
    if os.path.isfile("pyKCSconfig.txt"):
        file = open("pyKCSconfig.txt","r")
        lines = file.readlines()
        dosbox_location = lines[0].rstrip()
        device_id = int(lines [1].rstrip())
        baud = lines[2].rstrip()
        auto_name = lines[3].rstrip()     
    menu(dosbox_location,device_id,baud,auto_name)
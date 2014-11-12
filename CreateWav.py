import math
import wave
import struct
from config import *


fname = "WaveTest.wav"
frate = 11025.0  # framerate as a float
amp = 64000.0     # multiplier for amplitude
word = ''

sine_list_x = []
def write_wav_data_element(freq, vars):
    for x in range(int(vars.data_size)):
        sine_list_x.append(math.sin(2*math.pi*freq*(x/frate)))

def write_wav_data(progress, close_flag, vars):
    del sine_list_x[:]
    wav_file = wave.open(fname, "w")
    nchannels = 1
    sampwidth = 2
    framerate = int(frate)
    nframes = vars.data_size
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, framerate, nframes,
    comptype, compname))
    write_wav_data_element(vars.freqBeginEnd, vars)
    write_wav_data_element(vars.freqBeginEnd, vars)
    f = open('workfile.txt', 'r')
    str = word#f.read()
    progress['value']=25
    for i in str:
        k = ord(i)
        a = bin(k)
        for j in a:
            if j == '0':
                write_wav_data_element(vars.freq0, vars)
            if j == '1':
                write_wav_data_element(vars.freq1, vars)
            if j == 'b':
                write_wav_data_element(vars.freqb, vars)
    write_wav_data_element(vars.freqBeginEnd, vars)
    write_wav_data_element(vars.freqBeginEnd, vars)
    progress['value']=50
    for s in sine_list_x:
        wav_file.writeframes(struct.pack('h', int(s*amp/2)))
    progress['value']=100
    close_flag = True
    #progress.destroy()
    wav_file.close()
    del sine_list_x[:]




#!/usr/bin/env python
import pyaudio
from wave import struct as wave_struct
import wave
from numpy import blackman
from numpy.fft import rfft
from numpy import array
import numpy
import sys, time, os
import curses
from threading import Thread
from config import*

loop_running = False
#WINDOW = blackman(vars.CHUNK) # Using blackman window. For more information see
try: # Windows?
    import msvcrt
    def kbfunc():
        return ord(msvcrt.getch()) if msvcrt.kbhit() else 0
except: # Unix/Mac
    import select
    def kbfunc():
        inp, out, err = select.select([sys.stdin], [], [], 0.001) # 0.1 second delay
        return sys.stdin.readline() if sys.stdin in inp else 0

def play(vars):
    #define stream chunk
    #chunk = 1024
    #open a wav format music
    f = wave.open(r"WaveTest.wav","rb")
    #instantiate PyAudio
    p = pyaudio.PyAudio()
    #open stream
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                    channels = f.getnchannels(),
                    rate = f.getframerate(),
                    output = True)
    #read data
    data = f.readframes(vars.CHUNK)
    #paly stream
    while data != '':
        stream.write(data)
        data = f.readframes(vars.CHUNK)
    #stop stream
    stream.stop_stream()
    stream.close()
    #close PyAudio
    p.terminate()
    f.close()

class Decoder:

    term_width = 80 # Stores the character width of the terminal

    def __init__(self, vars):
        self.term_width = int(168)
        self.freq_list = []
        self.binstr = ''
        self.finStr = ''
        self.WINDOW = blackman(vars.CHUNK) # Using blackman window. For more information see


    def _open_audio(self, vars):
        """ Opens the audio device for listening """
        audio = pyaudio.PyAudio()
        stream = None
        while True: # Fix for Mac OS
            stream = audio.open(format = pyaudio.paInt16,
                                channels = 1,
                                rate = vars.RATE,
                                input = True,
                                output = False, # TODO
                                frames_per_buffer = vars.CHUNK)
            try:
                # On Mac OS, the first call to stream.read usually fails
                data = stream.read(vars.CHUNK)
                break
            except:
                stream.close()
        self.audio = audio
        self.stream = stream



    def _loop(self, vars):
        """ This loop runs until the user hits the Enter key """
        last_n = [0] * vars.SAMPLE_SIZE # Stores the values of the last N frequencies.
                                   # This list is used as an array
        curpos = 0   # Stores the index to the array where we will store our next value
        last_avg = 1 # Stores the average of the last N set of samples.
                     # This value will be compared to the current average to detect
                     # the change in note
        # play stream and find the frequency of each chunk
        #i = 0
        while loop_running:
            perfect_cnt = 0
            data = self.stream.read(vars.CHUNK)
            # unpack the data and times by the hamming window
            indata = array(wave_struct.unpack("%dh"%(len(data)/2), data))*self.WINDOW

            # Take the fft and square each value
            fftData=abs(rfft(indata))**2
            # find the maximum
            which = fftData[1:].argmax() + 1
            # use quadratic interpolation around the max
            thefreq = 0
            if which != len(fftData)-1:
                y0, y1, y2 = numpy.log(fftData[which-1:which+2:])
                x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
                # find the frequency and output it
                thefreq = (which+x1)*vars.RATE/vars.CHUNK
            else:
                thefreq = which*vars.RATE/vars.CHUNK
            # Store this freq in an array
            last_n[curpos] = int(thefreq)
            curpos += 1
            if curpos == vars.SAMPLE_SIZE:
                curpos = 0
            this_avg = sum(last_n) / vars.SAMPLE_SIZE # Compute the average
            #print(thefreq)
            self.freq_list.append(thefreq)
            #i += 1
            #if i == 1800:
            #    break


    def theMostCommonFreq(self, start, end, vars):
        amount_zeros = 0
        amount_ones = 0
        amount_of_b = 0
        amount_of_begin = 0
        for a in range(start, end, 1):
            if (self.freq_list[a] >= vars.Target_0 - 10) and (self.freq_list[a] <= vars.Target_0 + 10):
                amount_zeros = amount_zeros+1
            if (self.freq_list[a] >= vars.Target_1 - 10) and (self.freq_list[a] <= vars.Target_1 + 10):
                amount_ones = amount_ones + 1
            if (self.freq_list[a] >= vars.Target_b - 10) and (self.freq_list[a] <= vars.Target_b + 10):
                amount_of_b = amount_of_b + 1
            if (self.freq_list[a] >= vars.Target_Begin - 10) and (self.freq_list[a] <= vars.Target_Begin + 10):
                amount_of_begin = amount_of_begin + 1

        #if amount_ones == 0 and amount_zeros == 0 and amount_of_b == 0:
          #  return -1
        if amount_zeros > amount_ones and amount_zeros > amount_of_b and amount_zeros > amount_of_begin:
            return 0
        if amount_ones > amount_zeros and amount_ones > amount_of_b and amount_ones > amount_of_begin:
            return 1
        if amount_of_b > amount_ones and amount_of_b > amount_zeros and amount_of_b > amount_of_begin:
            return 2
        if amount_of_begin > amount_ones and amount_of_begin > amount_zeros and amount_of_begin > amount_of_b:
            return -1


    def analize_freq_list(self, vars):
        signal_size = 0
        beg = 0
        end = 0
        for a in range(0, len(self.freq_list), 1):
            if (self.freq_list[a] >= vars.Target_Begin - 10) and (self.freq_list[a] <= vars.Target_Begin+10)and beg == 0:
                beg = a
            if (self.freq_list[a] >= vars.Target_0 - 30) and (self.freq_list[a] <= vars.Target_0 + 30)or(self.freq_list[a] >= vars.Target_1 - 30) and (self.freq_list[a] <= vars.Target_1 +30):
                end = a - 1
                break
        signal_size = end - beg

        signal_size = 16
        for s in range(end, len(self.freq_list), signal_size):
            if self.theMostCommonFreq(s, s + signal_size, vars) == 0:
                self.binstr += '0'
            if self.theMostCommonFreq(s, s + signal_size, vars) == 1:
                self.binstr += '1'
            if self.theMostCommonFreq(s, s + signal_size, vars) == 2:
                self.binstr += 'b'
            if self.theMostCommonFreq(s, s + signal_size, vars) == -1:
                break



    def transformBinStr(self):
        arr = []
        b = ''
        k = []
        self.finStr = ''
        for a in range(0, len(self.binstr), 1):
            if self.binstr[a] == 'b':
                k.append(a)
        for m in range(0, len(k), 1):
            if m > 0:
                b = ''
                for i in range(k[m-1]+1, k[m]-1, 1):
                    b += self.binstr[i]
                arr.append(int(b, 2))
            if m == len(k)-1:
                b = ''
                for p in range(k[m]+1, len(self.binstr), 1):
                    b += self.binstr[p]
                arr.append(int(b, 2))
        for j in arr:
            if j <= 128:
                self.finStr += chr(j)
            else:
                self.finStr += "*"

    def _close_audio(self):
        """ Call this function at the end """
        self.stream.close()
        self.audio.terminate()

    def process(self, vars):
        print 'loop_finish'
        self.analize_freq_list(vars)
        print self.binstr
        self._close_audio()
        self.transformBinStr()
        self.binstr = ''
        print self.finStr

    def decode(self, vars):
        self.term_width = int(168)
        self.freq_list = []
        self.binstr = ''
        self.finStr = ''
        self._open_audio(vars)
        self._loop(vars)


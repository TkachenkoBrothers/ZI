#!/usr/bin/env python
import pyaudio
from wave import struct as wave_struct
from numpy import blackman
from numpy.fft import rfft
from numpy import array
import numpy
import sys, time, os
import curses




CHUNK = 250 # Chunk of audio input to consider
RATE = 44100 # Recording rate
WINDOW = blackman(CHUNK) # Using blackman window. For more information see
SAMPLE_SIZE = 8
                # Number of data points to average over. This is used for 2 things
                # 1. Reducing noise between subsequent string strokes
                # 2. We don't output too many values which might confuse the user
Target_Begin = 5000
Target_0 = 5200
Target_1 = 5300
Target_b = 5400

loop_running = False

try: # Windows?
    import msvcrt
    def kbfunc():
        return ord(msvcrt.getch()) if msvcrt.kbhit() else 0
except: # Unix/Mac
    import select
    def kbfunc():
        inp, out, err = select.select([sys.stdin], [], [], 0.001) # 0.1 second delay
        return sys.stdin.readline() if sys.stdin in inp else 0

class Decoder:

    term_width = 80 # Stores the character width of the terminal

    def __init__(self):
        self.term_width = int(168)
        self.freq_list = []
        self.binstr = ''
        self.finStr = ''



    def _open_audio(self):
        """ Opens the audio device for listening """
        audio = pyaudio.PyAudio()
        stream = None
        while True: # Fix for Mac OS
            stream = audio.open(format = pyaudio.paInt16,
                                channels = 1,
                                rate = RATE,
                                input = True,
                                output = False, # TODO
                                frames_per_buffer = CHUNK)
            try:
                # On Mac OS, the first call to stream.read usually fails
                data = stream.read(CHUNK)
                break
            except:
                stream.close()
        self.audio = audio
        self.stream = stream



    def _loop(self):
        """ This loop runs until the user hits the Enter key """
        last_n = [0] * SAMPLE_SIZE # Stores the values of the last N frequencies.
                                   # This list is used as an array
        curpos = 0   # Stores the index to the array where we will store our next value
        last_avg = 1 # Stores the average of the last N set of samples.
                     # This value will be compared to the current average to detect
                     # the change in note
        # play stream and find the frequency of each chunk
        i = 0
        while True:
            perfect_cnt = 0
            data = self.stream.read(CHUNK)
            # unpack the data and times by the hamming window
            indata = array(wave_struct.unpack("%dh"%(len(data)/2), data))*WINDOW

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
                thefreq = (which+x1)*RATE/CHUNK
            else:
                thefreq = which*RATE/CHUNK
            # Store this freq in an array
            last_n[curpos] = int(thefreq)
            curpos += 1
            if curpos == SAMPLE_SIZE:
                curpos = 0
            this_avg = sum(last_n) / SAMPLE_SIZE # Compute the average
            #print(thefreq)
            self.freq_list.append(thefreq)
            i += 1
            if i == 1800:
                break


    def theMostCommonFreq(self, start, end):
        amount_zeros = 0
        amount_ones = 0
        amount_of_b = 0
        amount_of_begin = 0
        for a in range(start, end, 1):
            if (self.freq_list[a] >= Target_0 - 10) and (self.freq_list[a] <= Target_0 + 10):
                amount_zeros = amount_zeros+1
            if (self.freq_list[a] >= Target_1 - 10) and (self.freq_list[a] <= Target_1 + 10):
                amount_ones = amount_ones + 1
            if (self.freq_list[a] >= Target_b - 10) and (self.freq_list[a] <= Target_b + 10):
                amount_of_b = amount_of_b + 1
            if (self.freq_list[a] >= Target_Begin - 10) and (self.freq_list[a] <= Target_Begin + 10):
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


    def analize_freq_list(self):
        signal_size = 0
        beg = 0
        end = 0
        for a in range(0, len(self.freq_list), 1):
            if (self.freq_list[a] >= Target_Begin - 10) and (self.freq_list[a] <= Target_Begin+10)and beg == 0:
                beg = a
            if (self.freq_list[a] >= Target_0 - 30) and (self.freq_list[a] <= Target_0 + 30)or(self.freq_list[a] >= Target_1 - 30) and (self.freq_list[a] <= Target_1 +30):
                end = a - 1
                break
        signal_size = end - beg

        signal_size = 16
        for s in range(end, len(self.freq_list), signal_size):
            if self.theMostCommonFreq(s, s + signal_size) == 0:
                self.binstr += '0'
            if self.theMostCommonFreq(s, s + signal_size) == 1:
                self.binstr += '1'
            if self.theMostCommonFreq(s, s + signal_size) == 2:
                self.binstr += 'b'
            if self.theMostCommonFreq(s, s + signal_size) == -1:
                break



    def transformBinStr(self):
        arr = []
        b = ''
        k = []

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

    def decode(self):
        self._open_audio()
        self._loop()
        self.analize_freq_list()
        print self.binstr
        self._close_audio()
        self.transformBinStr()
        print self.finStr





if __name__ == '__main__':
    u = Decoder()
    u.decode()

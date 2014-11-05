__author__ = 'Roman'
from Tkinter import *
import CreateWav
import Decoder
from threading import Thread

SPEED_OPTIONS_VIEW = [
    'extra low',
    'low',
    'middle',
    'high',
    'extra high',
]

SPEED_OPTIONS_CREATE_WAV = {
    'extra low': 8000,
    'low': 4000,
    'middle': 2000,
    'high': 1000,
    'extra high': 500,
}

SPEED_OPTIONS_DECODER = {
    'extra low': 2000,
    'low': 1000,
    'middle': 500,
    'high': 250,
    'extra high': 125,
}

DEFAULT_SETTINGS = {
    'data_size': 1000,
    'CHUNK': 250,
    'freqBeginEnd': 5000.0,
    'freq0': 5200.0,
    'freq1': 5300.0,
    'freqb': 5400.0,
    'Target_Begin': 5000,
    'Target_0':5200,
    'Target_1': 5300,
    'Target_b': 5400,
}

OPTIONS_MODE = 'options'
CODE_MODE = 'code'
DECODE_MODE = 'decode'
INFO_MODE = 'info'

def print_vars():
    print "setting data_size = ", CreateWav.data_size
    print "setting CHUNK = ", Decoder.CHUNK
    print "setting freqBeginEnd = ", CreateWav.freqBeginEnd
    print "setting freq0 = ", CreateWav.freq0
    print "setting freq1 = ", CreateWav.freq1
    print "setting freq1 = ", CreateWav.freq1

class App(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.menuframe = Frame(self)
        self.menuframe.grid(column=0, row=0, rowspan=4, sticky=(N, W, E, S))
        self.menuframe.columnconfigure(0, weight=0)
        self.menuframe.rowconfigure(0, weight=1)
        self.menuframe.rowconfigure(1, weight=1)
        self.menuframe.rowconfigure(2, weight=1)
        self.menuframe.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.create_widgets()
    def create_widgets(self):
        self.mode = 'code'
        self.button_coder = Button(self.menuframe, text="Coder", relief=SUNKEN, command=self.button_coder_click)
        self.button_coder.grid(column=0, row=0,padx=5, pady=5, sticky="nsew")
        self.button_decoder = Button(self.menuframe, text="Decoder", relief=RAISED, command=self.button_decoder_click)
        self.button_decoder.grid(column=0, row=1,padx=5, pady=5, sticky="nsew")
        self.button_options = Button(self.menuframe, text="Options", relief=RAISED, command=self.button_options_click)
        self.button_options.grid(column=0, row=2,padx=5, pady=5, sticky="nsew")
        self.button_info = Button(self.menuframe, text="Info", relief=RAISED, command=self.button_info_click)
        self.button_info.grid(column=0, row=3,padx=5, pady=5, sticky="nsew")
        self.create_coder()

    def button_options_click(self):
        self.config_modes(self.mode, OPTIONS_MODE)
        self.create_options()

    def destroy_options(self):
        self.speed_options_dropdown.destroy()
        self.label_speed_options.destroy()
        self.freq_begin_end.destroy()
        self.freq0.destroy()
        self.freq1.destroy()
        self.freq2.destroy()
        self.label_freq_begin_end.destroy()
        self.label_freq0.destroy()
        self.label_freq1.destroy()
        self.label_freq2.destroy()
        self.button_save_options.destroy()
        self.button_set_default_options.destroy()

    def create_options(self):
        self.speed = StringVar(self)
        self.speed.set(SPEED_OPTIONS_VIEW[2]) # default value
        self.speed_options_dropdown = apply(OptionMenu, (self, self.speed) + tuple(SPEED_OPTIONS_VIEW))
        self.speed_options_dropdown.grid(column=2, row=0, padx=5, pady=5, sticky="nsew")
        self.label_speed_options = Label(self, text="Speed")
        self.label_speed_options.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")
        self.freq_begin_end = Entry(self)
        self.freq_begin_end.grid(column=2, row=1, columnspan=4, padx=5, pady=5, sticky="nsew")
        self.label_freq_begin_end = Label(self, text="Freq begin end")
        self.label_freq_begin_end.grid(column=1, row=1, padx=5, pady=5, sticky="nsew")
        self.freq0 = Entry(self)
        self.freq0.grid(column=2, row=2, columnspan=4, padx=5, pady=5, sticky="nsew")
        self.label_freq0 = Label(self, text="Freq 0")
        self.label_freq0.grid(column=1, row=2, padx=5, pady=5, sticky="nsew")
        self.freq1 = Entry(self)
        self.freq1.grid(column=2, row=3, columnspan=4, padx=5, pady=5, sticky="nsew")
        self.label_freq1 = Label(self, text="Freq 1")
        self.label_freq1.grid(column=1, row=3, padx=5, pady=5, sticky="nsew")
        self.freq2 = Entry(self)
        self.freq2.grid(column=2, row=4, columnspan=4, padx=5, pady=5, sticky="nsew")
        self.label_freq2 = Label(self, text="Freq 2")
        self.label_freq2.grid(column=1, row=4, padx=5, pady=5, sticky="nsew")
        self.button_set_default_options = Button(self, text="Default", command=self.button_set_default_options_click)
        self.button_set_default_options.grid(column=3, row=5,padx=5, pady=5, sticky="nsew")
        self.button_save_options = Button(self, text="Save", command=self.button_save_options_click)
        self.button_save_options.grid(column=4, row=5,padx=5, pady=5, sticky="nsew")
        self.freq_begin_end.insert(0, str(CreateWav.freqBeginEnd))
        self.freq0.insert(0, str(CreateWav.freq0))
        self.freq1.insert(0, str(CreateWav.freq1))
        self.freq2.insert(0, str(CreateWav.freqb))

    def button_set_default_options_click(self):
        CreateWav.data_size = DEFAULT_SETTINGS['data_size']
        Decoder.CHUNK = DEFAULT_SETTINGS['CHUNK']
        CreateWav.freqBeginEnd = DEFAULT_SETTINGS['freqBeginEnd']
        CreateWav.freq0 = DEFAULT_SETTINGS['freq0']
        CreateWav.freq1 = DEFAULT_SETTINGS['freq1']
        CreateWav.freqb = DEFAULT_SETTINGS['freqb']
        Decoder.Target_Begin = DEFAULT_SETTINGS['Target_Begin']
        Decoder.Target_0 = DEFAULT_SETTINGS['Target_0']
        Decoder.Target_1 = DEFAULT_SETTINGS['Target_1']
        Decoder.Target_b = DEFAULT_SETTINGS['Target_b']
        self.button_options_click()
        print_vars()

    def button_save_options_click(self):
        CreateWav.data_size = SPEED_OPTIONS_CREATE_WAV[self.speed.get()]
        Decoder.CHUNK = SPEED_OPTIONS_DECODER[self.speed.get()]
        CreateWav.freqBeginEnd = self.freq_begin_end.get()
        CreateWav.freq0 = self.freq0.get()
        CreateWav.freq1 = self.freq1.get()
        CreateWav.freqb = self.freq2.get()
        Decoder.Target_Begin = self.freq_begin_end.get()
        Decoder.Target_0 = self.freq0.get()
        Decoder.Target_1 = self.freq1.get()
        Decoder.Target_b = self.freq2.get()
        print_vars()

    def config_modes(self, prev_mode, curr_mode):
        if prev_mode == DECODE_MODE:
            self.destroy_decoder()
        if prev_mode == INFO_MODE:
            self.destroy_info()
        if prev_mode == CODE_MODE:
            self.destroy_coder()
        if prev_mode == OPTIONS_MODE:
            self.destroy_options()
        if curr_mode == 'code':
            self.mode = CODE_MODE
            self.button_coder.config(relief=SUNKEN)
            self.button_decoder.config(relief=RAISED)
            self.button_info.config(relief=RAISED)
            self.button_options.config(relief=RAISED)
        if curr_mode == 'decode':
            self.mode = DECODE_MODE
            self.button_coder.config(relief=RAISED)
            self.button_decoder.config(relief=SUNKEN)
            self.button_info.config(relief=RAISED)
            self.button_options.config(relief=RAISED)
        if curr_mode == 'info':
            self.mode = INFO_MODE
            self.button_coder.config(relief=RAISED)
            self.button_decoder.config(relief=RAISED)
            self.button_info.config(relief=SUNKEN)
            self.button_options.config(relief=RAISED)
        if curr_mode == 'options':
            self.mode = OPTIONS_MODE
            self.button_coder.config(relief=RAISED)
            self.button_decoder.config(relief=RAISED)
            self.button_info.config(relief=RAISED)
            self.button_options.config(relief=SUNKEN)

    def create_coder_text_box(self):
        self.coder_text_box = Entry(self)
        self.coder_text_box.grid(column=1, columnspan=4, rowspan=4, row=0, padx=5, pady=5, sticky="nsew")
    def destroy_coder_text_box(self):
        self.coder_text_box.destroy()

    def create_decoder_text_box(self):
        self.decoder_text_box = Entry(self)
        self.decoder_text_box.grid(column=1, columnspan=4, rowspan=4, row=0, padx=5, pady=5, sticky="nsew")
    def destroy_decoder_text_box(self):
        self.decoder_text_box.destroy()

    def create_code_accept_button(self):
        self.button_accept_code = Button(self, text="Code", command=self.button_accept_code_click)
        self.button_accept_code.grid(column=4, row=5, padx=5, pady=5, sticky="nsew")
    def destroy_code_accept_button(self):
        self.button_accept_code.destroy()

    def create_code_play_button(self):
        self.button_play_code = Button(self, text="Play")
        self.button_play_code.grid(column=1, row=5, padx=5, pady=5, sticky="nsew")
    def destroy_code_play_button(self):
        self.button_play_code.destroy()

    def create_decode_stop_button(self):
        self.button_stop_decode = Button(self, text="Stop", command=self.button_decode_stop_click)
        self.button_stop_decode.grid(column=4, row=5,padx=5, pady=5, sticky="nsew")
    def destroy_decode_stop_button(self):
        self.button_stop_decode.destroy()

    def create_decode_start_button(self):
        self.button_start_decode = Button(self, text="Start", command=self.button_decode_start_click)
        self.button_start_decode.grid(column=1, row=5, padx=5, pady=5, sticky="nsew")
    def destroy_decode_start_button(self):
        self.button_start_decode.destroy()

    def create_decoder(self):
        self.create_decoder_text_box()
        self.create_decode_stop_button()
        self.create_decode_start_button()
        self.mode = 'decode'
    def destroy_decoder(self):
        self.destroy_decoder_text_box()
        self.destroy_decode_stop_button()
        self.destroy_decode_start_button()

    def create_coder(self):
        self.create_code_accept_button()
        self.create_coder_text_box()
        self.create_code_play_button()
        self.mode = 'code'
    def destroy_coder(self):
        self.destroy_code_accept_button()
        self.destroy_coder_text_box()
        self.destroy_code_play_button()

    def create_info(self):
        self.label_info = Label(self, text="This is beta version of sound \n coder program. Hello World i say to you!")
        self.label_info.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")
    def destroy_info(self):
        self.label_info.destroy()

    def button_decode_start_click(self):
        decoder = Decoder.Decoder()
        Decoder.loop_running = True
        t = Thread(target=decoder.decode)
        t.start()

    def button_decode_stop_click(self):
        Decoder.loop_running = False

    def button_coder_click(self):
        self.config_modes(self.mode, CODE_MODE)
        self.create_coder()

    def button_decoder_click(self):
        self.config_modes(self.mode, DECODE_MODE)
        self.create_decoder()

    def button_info_click(self):
        self.config_modes(self.mode, INFO_MODE)
        self.create_info()

    def button_accept_code_click(self):
        if self.mode == 'code' and self.coder_text_box.get():
            CreateWav.write_wav_data(self.coder_text_box.get())


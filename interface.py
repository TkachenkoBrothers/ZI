__author__ = 'Roman'
from Tkinter import *
import CreateWav
import Decoder

class App(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
    def create_widgets(self):
        self.mode = 'code'
        self.button_coder = Button(self, text="Coder", relief=SUNKEN, command=self.button_coder_click)
        self.button_coder.grid(column=0, row=0,padx=5, pady=5, sticky="nsew")
        self.button_decoder = Button(self, text="Decoder", relief=RAISED, command=self.button_decoder_click)
        self.button_decoder.grid(column=0, row=1,padx=5, pady=5, sticky="nsew")
        self.button_info = Button(self, text="Info", relief=RAISED, command=self.button_info_click)
        self.button_info.grid(column=0, row=2,padx=5, pady=5, sticky="nsew")
        self.create_coder()

    def create_coder_text_box(self):
        self.coder_text_box = Entry(self)
        self.coder_text_box.grid(column=1, columnspan=4, rowspan=3, row=0, padx=5, pady=5, sticky="nsew")
    def destroy_coder_text_box(self):
        self.coder_text_box.destroy()

    def create_decoder_text_box(self):
        self.decoder_text_box = Entry(self)
        self.decoder_text_box.grid(column=1, columnspan=4, rowspan=3, row=0, padx=5, pady=5, sticky="nsew")
    def destroy_decoder_text_box(self):
        self.decoder_text_box.destroy()

    def create_code_accept_button(self):
        self.button_accept_code = Button(self, text="Code", command=self.button_accept_code_click)
        self.button_accept_code.grid(column=4, row=3,padx=5, pady=5, sticky="nsew")
    def destroy_code_accept_button(self):
        self.button_accept_code.destroy()

    def create_code_play_button(self):
        self.button_play_code = Button(self, text="Play")
        self.button_play_code.grid(column=1, row=3,padx=5, pady=5, sticky="nsew")
    def destroy_code_play_button(self):
        self.button_play_code.destroy()

    def create_decode_stop_button(self):
        self.button_stop_decode = Button(self, text="Stop", command=self.button_decode_stop_click)
        self.button_stop_decode.grid(column=4, row=3,padx=5, pady=5, sticky="nsew")
    def destroy_decode_stop_button(self):
        self.button_stop_decode.destroy()

    def create_decode_start_button(self):
        self.button_start_decode = Button(self, text="Start", command=self.button_decode_start_click)
        self.button_start_decode.grid(column=1, row=3,padx=5, pady=5, sticky="nsew")
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
        self.mode = 'info'
    def destroy_info(self):
        self.label_info.destroy()

    def button_decode_start_click(self):
        decoder = Decoder.Decoder()
        Decoder.loop_running = True
        decoder.decode()

    def button_decode_stop_click(self):
        Decoder.loop_running = False

    def button_coder_click(self):
        self.button_coder.config(relief=SUNKEN)
        self.button_decoder.config(relief=RAISED)
        self.button_info.config(relief=RAISED)
        if self.mode == 'decode':
            self.destroy_decoder()
        if self.mode == 'info':
            self.destroy_info()
        self.create_coder()
    def button_decoder_click(self):
        self.button_coder.config(relief=RAISED)
        self.button_decoder.config(relief=SUNKEN)
        self.button_info.config(relief=RAISED)
        if self.mode == 'code':
            self.destroy_coder()
        if self.mode == 'info':
            self.destroy_info()
        self.create_decoder()
    def button_info_click(self):
        self.button_coder.config(relief=RAISED)
        self.button_decoder.config(relief=RAISED)
        self.button_info.config(relief=SUNKEN)
        if self.mode == 'decode':
            self.destroy_decoder()
        if self.mode == 'code':
            self.destroy_coder()
        self.create_info()
    def button_accept_code_click(self):
        if self.mode == 'code' and self.coder_text_box.get():
            CreateWav.write_wav_data(self.coder_text_box.get())


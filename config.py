
class Vars():
    def __init__(self):
        self.SAMPLE_SIZE = 8
        self.Target_Begin = 5000
        self.Target_0 = 5200
        self.Target_1 = 5300
        self.Target_b = 5400

        self.freq0 = 5200.0
        self.freq1 = 5300.0
        self.freqb = 5400.0
        self.freqBeginEnd = 5000.0
        self.data_size = 1000
        self.CHUNK = 250 # Chunk of audio input to consider
        self.RATE = 44100 # Recording rate


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
from os import path
import argparse
import librosa
import numpy as np
import matplotlib.pyplot as plt
import soundfile
import wave
import contextlib
import math


def read_wav_file(path):
    s, sr = librosa.load(path)
    return s,sr


def get_sound_length(path):
    with contextlib.closing(wave.open(path,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration


def time_stretch(sound, rate):
    # rate > 1, then the signal is sped up.
    # rate < 1, then the signal is slowed down
    sound_stretched = librosa.effects.time_stretch(sound, rate)
    return sound_stretched


def plot(x, y, ouput_name, x_label=None, y_label=None):
    plt.plot(x, y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.plot()
    plt.savefig("C:/Users/namn/PycharmProjects/Sound/"+ouput_name)
    #plt.show()


def select_portion(sound, left=0, right=0):
    left = left * sound[1]
    right = right * sound[1]
    return sound[0][left:right], sound[0][:left], sound[0][right:], left, right


if __name__ == '__main__':
    sound = read_wav_file("ImperialMarch60.wav")
    x = sound[0]
    sr = sound[1]
    sound_fast = librosa.effects.time_stretch(x, 2)
    soundfile.write('ImperialMarch60_fast.wav', sound_fast, 22050, subtype='PCM_24')


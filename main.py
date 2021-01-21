from os import path
import argparse
import librosa
import numpy as np
import matplotlib.pyplot as plt
import soundfile
import wave
import contextlib
import math


def get_sound_length(path):
    with contextlib.closing(wave.open(path,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration


def stretch(x, factor, nfft=2048):
    '''
    stretch an audio sequence by a factor using FFT of size nfft converting to frequency domain
    :param x: np.ndarray, audio array in PCM float32 format
    :param factor: float, stretching or shrinking factor, depending on if its > or < 1 respectively
    :return: np.ndarray, time stretched audio
    '''
    stft = librosa.core.stft(x, n_fft=nfft).transpose()  # i prefer time-major fashion, so transpose
    stft_rows = stft.shape[0]
    stft_cols = stft.shape[1]
    print(stft.shape)
    times = np.arange(0, stft_rows, factor)  # times at which new FFT to be calculated
    print(times.shape)
    hop = nfft / 4  # frame shift
    stft_new = np.zeros((len(times), stft_cols), dtype=np.complex_)

    phase_adv = (2 * np.pi * hop * np.arange(0, stft_cols)) / nfft

    phase = np.angle(stft[0])

    stft = np.concatenate((stft, np.zeros((1, stft_cols))), axis=0)

    for i, time in enumerate(times):
        left_frame = int(np.floor(time))
        local_frames = stft[[left_frame, left_frame + 1], :]
        right_wt = time - np.floor(time)  # weight on right frame out of 2
        local_mag = (1 - right_wt) * np.absolute(local_frames[0, :]) + right_wt * np.absolute(local_frames[1, :])
        local_dphi = np.angle(local_frames[1, :]) - np.angle(local_frames[0, :]) - phase_adv
        local_dphi = local_dphi - 2 * np.pi * np.floor(local_dphi / (2 * np.pi))
        stft_new[i, :] = local_mag * np.exp(phase * 1j)
        phase += local_dphi + phase_adv

    return librosa.core.istft(stft_new.transpose())


def stretch_wo_loop(x, factor, nfft=2048):
    '''
    Functionality same as stretch()
    :param x: np.ndarray, audio array in PCM float32 format
    :param factor: float, stretching or shrinking factor, depending on if its > or < 1 respectively
    :return: np.ndarray, time stretched audio
    '''
    stft = librosa.core.stft(x, n_fft=nfft).transpose()
    stft_rows = stft.shape[0]
    stft_cols = stft.shape[1]

    times = np.arange(0, stft_rows, factor)
    hop = nfft / 4
    phase_adv = (2 * np.pi * hop * np.arange(0, stft_cols)) / nfft
    stft = np.concatenate((stft, np.zeros((1, stft_cols))), axis=0)

    indices = np.floor(times).astype(np.int)
    alpha = np.expand_dims(times - np.floor(times), axis=1)
    mag = (1. - alpha) * np.absolute(stft[indices, :]) + alpha * np.absolute(stft[indices + 1, :])
    dphi = np.angle(stft[indices + 1, :]) - np.angle(stft[indices, :]) - phase_adv
    dphi = dphi - 2 * np.pi * np.floor(dphi / (2 * np.pi))
    phase_adv_acc = np.matmul(np.expand_dims(np.arange(len(times) + 1), axis=1), np.expand_dims(phase_adv, axis=0))
    phase = np.concatenate((np.zeros((1, stft_cols)), np.cumsum(dphi, axis=0)), axis=0) + phase_adv_acc
    phase += np.angle(stft[0, :])
    stft_new = mag * np.exp(phase[:-1, :] * 1j)
    return librosa.core.istft(stft_new.transpose())


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
    sound = librosa.core.load("C:/Users/namn/Downloads/file_example_WAV_1MG.wav")
    x = sound[0]
    sr = sound[1]
    # plot(np.asarray(range(0, len(sound[0])))/22050, sound[0], "original", "time", "magnitude")
    # soundfile.write("C:/Users/namn/PycharmProjects/Sound/original.wav", x, sr)
    # print("len(x)=", len(x))

    #>1 = speedup (shrink)
    #<0 = slowdown (stretch)
    selected_sound = select_portion(sound, 1, 10)
    print("origin length = ", len(selected_sound[0]))
    x_shrinked = stretch(selected_sound[0], 1.5)
    print("len(x_shrinked)=", len(x_shrinked))
    # plot(np.asarray(range(0, len(sound[0]))) / 22050, sound[0], "original", "time", "magnitude")
    # plt.plot()
    # plt.plot(np.asarray(range(selected_sound[3], selected_sound[4]))/22050, selected_sound[0])
    # plt.plot()
    plt.plot(np.asarray(range(0, selected_sound[3]))/22050, selected_sound[1])
    plt.plot()
    plt.plot(np.asarray(range(0, len(x_shrinked))) / 22050, x_shrinked)
    plt.plot()
    plt.plot(np.asarray(range()) / 22050, selected_sound[1])
    plt.plot()
    plt.show()


    # x_shrinked = stretch(x, 0.05)
    # print("len(x_shrinked)=", len(x_shrinked))
    # plot(range(0, len(x_shrinked)), x_shrinked, "speedup_audio", "time", "magnitude")
    # out_file = "C:/Users/namn/PycharmProjects/Sound/speedup_audio.wav"
    # soundfile.write(out_file, x_shrinked, sr)


    # x_stretched = stretch(x, 1.5)
    # print("len(x_stretched)=", len(x_stretched))
    # plot(range(0, len(x_stretched)),x_stretched, "slowdown_audio", "time", "magnitude")
    # out_file = "C:/Users/namn/PycharmProjects/Sound/slowdown_audio.wav"
    # soundfile.write(out_file, x_shrinked, sr)

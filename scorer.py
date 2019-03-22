# scores an epoch
# input: set of values for 30s epoch
# output: sleep stage

# might need to window the freqs to get a good fft resolution
# increasing sampling rate only increases frequency coverage (spans more values)
# to increase frequency resolution, you can either increase time or ZERO PAD
# Resolution = Fs / N where Fs is sampling freq and N is number of samples

# compare power spectrum ratio of two frequencies to determine which is more prominate

# don't take the FFT of the whole 30s epoch -- you want to do multiple
# STFT (short-time fourier transforms) with something like 1s hamming window (with like 0.5s overlaps)
# over the entire signal and then select best of the 60 features
# the PSD of each segment should be normalized to avoid individual differences

# https://www.frontiersin.org/articles/10.3389/fnins.2014.00263/full

# make sure the PSD is normalized (0.0 - 1.0)

# use hamming window to minimize lobes

# make sure the PSD is done right -- something about measuring it relative to each frequency bin?
# make sure the smaller power waves aren't getting lost in smoothing -- maybe that's what
# the relative power thing is?
# this might help: https://psychology.stackexchange.com/questions/17162/how-to-calculate-absolute-power-for-eeg-from-power-spectra-density
# or this: https://raphaelvallat.com/bandpower.html

# keyword: periodogram
# welch sounds to be the standard

# linear discriminant analysis?
# current problem: some features (delta, for example) seem to swamp data set
# For example, if you measure person's height on uM then it will seem like height is most important
# feature since it is so large

# dimensionality reduction?

# I think you need to use statistical methods to determine what the stage could be

# maybe you should try machine learning

# see if you can use annotations of sleep data by experts to compare

# maybe start with simple machine learning like Markov chains


import numpy as np
from scipy import signal as s
from scipy.integrate import simps

def score_epoch(signal, Fs):
    # samples = np.pad(signal, (0, 1500), 'constant')
    # fft = np.fft.fft(samples)
    # spec = np.abs(fft[:len(fft) // 2])
    # spec = np.square(spec)
    # spec = spec / (2000 * 200)
    # # 200 / (1500+500) = 0.1 Hz resolution
    # spec = spec[0:400]  # 0 - 40Hz

    # should probably make sure there is no DC offset
    #signal = signal - avg

    print(len(signal)/Fs)

    window = 1.0*Fs # probably need more samples to get a larger epoch
    freqs, psd = s.welch(signal, Fs, nperseg=window)
    freq_res = freqs[1] - freqs[0]

    # Define delta lower and upper limits
    low, high = 0.5, 4
    idx_delta = np.logical_and(freqs >= low, freqs <= high)
    delta_power = simps(psd[idx_delta], dx=freq_res)

    # Define theta lower and upper limits
    low, high = 4, 8
    idx_theta = np.logical_and(freqs >= low, freqs <= high)
    theta_power = simps(psd[idx_theta], dx=freq_res)

    # Define alpha lower and upper limits
    low, high = 9, 13
    idx_alpha = np.logical_and(freqs >= low, freqs <= high)
    alpha_power = simps(psd[idx_alpha], dx=freq_res)

    # Define beta lower and upper limits
    low, high = 14, 30
    idx_beta = np.logical_and(freqs >= low, freqs <= high)
    beta_power = simps(psd[idx_beta], dx=freq_res)

    #total_power = simps(psd, dx=freq_res)
    total_power = delta_power + theta_power + alpha_power + beta_power
    delta_rel_power = delta_power / total_power
    theta_rel_power = theta_power / total_power
    alpha_rel_power = alpha_power / total_power
    beta_rel_power = beta_power / total_power

    print('----')
    print('Relative delta power: %.3f' % delta_rel_power)
    print('Relative theta power: %.3f' % theta_rel_power)
    print('Relative alpha power: %.3f' % alpha_rel_power)
    print('Relative beta power: %.3f' % beta_rel_power)
    print('----')

    delta_beta_ratio = delta_rel_power / beta_rel_power
    theta_alpha_ratio = theta_rel_power / alpha_rel_power
    print('Delta/beta ratio: %.3f' % delta_beta_ratio)
    print('Theta/alpha ratio: %.3f' % theta_alpha_ratio)

    print('----')


    return psd

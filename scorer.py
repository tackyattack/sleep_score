# scores an epoch
# input: set of values
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
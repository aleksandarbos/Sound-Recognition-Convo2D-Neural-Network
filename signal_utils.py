"""
Copyright (C) 2011  David Morton

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import scipy.signal as scisig
import numpy
import matplotlib
from matplotlib import mlab
import bisect

def find_NFFT(frequency_resolution, sampling_frequency, 
              force_power_of_two=False):
    #This function returns the NFFT
    NFFT = (sampling_frequency*1.0)/frequency_resolution-2
    if force_power_of_two:
        pow_of_two = 1
        pot_nfft = 2**pow_of_two
        while pot_nfft < NFFT:
            pow_of_two += 1
            pot_nfft = 2**pow_of_two
        return pot_nfft
    else:
        return NFFT
        

def find_frequency_resolution(NFFT, sampling_frequency):
    return (sampling_frequency*1.0)/(NFFT + 2)

def find_NFFT_and_noverlap(frequency_resolution, sampling_frequency,
                           time_resolution, num_data_samples):
    NFFT =  find_NFFT(frequency_resolution, sampling_frequency)
    
    # finds the power of two which is just greater than NFFT
    pow_of_two = 1
    pot_nfft = 2**pow_of_two
    noverlap = pot_nfft-sampling_frequency*time_resolution
    while pot_nfft < NFFT or noverlap < 0:
        pow_of_two += 1
        pot_nfft = 2**pow_of_two
        noverlap = pot_nfft-sampling_frequency*time_resolution

    pot_frequency_resolution = find_frequency_resolution(pot_nfft, 
                                                         sampling_frequency)
    
    return {'NFFT':int(NFFT), 'power_of_two_NFFT':int(pot_nfft), 
            'noverlap':int(noverlap), 
            'power_of_two_frequency_resolution':pot_frequency_resolution} 

def resample_signal(signal, prev_sample_rate, new_sample_rate):
    rate_factor = new_sample_rate/float(prev_sample_rate)
    return scisig.resample(signal, int(len(signal)*rate_factor))    


def psd(signal, sampling_frequency, frequency_resolution,
        high_frequency_cutoff=None,  axes=None, **kwargs):
    """
    This function wraps matplotlib.mlab.psd to provide a more intuitive 
        interface.
    Inputs:
        signal                  : the input signal (a one dimensional array)
        sampling_frequency      : the sampling frequency of signal
        frequency_resolution    : the desired frequency resolution of the 
                                    specgram.  this is the guaranteed worst
                                    frequency resolution.
        --keyword arguments--
        axes=None               : If an Axes instance is passed then it will
                                  plot to that.
        **kwargs                : Arguments passed on to 
                                   matplotlib.mlab.psd
    Returns:
        Pxx
        freqs
    """
    if (high_frequency_cutoff is not None 
        and high_frequency_cutoff < sampling_frequency):
        resampled_signal = resample_signal(signal, sampling_frequency, 
                                                    high_frequency_cutoff)
    else:
        high_frequency_cutoff = sampling_frequency
        resampled_signal = signal
    num_data_samples = len(resampled_signal)
    NFFT= find_NFFT(frequency_resolution, high_frequency_cutoff, 
                    force_power_of_two=True) 
    if axes is not None:
        return axes.psd(resampled_signal, NFFT=NFFT, 
                             Fs=high_frequency_cutoff, 
                             noverlap=0, **kwargs)
    else:
        return mlab.psd(resampled_signal, NFFT=NFFT, 
                                        Fs=high_frequency_cutoff, 
                                        noverlap=0, **kwargs)

def plot_specgram(Pxx, freqs, bins, axes, logscale=True):
    if logscale:
        plotted_Pxx = 10*numpy.log10(Pxx)
    else:
        plotted_Pxx = Pxx
    extent = (bins[0], bins[-1], freqs[0], freqs[-1])
    im = axes.imshow(plotted_Pxx, aspect='auto', origin='lower', extent=extent)
    axes.set_xlabel('Time (s)')
    axes.set_ylabel('Frequency (Hz)')
    return im

def specgram(signal, sampling_frequency, time_resolution, 
             frequency_resolution, bath_signals=[], 
             high_frequency_cutoff=None,  axes=None, logscale=True, **kwargs):
    """
    This function wraps matplotlib.mlab.specgram to provide a more intuitive 
        interface.
    Inputs:
        signal                  : the input signal (a one dimensional array)
        sampling_frequency      : the sampling frequency of signal
        time_resolution         : the desired time resolution of the specgram
                                    this is the guaranteed worst time resolution
        frequency_resolution    : the desired frequency resolution of the 
                                    specgram.  this is the guaranteed worst
                                    frequency resolution.
        --keyword arguments--
        bath_signals            : Subtracts a bath signal from the spectrogram
        axes=None               : If an Axes instance is passed then it will
                                  plot to that.
        **kwargs                : Arguments passed on to 
                                   matplotlib.mlab.specgram
    Returns:
        If axes is None:
            Pxx
            freqs
            bins
        if axes is an Axes instance:
            Pxx, freqs, bins, and im
    """
    if (high_frequency_cutoff is not None 
        and high_frequency_cutoff < sampling_frequency):
        resampled_signal = resample_signal(signal, sampling_frequency, 
                                                    high_frequency_cutoff)
    else:
        high_frequency_cutoff = sampling_frequency
        resampled_signal = signal
    num_data_samples = len(resampled_signal)
    specgram_settings = find_NFFT_and_noverlap(frequency_resolution, 
                                               high_frequency_cutoff, 
                                               time_resolution, 
                                               num_data_samples)
    NFFT     = specgram_settings['power_of_two_NFFT']
    noverlap = specgram_settings['noverlap']
    Pxx, freqs, bins = mlab.specgram(resampled_signal, 
                                                NFFT=NFFT, 
                                                Fs=high_frequency_cutoff, 
                                                noverlap=noverlap, **kwargs)
    plotted_Pxx = Pxx
    if bath_signals:
        bath_signal = numpy.hstack(bath_signals)
        psd_Pxx, psd_freqs = psd(bath_signal, sampling_frequency, 
                                 frequency_resolution,
                                 high_frequency_cutoff=high_frequency_cutoff ) 
        plotted_Pxx = (Pxx.T/psd_Pxx).T

    if axes is not None:
        im = plot_specgram(plotted_Pxx, freqs, bins, axes, logscale=logscale)
        return plotted_Pxx, freqs, bins, im
    return plotted_Pxx, freqs, bins

def array_interpolation(array_1, array_2, fraction):
    """
    Returns an array of the same shape as array_1/array_2 but linearly 
        interpolated between them.
    """
    return array_1 + (array_2-array_1)*fraction

def specgram_slice(Pxx, freqs, bins, target_frequency):
    low_index = bisect.bisect_left(freqs,target_frequency) - 1
    high_index = low_index + 1

    # calculate fraction
    low_diff = target_frequency - freqs[low_index]
    diff = freqs[high_index] - freqs[low_index]
    fraction = low_diff/diff

    # find the power at target_frequency
    p_low = Pxx[low_index]
    p_high = Pxx[high_index]
    p_target = array_interpolation(p_low, p_high, fraction)

    return p_target, bins

def avg_specgram(signals, *args, **kwargs):
    """
    This function is an extension of the wrapper for specgram in that it 
        replaces signal (a single signal) with signals (pluaral). 
    """
    # run through signals and compute the specgrams for them individually
    # average and then return the average result

    # Ensure all signals passed in are of the same duration.
    first_signal_length = len(signals[0])
    for signal in signals[1:]:
        assert len(signal) == first_signal_length

    Pxx_list = []
    axes = None
    for signal in signals:
        if 'axes' in kwargs.keys():
            axes = kwargs['axes']
            del kwargs['axes']
        Pxx, freqs, bins = specgram(signal, *args, **kwargs)
        Pxx_list.append(Pxx)
    Pxx_array = numpy.array(Pxx_list)

    avg_Pxx = numpy.average(Pxx_list, axis=0)

    if axes is not None:
        if 'logscale' in kwargs.keys():
            logscale = kwargs['logscale']
            im = plot_specgram(avg_Pxx, freqs, bins, axes, logscale=logscale)
        else:
            im = plot_specgram(avg_Pxx, freqs, bins, axes)
        return avg_Pxx, freqs, bins, im
    # only happens if axes is None
    return avg_Pxx, freqs, bins

        
        





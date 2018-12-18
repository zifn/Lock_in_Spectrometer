import numpy as np
import os
import reference_signal as rf
import struct
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt


#1D Array of wavelength reference for each reading
wavelengths = np.genfromtxt(fname = "wavelengths.csv", delimiter = ",")

#2D Array of timestamp and intensities for each wavelength
intensities = np.genfromtxt(fname = "intensities.csv", delimiter = ",")

#Cutoff frequency for low pass filter (Hz)
cutoff = 5

#Order of the butterworth low pass filter
order = 5


i = 0
mixed = []
mixed_phaseShift = []
while (i < len(intensities)):
    j = 1
    timeStamp = intensities[i][0]
    ref_value = rf.refValue(timeStamp)
    ref_value_phaseShift = rf.refValue_phaseShift(timeStamp)
    mixed.append([timeStamp])
    mixed_phaseShift.append([timeStamp])
    while (j < len(intensities[i])):
        mixed[i].append(ref_value * intensities[i][j])
        mixed_phaseShift[i].append(ref_value_phaseShift * intensities[i][j])
        j += 1
    i += 1

mixed = np.asarray(mixed)
mixed_phaseShift = np.asarray(mixed_phaseShift)


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

#returns 0th column of mixed (timestamps in milliseconds)
time = mixed[:,0]

timeSteps = len(time)
totalTime = time[timeSteps - 1] - time[0]
timePerSample = totalTime/timeSteps

#Setting sample rate to fs in Hertz - approximates a constant sample rate
fs = 1000/timePerSample

#Applies low-pass filter to each column of mixed
i = 1
filtered = np.ndarray(shape = (timeSteps, len(mixed[0])))
filtered[:,0] = time
while (i < len(mixed[0])):
    data = mixed[:,i]
    filteredColumn = butter_lowpass_filter(data, cutoff, fs, order)
    filtered[:, i] = filteredColumn
    i += 1

#Applies low-pass filter to each column of mixed_phaseShift
i = 1
filtered_phaseShift = np.ndarray(shape = (timeSteps, len(mixed[0])))
filtered_phaseShift[:,0] = time
while (i < len(mixed_phaseShift[0])):
    data = mixed_phaseShift[:,i]
    filteredColumn = butter_lowpass_filter(data, cutoff, fs, order)
    filtered_phaseShift[:, i] = filteredColumn
    i += 1




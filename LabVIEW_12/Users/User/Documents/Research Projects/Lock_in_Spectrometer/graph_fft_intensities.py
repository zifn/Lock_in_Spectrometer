import numpy as np
import os
import reference_signal as rf
from numpy.fft import fft, ifft
import sys
import matplotlib.pyplot as plt
from scipy.signal import freqz

#1D Array of wavelength reference for each reading
wavelengths = np.genfromtxt(fname = "wavelengths.csv", delimiter = ",")

#2D Array of timestamp and intensities for each wavelength
intensities = np.genfromtxt(fname = "intensities.csv", delimiter = ",")

arguments = sys.argv

#Sampling rate of the reference signal DaQ
refFreq = float(arguments[1])

est_freq, est_phase, est_offset, est_amp = rf.setUp(intensities[0][0], refFreq)

def refValue (t):
    return est_amp * np.sin(est_freq*t+est_phase)


#Returns value of the reference signal phase shifted by pi/2 rad
def refValue_phaseShift (t):
    return est_amp * np.cos(est_freq*t+est_phase)

#Mixes signal with the reference signal
i = 0
mixed = []
mixed_phaseShift = []
while (i < len(intensities)):
    j = 1
    timeStamp = intensities[i][0]
    ref_value = refValue(timeStamp)
    ref_value_phaseShift = refValue_phaseShift(timeStamp)
    mixed.append([timeStamp])
    mixed_phaseShift.append([timeStamp])
    while (j < len(intensities[i])):
        mixed[i].append(ref_value * intensities[i][j])
        mixed_phaseShift[i].append(ref_value_phaseShift * intensities[i][j])
        j += 1
    i += 1

mixed = np.asarray(mixed)
mixed_phaseShift = np.asarray(mixed_phaseShift)
#graphs fft of every 100th column of intensities
i = 1
time = intensities[:, 0]
sampling_space = ((intensities[-1,0]-intensities[0,0])/(len(intensities))*1000)
frequencies = np.fft.fftfreq(len(time), d = sampling_space)
while (i < len(intensities)):
    data = intensities[:,i]
    transformedColumn = fft(data)/len(data)
    plt.figure(i + 1)
    plt.plot(frequencies, transformedColumn)
    plt.title(str(wavelengths[i]) + "nm Intensity in Freq Space")
    plt.xlabel("")
    plt.figure(i + 2)
    plt.plot(time, data)
    plt.title(str(wavelengths[i]) + "nm Intensity in Time space")
    plt.figure(i+3)
    plt.plot(time, mixed[:, i])
    plt.title(str(wavelengths[i]) + "nm Mixed in Time Space")
    plt.figure(i+4)
    plt.plot(frequencies, fft(mixed[:, i]))
    plt.title(str(wavelengths[i]) + "nm Mixed in Freq Space")

    i += 300
plt.show()
import numpy as np
import os
import reference_signal as rf
from scipy.fftpack import fft, ifft


#1D Array of wavelength reference for each reading
wavelengths = np.genfromtxt(fname = "wavelengths.csv", delimiter = ",")

#2D Array of timestamp and intensities for each wavelength
intensities = np.genfromtxt(fname = "intensities.csv", delimiter = ",")

#Cutoff frequency for low pass filter (Hz)
cutoff = .0023

#Format of lock_in output values (R, theta) vs (x, y)
polar = True

est_freq, est_phase, est_offset, est_amp = rf.setUp(intensities[0][0])

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


#Lowpass filter using the fft algorithm
def fft_lowpass(data, cutoff, fs):
    n = len(data)
    fourier = fft(data)
    freq_index = int(cutoff * n / np.pi)
    i = freq_index
    while(i < len(fourier)):
        fourier[i] = 0
        i += 1
    return ifft(fourier)



#returns 0th column of mixed (timestamps in milliseconds)
time = mixed[:,0]

timeSteps = len(time)
totalTime = time[timeSteps - 1] - time[0]
timePerSample = totalTime/timeSteps

#Setting sample rate to fs in Hertz - approximates a constant sample rate
fs = 1000/timePerSample

#Applies low-pass filter and averages output for each column of mixed
i = 1
#Number of wavelengths.
n = len(mixed[0])
filtered = []
while (i < n):
    data = mixed[:,i]
    filteredColumn = fft_lowpass(data, cutoff, fs)
    value = np.mean(filteredColumn)
    filtered.append(np.absolute(value))
    i += 1

#Applies low-pass filter and averages output for each column of mixed_phaseShift
i = 1
filtered_phaseShift = []
while (i < n):
    data = mixed_phaseShift[:,i]
    filteredColumn = fft_lowpass(data, cutoff, fs)
    value = np.mean(filteredColumn)
    filtered_phaseShift.append(np.absolute(value))
    i += 1

#Prints output to csv "lock_in_values_x.csv" and "lock_in_values_y.csv" as [last timeStamp], x0, x1... \n
#and the same for y
#The header is the wavelengths 
#takes in a list of lock in values, the phase shift values and their respective wavelengths
def cartesianOutput(values, values_phaseShift, wavelengths, time):
    timeIndex = time[-1]
    file1 = open("lock_in_values_x.csv", "a+")
    file2 = open("lock_in_values_y.csv", "a+")
    
    if (os.stat("lock_in_values_x.csv").st_size == 0):
        for wavelength in wavelengths:
            file1.write("," + str(wavelength))
            file2.write("," + str(wavelength))
        file1.write("\n")
        file2.write("\n")
    file1.write(str(timeIndex) + ",")
    file2.write(str(timeIndex) + ",")
    n = len(values)
    i = 0
    while (i < n):
        file1.write(str(values[i]))
        file2.write(str(values_phaseShift[i]))
        i += 1
        if (i < n):
            file1.write(",")
            file2.write(",")

    file1.write("\n")
    file2.write("\n")
    file1.close()
    file2.close()

#Prints output to csv "lock_in_values_r.csv" and "lock_in_values_theta.csv" as [last timeStamp], R0, R1... \n 
#and the same for theta
#The header is the wavelengths 
#takes in a list of lock in values, the phase shift values and their respective wavelengths
def polarOutput(values, values_phaseShift, wavelengths, time):
    timeIndex = time[-1]
    file1 = open("lock_in_values_r.csv", "a+")
    file2 = open("lock_in_values_theta.csv", "a+")
    if (os.stat("lock_in_values_r.csv").st_size == 0):
        for wavelength in wavelengths:
            file1.write("," + str(wavelength))
            file2.write("," + str(wavelength))
        file1.write("\n")
        file2.write("\n")
    file1.write(str(timeIndex) + ",")
    file2.write(str(timeIndex) + ",")
    n = len(values)
    i = 0
    while (i < n):
        x = values[i]
        y = values_phaseShift[i]
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(y, x)
        file1.write(str(r))
        file2.write(str(theta))
        i += 1
        if (i < n):
            file1.write(",")
            file2.write(",")

    file1.write("\n")
    file2.write("\n")
    file1.close()
    file2.close()

if (polar):
    polarOutput(filtered, filtered_phaseShift, wavelengths, time)
else:
    cartesianOutput(filtered, filtered_phaseShift, wavelengths, time)

def main():
    """
    Discription Here
    """

if __name__ == "__main__":
    main()
import numpy as np
import reference_signal as rf

#1D Array of wavelength reference for each reading
wavelengths = np.loadtxt(fname = "wavelengths.csv")

#2D array of intensities, first column is timestamp and later columns are intensity measurements for each wavelength
intensities = np.loadtxt(fname = "intensities.csv", delimiter = ",")


#loop that multiplies intensity data with the corresponding reference signal value
i = 0
while (i < len(intensities)):
    j = 1
    timeStamp = intensities[i][0]
    ref_value = rf.refValue(timeStamp)
    rev_value_phaseShift = rf.refValue_phaseShift(timeStamp)
    while (j < len(intensities[i])):

        j += 1

    i += 1

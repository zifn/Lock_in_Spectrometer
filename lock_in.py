import numpy as np
import reference_signal as rf

wavelengths = np.loadtxt(fname = "wavelengths.csv")
intensities = np.loadtxt(fname = "intensities.csv", delimiter = ",")
i = 0
while (i < len(intensities)):
    j = 1
    timeStamp = intensities[i][0]
    ref_value = rf.refValue(timeStamp)
    rev_value_phaseShift = rf.refValue_phaseShift(timeStamp)
    while (j < len(intensities[i])):
        
        j += 1

    i += 1

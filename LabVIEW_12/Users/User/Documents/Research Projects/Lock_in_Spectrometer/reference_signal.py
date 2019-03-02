#Sets up functions to return the value of the reference singal at a given time value
#Commented sections are for testing

import numpy as np
from scipy.optimize import leastsq



def setUp(startTime):
    rawInput = np.genfromtxt(fname = "RefData.csv", delimiter = ",")
    samplingRate = np.genfromtxt(fname = "wavelengths.csv", delimiter = ",")
    samplingRate = samplingRate[0] #Sampling rate of the reference data in Hz

    #Number of data points
    N = len(rawInput)
    #Array of time values for sample
    time = np.linspace(startTime, N/samplingRate, N)

    guess_phase = 0

    maxValue = max(rawInput)
    minValue = min(rawInput)
    guess_offset = np.mean(rawInput)

    #Guesses amplitude of wave
    greater_than_offset = []
    less_than_offset = []
    for value in rawInput:
        if value > guess_offset:
            greater_than_offset += [value]
        else:
            less_than_offset += [value]
    guess_amp = (np.mean(greater_than_offset) - np.mean(less_than_offset))/2


    #guesses frequency based on period in the middle of the data
    i = int(N/2)
    startingSign = (rawInput[i] - guess_offset > 0)
    while ((rawInput[i] - guess_offset > 0) == startingSign):
        i += 1
    startIndex = i
    while ((rawInput[i] - guess_offset > 0) != startingSign):
        i += 1
    endIndex = i


    guess_freq = 0.5 * samplingRate/(endIndex - startIndex)

    # we'll use this to plot our first estimate. This might already be good enough for you
    #data_first_guess = guess_amp * np.sin(time+guess_phase) + guess_offset


    # Define the function to optimize, in this case, we want to minimize the difference
    # between the actual data and our "guessed" parameters
    optimize_func = lambda x: x[3] * np.sin(x[0]*time * 2 * np.pi+x[1]) + x[2] - rawInput
    est_freq, est_phase, est_offset, est_amp = leastsq(optimize_func, [guess_freq, guess_phase, guess_offset, guess_amp])[0]
    return est_freq, est_phase, est_offset, est_amp


   

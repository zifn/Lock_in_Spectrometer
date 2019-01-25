#Returns the value of the reference singal at a given time value
import numpy as np
from scipy.optimize import leastsq
import pylab as plt


samplingRate = 1 #Sampling rate of the reference date in Hz
def setUp(startTime):
    rawInput = [ ]
    """i = 0
    cutoff_update = 0
    cutoff = 5000 + int(np.random.normal(scale = 1, loc = 0))
    while (i < 100000):
        if cutoff_update >= 5000:
            cutoff = 5000 + int(np.random.normal(scale = 100, loc = 0))
            cutoff_update = 0
        if (i % 10000 < cutoff):
            rawInput += [2]
        else:
            rawInput += [0]
        i += 1
        cutoff_update += 1"""

    #Number of data points
    N = len(rawInput)
    #Array of time values for sample
    time = np.linspace(startTime, N/samplingRate, N)

    guess_phase = 0 
    guess_offset = 1
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
    data_first_guess = np.sin(time+guess_phase) + guess_offset


    # Define the function to optimize, in this case, we want to minimize the difference
    # between the actual data and our "guessed" parameters
    optimize_func = lambda x: np.sin(x[0]*time * 2 * np.pi+x[1]) + x[2] - rawInput
    global est_amp
    global est_freq
    global est_phase
    est_freq, est_phase, est_offset = leastsq(optimize_func, [guess_freq, guess_phase, guess_offset])[0]


    """data_fit = np.sin(est_freq*2 * np.pi*time+est_phase) + est_offset
    data_first_guess = np.sin(guess_freq * 2 * np.pi*time+guess_phase) + est_offset
    plt.plot(time, rawInput, '.')
    plt.plot(time, data_first_guess, label='before fitting')
    plt.plot(time, data_fit, label='after fitting')
    plt.legend()
    plt.show()"""

def refValue (t):
    return np.sin(est_freq*t+est_phase)


#Returns value of the reference signal phase shifted by pi/2 rad
def refValue_phaseShift (t):
    return np.cos(est_freq*t+est_phase)

#setUp(0)

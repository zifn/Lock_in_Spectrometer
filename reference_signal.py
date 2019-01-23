#Returns the value of the reference singal at a given time value
import numpy as np
from scipy.optimize import leastsq
import pylab as plt

def setUp(startTime):
    rawInput = []
    samplingRate = 1 #In Hz
    #Number of data points
    N = len(rawInput)
    #Array of time values for sample
    time = np.linspace(startTime, N/samplingRate, N)

    guess_std = 3*np.std(rawInput)/(2**0.5)/(2**0.5)
    guess_phase = 0
    guess_freq = 1
    guess_amp = 1

    # we'll use this to plot our first estimate. This might already be good enough for you
    data_first_guess = guess_std*np.sin(time+guess_phase)


    # Define the function to optimize, in this case, we want to minimize the difference
    # between the actual data and our "guessed" parameters
    optimize_func = lambda x: x[0]*np.sin(x[1]*time+x[2]) - data
    global est_amp
    global est_freq
    global est_phase
    est_amp, est_freq, est_phase = leastsq(optimize_func, [guess_amp, guess_freq, guess_phase])[0]

def refValue (t):
    return est_amp*np.sin(est_freq*t+est_phase)


#Returns value of the reference signal phase shifted by pi/2 rad
def refValue_phaseShift (t):
    return est_amp*np.sin(est_freq*t+est_phase)



#def refValue (t):
 #   return amplitude * np.sin(guess_freq * t)


#Returns value of the reference signal phase shifted by pi/2 rad
#def refValue_phaseShift (t):
 #   return amplitude * np.cos(guess_freq * t)

#Returns the value of the reference singal at a given time value
import numpy as np
frequency = 1
amplitude = .01
def refValue (t):
    return amplitude * np.sin(frequency * t)


#Returns value of the reference signal phase shifted by pi/2 rad
def refValue_phaseShift (t):
    return amplitude * np.cos(frequency * t)
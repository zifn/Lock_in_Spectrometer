import numpy as np
import os
import reference_signal as rf
import struct

#1D Array of wavelength reference for each reading
wavelengths = np.loadtxt(fname = "wavelengths.csv")

intensities = np.loadtxt(fname = "intensities.csv")




i = 0
mixed = []
mixed_phaseShift = []
while (i < len(intensities)):
    j = 1
    timeStamp = intensities[i][0]
    ref_value = rf.refValue(timeStamp)
    rev_value_phaseShift = rf.refValue_phaseShift(timeStamp)
    mixed.append([timeStamp])
    mixed_phaseShift.append([timeStamp])
    while (j < len(intensities[i])):
        mixed[i].append(ref_value * intensities[i][j])
        mixed_phaseShift[i].append(ref_value_phaseShift * intensities[i][j])
        j += 1
    i += 1

#Deletes last line of file
"""def deleteEndLine (file):
    file = open(file, "rb+")


    #Move the pointer (similar to a cursor in a text editor) to the end of the file. 
    file.seek(0, os.SEEK_END)

    #This code means the following code skips the very last character in the file - 
    #i.e. in the case the last line is null we delete the last line 
    #and the penultimate one
    pos = file.tell() - 1

    #Read each character in the file one at a time from the penultimate 
    #character going backwards, searching for a newline character
    #If we find a new line, exit the search
    while pos > 0 and file.read(1) != b"\n":
        pos -= 1
        file.seek(pos, os.SEEK_SET)

    #So long as we're not at the start of the file, delete all the characters ahead of this position
    if pos > 0:
        file.seek(pos, os.SEEK_SET)
        file.truncate()

    file.close()



#Reads last line of file
def readEndLine (file):
    f = open(file, "rb+")
    line = -1

    f.seek(-2, os.SEEK_END)     # Jump to the second last byte.
    while f.read(1) != b"\n":   # Until EOL is found...
        f.seek(-2, os.SEEK_CUR) # ...jump back the read byte plus one more.
    last =  f.readline()
    struct.unpack('b', last)


    f.close()
    return last"""



#loop that multiplies intensity data with the corresponding reference signal value (mixes signal)
"""i = 0
while i < 1:
    line = readEndLine("intensities.csv")
    print(line)
    i += 1"""





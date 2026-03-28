# Taken from https://github.com/Devking/PythonMIDISynth


###################################################################################
#                                                                                 #
# This script is written by Wells Lucas Santo, for the final project component of #
# EE4163 at the NYU Tandon School of Engineering. Please give credit if you wish  #
# to reproduce this code.                                                         #
#                                                                                 #
# Be sure to read README.md for more information on this script.                  #
#                                                                                 #
# To see how this script came about, check out the 'Incremental Scripts' folder!  #
#                                                                                 #
###################################################################################

# Get a range of the frequencies for 120 keys, starting with the pitch C0
# This mathematically works because there is a separation of 1.059463 per
# pitch, in frequency. You may not be able to hear pitches until you get to
# around C4, which is the 48th key.
from math import sin, cos, pi
import numpy as np
import struct
import pyaudio
from pygame import midi
import math


def float_to_fraction(x, error=0.0001):
    n = int(math.floor(x))
    x -= n
    if x < error:
        return (n, 1)
    elif 1 - error < x:
        return (n+1, 1)
    # The lower fraction is 0/1
    lower_n = 0
    lower_d = 1
    # The upper fraction is 1/1
    upper_n = 1
    upper_d = 1
    while True:
        # The middle fraction is (lower_n + upper_n) / (lower_d + upper_d)
        middle_n = lower_n + upper_n
        middle_d = lower_d + upper_d
        # If x + error < middle
        if middle_d * (x + error) < middle_n:
            # middle is our new upper
            upper_n = middle_n
            upper_d = middle_d
        # Else If middle < x - error
        elif middle_n < (x - error) * middle_d:
            # middle is our new lower
            lower_n = middle_n
            lower_d = middle_d
        # Else middle is our best fraction
        else:
            return (n * middle_d + middle_n, middle_d)


fractionsjt = [
    1,
    16/15,
    9/8,  # 8/7
    6/5,
    5/4,
    4/3,
    45/32,
    3/2,
    8/5,
    5/3,
    7/4,  # 16/9
    15/8
]


def temp12eq(i):
    return 440 * 2 ** ((i - 69) / 12)


def justtune(r, i):
    r = r % 12
    fr = temp12eq(r)
    return fractionsjt[(i + 12 - r) % 12] * fr * (2 ** ((i - r) // 12))


def temp12eqfreqs():
    return [temp12eq(i) for i in range(0, 240)]


def justtunefreqs(r):
    return [justtune(r, i) for i in range(0, 240)]


# One octave but split using geometric division
def oneoctave():
    return [(440 * 2 ** ((i - 21) / 87)) for i in range(0, 240)]


# One octave but split using normal division
def oneoctave2():
    return [(440 * (1 + (i - 21) / 87)) for i in range(0, 240)]


# First 2 octaves from 12tet, first 2 octaves from just tune, then second 2 oct from 12tet ....
def justTuneNormalTune(r):
    nfreqs = temp12eqfreqs()
    jfreqs = justtunefreqs(r)
    afreqs = [nfreqs, jfreqs]

    freqs = []
    for i in range(0, 228):
        b = (i // 24) % 2
        a = i - b * 24 + 12

        freqs.append(afreqs[b][a])

    return freqs[12:]


f = justTuneNormalTune(0)
bbbb = [float_to_fraction(i / 440) for i in f]

# These macros come from the MIDI event values that my Alesis Q49 uses for
# detecting KEYUP and KEYDOWN events.
KEYDOWN = 144
KEYUP = 128

# Choose how many notes you want to be able to play at once
NOSTREAMS = 10

# Import all the necessary packages

###############################
# Initialize sound parameters #
###############################

# This is based on the second-order difference equation code that we have used
# in the class, written by Professor Ivan Selesnick.

blockSize = 32
sampleWidth = 2
numChannels = 1
samplingRate = 16000

Ta = 0.8
r = 0.01 ** (1.0 / (Ta * samplingRate))

# Calculate coefficients based on frequencies
om = [2.0 * pi * float(f1) / samplingRate for f1 in f]
a1 = [-2*r*cos(om1) for om1 in om]
a2 = r**2
b0 = [sin(om1) for om1 in om]

# Open the audio output streams
p = pyaudio.PyAudio()

# Put the streams into a circular buffer
# Use list comprehension to make the streams directly in this list
stream_buffer = [p.open(format=p.get_format_from_width(sampleWidth),
                        channels=numChannels,
                        frames_per_buffer=blockSize,
                        rate=samplingRate,
                        input=False,
                        output=True)
                 for i in range(NOSTREAMS)]

# Circular buffer of arrays
y = [np.zeros(blockSize) for i in range(NOSTREAMS)]
x = [np.zeros(blockSize) for i in range(NOSTREAMS)]

# Circular buffer of ints
pitch = [0 for i in range(NOSTREAMS)]
accesskey = 0

#######################################
# Initialize input detection for MIDI #
#######################################

midi.init()
INPUTNO = midi.get_default_input_id()
input = midi.Input(INPUTNO)

print('*******************')
print('** Ready to play **')
print('*******************')

while True:

    # For ALL streams, set current input to 0, since nothing is being played
    # at the current moment (until a key is pressed)
    for n in range(NOSTREAMS):
        x[n][0] = 0.0

    if input.poll():
        eventslist = input.read(1000)

        for e in eventslist:
            event = e[0]
            eventType = event[0]
            eventID = event[1]
            eventValue = event[2]

            if eventType == KEYDOWN:
                print('Keydown on key', eventID, 'with intensity',
                      eventValue, 'ratio:', bbbb[eventID], 'prop:', f[eventID] / 440)

                # Trigger an impulse due to a keypress
                # Notice that we are triggering the impulse in the stream that
                # 'accesskey' refers to -- and then we will update 'accesskey'
                # to utilize our circular array of streams properly.
                x[accesskey][0] = 15000 * (eventValue / 130.0)
                pitch[accesskey] = eventID % 120
                accesskey = (accesskey + 1) % NOSTREAMS

            elif eventType == KEYUP:
                print('Keyup on key', eventID)

    # Update the value of the difference equation
    for n in range(blockSize):

        # Update output for all streams
        for i in range(NOSTREAMS):
            y[i][n] = b0[pitch[i]] * x[i][n] - \
                a1[pitch[i]] * y[i][n-1] - a2 * y[i][n-2]

    # Output the value of all streams (this all happens at once!)
    # PyAudio will allow this to play the output CONCURRENTLY
    # (That is, sound from all streams will play at the same time, not one after the other!)
    for i in range(NOSTREAMS):
        y[i] = np.clip(y[i], -2 ** 15 + 1, 2 ** 15 - 1)
        data = struct.pack('h' * blockSize, *[int(i) for i in y[i]])
        stream_buffer[i].write(data, blockSize)

# Close up all of the streams properly
for i in range(NOSTREAMS):
    stream_buffer[i].stop_stream()
    stream_buffer[i].close()

p.terminate()
midi.quit()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 12:28:34 2020

@author: ebalestr

Episode 0: Euler's formula

The present code guides you to how multplying stuff for e^ni is fun, and what does 
it accomplishes in one specific special case

"""

#%% =============================================================================
# IMPORTING LIBRARIES
# =============================================================================

# as usual, we need some stuff that some holy people had the patience to code 
# to simplify us the job **a lot**

import numpy as np # the most used python library for numerical calculation
import matplotlib.pyplot as plt # a well known library for generating plot in a MATLAB-like syntax (that I'm comfortable with)
import signalprocessing_helper as sigp # our own helper set of functions present in this very same repository
import matplotlib.animation as animation

#%% ===========================================================================
# PARAMETER DEFINITION
# =============================================================================

# This part serves to build a signal of interest, by defining a time window, the
# sampling frequency, and how the actual signal will look like.

# signal sampling frequency (aka, how many times per second do we record information?)
SF = 500

# time window: define starting point, length, and pace (inverse of sampling frequency)
t = np.arange(0, 1+1/SF, step=1/SF)

# convert the time window as period: multiply it for 2pi
# this simple operation allows us to clean up a bit all the following formulas
T = t*2*np.pi

signalfreq = 5
transformfreq = 5

# define our signal
signal = np.cos(signalfreq*T + np.pi/4)

# define the kind of transformation we want to apply
transformation = np.exp(-T*1j*transformfreq)

# define how the transformation is in relation to the signal
new_s = signal*transformation


MyTransform = sigp.InteractiveTransform(t, signal, new_s, signalfreq, transformfreq)
MyTransform.start_animation()











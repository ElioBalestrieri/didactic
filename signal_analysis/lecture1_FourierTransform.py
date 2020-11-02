#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 12:28:34 2020

@author: ebalestr

Episode 1: Fourier transform and its inverse

The present code guides you through the realization of a fourier machine which 
decomposes a signal (that we generate here) into its oscillatory components.

As a proof of concept it aims to reconstruct the original signal from the 
components, to show that this magic is actually working ;)

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
# Then we define our frequency range & resolution for the Fourier transform

# signal sampling frequency (aka, how many times per second do we record information?)
SF = 100

# time window: define starting point, length, and pace (inverse of sampling frequency)
t = np.arange(0, 4+1/SF, step=1/SF)

# convert the time window as period: multiply it for 2pi
# this simple operation allows us to clean up a bit all the following formulas
T = t*2*np.pi

# signal generation: unleash your creativity!!!
# you can add whatever you want to create a signal as a function of period. 
# A good starting point though is to sum a series of sinusoid. Generally, in order to have
# a better control on what you add up, remember the following:
#
# y(T) = A * sin(T * f + theta)
#
# where A is the amplitude (how widely the sinusoid oscillates around the 0), 
# f is the frequency (how many cycles does the function has over a period), theta
# is the phase angle (how shifted the function is along the x axis), and T is the 
# period (in our present script, defined as time*2*pi)
#
# Just try out different parameters and plot!

signal = (
    7*np.sin(T) +               # slow strong component
    5*np.cos(T*2)+              # it does not have necessarily to be sin: cos is good as well!
    3*np.sin(T*5)+
    3*np.cos(T*10 + np.pi/3)+
    2*np.cos(T*20)+
    3*np.sin(T*40 - np.pi/6)               # high frequency component. Riddle: what does it happen if you add a sinusoid  
    )                                                               # whose frequency exceeds half of the SF?

# plot for checking our signal
plt.figure()
plt.subplot(3, 1, 1)
plt.plot(t, signal, 'k', linewidth=3)
plt.xlabel('time (s)')
plt.title('our signal')
plt.tight_layout()

#%% ===========================================================================
# SPECTRA COMPUTATION
# =============================================================================

# OK, we need to define how many frequencies we're gonna probe for our conversion
nfreqs = int(np.floor(t.size/2)+1)
freqspace = np.linspace(0, SF/2, nfreqs)

# almost ready to go! let's just initialize one array to store our transform, and
# another to store the reconstructed signal from the fourier transform
spectra = np.zeros(nfreqs, dtype=complex)
reconstructed = np.zeros(t.size, dtype=complex)

acc = 0 # accumulator for indexing the right position
for iFreq in freqspace:
    
    # here comes the fourier transform core!
    spectra[acc] = (np.exp(-T*1j*iFreq)*signal).sum() / (signal.size/2)
    
    # and compute its inverse as well
    comp = np.exp(T*1j*iFreq)*spectra[acc]
    reconstructed += comp
    
    # update index
    acc +=1
    
    
# that's it folks :D
# check out!
plt.subplot(3, 1, 2)
plt.plot(freqspace, np.abs(spectra), linewidth=3)
plt.title('spectra')
plt.xlabel('frequency (Hz)')
plt.ylabel('amplitude')   
plt.tight_layout() 

    
plt.subplot(3, 1, 3)
plt.plot(t, signal, label='original')
plt.plot(t, np.real(reconstructed), label='reconstructed')    
plt.xlabel('time (s)')
plt.title('original signal vs reconstructed')
plt.legend()
plt.tight_layout()
   

#%% ===========================================================================
# INTERACTIVE PLOTTING
# =============================================================================
WriterClass = animation.writers['ffmpeg']
writer = WriterClass(fps=3, metadata=dict(artist='Me'), bitrate=6000) # example default
myplot = sigp.InteractivePlotFourier(signal, t, freqspace, T, spectra)
animated_image = myplot.start_animation()
animated_image.save('myvideo.mp4', writer=writer)


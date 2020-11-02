#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 15:33:34 2020

@author: elio
"""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation



t = np.linspace(0, 3, 601)
T = t*2*np.pi
Nfreqs = 501

signal = (3*np.sin(2*T+np.pi/2) + 
          2*np.sin(4*T) + .5*np.cos(10*T))

freqspace = np.linspace(0, 20, 10001)

trans_signal = np.zeros((Nfreqs, 1), dtype=complex)

# acc = 0
# for iFreq in freqspace:
    
#     wrapper = np.exp(-T*1j*iFreq)

#     wrapped_signal = signal*wrapper
    
#     z_ = wrapped_signal.sum()/signal.size

#     trans_signal[acc] = z_
    
#     acc+=1
    
    
    
# plt.figure()
# plt.subplot(2, 1, 1)

# plt.plot(t, signal)

# plt.subplot(2, 1, 2)

# plt.plot(freqspace, np.abs(trans_signal))



#%% fancy plotting


dyn_fig = plt.figure()

ax_complexplane = plt.subplot(2, 3, 1)
plt.xlim(-10, 10)
plt.ylim(-10, 10)


ax_powerspectra = plt.subplot(2, 3, (2, 3))

# functions that are gonna be called in the plot recursion
def fourier(iFreq, freqspace, T, signal):
    
    wrapper = np.exp(-T*1j*iFreq)
    wrapped_signal = signal*wrapper    
    z_ = wrapped_signal.sum()/signal.size
    
    xcoordcloud = np.real(wrapped_signal)
    ycoordcloud = np.imag(wrapped_signal)
    
    xcoord_Z = np.real(z_)
    ycoord_Z = np.imag(z_)

    return xcoordcloud, ycoordcloud, xcoord_Z, ycoord_Z


def update_visual(freqidx, scattercloud, scattervect, linepower, freqspace,
                  T, signal, pwrspctr):
    
    iFreq = freqspace[freqidx]    
    
    xcoordcloud, ycoordcloud, xcoord_Z, ycoord_Z = fourier(iFreq, freqspace, 
                                                           T, signal)
    
    # scattercloud.set_offsets(np.array([xcoordcloud, ycoordcloud]).T)
    scattercloud.set_data(xcoordcloud, ycoordcloud)


    scattervect.set_offsets(np.array([xcoord_Z, ycoord_Z]).T)

    return scattercloud, scattervect


# actual inizialization of the plotting

scattercloud, = ax_complexplane.plot([], [], 'k')
scattervect = ax_complexplane.scatter([], [], s=50, c='r')


line_ani = animation.FuncAnimation(dyn_fig, update_visual, 10001, 
                                   fargs=(scattercloud, scattervect, 0, 
                                          freqspace, T, signal, 0),
                                   interval=126, blit=True)    



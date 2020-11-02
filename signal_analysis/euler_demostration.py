#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 16:27:23 2020

@author: elio
"""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


#%% definition of period, and original signal

T = np.linspace(-np.pi, np.pi, 256)

orig_sign = (8*np.sin(T) + 5*np.sin(T*7 + np.pi/2) + 6*np.sin(T*5+np.pi/4) + 
             4*np.sin(T*30+np.pi/3) + 2*np.sin(T*60+np.pi/3))


freqspace = np.linspace(0, 126, 127)

spectra = np.fft.fft(orig_sign)[0:127]/(orig_sign.size/2)

visualspectra = np.abs(spectra)

fig1 = plt.figure()
plt.subplot(2, 3, (1, 3))
plt.plot(freqspace, visualspectra)

ax2 = plt.subplot(2, 3, (5, 6))
plt.plot(T, orig_sign, linewidth=3, color='black')

# create table of frequency, amplitude and phases, and sort them according to magnitude
eulertable = np.array([freqspace, visualspectra, np.angle(spectra)]).T
eulertable = eulertable[np.flip(eulertable[:,1].argsort()),]


#%% take N components
N = 10


def angle2coordinates(eulertable, N, thisangle):
    
    lisvals = [0]
    
    for iN in range(N):
        
        freq = eulertable[iN, 0]
        ampl = eulertable[iN, 1]
        phase = eulertable[iN, 2]
        cmplx = ampl*np.exp((thisangle+ phase)*freq*1j)            
        transformed = cmplx + lisvals[iN]
        lisvals.append(transformed)

    xcoords = np.real(lisvals)
    ycoords = np.imag(lisvals)
    
    return xcoords, ycoords, lisvals
    
    
    
    
#%%

def update_line(anglepos, allangles, eulertable, N, line, scatters, s_sign):

    thisangle = allangles[anglepos]
    xcoords, ycoords, lisvals = angle2coordinates(eulertable, N, thisangle)


    line.set_data(xcoords, ycoords)
    scatters.set_offsets(np.array([xcoords, ycoords]).T)

    s_sign.set_offsets(np.array([thisangle, np.abs(lisvals[-1]).T]))
    
    return line, scatters, s_sign


data = T

ax1 = plt.subplot(2, 3, 4)

l, = ax1.plot([], [], 'k')
s = ax1.scatter([], [], c='r')
s_sign = ax2.scatter([], [], c='r')
plt.xlim(-20, 20)
plt.ylim(-20, 20)
# ax1.xlabel('x')
# ax1.title('test')
line_ani = animation.FuncAnimation(fig1, update_line, 256, 
                                   fargs=(data, eulertable, N, l, s, s_sign),
                                   interval=64, blit=True)    
    

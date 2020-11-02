#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 12:39:11 2020

@author: ebalestr

helper file for the Fourier lectures


"""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


#%% ===========================================================================
# INTERACTIVE PLOTS LECTURE 1
# =============================================================================

def onClick(event):
    global pause
    pause ^= True

class InteractivePlotFourier:
    
    def __init__(self, signal, t, freqspace, T, spectra):
        
        title_fontsize = 20
        label_fontsize = 16
        
        # initialize figure
        self.dyn_fig = plt.figure(figsize=[13, 9])
        self.dyn_fig.canvas.mpl_connect('button_press_event', onClick)

        self.ax_complexplane = plt.subplot(2, 3, 1)
        plt.xlim(-40, 40)
        plt.ylim(-40, 40)
        plt.title('complex plane', fontsize=title_fontsize)
        plt.xlabel('real', fontsize=label_fontsize)
        plt.ylabel('imaginary', fontsize=label_fontsize)
        plt.tight_layout()
        self.ax_complexplane.set_aspect('equal')


        self.ax_powerspectra = plt.subplot(2, 3, (2, 3))
        plt.title('spectra', fontsize=title_fontsize)
        plt.xlabel('frequency (Hz)', fontsize=label_fontsize)
        plt.ylabel('amplitude', fontsize=label_fontsize)
        plt.xlim(freqspace.min(), freqspace.max())
        plt.ylim(0, np.abs(spectra).max() + 2)
        
        plt.tight_layout()
        
        self.ax_signapprox = plt.subplot(2, 3, (4, 6))
        plt.plot(t, signal, 'k', linewidth=3, label='original')
        plt.title('reconstructed signal \nvs original', fontsize=title_fontsize)
        plt.xlabel('time (s)', fontsize=label_fontsize)
        plt.tight_layout()
                
        # initialize the graph handle for each one of the axis
        self.complexpat, = self.ax_complexplane.plot([], [], 'k', alpha=.6)
        self.gravitycenter = self.ax_complexplane.scatter([], [], s=50, c='r')
        self.spectraline, = self.ax_powerspectra.plot([], [], 'firebrick', linewidth=3)
        self.inverse, = self.ax_signapprox.plot([], [], 'darkorange', alpha=.9, label='reconstructed')
        
        # append arrays
        self.t = t
        self.signal = signal
        self.T = T
        self.freqspace = freqspace
        self.comp = np.zeros(t.size, dtype=complex)
        self.spectra = np.zeros(freqspace.size, dtype=complex)*np.nan
    
    
    def fourier(self, iFreq, freqidx):
        
        wrapper = np.exp(-self.T*1j*iFreq)
        wrapped_signal = self.signal*wrapper    
        z_ = wrapped_signal.sum()/(self.signal.size/2)
        
        # store value z_
        self.spectra[freqidx] = z_
    
        self.xcoordcloud = np.real(wrapped_signal)
        self.ycoordcloud = np.imag(wrapped_signal)
    
        self.xcoord_Z = np.real(z_)
        self.ycoord_Z = np.imag(z_)

        inv_z_ = np.exp(self.T*1j*iFreq)*z_
        
        self.comp += inv_z_
        
        self.iFreq = iFreq
        
        
    def update_visual(self, freqidx):
                    
        iFreq = self.freqspace[freqidx]
                        
        self.fourier(iFreq, freqidx)
        
        # update animation on the complex plane
        self.complexpat.set_data(self.xcoordcloud, self.ycoordcloud)
        self.gravitycenter.set_offsets(np.array([self.xcoord_Z, 
                                                 self.ycoord_Z]).T)
        self.spectraline.set_data(self.freqspace, np.abs(self.spectra))
        
        self.inverse.set_data(self.t, np.real(self.comp))
        self.ax_signapprox.legend(loc=3)
        
        return self.complexpat, self.gravitycenter, self.spectraline, self.inverse
    
    
    def start_animation(self):
        
        interval = 300
        nfreqs = self.freqspace.size
        
        this_animation = animation.FuncAnimation(self.dyn_fig, self.update_visual,
                                                 nfreqs, interval=interval,
                                                 blit=True, repeat=False)
        
        return this_animation
    
    
            
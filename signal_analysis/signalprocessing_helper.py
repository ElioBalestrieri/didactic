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
                                                 blit=True, repeat=True)
        
        return this_animation
    
    
#%% plot Euler

class InteractiveTransform:
    
    def __init__(self, x, original, transformed, freqsignal, freqtransform):
            
        
        title_fontsize = 20
        label_fontsize = 16

        
        self.real_original = np.real(original)[:, np.newaxis]
        self.imag_original = np.imag(original)[:, np.newaxis]
        self.real_transformed = np.real(transformed)[:, np.newaxis]
        self.imag_tranformed = np.imag(transformed)[:, np.newaxis]
        
        self.fig = plt.figure(figsize=[13, 9])
        self.ax1 = plt.subplot(1, 2, 1)
        
        self.ax1.scatter(x, original, s=5, c='k')
        plt.title('sinusoid frequency='+str(freqsignal), fontsize=title_fontsize)
        
        #%% now set the animation properly to show the transformation
        self.diff_real = self.real_transformed-self.real_original
        self.diff_imag = self.imag_tranformed-self.imag_original        
        
        self.step = 300 
        self.interval = 30 # ms * step
        
        # get hanning taper to nicely smooth the animation at the edges
        han = np.hanning(self.step)/np.hanning(self.step).sum()
             
        # paced differences
        self.paced_diff_real = self.diff_real * han[np.newaxis, :]
        self.paced_diff_imag = self.diff_imag * han[np.newaxis, :]
        
        # define second axes, and initialize scatterplot for dynamic transform later on
        self.ax2 = plt.subplot(1, 2, 2)
        plt.xlim(-2, 2)
        plt.ylim(-2, 2)
        plt.tight_layout()
        plt.title('transform frequency='+str(freqtransform), fontsize=title_fontsize)


        self.complexplane = self.ax2.scatter([], [], s=5, c='k')
        self.ax2.set_aspect('equal')

        plt.show()
        
        # cumsum paces
        self.cumsum_real = self.real_original+ np.cumsum(self.paced_diff_real, axis=1)
        self.cumsum_imag = self.imag_original+ np.cumsum(self.paced_diff_imag, axis=1)
          
    
    def update_transform(self, istep):
        
        new_x = self.cumsum_real[:, istep]
        new_y = self.cumsum_imag[:, istep]
        
        mat = np.concatenate((new_x[:,np.newaxis], new_y[:,np.newaxis]), axis=1)
        
        self.complexplane.set_offsets(mat)
        
        return self.complexplane,
    

    def start_animation(self):
        
        this_animation = animation.FuncAnimation(self.fig, self.update_transform,
                                                 self.step, interval=self.interval,
                                                 blit=True, repeat=False)


        return this_animation
    
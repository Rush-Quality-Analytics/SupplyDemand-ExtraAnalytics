import matplotlib.pyplot as plt
import pandas as pd
import csv # csv import functionality
import time # library for time functionality
import sys
import warnings # needed for suppression of unnecessary warnings
import base64 # functionality for encoding binary data to ASCII characters and decoding back to binary data
import numpy as np
import datetime 
import sys
from math import pi


def fig_fxn(fig, model, n):
    
    fig.add_subplot(3, 3, n)
    Y = []
    
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Cumulative cases', fontsize=12)
    
    if model == 'Logistic, Gaussian\n& SEIR-SD':
        x = np.linspace(-4, 5, 100)
        Y = 1/(1 + np.exp(-x + 1))
        plt.plot(x, Y, c ='k', linewidth=3)
        #plt.text(r'$N = a/a + N_{0}
        
        
    elif model == 'Exponential':
        x = np.linspace(-0, 10, 100)
        r = 0.5
        Y = np.exp(r*x)
        plt.plot(x, Y, c ='k', linewidth=3)
        
        
    elif model == 'Quadratic':
        x = np.linspace(-.5, 4, 100)
        Y = x**2 + x
        plt.plot(x, Y, c ='k', linewidth=3)
        
        
    plt.title(model, fontweight='bold', fontsize=12)
    plt.yticks([])
    plt.xticks([])
        
    #plt.tick_params(axis='both', labelsize=8, rotation=45)
        
    
    
    return fig
    
    


fig = plt.figure(figsize=(10, 10))
models = ['Exponential', 'Quadratic', 'Logistic, Gaussian\n& SEIR-SD']


ns = [1,2,3]
for i, model in enumerate(models):
    fig = fig_fxn(fig, model, ns[i])
    




plt.subplots_adjust(wspace=0.35, hspace=0.37)
plt.savefig('figures/Model_Forms.png', dpi=400, bbox_inches = "tight")
plt.close()
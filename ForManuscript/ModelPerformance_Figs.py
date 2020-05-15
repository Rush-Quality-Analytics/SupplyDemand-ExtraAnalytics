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



def hulls(x, y, clim):
    grain_p = 1
    xran = np.arange(min(x), max(x)+1, grain_p).tolist()
    binned = np.digitize(x, xran).tolist()
    bins = [list([]) for _ in range(len(xran))]
    
    for ii, val in enumerate(binned):
        bins[val-1].append(y[ii])
    
    pct5 = []
    pct50 = []
    pct95 = []
    xran2 = []
    
    for iii, _bin in enumerate(bins):
        if len(_bin) > 0:
            pct5.append(np.percentile(_bin, 100 - clim))
            pct50.append(np.percentile(_bin, 50))
            pct95.append(np.percentile(_bin, clim))
            xran2.append(xran[iii])
    
    return xran2, pct5, pct95, pct50




def fig_fxn(fig, model, fits_df, locations, max_len, n, dates, clr):
    
    fig.add_subplot(3, 3, n)
    X = []
    Y = []
    for loc in locations:
        try:
            
            fits_df_loc = fits_df[fits_df['focal_loc'] == loc]
            r2s = fits_df_loc['obs_pred_r2'].tolist()
            #print(max_len)
            x = list(range(len(r2s)))
            #x = max_len - (np.array(list(range(len(r2s)))) + 1)
            #x = list(np.flip(x))
            
            X.extend(x)
            Y.extend(r2s)
            
            
        except:
            continue
        
    for clim in [90, 75, 55]:
        
        xran, pct_low, pct_hi, pct50 = hulls(X, Y, clim)
        print(len(dates), len(xran), len(pct_low), len(pct_hi))
        x = np.array(xran) + 7
        plt.fill_between(x, pct_low, pct_hi, facecolor= clr, alpha=0.4, lw=0.2)
        
    plt.xlabel('Days since 3/10', fontweight='bold', fontsize=10)
    plt.ylabel(r'$r^{2}$', fontweight='bold', fontsize=12)
    
    if model == 'logistic': model = 'Logistic'
    elif model == 'exponential': model = 'Exponential'
    elif model == 'quadratic': model = 'Quadratic'
    elif model == '3rd degree polynomial': model = 'Cubic'
    
    plt.title(model, fontweight='bold', fontsize=12)
    
    ax = plt.gca()
    temp = ax.xaxis.get_ticklabels()
    temp = list(set(temp) - set(temp[::1]))
    for label in temp:
        label.set_visible(False)
        
    plt.tick_params(axis='both', labelsize=7, rotation=0)
    
    plt.xlim(6, 50)
    if model != 'Exponential':
        plt.ylim(0.9, 1.)
    
    return fig, pct50
    
    
    
model_fits_df = pd.read_pickle('data/model_results_dataframe.pkl')
#print(list(model_fits_df))

# obs_y
# pred_y
# forecasted_y
# pred_dates
# forecast_dates
# label
# obs_pred_r2
# model
# focal_loc
# PopSize
# ArrivalDate


fig = plt.figure(figsize=(10, 10))

#models = list(set(model_fits_df['model']))
models = ['Exponential', 'Logistic', 'Quadratic', 
          'Gaussian', 'SEIR-SD']

model_clrs = ['r', 'orange', 'green', 'b', 'purple']

avgR2s = []
#print(models)
#sys.exit()

locations = list(set(model_fits_df['focal_loc']))
locations.sort()


    

ns = [1,2,4,5,7]
for i, model in enumerate(models):
    max_len = 0
    dates = []

    for loc in locations:
        df = model_fits_df[model_fits_df['focal_loc'] == loc]
        df = df[df['model'] == model]
        r2s = df['obs_pred_r2']
        d = df['pred_dates'].values[-1]
        
        d = d[6:]
        
        if len(r2s) > max_len:
            max_len = len(r2s)
            dates = d
    
    #print(max_len, len(dates))
    
    fits_df = model_fits_df[model_fits_df['model'] == model]
    fig, avg = fig_fxn(fig, model, fits_df, locations, max_len, ns[i], dates, model_clrs[i])
    avgR2s.append(avg)
    


fig.add_subplot(3, 3, 8)

x = np.array(list(range(len(avgR2s[0])))) + 7

for i, model in enumerate(models):
    if i == 0:
        continue
    
    plt.plot(x, avgR2s[i], c=model_clrs[i], linewidth=2, alpha=0.6, label=model)
    

plt.ylim(0.95, 1.0)
plt.tick_params(axis='both', labelsize=7, rotation=0)
plt.xlabel('Days since 3/10', fontweight='bold', fontsize=10)
plt.ylabel(r'$r^{2}$', fontweight='bold', fontsize=12)
plt.legend(fontsize=10)

plt.subplots_adjust(wspace=0.35, hspace=0.4)
plt.savefig('figures/Model_Performance.png', dpi=400, bbox_inches = "tight")
plt.close()
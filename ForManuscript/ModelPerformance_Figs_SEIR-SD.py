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




def fig_fxn(fig, model, fits_df, locations, max_len, n, dates):
    
    fig.add_subplot(2, 2, n)
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
        
    for clim in [95, 75, 55]:
        
        xran, pct5, pct95, pct50 = hulls(X, Y, clim)
        print(len(dates), len(xran), len(pct5), len(pct95))
        x = np.array(xran) + 7
        plt.fill_between(x, pct5, pct95, facecolor= 'b', alpha=0.4, lw=0.2)
        
    plt.xlabel('Days since 3/10\nor since first reported case', fontweight='bold', fontsize=10)
    plt.ylabel(r'$r^{2}$' + ', Observed vs. Predicted', fontweight='bold', fontsize=12)
    
    
    plt.title(model, fontweight='bold', fontsize=14)
    
    ax = plt.gca()
    temp = ax.xaxis.get_ticklabels()
    temp = list(set(temp) - set(temp[::1]))
    for label in temp:
        label.set_visible(False)
        
    plt.tick_params(axis='both', labelsize=6, rotation=45)
    
    return fig
    
    
    
model_fits_df = pd.read_pickle('model_results_dataframe.pkl')
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


fig = plt.figure(figsize=(8, 8))

#models = list(set(model_fits_df['model']))
models = ['SEIR-SD']
#print(models)
#sys.exit()

locations = list(set(model_fits_df['focal_loc']))
locations.sort()


    


for i, model in enumerate(models):
    max_len = 0
    dates = []

    for loc in locations:
        df = model_fits_df[model_fits_df['focal_loc'] == loc]
        df = df[df['model'] == model]
        r2s = df['obs_pred_r2']
        d = df['pred_dates'].values[-1]
        
        d = d[6:]
        #if model != 'SEIR-SD': d = d[6:]
        #elif model == 'SEIR-SD': d = d[-16:]
        
        #print(model, len(d), len(r2s))
        #sys.exit()
        
        if len(r2s) > max_len:
            max_len = len(r2s)
            dates = d
    
    #print(max_len, len(dates))
    fits_df = model_fits_df[model_fits_df['model'] == model]
    fig = fig_fxn(fig, model, fits_df, locations, max_len, i+1, dates)
    




plt.subplots_adjust(wspace=0.35, hspace=0.37)
plt.savefig('figures/Model_Performance_SEIR-SD.png', dpi=400, bbox_inches = "tight")
plt.close()
import pandas as pd
#import sys
import numpy as np
import datetime 

import model_fxns as fxns



# IMPORT DATA
seir_fits_df = pd.read_csv('data/SEIR-SD_States_Update.txt', sep='\t')
StatePops = pd.read_csv('data/StatePops.csv')
    
cases_df = pd.read_csv('data/COVID-CASES-DF.txt', sep='\t') 
cases_df = cases_df[cases_df['Country/Region'] == 'US']
cases_df = cases_df[cases_df['Province/State'] != 'US']
cases_df = cases_df[cases_df['Province/State'] != 'American Samoa']
cases_df = cases_df[cases_df['Province/State'] != 'Northern Mariana Islands']
cases_df = cases_df[cases_df['Province/State'] != 'Wuhan Evacuee']
cases_df = cases_df[cases_df['Province/State'] != 'Virgin Islands, U.S.']

    
cases_df.drop(columns=['Unnamed: 0'], inplace=True)
    

models = ['Logistic', 'SEIR-SD', 'Exponential', 'Quadratic', 'Gaussian']
locations = list(set(cases_df['Province/State']))
locations.sort()

ForecastDays_O = 60

            
col_names =  ['obs_y', 'pred_y', 'forecasted_y', 'pred_dates', 'forecast_dates', 'label', 'obs_pred_r2', 'model', 
                          'focal_loc', 'PopSize', 'ArrivalDate']
            
model_fits_df  = pd.DataFrame(columns = col_names)
    
            
    
for focal_loc in locations:
    print(focal_loc)
   
    try:
        PopSize = StatePops[StatePops['Province/State'] == focal_loc]['PopSize'].tolist()    
        PopSize = PopSize[0]
        ArrivalDate = StatePops[StatePops['Province/State'] == focal_loc]['Date_of_first_reported_infection'].tolist()
        ArrivalDate = ArrivalDate[0]
        SEIR_Fit = seir_fits_df[seir_fits_df['focal_loc'] == focal_loc]
 
    except:
        continue
        
    for model in models:
        print(model)
            
        new_cases = []
                    
        # A function to generate all figures and tables
                    
        # variables:
            # obs_x: observed x values
            # obs_y: observed y values
            # model: the model to fit
            # T0: likely date of first infection
            # ForecastDays: number of days ahead to extend predictions
            # N: population size of interest
            # ArrivalDate: likely data of first infection (used by SEIR-SD model)
            # incubation_period: disease-specific epidemilogical parameter
            # average number of days until an exposed person becomes
            # begins to exhibit symptoms of infection
            # infectious_period: disease-specific epidemilogical parameter
            # average number of days an infected person is infected
            # rho: disease-specific epidemilogical parameter
            # aka basic reproductive number
            # average number of secondary infections produced by a typical case 
            # of an infection in a population where everyone is susceptible
            # socdist: population-specific social-distancing parameter
                    
            # declare the following as global variables so their changes can be 
            # seen/used by outside functions
                    
                
        # add 1 to number of forecast days for indexing purposes
        ForecastDays = int(ForecastDays_O+1)
                    
                    
        # filter main dataframe to include only the chosen location
        df_sub = cases_df[cases_df['Province/State'] == focal_loc]
                    
        # get column labels, will filter below to extract dates
        yi = list(df_sub)
                    
        obs_y_trunc = []
        obs_y = df_sub.iloc[0,4:].values
        
        i = 0
        while obs_y[i] == 0:
            i+=1

        obs_y = obs_y[i:]
        #if model == 'SEIR-SD':
        #    ran_len = -15
        #else:
        ran_len = -1 * (len(obs_y) - 7)
        
        for i, j in enumerate(list(range(-10, 1))):
                        
            if j == 0:
                # get dates for today's predictions/forecast
                DATES = yi[4:]
                obs_y_trunc = df_sub.iloc[0,4:].values
            else:
                # get dates for previous days predictions/forecast
                DATES = yi[4:j]
                obs_y_trunc = df_sub.iloc[0,4:j].values
                        
                        
                        
            # remove leading zeros from observed y values 
            # and coordinate it with dates
            ii = 0
            while obs_y_trunc[ii] == 0: ii+=1
            y = obs_y_trunc[ii:]
            dates = DATES[ii:]
                        
                
            # declare x as a list of integers from 0 to len(y)
            x = list(range(len(y)))
            
            # Call function to use chosen model to obtain:
            #    r-square for observed vs. predicted
            #    predicted y-values
            #    forecasted x and y values
            iterations = 2
            obs_pred_r2, obs_x, pred_y, forecasted_x, forecasted_y, params = fxns.fit_curve(x, y, 
                                model, ForecastDays, PopSize, ArrivalDate, j, iterations, SEIR_Fit)
                        
            # convert y values to numpy array
            y = np.array(y)
            
            # because it isn't based on a best fit line,
            # and the y-intercept is forced through [0,0]
            # a model can perform so poorly that the 
            # observed vs predicted r-square is negative (a nonsensical value)
            # if this happens, report the r-square as 0.0
            if obs_pred_r2 < 0:
                obs_pred_r2 = 0.0
        
            # convert any y-values (observed, predicted, or forecasted)
            # that are less than 0 (nonsensical values) to 0.
            y[y < 0] = 0
            pred_y = np.array(pred_y)
            pred_y[pred_y < 0] = 0
        
            forecasted_y = np.array(forecasted_y)
            forecasted_y[forecasted_y < 0] = 0
                
            # number of from ArrivalDate to end of forecast window
            #numdays = len(forecasted_x)
            latest_date = pd.to_datetime(dates[-1])
            first_date = pd.to_datetime(dates[0])
        
            # get the date of the last day in the forecast window
            future_date = latest_date + datetime.timedelta(days = ForecastDays-1)
                
            # get all dates from ArrivalDate to the last day in the forecast window
            fdates = pd.date_range(start=first_date, end=future_date)
            fdates = fdates.strftime('%m/%d')
                
            # designature plot label for legend
            if j == 0:
                label='Current forecast'
                    
            else:
                label = str(-j)+' day old forecast'
                    
                    
            if label == 'Current forecast':
                for i, val in enumerate(forecasted_y):
                    if i > 0:
                        if forecasted_y[i] - forecasted_y[i-1] > 0:
                            new_cases.append(forecasted_y[i] - forecasted_y[i-1])
                        else:
                            new_cases.append(0)
                    if i == 0:
                        new_cases.append(forecasted_y[i])
                            
                        
            # get dates from ArrivalDate to the current day
            dates = pd.date_range(start=first_date, end=latest_date)
            dates = dates.strftime('%m/%d')
                
                
            output_list = [y, pred_y, forecasted_y, dates, fdates,
                           label, obs_pred_r2, model, focal_loc, PopSize, 
                           ArrivalDate]
                
            model_fits_df.loc[len(model_fits_df)] = output_list
                
            print(obs_pred_r2)
            
        print('\n')


model_fits_df.to_pickle('model_results_dataframe.pkl')
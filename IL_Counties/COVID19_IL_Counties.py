import pandas as pd


JH_DATA_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
df = pd.read_csv(JH_DATA_URL)

df = df[df['Province_State'] == 'Illinois']
df = df[df['Admin2'] != 'Out of IL']
df = df[df['Admin2'] != 'Unassigned']

df.drop(['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Province_State', 'Country_Region', 'Lat', 'Long_', 'Combined_Key'], 
        axis=1, inplace=True)    


counties = list(set(df['Admin2']))
counties.sort()

dates = list(df)[1:]

col_names = counties
row_names = dates

lofl = []
for ct in counties:
    cases = df[df['Admin2'] == ct].iloc[0].tolist()
    cases = cases[1:]
    
    print(len(cases))
    lofl.append(cases)

print(len(lofl))

lofl = list(map(list, zip(*lofl)))
new_df = pd.DataFrame(lofl, columns=counties)

new_df.index = dates

new_df.to_csv('IL-COVID-CASES.txt', sep='\t')
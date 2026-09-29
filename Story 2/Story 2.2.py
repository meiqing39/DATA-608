# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 13:11:23 2026

@author: Maggie
"""
## Approach 

# I will be creating data visulizations to answer the question "Has the FED been able to fulfill the mandate given to it by Congress?
# (control inflation and to maintain low unemployment.)


#Data Source

#https://fred.stlouisfed.org/docs/api/fred/category_series.html

import requests
import pandas as pd
from functools import reduce



# 1 GET API, EXTRA DATA from  create tables and merge 


# Credentials and endpoint setup
api_key = 'bc57f280a7d785379cd60e9dc96a4abb'
url = 'https://api.stlouisfed.org/fred/series/observations'

# Dictionary with IDs (key:value pairs)
series_dict = {
    'FEDFUNDS': 'fed_funds_rate',
    'CPIAUCSL': 'inflation_rate',
    'UNRATE': 'unemployment_rate'
}

dataframes = []

for series_id, col_name in series_dict.items():
    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': '2001-09-01',  #use for 25 years ago
        'observation_end': '2026-09-01'
    }
    
    if series_id == 'CPIAUCSL': #If series_id names equal to CPI, tell API to return year over year % change
        params['units'] = 'pc1' #Mod parameters only for CPI
        
    response = requests.get(url, params=params) # HTTP GET request
    data = response.json()  # Extract JSON payload
    df = pd.DataFrame(data['observations'])
    df = df[['date', 'value']].rename(columns={'value': col_name}) #keep date and value col, rename value col
    df[col_name] = pd.to_numeric(df[col_name], errors='coerce') #check if values are #s
    df['date'] = pd.to_datetime(df['date'])  #check if dates are datetime objects
    dataframes.append(df) # attach


last_df = reduce(lambda left, right: pd.merge(left, right, on='date', how='outer'), dataframes) # merge tables 
last_df = last_df.sort_values('date')
last_df = last_df.dropna()    #remove NaN missing dates
last_df = last_df.reset_index(drop=True)  #reset to count from index 0 and up

print(last_df.head())


# Plot data with seaborn and matplot package

import seaborn as sns
import matplotlib.pyplot as plt




long_df = last_df.melt(id_vars=['date'], 
                       value_vars=['fed_funds_rate', 'inflation_rate', 'unemployment_rate'],
                       var_name='Metric', 
                       value_name='Rate (%)')


long_df['Metric'] = long_df['Metric'].replace({     #REPLACE metric names
    'fed_funds_rate': 'Fed Funds Rate',
    'inflation_rate': 'Inflation Rate (CPI)',
    'unemployment_rate': 'Unemployment Rate'
})
plot_1 = long_df[(long_df['date'] >= '2001-09-01') & (long_df['date'] < '2010-01-01')] #slice (filter it)
plot_2 = long_df[(long_df['date'] >= '2010-01-01') & (long_df['date'] < '2020-01-01')]
plot_3 = long_df[(long_df['date'] >= '2020-01-01')]

sns.set_style("white")  #gets rid of gridline (data to ink ratio tufte)
palette = {"Fed Funds Rate": "blue", "Inflation Rate (CPI)": "red", "Unemployment Rate": "black"}  # set same color palette for all 3 graph

def format_chart(ax, title, xlabel, ylabel):   #use less ink
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_title(title, fontsize=22, fontweight='bold', pad=20)
    ax.set_xlabel(xlabel, fontsize=14, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=14, fontweight='bold')
    ax.tick_params(labelsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.4)

# PLOT 1
plt.figure(figsize=(10, 5)) 
sns.lineplot(data=plot_1, x='date', y='Rate (%)', hue='Metric', palette=palette, linewidth=2.5)

plt.axvline(pd.to_datetime('2004-06-01'), color='blue', linestyle='--', linewidth=2)  
plt.text(pd.to_datetime('2004-07-01'), 8, 'Fed Begins Rate Hikes', color='blue', fontweight='bold')
plt.axvline(pd.to_datetime('2008-09-15'), color='black', linestyle='--', linewidth=2) 
plt.text(pd.to_datetime('2008-11-01'), 8, 'Lehman Bros\nCollapse', color='black', fontweight='bold')
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0) #move legend outside chart from blocking
ax = plt.gca()    #big title formated
format_chart(ax, 'The Fed Abandons Inflation Defense to Rescue Jobs', 'Date', 'Rate (%)') 

plt.savefig('plot1_recession.png', dpi=300, bbox_inches='tight') 
plt.show()

# PLOT 2
plt.figure(figsize=(10, 5))
sns.lineplot(data=plot_2, x='date', y='Rate (%)', hue='Metric', palette=palette, linewidth=2.5)
plt.axvline(pd.to_datetime('2015-12-16'), color='blue', linestyle='--', linewidth=2)
plt.text(pd.to_datetime('2016-01-15'), 8, 'First Rate Hike in 7 Years ("Liftoff")', color='blue', fontweight='bold') 
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0) 
ax = plt.gca()
format_chart(ax, 'A Decade of Cheap Capital Achieves Full Employment', 'Date', 'Rate (%)')   

plt.savefig('plot2_recovery.png', dpi=300, bbox_inches='tight')
plt.show()

# PLOT 3
plt.figure(figsize=(10, 5))
sns.lineplot(data=plot_3, x='date', y='Rate (%)', hue='Metric', palette=palette, linewidth=2.5)
plt.axvline(pd.to_datetime('2020-03-01'), color='grey', linestyle='--', linewidth=2) 
plt.text(pd.to_datetime('2020-04-01'), 12, 'COVID-19 Lockdowns', color='grey', fontweight='bold') 
plt.axvline(pd.to_datetime('2022-03-01'), color='blue', linestyle='--', linewidth=2)  
plt.text(pd.to_datetime('2022-04-01'), 12, 'Fed Begins Rate Hikes', color='blue', fontweight='bold')
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0) 
ax = plt.gca()
format_chart(ax, '40-Year High Inflation Forces Aggressive Rate Hikes', 'Date', 'Rate (%)')

plt.savefig('plot3_covid.png', dpi=300, bbox_inches='tight')
plt.show()

# PLOT 4 SCATTER unemployment vs inflation

plt.figure(figsize=(10, 7))

scatter = plt.scatter(
    x=last_df['unemployment_rate'], 
    y=last_df['inflation_rate'], 
    c=last_df['fed_funds_rate'], 
    cmap='coolwarm',
    alpha=0.8,
    edgecolors='w',
    s=75 
)
plt.axhline(y=2.0, color='black', linestyle='--', alpha=0.5) 
plt.axvline(x=4.0, color='black', linestyle='--', alpha=0.5)
plt.text(12, 2.2, 'Fed Target Inflation (2%)', fontweight='bold', alpha=0.7) 
plt.text(4.2, 8.5, 'Full Employment (~4%)', fontweight='bold', alpha=0.7)
cbar = plt.colorbar(scatter, orientation = 'horizontal', pad=0.12)
cbar.set_label('Fed Funds Rate (%)\nBlue = Rate Cuts (Help Jobs) | Red = Rate Hikes (Fight Inflation)', 
               fontweight='bold', labelpad =10)  

plt.annotate('2022 Crisis\n(High Inflation, High Rates)', 
             xy=(3.8, 8.2),           # Add arrow coordinates
             xytext=(5.5, 6.5),       # add text using coordinates
             color='darkred', fontweight='bold',
             arrowprops=dict(color='darkred', arrowstyle='->', lw=2))

plt.annotate('Great Recession\n(High Unemployment, Low Rates)',      
             xy=(10.0, -2.0),         # use coordinate to point at the 10% unemployment cluster
             xytext=(10.5, -1.0),     
             color='blue', fontweight='bold',
             arrowprops=dict(color='blue', arrowstyle='->', lw=2))

plt.annotate('COVID-19 Lockdown\n(Unemployment at 14.7%)', 
             xy=(14.7, 0.3),          # Points to the extreme right dot
             xytext=(11.0, 4.0),      # add Text to sits above it with coordinates
             color='black', fontweight='bold',
             arrowprops=dict(color='black', arrowstyle='->',alpha = 0.3, lw=2))  #add alpha so the arrow doesn't block off words behind it


ax = plt.gca()
format_chart(ax, 'The Mandate Trade-off: Mapping the Contradiction', 'Unemployment Rate (%)', 'Inflation Rate (CPI %)')

plt.savefig('plot4.png', dpi=300, bbox_inches='tight')
plt.show()


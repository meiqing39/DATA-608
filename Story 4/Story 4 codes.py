# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 14:07:43 2026

@author: Maggie
"""

# load packages
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker


sns.set_style("white")

# create function ahead to remove chart junk and set Large Action Titles automatically
def format_spines(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#dddddd')
    ax.spines['bottom'].set_color('#dddddd')
    ax.tick_params(labelsize=12)
    
# function to format x axis 
formatter = ticker.FuncFormatter(lambda x, pos: f'${int(x/1000)}k' if x != 0 else '$0')

# Upload csv

df_salaries = pd.read_csv('https://github.com/meiqing39/DATA-608/raw/refs/heads/main/Story%204/DataScience_salaries_2025.csv')
df_bls = pd.read_excel('https://github.com/meiqing39/DATA-608/raw/refs/heads/main/Story%204/state_M2025_dl.xlsx')


# Data Clean : Role description
df_us_roles = df_salaries[df_salaries['company_location'] == 'US'].copy() #from salaries, create copy that consist of only US salary roles


# Group titles into 3 Roles (Kaggle data salaries)
def map_role(title):
    t = str(title).lower()
    if 'scientist' in t or 'machine learning' in t or 'ml' in t or 'research' in t:
        return 'Data Science & ML'
    elif 'architect' in t or 'engineer' in t or 'developer' in t:
        return 'Data Engineering & Architecture'
    elif 'analyst' in t or 'analytics' in t:
        return 'Data Analytics'
    else:
        return 'Other'
    
# Clean salaries     
df_us_roles = df_salaries[df_salaries['company_location'] == 'US'].copy()
df_us_roles['Role_Descriptor'] = df_us_roles['job_title'].apply(map_role)
role_clean = df_us_roles[df_us_roles['Role_Descriptor'] != 'Other']
role_avg = role_clean.groupby('Role_Descriptor')['salary_in_usd'].mean().sort_values(ascending=False).reset_index()


# Chart 1 Salary Averages by Role 

fig, ax1 = plt.subplots(figsize=(10, 5))

# Highlight #1 in Crimson, mute the rest
colors = ['#B22222' if role == 'Data Science & ML' else '#cccccc' for role in role_avg['Role_Descriptor']]
sns.barplot(data=role_avg, x='salary_in_usd', y='Role_Descriptor', palette=colors, ax=ax1)

format_spines(ax1)
ax1.set_xlabel('Average Salary (USD)', fontsize=14, fontweight='bold', labelpad=10)
ax1.set_ylabel('')

#Add kicker

fig.suptitle('Data Practitioners Average $113k - $177k Depending on Technical Specialization', 
             fontsize=16, fontweight='bold', ha='left', x=0.08, y=0.96)
    
# Calculates premium
ds_salary = role_avg.iloc[0]['salary_in_usd']        # ~$177k
analytics_salary = role_avg.iloc[2]['salary_in_usd'] # ~$113k
premium = ds_salary - analytics_salary

# Label inside bar also to remove gridline
for i, v in enumerate(role_avg['salary_in_usd']):
    ax1.text(v - 3000, i, f"${v:,.0f}", color='white' if i==0 else 'black',
             fontweight='bold', fontsize=12, va='center', ha='right') # ha means align to right
 
ax1.annotate(f'+${premium/1000:.0f}k more than\n Data Analytics', 
             xy=(ds_salary, 0),                  # Arrow at red bar end
             xytext=(ds_salary + 18000, 0),      # Text box on the right
             color='#B22222', fontweight='bold', fontsize=11, va='center',
             bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#B22222", lw=1.5), # Creates text box
             arrowprops=dict(color='#B22222', arrowstyle='->', lw=2))       
   

ax1.set_xlim(0, 245000)   #extend x axis 


ax1.xaxis.set_major_formatter(formatter)

plt.savefig('plot1_role_averages.png', dpi=300, bbox_inches='tight')
plt.show()


# Chart 2: Salary Distribution (Box Plot for the question of Variations)

fig, ax2 = plt.subplots(figsize=(10, 6))

sns.boxplot(data=role_clean, x='salary_in_usd', y='Role_Descriptor', order=role_avg['Role_Descriptor'], 
            palette=colors, showfliers=False, width=0.5, ax=ax2)

format_spines(ax2)
ax2.set_xlabel('Salary Distribution Spread (USD)', fontsize=14, fontweight='bold', labelpad=10)
ax2.set_ylabel('')

# Extract 75th percentile (q3) math for data science to use in label
stats = role_clean[role_clean['Role_Descriptor'] == 'Data Science & ML']['salary_in_usd'].describe()
q3_ds = stats['75%']


# draw arrow to the top 25% boundary in red box
ax2.annotate(f'Top 25% Threshold\n(Starts at ${q3_ds/1000:.0f}k)', 
             xy=(q3_ds, 0),                  # arrow at red box right side
             xytext=(q3_ds + 18000, -0.25),  # Text sits above and on right
             color='#B22222', fontweight='bold', va='center',
             arrowprops=dict(color='#B22222', arrowstyle='->', lw=2))

# label median values
for i, role in enumerate(role_avg['Role_Descriptor']):
    median_val = role_clean[role_clean['Role_Descriptor'] == role]['salary_in_usd'].median() # median above box
    ax2.text(median_val, i - 0.32, f"Median: ${median_val/1000:.0f}k",  
             color='black', fontweight='bold', ha='center', fontsize=10)

fig.suptitle('Averages Hide the Ceiling: The Top 25% of Technical Practitioners Exceed $216k', fontsize=16, fontweight='bold', ha='left', x=0.08, y=0.96)

ax2.xaxis.set_major_formatter(formatter)
plt.savefig('plot2_role_distribution.png', dpi=300, bbox_inches='tight')
plt.show()


# Data Clean : df_post for States (BLS Data)

target_codes = ['15-2051', '15-1243', '15-1211']
df_bls_filtered = df_bls[df_bls['OCC_CODE'].isin(target_codes)].copy()

cols_to_clean = ['A_MEAN', 'A_PCT10', 'A_PCT25', 'A_MEDIAN', 'A_PCT75', 'A_PCT90']
for col in cols_to_clean:
    df_bls_filtered[col] = pd.to_numeric(df_bls_filtered[col].astype(str).str.replace(',', '', regex=False).str.replace('*', '', regex=False).str.replace('#', '', regex=False), errors='coerce')

valid_bls = df_bls_filtered.dropna(subset=['A_MEAN', 'AREA_TITLE']).copy()
state_avg = valid_bls.groupby('AREA_TITLE')['A_MEAN'].mean().sort_values(ascending=False).head(8).reset_index()
bls_vars = valid_bls.groupby('AREA_TITLE')[cols_to_clean].mean().loc[state_avg['AREA_TITLE']].reset_index()


# Chart 3: State  (Cleveland Dot plot)

fig, ax3 = plt.subplots(figsize=(10, 6))

# Highlight top 3 states 
top_3 = ['California', 'Massachusetts', 'Washington']
dot_colors = ['#B22222' if state in top_3 else '#555555' for state in state_avg['AREA_TITLE']]


sns.stripplot(data=state_avg, x='A_MEAN', y='AREA_TITLE', size=14, palette=dot_colors, orient='h', ax=ax3)

format_spines(ax3)
ax3.set_xlabel('Average Salary (USD)', fontsize=14, fontweight='bold', labelpad=10)
ax3.set_ylabel('')
ax3.grid(axis='y', linestyle='--', alpha=0.3)

# National Average Line
national_avg = valid_bls['A_MEAN'].mean()
ax3.axvline(national_avg, color='grey', linestyle='--', alpha=0.8)


ax3.annotate(f'National Avg (~${national_avg/1000:.0f}k)', 
             xy=(national_avg, 7.2),             # The tip of the arrow on the dashed line
             xytext=(national_avg + 3000, 7.2), # text box location (shifted to the right)
             color='red', fontweight='bold', va='center',
             arrowprops=dict(color='red', arrowstyle='->', lw=2))

# Data labels next to every dot
for i, row in enumerate(state_avg.itertuples()):
    ax3.text(row.A_MEAN + 2000, i, f"${row.A_MEAN:,.0f}", color=dot_colors[i], fontweight='bold', va='center')

# Kicker Structure
fig.suptitle('Geography Shifts the Baseline: Top Hubs Pay $25k+  Above National Average', 
             fontsize=17, fontweight='bold', ha='left', x=0.08, y=0.96)

ax3.set_xlim(105000, 165000) # extend x axis limit so labels can be seen
ax3.xaxis.set_major_formatter(formatter)
plt.savefig('plot3_states_bls.png', dpi=300, bbox_inches='tight')
plt.show()


# Chart 4 State variation (range plot)

fig, ax4 = plt.subplots(figsize=(10, 6))

states = bls_vars['AREA_TITLE']
y_pos = np.arange(len(states))

# Match box to top 3 highlighted states
top_3 = ['California', 'Massachusetts', 'Washington']
box_colors = ['#D27979' if state in top_3 else '#cccccc' for state in states]
dot_colors = ['#B22222' if state in top_3 else '#555555' for state in states]

# Draw range lines
ax4.hlines(y_pos, bls_vars['A_PCT10'], bls_vars['A_PCT90'], color='lightgrey', linewidth=3)
ax4.hlines(y_pos, bls_vars['A_PCT25'], bls_vars['A_PCT75'], color=box_colors, linewidth=12)

# Add $170k Threshold Anchor Line
threshold = 170000
ax4.axvline(threshold, color='#B22222', linestyle=':', alpha=0.6)


# Label threshold line on top of chart (y = 6.5)
ax4.annotate('Top 25% Threshold ($170k)', 
             xy=(threshold, 6.5),             
             xytext=(threshold + 5000, 6.5), 
             color='#B22222', fontweight='bold', va='center',
             arrowprops=dict(color='#B22222', arrowstyle='->', lw=1.5))


# Data Labels (Medians and 75th Percentiles)
for i in range(len(states)):
    state_name = states.iloc[i]
    median_val = bls_vars['A_MEDIAN'].iloc[i]
    q3_val = bls_vars['A_PCT75'].iloc[i]
    
    # place median marker
    ax4.plot(median_val, y_pos[i], 'o', color=dot_colors[i], markersize=7)
    
    # Label median dots above marker
    ax4.text(median_val, i + 0.25, f"${median_val/1000:.0f}k", color='#333333', fontsize=10, ha='center', fontweight='bold')
    
    # Label 75th Percentile for the Top 3 states
    if state_name in top_3:
        ax4.text(q3_val + 3000, i, f"${q3_val/1000:.0f}k", color='#B22222', fontweight='bold', va='center')

format_spines(ax4)
ax4.set_yticks(y_pos)
ax4.set_yticklabels(states, fontsize=12)
ax4.set_xlabel('Salary Distribution Spread (USD)', fontsize=14, fontweight='bold', labelpad=10)


ax4.xaxis.set_major_formatter(formatter)
ax4.set_xlim(60000, 225000)



fig.suptitle('The Ultimate Multiplier: In the Top 3 (CA, WA, MA), 25% of Practitioners Earn Over $170k', fontsize=17, fontweight='bold', ha='left', x=0.08, y=0.96)

plt.savefig('plot4_state_distribution_bls.png', dpi=300, bbox_inches='tight')
plt.show()
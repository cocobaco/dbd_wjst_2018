# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 07:24:41 2018

@author: rop
"""

# for WJST paper (2018)


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


###############
SAVE_FIG = True
###############

# get time string (for file saving)
now = datetime.now()
time_str = now.strftime('%Y%m%d-%H%M')

# get data
df = pd.read_csv('dbd.csv')
print(df)
#df = df.transpose()
#df.reset_index(inplace=True)
#df.columns = df.iloc[0]
#df.drop(0, inplace=True)
#df.rename(columns={'Unnamed: 0': 'treat_time'}, inplace=True)
#df = df.reindex(df.index.drop(0))
#
#for i in range(df.shape[0]):
#    if i < 4:
#        df.loc[i, 'sample'] = 'Licorice' 
#    else:
#        df.loc[i, 'sample'] = 'Sappan Tree'
#df.drop(['Licorice', 'Sappan  Tree'], axis=1, inplace=True)

df.loc[:, 'aerobic_count'] = [x[0] for x in df['Total aerobic plate count'].str.split('+')]
df.loc[:, 'aerobic_err'] = [x[1] for x in df['Total aerobic plate count'].str.split('+')]
bad_chars = 'abc'
for char in bad_chars:
    df.loc[:, 'aerobic_err'] = df['aerobic_err'].str.replace(char, '')

df.loc[:, 'yeast_mold_count'] = [x[0] for x in df['Total yeast & mold count'].str.split('+')]
df.loc[:, 'yeast_mold_err'] = [x[1] for x in df['Total yeast & mold count'].str.split('+')]
for char in bad_chars:
    df.loc[:, 'yeast_mold_err'] = df['yeast_mold_err'].str.replace(char, '')

df.drop(['Total aerobic plate count', 'Total yeast & mold count'], axis=1, inplace=True)

# clean up column names
df.rename(columns={'Coliform (MPN/g)': 'coliform', 
                   'E. coli  (MPN/g)': 'e.coli'}, inplace=True)
df.loc[:, 'coliform'] = df['coliform'].replace('< 3', '0')
df.loc[:, 'e.coli'] = df['e.coli'].replace('< 3', '0')

df.loc[:, 'coliform_min'] = [x.split('-')[0] if '-' in x else x for x in df['coliform']]
df.loc[:, 'coliform_max'] = [x.split('-')[1] if '-' in x else x for x in df['coliform']]
df.drop('coliform', axis=1, inplace=True)

# convert to correct data types
print(df.dtypes)
df['aerobic_count'] = df['aerobic_count'].astype(float)
df['aerobic_err'] = df['aerobic_err'].astype(float)
df['yeast_mold_count'] = df['yeast_mold_count'].astype(float)
df['yeast_mold_err'] = df['yeast_mold_err'].astype(float)
df['coliform_min'] = df['coliform_min'].astype(float)
df['coliform_max'] = df['coliform_max'].str.replace(',', '').astype(float)
print(df)

licorice = df[df['sample']=='licorice']
sappan = df[df['sample']=='sappan tree']

#plt.style.use('fivethirtyeight')
plt.style.use('ggplot')
#plt.style.use('seaborn')


fig, ax = plt.subplots()
licorice.plot(kind='scatter', x='treat_time', y='aerobic_count', 
              label='licorice', c='r', ax=ax)
sappan.plot(kind='scatter', x='treat_time', y='aerobic_count', 
            label='sappan', c='b', ax=ax)
#ax.bar(licorice['treat_time'], licorice['aerobic_count'], label='licorice')
#ax.bar(sappan['treat_time'], sappan['aerobic_count'], label='sappan')
plt.legend()
plt.show()

fig, ax = plt.subplots()
ax.bar(licorice['treat_time'], licorice['aerobic_count'], label='licorice')
ax.bar(sappan['treat_time']+1, sappan['aerobic_count'], label='sappan')
ax.set_xlabel('treat time')
ax.set_ylabel('aerobic count')
plt.sca(ax)
plt.legend()

sns.set_style('whitegrid')
sns.set_palette("colorblind")  
# available: deep, muted, bright, pastel, dark, colorblind

plt.figure()
g = sns.barplot(data=df, x='treat_time', y='aerobic_count', hue='sample')
plt.xlabel('treatment time')
plt.ylabel('aerobic count')

plt.figure()
g = sns.barplot(data=df, x='treat_time', y='yeast_mold_count', hue='sample')
plt.xlabel('treatment time')
plt.ylabel('yeast and mold count')


# ------- Figures for paper --------

plt.figure()
g = sns.lmplot(data=df, x='treat_time', y='aerobic_count', 
               fit_reg=True, ci=95, aspect=1, hue='sample', 
               legend=False)
ax = g.axes.flat[0]
ax.set_xlabel('treatment time (min)', fontsize=14)
ax.set_ylabel('aerobic plate count (log CFU/g)', fontsize=14)
#xticklabels = df['treat_time'].unique()
xticklabels = ax.get_xticklabels()
yticklabels = ax.get_yticklabels()
ax.set_xticklabels(xticklabels, fontsize=14)
ax.set_yticklabels(yticklabels, fontsize=14)
ax.legend(fontsize=14)
#plt.setp(g.axes.flat.get_legend().get_texts(), fontsize=14)
#plt.setp(g.axes.flat.get_legend().get_title(), fontsize=14)
if SAVE_FIG:
    outFile = ''.join(['fig_', 'apc', '_', time_str, '.png'])
    g.savefig(outFile, dpi=400)


plt.figure()
g = sns.lmplot(data=df, x='treat_time', y='yeast_mold_count', 
               fit_reg=True, ci=95, aspect=1, hue='sample', 
               legend=False)
ax = g.axes.flat[0]
ax.set_xlabel('treatment time (min)', fontsize=14)
ax.set_ylabel('yeast and mold count (log CFU/g)', fontsize=14)
xticklabels = ax.get_xticklabels()
yticklabels = ax.get_yticklabels()
ax.set_xticklabels(xticklabels, fontsize=14)
ax.set_yticklabels(yticklabels, fontsize=14)
ax.legend(fontsize=14)
if SAVE_FIG:
    outFile = ''.join(['fig_', 'ymc', '_', time_str, '.png'])
    g.savefig(outFile, dpi=400)

plt.show()
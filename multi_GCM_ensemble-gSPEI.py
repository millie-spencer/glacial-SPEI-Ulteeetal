#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Multi-model ensemble SPEI analysis using pandas
Created on Wed Apr 15 15:55:58 2020

@author: EHU
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import gSPEI as gSPEI

fpath = './data/SPEI_Files/'

## Settings in filenames
integration_times = np.arange(3, 28, 4) # all SPEI integration times used
modelnames = ['CanESM2', 'CCSM4', 'CNRM-CM5', 'CSIRO-Mk3-6-0', 'GISS-E2-R', 'INMCM4', 'MIROC-ESM', 'NorESM1-M'] # all models used in comparison
scenarios = ['Rcp4p5', 'Rcp8p5'] # climate scenarios
cases = ['NRunoff', 'WRunoff', 'diff'] # inclusion of glacier runoff

## Basins in the order they are written
basin_names = ['INDUS','TARIM','BRAHMAPUTRA','ARAL SEA','COPPER','GANGES','YUKON','ALSEK','SUSITNA','BALKHASH','STIKINE','SANTA CRUZ',
'FRASER','BAKER','YANGTZE','SALWEEN','COLUMBIA','ISSYK-KUL','AMAZON','COLORADO','TAKU','MACKENZIE','NASS','THJORSA','JOEKULSA A F.',
'KUSKOKWIM','RHONE','SKEENA','OB','OELFUSA','MEKONG','DANUBE','NELSON RIVER','PO','KAMCHATKA','RHINE','GLOMA','HUANG HE','INDIGIRKA',
'LULE','RAPEL','SANTA','SKAGIT','KUBAN','TITICACA','NUSHAGAK','BIOBIO','IRRAWADDY','NEGRO','MAJES','CLUTHA','DAULE-VINCES',
'KALIXAELVEN','MAGDALENA','DRAMSELV','COLVILLE']

yrs = np.linspace(1900, 2101, num=2412)

## Read all in to dict by GCM as in other gSPEI scripts
SPEI_by_model = {m: {} for m in modelnames} # create dictionary indexed by model name
for m in modelnames:
    norunoff_f_m = fpath+'NRunoff_{}_{}_{}.txt'.format(integration_times[3], m, scenarios[0])
    wrunoff_f_m = fpath+'WRunoff_{}_{}_{}.txt'.format(integration_times[3], m, scenarios[0])
    SPEI_by_model[m]['NRunoff'] = np.loadtxt(norunoff_f_m)
    SPEI_by_model[m]['WRunoff'] = np.loadtxt(wrunoff_f_m)
    SPEI_by_model[m]['diff'] = SPEI_by_model[m]['WRunoff'] - SPEI_by_model[m]['NRunoff']

## Re-structure dictionary and create pandas DataFrames aggregated by basin
SPEI_by_basin = gSPEI.sort_models_to_basins(SPEI_by_model)

## Compute multi-GCM ensemble means and quartiles
r = gSPEI.basin_ensemble_mean(SPEI_by_basin, 'TARIM', 'WRunoff').rolling(window=12*30).mean()
q1 = gSPEI.basin_quartile(SPEI_by_basin, 'TARIM', 'WRunoff', q=0.25).rolling(window=12*30).mean()
q2 = gSPEI.basin_quartile(SPEI_by_basin, 'TARIM', 'WRunoff', q=0.75).rolling(window=12*30).mean()

## Make example figure
rm = SPEI_by_basin['TARIM']['WRunoff'].rolling(window=12*30, axis=0).mean()
rm_q1 = rm.quantile(q=0.25, axis=1)
rm_q3 = rm.quantile(q=0.75, axis=1)
single_models = [SPEI_by_basin['TARIM']['WRunoff'][m].rolling(window=12*30).mean() for m in modelnames]

colors_w = cm.get_cmap('Blues')(np.linspace(0.2, 1, num=len(modelnames)))
fig, ax = plt.subplots()
ax.plot(yrs, r, 'k', linewidth=3.0)
ax.plot(yrs, rm_q1, 'k')
ax.plot(yrs, rm_q3, 'k')
for i in range(len(modelnames)):
    ax.plot(yrs, single_models[i], color=colors_w[i])
ax.fill_between(yrs, rm_q1, rm_q3, color='k', alpha=0.2)
ax.tick_params(axis='both', labelsize=12)
ax.set_xticks([1900,1950, 2000, 2050, 2100])
ax.set_xlabel('Years', fontsize=14)
ax.set_ylabel('Rolling mean SPEI', fontsize=14)

## Functions to support SPEI drought index analysis
## Code: EHU | SPEI data: SC
## 12 Sept 2019

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from datetime import date

## Constants associated with this analysis
yrs = np.linspace(1900, 2101, num=2412)
model_names = ['CanESM2', 'CCSM4', 'CNRM-CM5', 'CSIRO-Mk3-6-0', 'GISS-E2-R', 'INMCM4', 'MIROC-ESM', 'NorESM1-M'] # all models used in comparison
scenarios = ['Rcp4p5', 'Rcp8p5'] # climate scenarios
basin_names = ['INDUS','TARIM','BRAHMAPUTRA','ARAL SEA','COPPER','GANGES','YUKON','ALSEK','SUSITNA','BALKHASH','STIKINE','SANTA CRUZ',
'FRASER','BAKER','YANGTZE','SALWEEN','COLUMBIA','ISSYK-KUL','AMAZON','COLORADO','TAKU','MACKENZIE','NASS','THJORSA','JOEKULSA A F.',
'KUSKOKWIM','RHONE','SKEENA','OB','OELFUSA','MEKONG','DANUBE','NELSON RIVER','PO','KAMCHATKA','RHINE','GLOMA','HUANG HE','INDIGIRKA',
'LULE','RAPEL','SANTA','SKAGIT','KUBAN','TITICACA','NUSHAGAK','BIOBIO','IRRAWADDY','NEGRO','MAJES','CLUTHA','DAULE-VINCES',
'KALIXAELVEN','MAGDALENA','DRAMSELV','COLVILLE']


def plot_basin_runmean(basin_id, permodel_dict, which='diff', window_yrs=30, cmap_name='viridis', show_labels=True, show_plot=True, save_plot=False, output_tag=None):
    """Make a plot of running mean difference in SPEI for a given basin, comparing across models.
    Arguments:
        basin_id: integer, index of basin in the standard list "basin_names"
        permodel_dict: dictionary storing SPEI per model, with the structure dict[modelname]['diff'/'WRunoff'/'NRunoff'][basinname] = basin difference in SPEI for this model
        which: string identifying 'WRunoff' (with glacial runoff), 'NRunoff' (no runoff), or 'diff' (their difference)
        window_yrs: number of years to consider in running average.  Default 30
        cmap_name: name of matplotlib colormap from which to select line colors. Default 'viridis'
        show_plot: Boolean, whether to show the resulting plot.  Default True
        save_plot: Boolean, whether to save the plot in the working directory.  Default False
        output_tag: anything special to note in output filename, e.g. global settings applied. Default None will label 'default'
    """
    window_size = 12 * window_yrs # size of window given monthly data
    basin_runavg_bymodel = [np.convolve(permodel_dict[m][which][basin_id], np.ones((window_size,))/window_size, mode='valid') for m in model_names] #compute running means
    colors = cm.get_cmap(cmap_name)(np.linspace(0, 1, num=len(model_names)))
    styles = ('-',':')
    fig, ax = plt.subplots()
    for k,m in enumerate(model_names):
        ax.plot(yrs[(window_size/2):-(window_size/2 -1)], basin_runavg_bymodel[k], label=m, color=colors[k], ls=styles[np.mod(k, len(styles))], linewidth=2.0)
    ax.tick_params(axis='both', labelsize=14)
    ax.set_xticks([1900,1950, 2000, 2050, 2100])
    if show_labels:
        ax.set_xlabel('Years', fontsize=16)
        ax.set_ylabel('Mean SPEI {}'.format(which), fontsize=16)
        ax.set_title('{} year running mean, {} case, {} basin'.format(window_yrs, which, basin_names[basin_id]), fontsize=18)
    ax.legend(loc='best')
    plt.tight_layout()
    if save_plot:
        if output_tag is None:
            output_tag='default'
        plt.savefig(fname='{}yr_runmean-{}-{}_basin-{}-{}.png'.format(window_yrs, which, basin_names[basin_id], output_tag, date.today()))
    if show_plot:
        plt.show()
    

def plot_runmean_comparison(basin_id, permodel_dict, window_yrs=30, cmaps=('Blues', 'Wistia'), show_labels=True, show_plot=True, save_plot=False, output_tag=None):
    """Make a plot comparing running-average model projections of SPEI with and without glacial runoff.
    Arguments:
        basin_id: integer, index of basin in the standard list "basin_names"
        permodel_dict: dictionary storing SPEI per model, with the structure dict[modelname]['diff'/'WRunoff'/'NRunoff'][basinname] = basin difference in SPEI for this model
        window_yrs: number of years to consider in running average.  Default 30
        cmaps: tuple (str, str) of matplotlib colormap names from which to select line colors for each case. Default ('Blues', 'Greys')
        show_plot: Boolean, whether to show the resulting plot.  Default True
        save_plot: Boolean, whether to save the plot in the working directory.  Default False
        output_tag: anything special to note, e.g. global settings applied. Default None will label 'default'
    """
    window_size = 12 * window_yrs # size of window given monthly data
    basin_runavg_w = [np.convolve(permodel_dict[m]['WRunoff'][basin_id], np.ones((window_size,))/window_size, mode='valid') for m in model_names] #compute running means
    basin_runavg_n = [np.convolve(permodel_dict[m]['NRunoff'][basin_id], np.ones((window_size,))/window_size, mode='valid') for m in model_names] #compute running means
    colors_w = cm.get_cmap(cmaps[0])(np.linspace(0.2, 1, num=len(model_names)))
    colors_n = cm.get_cmap(cmaps[1])(np.linspace(0.2, 1, num=len(model_names)))
    fig, ax = plt.subplots()
    plt.axhline(y=0, color='Gainsboro', linewidth=2.0)
    for k,m in enumerate(model_names):
        ax.plot(yrs[(window_size/2):-(window_size/2 -1)], basin_runavg_w[k], label=m, color=colors_w[k], linewidth=2.0)
        ax.plot(yrs[(window_size/2):-(window_size/2 -1)], basin_runavg_n[k], ls='-.', color=colors_n[k], linewidth=2.0)
    ax.tick_params(axis='both', labelsize=14)
    ax.set_xticks([1900,1950, 2000, 2050, 2100])
    if show_labels:
        ax.set_xlabel('Years', fontsize=16)
        ax.set_ylabel('SPEI', fontsize=16)
        ax.set_title('{} year running average trajectories, {} basin'.format(window_yrs, basin_names[basin_id]), fontsize=18)
    ax.legend(loc='best')
    plt.tight_layout()
    if save_plot:
        if output_tag is None:
            output_tag='default'
        plt.savefig(fname='{}yr_runmean_comp-{}_basin-{}-{}.png'.format(window_yrs, basin_names[basin_id], output_tag, date.today()))
    if show_plot:
        plt.show()


def plot_basin_runvar(basin_id, permodel_dict, which='diff', window_yrs=30, cmaps='viridis', show_labels=True, show_plot=True, save_plot=False, output_tag=None):
    """Make a plot comparing running-average model projections of SPEI with and without glacial runoff.
    Arguments:
        basin_id: integer, index of basin in the standard list "basin_names"
        permodel_dict: dictionary storing SPEI per model, with the structure dict[modelname]['diff'/'WRunoff'/'NRunoff'][basinname] = basin difference in SPEI for this model
        window_yrs: number of years to consider in running average.  Default 30
        cmaps: tuple (str, str) of matplotlib colormap names from which to select line colors for each case. Default ('Blues', 'Greys')
        show_plot: Boolean, whether to show the resulting plot.  Default True
        save_plot: Boolean, whether to save the plot in the working directory.  Default False
        output_tag: anything special to note, e.g. global settings applied. Default None will label 'default'
    """
    basin_dict = {m: {'NRunoff': [], 'WRunoff': [], 'diff': []} for m in model_names}
    varwindow = 12*window_yrs # number of months to window in rolling variance
    for m in model_names:
        nr = pd.Series(permodel_dict[m]['NRunoff'][basin_id])
        wr = pd.Series(permodel_dict[m]['WRunoff'][basin_id])
        basin_dict[m]['NRunoff'] = nr.rolling(window=varwindow).var()
        basin_dict[m]['WRunoff'] = wr.rolling(window=varwindow).var()
        basin_dict[m]['diff'] = basin_dict[m]['WRunoff'] - basin_dict[m]['NRunoff']
            
    colors = cm.get_cmap(cmaps)(np.linspace(0.2, 1, num=len(model_names)))
    styles = ('-',':')
    fig, ax = plt.subplots()
    plt.axhline(y=0, color='Gainsboro', linewidth=2.0)
    for k,m in enumerate(model_names):
        ax.plot(yrs, basin_dict[m][which], label=m, color=colors[k], ls=styles[np.mod(k, len(styles))], linewidth=2.0)
    ax.tick_params(axis='both', labelsize=14)
    ax.set_xticks([1900,1950, 2000, 2050, 2100])
    if show_labels:
        ax.set_xlabel('Years', fontsize=16)
        ax.set_ylabel('SPEI variance {}'.format(which), fontsize=16)
        ax.set_title('{} year running variance by model, {} case, {} basin'.format(window_yrs, which, basin_names[basin_id]), fontsize=18)
    ax.legend(loc='best')
    plt.tight_layout()
    if save_plot:
        if output_tag is None:
            output_tag='default'
        plt.savefig(fname='{}yr_runvar-{}-{}_basin-{}-{}.png'.format(window_yrs, which, basin_names[basin_id], output_tag, date.today()))
    if show_plot:
        plt.show()

    

def glacial_meandiff(permodel_dict, years=(2070, 2100), return_range=True):
    """Calculate the difference in 30-yr mean SPEI with vs. without runoff
    Arguments:
        permodel_dict: dictionary storing SPEI per model, with the structure dict[modelname]['WRunoff'/'NRunoff'][basinname] = basin difference in SPEI for this model
        years: what years of scenario to examine. Default (2070, 2100)
        return_range: whether to return low/high multi-model range. Default True
    Outputs:
        median difference in mean(WRunoff)-mean(NRunoff)
        range in mean difference, expressed as 2xN array of (median-low, high-meadian) for errorbar plotting
    """
    idx_i, idx_f = 12*np.array((years[0]-1900, years[1]-1899)) #add 12 months to last year so that calculation goes for all 12 months
    bas_glac_meanmed = []
    bas_glac_lowmeans = []
    bas_glac_highmeans = []
    
    for i in range(len(basin_names)):
        bmeans_n = [np.nanmean(permodel_dict[m]['NRunoff'][i][idx_i:idx_f]) for m in model_names]
        bmeans_g = [np.nanmean(permodel_dict[m]['WRunoff'][i][idx_i:idx_f]) for m in model_names]
        basin_glacial_meanshift = np.array(bmeans_g) - np.array(bmeans_n)
        bas_glac_meanmed.append(np.nanmedian(basin_glacial_meanshift))
        bas_glac_lowmeans.append(np.nanmedian(basin_glacial_meanshift) - np.nanmin(basin_glacial_meanshift))
        bas_glac_highmeans.append(np.nanmax(basin_glacial_meanshift) - np.nanmedian(basin_glacial_meanshift))

    mean_spread = np.stack((bas_glac_lowmeans, bas_glac_highmeans))
    
    if return_range:
        return bas_glac_meanmed, mean_spread
    else:
        return bas_glac_meanmed
        
def glacial_vardiff(permodel_dict, years=(2070, 2100), return_range=True):
    """Calculate the difference in 30-yr SPEI variance with vs. without runoff
    Arguments:
        permodel_dict: dictionary storing SPEI per model, with the structure dict[modelname]['WRunoff'/'NRunoff'][basinname] = basin difference in SPEI for this model
        years: what years of scenario to examine. Default (2070, 2100)
        return_range: whether to return low/high multi-model range. Default True
    Outputs:
        median difference in var(WRunoff)-var(NRunoff)
        range in variance difference, expressed as 2xN array of (median-low, high-meadian) for errorbar plotting
    """
    idx_i, idx_f = 12*np.array((years[0]-1900, years[1]-1899)) #add 12 months to last year so that calculation goes for all 12 months
    bas_glac_varmed = []
    bas_glac_lowvars = []
    bas_glac_highvars = []
    
    for i in range(len(basin_names)):
        bvar_n = [np.nanvar(permodel_dict[m]['NRunoff'][i][idx_i:idx_f]) for m in model_names]
        bvar_g = [np.nanvar(permodel_dict[m]['WRunoff'][i][idx_i:idx_f]) for m in model_names]
        basin_glacial_varshift = np.array(bvar_g) - np.array(bvar_n)
        bas_glac_varmed.append(np.nanmedian(basin_glacial_varshift))
        bas_glac_lowvars.append(np.nanmedian(basin_glacial_varshift) - np.nanmin(basin_glacial_varshift))
        bas_glac_highvars.append(np.nanmax(basin_glacial_varshift) - np.nanmedian(basin_glacial_varshift))
        
    var_spread = np.stack((bas_glac_lowvars, bas_glac_highvars))

    if return_range:
        return bas_glac_varmed, var_spread
    else:
        return bas_glac_varmed


## New functions to produce multi-GCM ensemble plots -- added 27 Apr 2020
        
def sort_models_to_basins(permodel_dict, cases_included=['NRunoff', 'WRunoff', 'diff']):
    """Re-format a dictionary loaded in by GCM to be sorted by basin name first.
    Facilitates multi-GCM ensemble estimates for each basin.

    Parameters
    ----------
    permodel_dict : DICT
        Stores SPEI per model, with the structure dict[modelname]['WRunoff'/'NRunoff'][basinname] = basin SPEI for this model and case
    cases_included : LIST of STR
        Names cases 'WRunoff' (with glacial runoff), 'NRunoff' (no glacial runoff), 'diff' (their difference) included in input/output
        
    Returns
    -------
    perbasin_dict: DICT
        Stores SPEI per basin
    """
    cases = cases_included # inclusion of glacier runoff
    
    SPEI_by_basin = {b: {} for b in basin_names} # create dictionary indexed by basin name
    for i, b in enumerate(basin_names):
        SPEI_by_basin[b] = {case: {} for case in cases}
        for case in cases:
            tempdict = {}
            for m in model_names:
                tempdict[m] = permodel_dict[m][case][i] # pull data from SPEI_by_model into this new dict
            SPEI_by_basin[b][case] = pd.DataFrame.from_dict(tempdict)

    return SPEI_by_basin

def basin_ensemble_mean(dict_by_basin, basin_name, case):
    """Compute the multi-GCM ensemble mean SPEI for a given basin and case
    
    Parameters
    ----------
    dict_by_basin : DICT
        Stores SPEI per basin
    basin_name : STR
        Which basin to study
    case : STR
        'WRunoff', 'NRunoff', 'diff'
        
    Returns
    -------
    em: pandas.Series object
        Ensemble mean SPEI for this basin and case
    
    """
    basin_df = dict_by_basin[basin_name][case]
    em = basin_df.mean(axis=1) #compute mean among all models at each timestep
    return em # a pandas Series object

def basin_quartile(dict_by_basin, basin_name, case, q=0.25):
    """Compute the multi-GCM ensemble first quartile for a given basin and case
    
    Parameters
    ----------
    dict_by_basin : DICT
        Stores SPEI per basin
    basin_name : STR
        Which basin to study
    case : STR
        'WRunoff', 'NRunoff', 'diff'
    q : FLOAT
        Value between 0-1 indicating which quartile to compute. q=0.25 for first, 0.75 for third, etc.
        
    Returns
    -------
    em: pandas.Series object
        First quartile SPEI for this basin and case
    
    """
    basin_df = dict_by_basin[basin_name][case]
    q1 = basin_df.quantile(q=q, axis=1)
    return q1

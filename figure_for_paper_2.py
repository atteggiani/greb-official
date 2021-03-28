import warnings
warnings.simplefilter("ignore")
import myfuncs as my
from myfuncs import GREB as greb
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator,FormatStrFormatter
import numpy as np
import matplotlib.cm as cm
import os 
import cartopy.crs as ccrs
import matplotlib.colors as colors

output_folder = "/Users/dmar0022/university/phd/phd_project/Papers/Counteracting global warming by using a locally variable Solar Radiation Management/figs_for_paper"
matplotlib.rcParams.update({'font.size': 14})
nlev=200

# DATA
r_cld=greb.from_binary(greb.greb_folder()+'/r_calibration_cloud').r
r_sw=greb.from_binary(greb.greb_folder()+'/r_calibration_solar').r

def plot_fig2_sw(nlev=100):
    '''
    Sensitivity matrix
    '''
    fig = plt.figure(figsize=(16,3),constrained_layout=False)
    heights = [10,1]
    wspace=0.15; hspace=0.15; ncols=3; nrows=2
    gs1=fig.add_gridspec(ncols=ncols, nrows=nrows,
                         height_ratios=heights,
                         wspace=wspace, hspace=hspace,
                         bottom=0, top=1)
    # S ANNUAL MEAN
    ax1 = fig.add_subplot(gs1[0, 0],projection=ccrs.Robinson())
    im=r_sw.annual_mean(30*12).plotvar(ax=ax1,
                                add_colorbar=False,
                                levels=np.linspace(0,0.2,nlev),
                                cmap=cm.viridis,
                                title='$S_{SW}$')
    # S DJF MEAN
    ax2 = fig.add_subplot(gs1[0, 1],projection=ccrs.Robinson())
    im2=r_sw.isel(time=slice(-30*12,None)).group_by('season').sel(time='DJF').plotvar(ax=ax2,
                                add_colorbar=False,
                                levels=np.linspace(0,0.2,nlev),
                                cmap=cm.viridis,
                                title='$S_{SW}$ DJF')
    # S JJA MEAN                                
    ax3 = fig.add_subplot(gs1[0, 2],projection=ccrs.Robinson())
    r_sw.isel(time=slice(-30*12,None)).group_by('season').sel(time='JJA').plotvar(ax=ax3,
                                add_colorbar=False,
                                levels=np.linspace(0,0.2,nlev),
                                cmap=cm.viridis,
                                title='$S_{SW}$ JJA')
    # Colorbar 
    ax4 = fig.add_subplot(gs1[1, 0:])
    plt.colorbar(im,cax=ax4, orientation='horizontal',
                 ticks=np.arange(0,0.2+0.025,0.025),
                 label='K/(W $m^{-2}$)')

def plot_fig2_cld(nlev=100):
    '''
    Sensitivity matrix
    '''
    fig = plt.figure(figsize=(16,3),constrained_layout=False)
    heights = [10,1]
    wspace=0.15; hspace=0.15; ncols=3; nrows=2
    gs1=fig.add_gridspec(ncols=ncols, nrows=nrows,
                         height_ratios=heights,
                         wspace=wspace, hspace=hspace,
                         bottom=0, top=1)
    # S ANNUAL MEAN
    ax1 = fig.add_subplot(gs1[0, 0],projection=ccrs.Robinson())
    im=r_cld.annual_mean(30*12).plotvar(ax=ax1,
                                add_colorbar=False,
                                levels=np.linspace(-10,0,nlev),
                                cmap=cm.viridis,
                                title='$S_{CLD}$')
    # S DJF MEAN
    ax2 = fig.add_subplot(gs1[0, 1],projection=ccrs.Robinson())
    im2=r_cld.isel(time=slice(-30*12,None)).group_by('season').sel(time='DJF').plotvar(ax=ax2,
                                add_colorbar=False,
                                levels=np.linspace(-10,3,nlev),
                                norm = colors.DivergingNorm(vmin=-10,vcenter=0,vmax=3),
                                cmap=cm.viridis,
                                title='$S_{CLD}$ DJF')
    # S JJA MEAN                                
    ax3 = fig.add_subplot(gs1[0, 2],projection=ccrs.Robinson())
    r_cld.isel(time=slice(-30*12,None)).group_by('season').sel(time='JJA').plotvar(ax=ax3,
                                add_colorbar=False,
                                levels=np.linspace(-10,3,nlev),
                                norm = colors.DivergingNorm(vmin=-10,vcenter=0,vmax=3),
                                cmap=cm.viridis,
                                title='$S_{CLD}$ JJA')
    # Colorbar 
    ax4 = fig.add_subplot(gs1[1, 0])
    plt.colorbar(im,cax=ax4, orientation='horizontal',
                 ticks=np.arange(-10,0+1,1),
                 label='K')
    ax5 = fig.add_subplot(gs1[1, 1:])
    plt.colorbar(im2,cax=ax5, orientation='horizontal',
                 ticks=np.arange(-10,3+1,1),
                 label='K')

plot_fig2_sw(nlev)
plt.savefig(os.path.join(output_folder,"fig2_sw.png"),dpi=300,bbox_inches="tight")

plot_fig2_cld(nlev)
plt.savefig(os.path.join(output_folder,"fig2_cld.png"),dpi=300,bbox_inches="tight")

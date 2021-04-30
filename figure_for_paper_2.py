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
Scld=greb.from_binary(os.path.join(greb.greb_folder(),'S_sensitivity/cloud/Scld')).S
Ssw=greb.from_binary(os.path.join(greb.greb_folder(),'S_sensitivity/solar/Ssw')).S

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
    min,max,du = 0,0.08,0.02
    # S ANNUAL MEAN
    ax1 = fig.add_subplot(gs1[0, 0],projection=ccrs.Robinson())
    im=Ssw.annual_mean(30*12).plotvar(ax=ax1,
                                add_colorbar=False,
                                levels=np.linspace(min,max,nlev),
                                cmap=cm.viridis,
                                statistics='gmean',
                                title='$S_{SW}$')
    # S DJF MEAN
    ax2 = fig.add_subplot(gs1[0, 1],projection=ccrs.Robinson())
    im2=Ssw.isel(time=slice(-30*12,None)).group_by('season').sel(time='DJF').plotvar(ax=ax2,
                                add_colorbar=False,
                                levels=np.linspace(min,max,nlev),
                                cmap=cm.viridis,
                                statistics='gmean',
                                title='$S_{SW}$ DJF')
    # S JJA MEAN                                
    ax3 = fig.add_subplot(gs1[0, 2],projection=ccrs.Robinson())
    Ssw.isel(time=slice(-30*12,None)).group_by('season').sel(time='JJA').plotvar(ax=ax3,
                                add_colorbar=False,
                                levels=np.linspace(min,max,nlev),
                                cmap=cm.viridis,
                                statistics='gmean',
                                title='$S_{SW}$ JJA')
    # Colorbar 
    ax4 = fig.add_subplot(gs1[1, 0:])
    plt.colorbar(im,cax=ax4, orientation='horizontal',
                 ticks=np.arange(min,max+du,du),
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
    im=Scld.annual_mean(30*12).plotvar(ax=ax1,
                                add_colorbar=False,
                                levels=np.linspace(-10,0,nlev),
                                cmap=cm.viridis_r,
                                statistics='gmean',
                                title='$S_{CLD}$')
    # S DJF MEAN
    ax2 = fig.add_subplot(gs1[0, 1],projection=ccrs.Robinson())
    im2=Scld.isel(time=slice(-30*12,None)).group_by('season').sel(time='DJF').plotvar(ax=ax2,
                                add_colorbar=False,
                                levels=np.linspace(-10,3,nlev),
                                norm = colors.DivergingNorm(vmin=-10,vcenter=0,vmax=3),
                                cmap=cm.viridis_r,
                                statistics='gmean',
                                title='$S_{CLD}$ DJF')
    # S JJA MEAN                                
    ax3 = fig.add_subplot(gs1[0, 2],projection=ccrs.Robinson())
    Scld.isel(time=slice(-30*12,None)).group_by('season').sel(time='JJA').plotvar(ax=ax3,
                                add_colorbar=False,
                                levels=np.linspace(-10,3,nlev),
                                norm = colors.DivergingNorm(vmin=-10,vcenter=0,vmax=3),
                                cmap=cm.viridis_r,
                                statistics='gmean',
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

def plot_fig2_all(nlev=100):
    '''
    Sensitivity matrix
    '''
    fig = plt.figure(figsize=(16,7),constrained_layout=False)
    heights = [10,1]
    wspace=0.15; hspace=0.1; ncols=3; nrows=2
    gs1=fig.add_gridspec(ncols=ncols, nrows=nrows,
                         height_ratios=heights,
                         wspace=wspace, hspace=hspace,
                         top=0.95,bottom=0.55)
    gs2=fig.add_gridspec(ncols=ncols, nrows=nrows,
                         height_ratios=heights,
                         wspace=wspace, hspace=hspace,
                         top=0.45,bottom=0.05)    
    
    min,max,du = 0,0.08,0.02
    # Ssw ANNUAL MEAN
    ax1 = fig.add_subplot(gs1[0, 0],projection=ccrs.Robinson())
    im=Ssw.annual_mean().plotvar(ax=ax1,
                                add_colorbar=False,
                                levels=np.linspace(min,max,nlev),
                                cmap=cm.viridis,
                                statistics='gmean',
                                title='$S_{SW}$')
    
    # Ssw DJF MEAN
    ax2 = fig.add_subplot(gs1[0, 1],projection=ccrs.Robinson())
    im2=Ssw.group_by('season').sel(time='DJF').plotvar(ax=ax2,
                                add_colorbar=False,
                                levels=np.linspace(min,max,nlev),
                                cmap=cm.viridis,
                                statistics='gmean',
                                title='$S_{SW}$ DJF')

    # Ssw JJA MEAN                                
    ax3 = fig.add_subplot(gs1[0, 2],projection=ccrs.Robinson())
    Ssw.group_by('season').sel(time='JJA').plotvar(ax=ax3,
                                add_colorbar=False,
                                levels=np.linspace(min,max,nlev),
                                cmap=cm.viridis,
                                statistics='gmean',
                                title='$S_{SW}$ JJA')

    # Colorbar 
    ax4 = fig.add_subplot(gs1[1, :])
    plt.colorbar(im,cax=ax4, orientation='horizontal',
                 ticks=np.arange(min,max+du,du),
                 label='K/(W $m^{-2}$)')
    
    min,max,du = 0,0.08,0.02
    # Scld ANNUAL MEAN
    ax5 = fig.add_subplot(gs2[0, 0],projection=ccrs.Robinson())
    im3=Scld.annual_mean().plotvar(ax=ax5,
                                add_colorbar=False,
                                levels=np.linspace(-10,0,nlev),
                                cmap=cm.viridis_r,
                                statistics='gmean',
                                title='$S_{CLD}$')
    
    # Scld DJF MEAN
    ax6 = fig.add_subplot(gs2[0, 1],projection=ccrs.Robinson())
    im4=Scld.group_by('season').sel(time='DJF').plotvar(ax=ax6,
                                add_colorbar=False,
                                levels=np.linspace(-10,3,nlev),
                                norm = colors.DivergingNorm(vmin=-10,vcenter=0,vmax=3),
                                cmap=cm.viridis_r,
                                statistics='gmean',
                                title='$S_{CLD}$ DJF')

    # Scld JJA MEAN                                
    ax7 = fig.add_subplot(gs2[0, 2],projection=ccrs.Robinson())
    Scld.group_by('season').sel(time='JJA').plotvar(ax=ax7,
                                add_colorbar=False,
                                levels=np.linspace(-10,3,nlev),
                                norm = colors.DivergingNorm(vmin=-10,vcenter=0,vmax=3),
                                cmap=cm.viridis_r,
                                statistics='gmean',
                                title='$S_{CLD}$ JJA')

    # Colorbar 
    ax8 = fig.add_subplot(gs2[1, 0])
    plt.colorbar(im3,cax=ax8, orientation='horizontal',
                 ticks=np.arange(-10,0+1,1),
                 label='K')
    ax9 = fig.add_subplot(gs2[1, 1:])
    plt.colorbar(im4,cax=ax9, orientation='horizontal',
                 ticks=np.arange(-10,3+1,1),
                 label='K')                

plot_fig2_sw(nlev)
plt.savefig(os.path.join(output_folder,"fig2_sw.png"),dpi=300,bbox_inches="tight")

plot_fig2_cld(nlev)
plt.savefig(os.path.join(output_folder,"fig2_cld.png"),dpi=300,bbox_inches="tight")

plot_fig2_all(nlev)
plt.savefig(os.path.join(output_folder,"fig2_all.png"),dpi=300,bbox_inches="tight")

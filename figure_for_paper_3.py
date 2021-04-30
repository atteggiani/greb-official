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
from myfuncs import Colormaps as colormaps

output_folder = "/Users/dmar0022/university/phd/phd_project/Papers/Counteracting global warming by using a locally variable Solar Radiation Management/figs_for_paper"
matplotlib.rcParams.update({'font.size': 14})
nlev=200

# DATA
sw=greb.from_binary("/Users/dmar0022/university/phd/greb-official/artificial_solar_radiation/sw.artificial.iteration_0.34corr/sw.artificial.iter5_0.34corr.bin").solar
sw_ctl = greb.from_binary(greb.solar_def_file()).solar.isel(time=slice(-30*12,None))
cld=greb.from_binary("/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial.iteration_0.3corr/cld.artificial.iter16_0.3corr.bin").cloud
cld_ctl = greb.from_binary(greb.cloud_def_file()).cloud.isel(time=slice(-30*12,None))

def plot_fig3_sw(nlev=100):
    '''
    Aritificial SW matrix (best iteration)
    '''
    fig = plt.figure(figsize=(16,3),constrained_layout=False)
    heights = [10,1]
    wspace=0.15; hspace=0.15; ncols=3; nrows=2
    gs1=fig.add_gridspec(ncols=ncols, nrows=nrows,
                         height_ratios=heights,
                         wspace=wspace, hspace=hspace,
                         bottom=0, top=1)
    min,max,du = -12,0,1
    # SW ANNUAL MEAN
    ax1 = fig.add_subplot(gs1[0, 0],projection=ccrs.Robinson())
    im=sw.annual_mean(30*12).anomalies().plotvar(ax=ax1,
                                add_colorbar=False,
                                levels=np.linspace(min,max,nlev),
                                cmap=colormaps.seq_tsurf_hot_r,
                                title='Artificial SW Radiation')
    # SW DJF MEAN
    ax2 = fig.add_subplot(gs1[0, 1],projection=ccrs.Robinson())
    d1=sw.isel(time=slice(-30*12,None)).group_by('season').sel(time='DJF') - sw_ctl.group_by('season').sel(time='DJF')
    d1.plotvar(ax=ax2,
                    add_colorbar=False,
                    levels=np.linspace(min,max,nlev),
                    cmap=colormaps.seq_tsurf_hot_r,
                    title='Artificial SW Radiation DJF')
    # SW JJA MEAN                                
    ax3 = fig.add_subplot(gs1[0, 2],projection=ccrs.Robinson())
    d2=sw.isel(time=slice(-30*12,None)).group_by('season').sel(time='JJA') - sw_ctl.group_by('season').sel(time='JJA')
    d2.plotvar(ax=ax3,
                add_colorbar=False,
                levels=np.linspace(min,max,nlev),
                cmap=colormaps.seq_tsurf_hot_r,
                title='Artificial SW Radiation JJA')
    # Colorbar 
    ax4 = fig.add_subplot(gs1[1, :])
    plt.colorbar(im,cax=ax4, orientation='horizontal',
                 ticks=np.arange(min,max+du,du),
                 label='$W/m^{2}$')

def plot_fig3_cld(nlev=100):
    '''
    Aritificial CLD matrix (best iteration)
    '''
    fig = plt.figure(figsize=(16,3),constrained_layout=False)
    heights = [10,1]
    wspace=0.15; hspace=0.15; ncols=3; nrows=2
    gs1=fig.add_gridspec(ncols=ncols, nrows=nrows,
                         height_ratios=heights,
                         wspace=wspace, hspace=hspace,
                         bottom=0, top=1)
    # CLD ANNUAL MEAN
    ax1 = fig.add_subplot(gs1[0, 0],projection=ccrs.Robinson())
    im=cld.annual_mean(30*12).anomalies().plotvar(ax=ax1,
                                add_colorbar=False,
                                levels=np.linspace(0,0.3,nlev),
                                norm=colors.DivergingNorm(vmin=0,vcenter=0.08,vmax=0.3),
                                cmap=cm.binary,
                                title='Artificial Cloud Cover')
    # CLD DJF MEAN
    ax2 = fig.add_subplot(gs1[0, 1],projection=ccrs.Robinson())
    d1=cld.isel(time=slice(-30*12,None)).group_by('season').sel(time='DJF') - cld_ctl.group_by('season').sel(time='DJF')
    im2=d1.plotvar(ax=ax2,
                    add_colorbar=False,
                    levels=np.linspace(0,0.5,nlev),
                    norm=colors.DivergingNorm(vmin=0,vcenter=0.1,vmax=0.5),
                    cmap=cm.binary,
                    title='Artificial Cloud Cover DJF')
    # CLD JJA MEAN                                
    ax3 = fig.add_subplot(gs1[0, 2],projection=ccrs.Robinson())
    d2=cld.isel(time=slice(-30*12,None)).group_by('season').sel(time='JJA') - cld_ctl.group_by('season').sel(time='JJA')
    d2.plotvar(ax=ax3,
                add_colorbar=False,
                levels=np.linspace(0,0.5,nlev),
                norm=colors.DivergingNorm(vmin=0,vcenter=0.1,vmax=0.5),
                cmap=cm.binary,
                title='Artificial Cloud Cover JJA')
    # Colorbar 
    ax4 = fig.add_subplot(gs1[1, 0])
    plt.colorbar(im,cax=ax4, orientation='horizontal',
                 ticks=np.arange(0,0.3+0.05,0.05))
    ax5 = fig.add_subplot(gs1[1, 1:])
    plt.colorbar(im2,cax=ax5, orientation='horizontal',
                 ticks=np.arange(0,0.5+0.1,0.1))

def plot_fig3_all(nlev=100):
    fig1 = plt.figure(figsize=(16,7),constrained_layout=False)
    heights = [10,1]
    wspace=0.15; hspace=0.1; ncols=3; nrows=2
    gs1=fig1.add_gridspec(ncols=ncols, nrows=nrows,
                         height_ratios=heights,
                         wspace=wspace, hspace=hspace,
                         top=0.97,bottom=0.52,
                         left=0.1,right=0.95)
    gs2=fig1.add_gridspec(ncols=ncols, nrows=nrows,
                         height_ratios=heights,
                         wspace=wspace, hspace=hspace,
                         top=0.46,bottom=0.01,
                         left=0.1,right=0.95)
    gs3=fig1.add_gridspec(ncols=1, nrows=2,
                          hspace=hspace,
                         left=0.05,right=0.1)
    gs4=fig1.add_gridspec(ncols=ncols, nrows=1,
                         wspace=wspace,
                         top=0.99,bottom=0.95,
                         left=0.1,right=0.95)
    # PLOT TITLES
    f1_axt1 = fig1.add_subplot(gs4[0, 0])
    plt.text(0.5,0,"ANNUAL MEAN",
             horizontalalignment = "center",
             verticalalignment = "bottom",
             fontsize=16)
    plt.axis('off')             
    f1_axt2 = fig1.add_subplot(gs4[0, 1])
    plt.text(0.5,0,"DJF MEAN",
             horizontalalignment = "center",
             verticalalignment = "bottom",
             fontsize=16)
    plt.axis('off')             
    f1_axtt3 = fig1.add_subplot(gs4[0, 2])
    plt.text(0.5,0,"JJA MEAN",
             horizontalalignment = "center",
             verticalalignment = "bottom",
             fontsize=16)     
    plt.axis('off')                                     
    # VARIABLE TITLES  
    f1_ax1 = fig1.add_subplot(gs3[0, 0])
    plt.text(0.3,0.7,"ARITIFICIAL\nSW RADIATION",
             horizontalalignment = "center",
             verticalalignment = "center",
             rotation=90,
             fontsize=16)
    plt.axis('off')
    f1_ax1 = fig1.add_subplot(gs3[1, 0])             
    plt.text(0.3,0.42,"ARITIFICIAL\nCLOUD COVER",
             horizontalalignment = "center",
             verticalalignment = "center",
             rotation=90,
             fontsize=16)             
    plt.axis('off')
    
    min,max,du = -12,0,1
    # SW ANNUAL MEAN
    ax1 = fig1.add_subplot(gs1[0, 0],projection=ccrs.Robinson())
    im=sw.annual_mean(30*12).anomalies().plotvar(ax=ax1,
                                add_colorbar=False,
                                levels=np.linspace(min,max,nlev),
                                cmap=colormaps.seq_tsurf_hot_r,
                                title='')
    # SW DJF MEAN
    ax2 = fig1.add_subplot(gs1[0, 1],projection=ccrs.Robinson())
    d1=sw.isel(time=slice(-30*12,None)).group_by('season').sel(time='DJF') - sw_ctl.group_by('season').sel(time='DJF')
    d1.plotvar(ax=ax2,
                    add_colorbar=False,
                    levels=np.linspace(min,max,nlev),
                    cmap=colormaps.seq_tsurf_hot_r,
                    title='')
    # SW JJA MEAN                                
    ax3 = fig1.add_subplot(gs1[0, 2],projection=ccrs.Robinson())
    d2=sw.isel(time=slice(-30*12,None)).group_by('season').sel(time='JJA') - sw_ctl.group_by('season').sel(time='JJA')
    d2.plotvar(ax=ax3,
                add_colorbar=False,
                levels=np.linspace(min,max,nlev),
                cmap=colormaps.seq_tsurf_hot_r,
                title='')
    # Colorbar 
    ax4 = fig1.add_subplot(gs1[1, :])
    cb=plt.colorbar(im,cax=ax4, orientation='horizontal',
                 ticks=np.arange(min,max+du,du))
    cb.set_label('$W/m^{2}$',labelpad=-12,x=0.48)

    # CLD ANNUAL MEAN
    ax5 = fig1.add_subplot(gs2[0, 0],projection=ccrs.Robinson())
    im2=cld.annual_mean(30*12).anomalies().plotvar(ax=ax5,
                                add_colorbar=False,
                                levels=np.linspace(0,0.3,nlev),
                                norm=colors.DivergingNorm(vmin=0,vcenter=0.08,vmax=0.3),
                                cmap=cm.binary,
                                title='')
    # CLD DJF MEAN
    ax6 = fig1.add_subplot(gs2[0, 1],projection=ccrs.Robinson())
    d1=cld.isel(time=slice(-30*12,None)).group_by('season').sel(time='DJF') - cld_ctl.group_by('season').sel(time='DJF')
    im3=d1.plotvar(ax=ax6,
                    add_colorbar=False,
                    levels=np.linspace(0,0.5,nlev),
                    norm=colors.DivergingNorm(vmin=0,vcenter=0.1,vmax=0.5),
                    cmap=cm.binary,
                    title='')
    # CLD JJA MEAN                                
    ax7 = fig1.add_subplot(gs2[0, 2],projection=ccrs.Robinson())
    d2=cld.isel(time=slice(-30*12,None)).group_by('season').sel(time='JJA') - cld_ctl.group_by('season').sel(time='JJA')
    d2.plotvar(ax=ax7,
                add_colorbar=False,
                levels=np.linspace(0,0.5,nlev),
                norm=colors.DivergingNorm(vmin=0,vcenter=0.1,vmax=0.5),
                cmap=cm.binary,
                title='')
    # Colorbar 
    ax8 = fig1.add_subplot(gs2[1, 0])
    plt.colorbar(im2,cax=ax8, orientation='horizontal',
                 ticks=np.arange(0,0.3+0.05,0.05))
    ax9 = fig1.add_subplot(gs2[1, 1:])
    plt.colorbar(im3,cax=ax9, orientation='horizontal',
                 ticks=np.arange(0,0.5+0.1,0.1))

plot_fig3_sw(nlev)
plt.savefig(os.path.join(output_folder,"fig3_sw.png"),dpi=300,bbox_inches="tight")

plot_fig3_cld(nlev)
plt.savefig(os.path.join(output_folder,"fig3_cld.png"),dpi=300,bbox_inches="tight")

plot_fig3_all(nlev)
plt.savefig(os.path.join(output_folder,"fig3_all.png"),dpi=300,bbox_inches="tight")

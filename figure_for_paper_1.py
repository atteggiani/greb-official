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
# control=greb.from_binary(greb.control_def_file())[['tsurf','precip']]
co2x2=greb.from_binary(os.path.join(greb.scenario_2xCO2()))[['tsurf','precip']]
srm_sw=greb.from_binary(os.path.join(greb.output_folder(),'scenario.exp-931.geoeng.2xCO2.sw.artificial.iter5_0.34corr_50yrs'))[['tsurf','precip']]
srm_cld=greb.from_binary(os.path.join(greb.output_folder(),'scenario.exp-930.geoeng.2xCO2.cld.artificial.iter16_0.3corr_50yrs'))[['tsurf','precip']]
homogeneous_sw=greb.from_binary("/Users/dmar0022/university/phd/greb-official/output/scenario.exp-931.geoeng.2xCO2.sw.artificial.frominput_x0.97954535_homogeneous_50yrs.bin")[['tsurf','precip']]
homogeneous_cld=greb.from_binary("/Users/dmar0022/university/phd/greb-official/output/scenario.exp-930.geoeng.2xCO2.cld.artificial.frominput_x1.093056_homogeneous_50yrs.bin")[['tsurf','precip']]

# SW
def plot_fig1_amean_sw(nlev=100):
    '''
    Annual Means for tsurf and precip.
    exp: 2xco2, homogeneous, srm
    '''
    fun=lambda x: x.annual_mean(30*12)
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
    plt.text(0.5,0,"2xCO2",
             horizontalalignment = "center",
             verticalalignment = "bottom",
             fontsize=16)
    plt.axis('off')             
    f1_axt2 = fig1.add_subplot(gs4[0, 1])
    plt.text(0.5,0,"Homogeneous SRM$_{SW}$",
             horizontalalignment = "center",
             verticalalignment = "bottom",
             fontsize=16)
    plt.axis('off')             
    f1_axtt3 = fig1.add_subplot(gs4[0, 2])
    plt.text(0.5,0,"Localized SRM$_{SW}$",
             horizontalalignment = "center",
             verticalalignment = "bottom",
             fontsize=16)     
    plt.axis('off')                                     
    # VARIABLE TITLES  
    f1_ax1 = fig1.add_subplot(gs3[0, 0])
    plt.text(0.3,0.7,"SURFACE\nTEMPERATURE",
             horizontalalignment = "center",
             verticalalignment = "center",
             rotation=90,
             fontsize=16)
    plt.axis('off')
    f1_ax1 = fig1.add_subplot(gs3[1, 0])             
    plt.text(0.3,0.42,"PRECIPITATION",
             horizontalalignment = "center",
             verticalalignment = "center",
             rotation=90,
             fontsize=16)             
    plt.axis('off')               
    # TSURF  
    f1_ax1 = fig1.add_subplot(gs1[0, 0],projection=ccrs.Robinson())
    im=fun(co2x2.tsurf).anomalies().plotvar(ax=f1_ax1,
                                   levels=np.linspace(1,5,nlev),
                                   cmap=my.Colormaps.seq_tsurf_hot,
                                   add_colorbar=False,
                                   title='')
    f1_ax2 = fig1.add_subplot(gs1[0, 1],projection=ccrs.Robinson())
    im2=fun(homogeneous_sw.tsurf).anomalies().plotvar(ax=f1_ax2,
                                   levels=np.linspace(-1,1,nlev),
                                   add_colorbar=False,
                                   title='')
    f1_ax3 = fig1.add_subplot(gs1[0, 2],projection=ccrs.Robinson())
    im3=fun(srm_sw.tsurf).anomalies().plotvar(ax=f1_ax3,
                                   levels=np.linspace(-1,1,nlev),
                                   add_colorbar=False,
                                   title='')
    # Tsurf Colorbars
    f1_ax4 = fig1.add_subplot(gs1[1, 0])
    plt.colorbar(im,cax=f1_ax4, orientation='horizontal',label='K',
                 ticks=np.arange(1,5+0.5,0.5))
    f1_ax5 = fig1.add_subplot(gs1[1, 1:])
    plt.colorbar(im2,cax=f1_ax5, orientation='horizontal',label='K',
                 ticks=np.arange(-1,1+0.25,0.25))
    # PRECIP
    f1_ax7 = fig1.add_subplot(gs2[0, 0],projection=ccrs.Robinson())
    im=fun(co2x2.precip).anomalies().plotvar(ax=f1_ax7,
                                   levels=np.linspace(0,1.5,nlev),
                                   cmap=my.Colormaps.seq_precip_wet,
                                   add_colorbar=False,
                                   title='')
    f1_ax8 = fig1.add_subplot(gs2[0, 1],projection=ccrs.Robinson())
    im2=fun(homogeneous_sw.precip).anomalies().plotvar(ax=f1_ax8,
                                   levels=np.linspace(-0.5,0.5,nlev),
                                   add_colorbar=False,
                                   title='')
    f1_ax9 = fig1.add_subplot(gs2[0, 2],projection=ccrs.Robinson())
    im3=fun(srm_sw.precip).anomalies().plotvar(ax=f1_ax9,
                                   levels=np.linspace(-0.5,0.5,nlev),
                                   add_colorbar=False,
                                   title='')
    # Precip Colorbars
    f1_ax10 = fig1.add_subplot(gs2[1, 0])
    plt.colorbar(im,cax=f1_ax10, orientation='horizontal',label='mm/day',
                 ticks=np.arange(0,1.5+0.25,0.25))
    f1_ax11 = fig1.add_subplot(gs2[1, 1:])
    plt.colorbar(im2,cax=f1_ax11, orientation='horizontal',label='mm/day',
                 ticks=np.arange(-0.5,0.5+0.1,0.1))

def plot_fig1_seascyc_sw(nlev=100):
    '''
    Annual Means for tsurf and precip.
    exp: 2xco2, homogeneous, srm
    '''
    fun=lambda x: x.seasonal_cycle(30*12)
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
    plt.text(0.5,0,"2xCO2",
             horizontalalignment = "center",
             verticalalignment = "bottom",
             fontsize=16)
    plt.axis('off')             
    f1_axt2 = fig1.add_subplot(gs4[0, 1])
    plt.text(0.5,0,"Homogeneous SRM$_{SW}$",
             horizontalalignment = "center",
             verticalalignment = "bottom",
             fontsize=16)
    plt.axis('off')             
    f1_axtt3 = fig1.add_subplot(gs4[0, 2])
    plt.text(0.5,0,"Localized SRM$_{SW}$",
             horizontalalignment = "center",
             verticalalignment = "bottom",
             fontsize=16)     
    plt.axis('off')                                     
    # VARIABLE TITLES  
    f1_ax1 = fig1.add_subplot(gs3[0, 0])
    plt.text(0.3,0.7,"SURFACE\nTEMPERATURE",
             horizontalalignment = "center",
             verticalalignment = "center",
             rotation=90,
             fontsize=16)
    plt.axis('off')
    f1_ax1 = fig1.add_subplot(gs3[1, 0])             
    plt.text(0.3,0.42,"PRECIPITATION",
             horizontalalignment = "center",
             verticalalignment = "center",
             rotation=90,
             fontsize=16)             
    plt.axis('off')   
    # TSURF  
    f1_ax1 = fig1.add_subplot(gs1[0, 0],projection=ccrs.Robinson())
    im=fun(co2x2.tsurf).anomalies().plotvar(ax=f1_ax1,
                                   levels=np.linspace(-1,1,nlev),
                                   add_colorbar=False,
                                   title='',
                                   statistics="rms")
    f1_ax2 = fig1.add_subplot(gs1[0, 1],projection=ccrs.Robinson())
    im2=fun(homogeneous_sw.tsurf).anomalies().plotvar(ax=f1_ax2,
                                   levels=np.linspace(-1,1,nlev),
                                   add_colorbar=False,
                                   title='',
                                   statistics="rms")
    f1_ax3 = fig1.add_subplot(gs1[0, 2],projection=ccrs.Robinson())
    im3=fun(srm_sw.tsurf).anomalies().plotvar(ax=f1_ax3,
                                   levels=np.linspace(-1,1,nlev),
                                   add_colorbar=False,
                                   title='',
                                   statistics="rms")
    # Tsurf Colorbars
    f1_ax4 = fig1.add_subplot(gs1[1, 0:])
    plt.colorbar(im,cax=f1_ax4, orientation='horizontal',label='K',
                 ticks=np.arange(-1,1+0.25,0.25))

    # PRECIP
    f1_ax7 = fig1.add_subplot(gs2[0, 0],projection=ccrs.Robinson())
    im=fun(co2x2.precip).anomalies().plotvar(ax=f1_ax7,
                                   levels=np.linspace(-0.5,0.5,nlev),
                                   add_colorbar=False,
                                   title='',
                                   statistics="rms")
    f1_ax8 = fig1.add_subplot(gs2[0, 1],projection=ccrs.Robinson())
    im2=fun(homogeneous_sw.precip).anomalies().plotvar(ax=f1_ax8,
                                   levels=np.linspace(-0.5,0.5,nlev),
                                   add_colorbar=False,
                                   title='',
                                   statistics="rms")
    f1_ax9 = fig1.add_subplot(gs2[0, 2],projection=ccrs.Robinson())
    im3=fun(srm_sw.precip).anomalies().plotvar(ax=f1_ax9,
                                   levels=np.linspace(-0.5,0.5,nlev),
                                   add_colorbar=False,
                                   title='',
                                   statistics="rms")
    # Precip Colorbars
    f1_ax10 = fig1.add_subplot(gs2[1, 0:])
    plt.colorbar(im,cax=f1_ax10, orientation='horizontal',label='mm/day',
                 ticks=np.arange(-0.5,0.5+0.1,0.1))

# CLD
def plot_fig1_amean_cld(nlev=100):
    '''
    Annual Means for tsurf and precip.
    exp: 2xco2, homogeneous, srm
    '''
    fun=lambda x: x.annual_mean(30*12)
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
    plt.text(0.5,0,"2xCO2",
             horizontalalignment = "center",
             verticalalignment = "bottom",
             fontsize=16)
    plt.axis('off')             
    f1_axt2 = fig1.add_subplot(gs4[0, 1])
    plt.text(0.5,0,"Homogeneous SRM$_{CLD}$",
             horizontalalignment = "center",
             verticalalignment = "bottom",
             fontsize=16)
    plt.axis('off')             
    f1_axtt3 = fig1.add_subplot(gs4[0, 2])
    plt.text(0.5,0,"Localized SRM$_{CLD}$",
             horizontalalignment = "center",
             verticalalignment = "bottom",
             fontsize=16)     
    plt.axis('off')                                     
    # VARIABLE TITLES  
    f1_ax1 = fig1.add_subplot(gs3[0, 0])
    plt.text(0.3,0.7,"SURFACE\nTEMPERATURE",
             horizontalalignment = "center",
             verticalalignment = "center",
             rotation=90,
             fontsize=16)
    plt.axis('off')
    f1_ax1 = fig1.add_subplot(gs3[1, 0])             
    plt.text(0.3,0.42,"PRECIPITATION",
             horizontalalignment = "center",
             verticalalignment = "center",
             rotation=90,
             fontsize=16)             
    plt.axis('off')   
    # TSURF  
    f1_ax1 = fig1.add_subplot(gs1[0, 0],projection=ccrs.Robinson())
    im=fun(co2x2.tsurf).anomalies().plotvar(ax=f1_ax1,
                                   levels=np.linspace(1,5,nlev),
                                   cmap=my.Colormaps.seq_tsurf_hot,
                                   add_colorbar=False,
                                   title='')
    f1_ax2 = fig1.add_subplot(gs1[0, 1],projection=ccrs.Robinson())
    im2=fun(homogeneous_cld.tsurf).anomalies().plotvar(ax=f1_ax2,
                                   levels=np.linspace(-1,1,nlev),
                                   add_colorbar=False,
                                   title='')
    f1_ax3 = fig1.add_subplot(gs1[0, 2],projection=ccrs.Robinson())
    im3=fun(srm_cld.tsurf).anomalies().plotvar(ax=f1_ax3,
                                   levels=np.linspace(-1,1,nlev),
                                   add_colorbar=False,
                                   title='')
    # Tsurf Colorbars
    f1_ax4 = fig1.add_subplot(gs1[1, 0])
    plt.colorbar(im,cax=f1_ax4, orientation='horizontal',label='K',
                 ticks=np.arange(1,5+0.5,0.5))
    f1_ax5 = fig1.add_subplot(gs1[1, 1:])
    plt.colorbar(im2,cax=f1_ax5, orientation='horizontal',label='K',
                 ticks=np.arange(-1,1+0.25,0.25))
    # PRECIP
    f1_ax7 = fig1.add_subplot(gs2[0, 0],projection=ccrs.Robinson())
    im=fun(co2x2.precip).anomalies().plotvar(ax=f1_ax7,
                                   levels=np.linspace(0,1.5,nlev),
                                   cmap=my.Colormaps.seq_precip_wet,
                                   add_colorbar=False,
                                   title='')
    f1_ax8 = fig1.add_subplot(gs2[0, 1],projection=ccrs.Robinson())
    im2=fun(homogeneous_cld.precip).anomalies().plotvar(ax=f1_ax8,
                                   levels=np.linspace(-0.5,0.5,nlev),
                                   add_colorbar=False,
                                   title='')
    f1_ax9 = fig1.add_subplot(gs2[0, 2],projection=ccrs.Robinson())
    im3=fun(srm_cld.precip).anomalies().plotvar(ax=f1_ax9,
                                   levels=np.linspace(-0.5,0.5,nlev),
                                   add_colorbar=False,
                                   title='')
    # Precip Colorbars
    f1_ax10 = fig1.add_subplot(gs2[1, 0])
    plt.colorbar(im,cax=f1_ax10, orientation='horizontal',label='mm/day',
                 ticks=np.arange(0,1.5+0.25,0.25))
    f1_ax11 = fig1.add_subplot(gs2[1, 1:])
    plt.colorbar(im2,cax=f1_ax11, orientation='horizontal',label='mm/day',
                 ticks=np.arange(-0.5,0.5+0.1,0.1))

def plot_fig1_seascyc_cld(nlev=100):
    '''
    Annual Means for tsurf and precip.
    exp: 2xco2, homogeneous, srm
    '''
    fun=lambda x: x.seasonal_cycle(30*12)
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
    plt.text(0.5,0,"2xCO2",
             horizontalalignment = "center",
             verticalalignment = "bottom",
             fontsize=16)
    plt.axis('off')             
    f1_axt2 = fig1.add_subplot(gs4[0, 1])
    plt.text(0.5,0,"Homogeneous SRM$_{CLD}$",
             horizontalalignment = "center",
             verticalalignment = "bottom",
             fontsize=16)
    plt.axis('off')             
    f1_axtt3 = fig1.add_subplot(gs4[0, 2])
    plt.text(0.5,0,"Localized SRM$_{CLD}$",
             horizontalalignment = "center",
             verticalalignment = "bottom",
             fontsize=16)     
    plt.axis('off')                                     
    # VARIABLE TITLES  
    f1_ax1 = fig1.add_subplot(gs3[0, 0])
    plt.text(0.3,0.7,"SURFACE\nTEMPERATURE",
             horizontalalignment = "center",
             verticalalignment = "center",
             rotation=90,
             fontsize=16)
    plt.axis('off')
    f1_ax1 = fig1.add_subplot(gs3[1, 0])             
    plt.text(0.3,0.42,"PRECIPITATION",
             horizontalalignment = "center",
             verticalalignment = "center",
             rotation=90,
             fontsize=16)             
    plt.axis('off')   
    # TSURF  
    f1_ax1 = fig1.add_subplot(gs1[0, 0],projection=ccrs.Robinson())
    im=fun(co2x2.tsurf).anomalies().plotvar(ax=f1_ax1,
                                   levels=np.linspace(-1,1,nlev),
                                   add_colorbar=False,
                                   title='',
                                   statistics="rms")
    f1_ax2 = fig1.add_subplot(gs1[0, 1],projection=ccrs.Robinson())
    im2=fun(homogeneous_cld.tsurf).anomalies().plotvar(ax=f1_ax2,
                                   levels=np.linspace(-1,1,nlev),
                                   add_colorbar=False,
                                   title='',
                                   statistics="rms")
    f1_ax3 = fig1.add_subplot(gs1[0, 2],projection=ccrs.Robinson())
    im3=fun(srm_cld.tsurf).anomalies().plotvar(ax=f1_ax3,
                                   levels=np.linspace(-1,1,nlev),
                                   add_colorbar=False,
                                   title='',
                                   statistics="rms")
    # Tsurf Colorbars
    f1_ax4 = fig1.add_subplot(gs1[1, 0:])
    plt.colorbar(im,cax=f1_ax4, orientation='horizontal',label='K',
                 ticks=np.arange(-1,1+0.25,0.25))

    # PRECIP
    f1_ax7 = fig1.add_subplot(gs2[0, 0],projection=ccrs.Robinson())
    im=fun(co2x2.precip).anomalies().plotvar(ax=f1_ax7,
                                   levels=np.linspace(-0.5,0.5,nlev),
                                   add_colorbar=False,
                                   title='',
                                   statistics="rms")
    f1_ax8 = fig1.add_subplot(gs2[0, 1],projection=ccrs.Robinson())
    im2=fun(homogeneous_cld.precip).anomalies().plotvar(ax=f1_ax8,
                                   levels=np.linspace(-0.5,0.5,nlev),
                                   add_colorbar=False,
                                   title='',
                                   statistics="rms")
    f1_ax9 = fig1.add_subplot(gs2[0, 2],projection=ccrs.Robinson())
    im3=fun(srm_cld.precip).anomalies().plotvar(ax=f1_ax9,
                                   levels=np.linspace(-0.5,0.5,nlev),
                                   add_colorbar=False,
                                   title='',
                                   statistics="rms")
    # Precip Colorbars
    f1_ax10 = fig1.add_subplot(gs2[1, 0:])
    plt.colorbar(im,cax=f1_ax10, orientation='horizontal',label='mm/day',
                 ticks=np.arange(-0.5,0.5+0.1,0.1))

# PLOTS
plot_fig1_amean_sw(nlev)
plt.savefig(os.path.join(output_folder,"fig1_amean_sw.png"),dpi=300,bbox_inches="tight")

plot_fig1_seascyc_sw(nlev)
plt.savefig(os.path.join(output_folder,"fig1_seascyc_sw.png"),dpi=300,bbox_inches="tight")

plot_fig1_amean_cld(nlev)
plt.savefig(os.path.join(output_folder,"fig1_amean_cld.png"),dpi=300,bbox_inches="tight")

plot_fig1_seascyc_cld(nlev)
plt.savefig(os.path.join(output_folder,"fig1_seascyc_cld.png"),dpi=300,bbox_inches="tight")
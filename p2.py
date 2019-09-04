# LIBRARIES
 import xarray as xr
 # import sys
 # import warnings
 # import os
 # import numpy as np
 # import iris

 # import iris.coord_categorisation
 # import matplotlib.patches as mpatches
 # import matplotlib.pyplot as plt
 # import matplotlib.cm as cm
 # import iris.quickplot as qplt
 # import iris.plot as iplt
 # import cartopy.crs as ccrs
 # import cartopy.feature as cfeature
 # from datetime import datetime as dtime
 # import matplotlib.dates as mdates
 # from scipy import interpolate
 # import matplotlib.gridspec as gridspec

 def plot_clouds_and_tsurf(*cloudfiles, years=50, coords = None, labels = None):
     import matplotlib.ticker as ticker
     def get_tsurf(*fnames):
         mdays=np.array([31,28,31,30,31,30,31,31,30,31,30,31])
         tsurf = []
         for f in fnames:
             t=data_from_binary(f,'monthly')['tsurf']
             t=np.repeat(t,mdays*2,axis=0)
             s=t.shape
             t_=np.zeros(s)
             for i in np.arange(s[1]):
                 for j in np.arange(s[2]):
                     t_[:,i,j]=spline_interp(t[:,i,j])
             tsurf.append(t_)
         return tsurf

     cloud = [data_from_binary(f)['cloud'] for f in cloudfiles]
     cloud_ctr = data_from_binary(constants.cloud_def_file())['cloud']
     tfiles = [get_scenario_filename(f,years=years) for f in cloudfiles]
     tsurf = get_tsurf(*tfiles)
     tsurf_ctr = get_tsurf(constants.control_def_file())

     cloud_anomaly = [c-cloud_ctr for c in cloud]
     tsurf_anomaly = [(t-tsurf_ctr).squeeze() for t in tsurf]
     if coords is None:
         coords = [(42,12.5),(-37.8,145),(-80,0),(80,0),(0,230)]
     gs = gridspec.GridSpec(2, 2, wspace=0.25, hspace=0.4)

     for coord in coords:
         plt.figure()

         ax1 = plt.subplot(gs[0, 0])
         plot_annual_cycle(coord,*cloud_anomaly)
         ax1.set_ylim([-1,1])
         ax1.set_title('cloud anomaly annual cycle',fontsize=10)
         l=ax1.get_legend()
         if labels is not None:
             for a,label in zip(l.get_texts(),labels): a.set_text(label)
         l.set_bbox_to_anchor([-0.18,1.2])
         for tick in ax1.xaxis.get_major_ticks(): tick.label.set_fontsize(6.5)

         ax2 = plt.subplot(gs[0,1])
         plot_annual_cycle(coord,*tsurf_anomaly)
         ax2.set_ylim([-5,5])
         ax2.set_title('tsurf anomaly annual cycle',fontsize=10)
         ax2.get_legend().remove()
         for tick in ax2.xaxis.get_major_ticks(): tick.label.set_fontsize(6.5)
         ax2.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))

         ax3 = plt.subplot(gs[1, 0])
         plot_annual_cycle(coord,*cloud)
         ax3.set_ylim([0,1])
         ax3.set_title('cloud annual cycle',fontsize=10)
         ax3.get_legend().remove()
         for tick in ax3.xaxis.get_major_ticks(): tick.label.set_fontsize(6.5)

         ax4 = plt.subplot(gs[1,1])
         plot_annual_cycle(coord,*tsurf)
         ax4.set_ylim([223,323])
         ax4.set_title('tsurf annual cycle',fontsize=10)
         ax4.get_legend().remove()
         for tick in ax4.xaxis.get_major_ticks(): tick.label.set_fontsize(6.5)
         ax4.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.0f'))

         axP = plt.gcf().axes[1]
         axP.set_position([0.265, 0.95, 0.5, 0.15])





 def plot_clouds(filename,filename_base = None,outpath=None):
     from random import randint
     from datetime import timedelta

     fl=False
     if filename_base is not None:
         fl=True
         data_base=cube_from_binary(filename_base)
         name_base=os.path.split(rmext(filename_base))[1]

     data=cube_from_binary(filename)
     name=os.path.split(rmext(filename))[1]
     if outpath is not None:
         outpath=os.path.join(outpath,name)
         os.makedirs(outpath,exist_ok=True)
         if fl:
             outpath_diff=os.path.join(outpath,name,'diff_'+name_base)
             os.makedirs(outpath_diff,exist_ok=True)
     else:
         outpath_diff = None

     # Plot annual data
     plt.figure()
     plot_param.from_cube(data).to_annual_mean().assign_var().plot(outpath = outpath,
                             coast_param = {'edgecolor':[0,.5,0.3]},statistics=True)
     if fl:
         plt.figure()
         plot_param.from_cube(data).to_annual_mean().to_anomalies(data_base).assign_var().plot(outpath = outpath_diff,
                                 coast_param = {'edgecolor':[0,.5,0.3]},statistics=True)

     # Plot seasonal cycle datad
     plt.figure()
     plot_param.from_cube(data).to_seasonal_cycle().assign_var().plot(outpath = outpath,
                             coast_param = {'edgecolor':[0,.5,0.3]},statistics=True)
     if fl:
         plt.figure()
         plot_param.from_cube(data).to_seasonal_cycle().to_anomalies(data_base).assign_var().plot(outpath = outpath_diff,
                                 coast_param = {'edgecolor':[0,.5,0.3]},statistics=True)
     # Plot time data over 3 points (to check seasonality and general diagnostic)
     P = [(42,12.5),(-37.8,145),(-80,0),(0,230)]
     for p in P:
         plt.figure()
         if fl:
             plot_annual_cycle(p,data,data_base,title = 'Cloud annual cycle',name = 'cloud')
         else:
             plot_annual_cycle(p,data,title = 'Cloud annual cycle',name = 'cloud')

     os.remove(filename+'.nc')
     if filename_base is not None: os.remove(filename_base+'.nc')

 class plot_param:

     def __init__(self, cube = None, units = None, cmap = None, cmaplev = None,
                  cbticks = None, cbextmode = None, defname = None,
                  varname = None, tit = None, flags = None):

         self.cube = cube
         self.cmap = cmap
         self.cmaplev = cmaplev
         self.cbticks = cbticks
         self.cbextmode = cbextmode
         self.units = units
         self.defname = defname
         self.varname = varname
         self.tit = tit
         self.flags = flags if (flags is None or isinstance(flags,list)) else [flags]

     def plot(self, outpath = None, ax = None, projection = ccrs.Robinson(),
              coast_param = {},
              land_param = {'edgecolor':'face', 'facecolor':'black'},
              title_param = {'fontsize':12},
              colorbar_param = {},
              save_param = {'dpi':300, 'bbox_inches':'tight'},
              statistics=True):
         # plt.figure(figsize=(12, 8))
         plt.axes(projection=projection) if ax is None else plt.axes(ax)
         try:
             iplt.contourf(self.get_cube(), levels = self.get_cmaplev(), cmap = self.get_cmap(),
                           extend=self.get_cbextmode())
         except:
             print('{} could not be plotted due to a contour plot error\n'.format(self.get_varname()))
             return
         plt.gca().add_feature(cfeature.COASTLINE,**coast_param)
         if self.get_defname() == 'tocean':
             plt.gca().add_feature(cfeature.NaturalEarthFeature('physical',
                                                   'land', '110m', **land_param))
         plt.colorbar(orientation='horizontal', extend=self.get_cbextmode(),
                      label=self.get_units(), ticks=self.get_cbticks(),**colorbar_param)
         plt.title(self.get_tit(),**title_param)
         if statistics:
             txt = ('gmean = {:.3f}'+'\n'+'rms = {:.3f}').format(self.gmean(),self.rms())
             # txt = ('gmean = {:.3f}'+'\n'+\
             #       'std = {:.3f}'+'\n'+\
             #       'rms = {:.3f}').format(self.gmean(),self.std(),self.rms())
             plt.text(1.05,1,txt,verticalalignment='top',horizontalalignment='right',
                      transform=plt.gca().transAxes,fontsize=6)
         if outpath is not None:
             plt.savefig(os.path.join(outpath,'.'.join([self.get_varname(),
                         self.get_ext()])),  format = self.get_ext(),**save_param)

     def gmean(self):
         return (global_mean(self.get_cube())).data

     def rms(self):
         return np.sqrt((global_mean(self.get_cube()**2)).data)


 # ====================================================================
 # ====================================================================
 # ====================================================================
     def tatmos(self):
         flags = self.get_flags()
         self.set_varname('tatmos')
         self.set_units('[K]')
         self.set_tit('Atmospheric Temperature')
         self.set_cmap(cm.RdBu_r)
         if 'anom' in flags:
             if 'amean' in flags:
                 self.set_cmaplev(np.arange(-2,2+0.2,0.2))
                 self.set_cbticks(np.arange(-2,2+0.4,0.4))
             elif 'seascyc' in flags:
                 self.set_cmaplev(np.arange(-2,2+0.2,0.2))
                 self.set_cbticks(np.arange(-2,2+0.4,0.4))
         else:
             if 'amean' in flags:
                 self.set_cmaplev(np.arange(223,323+5,5))
                 self.set_cbticks(np.arange(223,323+10,10))
             elif 'seascyc' in flags:
                 self.set_cmaplev(np.arange(-20,20+2,2))
                 self.set_cbticks(np.arange(-20,20+4,4))
         return self

     def tsurf(self):
         flags = self.get_flags()
         self.set_varname('tsurf')
         self.set_units('[K]')
         self.set_tit('Surface Temperature')
         self.set_cmap(cm.RdBu_r)
         if 'anom' in flags:
             if 'amean' in flags:
                 self.set_cmaplev(np.arange(-2,2+0.2,0.2))
                 self.set_cbticks(np.arange(-2,2+0.4,0.4))
             elif 'seascyc' in flags:
                 self.set_cmaplev(np.arange(-2,2+0.2,0.2))
                 self.set_cbticks(np.arange(-2,2+0.4,0.4))
         else:
             if 'amean' in flags:
                 self.set_cmaplev(np.arange(223,323+5,5))
                 self.set_cbticks(np.arange(223,323+10,10))
             elif 'seascyc' in flags:
                 self.set_cmaplev(np.arange(-20,20+2,2))
                 self.set_cbticks(np.arange(-20,20+4,4))
         return self

     def tocean(self):
         flags = self.get_flags()
         self.set_varname('tocean')
         self.set_units('[K]')
         self.set_tit('Ocean Temperature')
         self.set_cmap(cm.RdBu_r)
         if 'anom' in flags:
             if 'amean' in flags:
                 self.set_cmaplev(np.arange(-1,1+0.1,0.1))
                 self.set_cbticks(np.arange(-1,1+0.2,0.2))
             elif 'seascyc' in flags:
                 self.set_cmaplev(np.arange(-1,1+0.1,0.1))
                 self.set_cbticks(np.arange(-1,1+0.2,0.2))
         else:
             if 'amean' in flags:
                 self.set_cmaplev(np.arange(273,303+5,3))
                 self.set_cbticks(np.arange(273,303+10,3))
             elif 'seascyc' in flags:
                 self.set_cmaplev(np.arange(-1,1+1e-1,1e-1))
                 self.set_cbticks(np.arange(-1,1+2e-1,2e-1))
         return self

     def precip(self):
         flags = self.get_flags()
         self.set_varname('precip')
         self.set_units('[mm][day-1]')
         self.set_tit('Precipitation')
         self.set_cmap(cm.GnBu)
         if 'anom' in flags:
             if 'amean' in flags:
                 self.set_cmaplev(np.arange(-1,1+0.1,0.1))
                 self.set_cbticks(np.arange(-1,1+0.2,0.2))
             elif 'seascyc' in flags:
                 self.set_cmaplev(np.arange(-1,1+0.1,0.1))
                 self.set_cbticks(np.arange(-1,1+0.2,0.2))
         else:
             if 'amean' in flags:
                 self.set_cmaplev(np.arange(0,9+1,1))
                 self.set_cbticks(np.arange(0,9+1,1))
                 self.set_cbextmode('max')
             elif 'seascyc' in flags:
                 self.set_cmaplev(np.arange(-6,6+1,1))
                 self.set_cmaplev(np.arange(-6,6+1,1))
         return self

     def eva(self):
         flags = self.get_flags()
         self.set_units('[mm][day-1]')
         self.set_varname('eva')
         self.set_tit('Evaporation')
         self.set_cmap(cm.GnBu)
         if 'anom' in flags:
             if 'amean' in flags:
                 self.set_cmaplev(np.arange(-1,1+0.1,0.1))
                 self.set_cbticks(np.arange(-1,1+0.2,0.2))
             elif 'seascyc' in flags:
                 self.set_cmaplev(np.arange(-1,1+0.1,0.1))
                 self.set_cbticks(np.arange(-1,1+0.2,0.2))
         else:
             if 'amean' in flags:
                 self.set_cmap(cm.Blues)
                 self.set_cmaplev(np.arange(0,10+1,1))
                 self.set_cbticks(np.arange(0,10+1,1))
             elif 'seascyc' in flags:
                 self.set_cmaplev(np.arange(-3,3+0.5,0.5))
                 self.set_cbticks(np.arange(-3,3+0.5,0.5))
         return self

     def qcrcl(self):
         flags = self.get_flags()
         self.set_units('[mm][day-1]')
         self.set_varname('qcrcl')
         self.set_tit('Circulation')
         self.set_cmap(cm.RdBu_r)
         if 'anom' in flags:
             if 'amean' in flags:
                 self.set_cmaplev(np.arange(-1,1+0.1,0.1))
                 self.set_cbticks(np.arange(-1,1+0.2,0.2))
             elif 'seascyc' in flags:
                 self.set_cmaplev(np.arange(-1,1+0.1,0.1))
                 self.set_cbticks(np.arange(-1,1+0.2,0.2))
         else:
             if 'amean' in flags:
                 self.set_cmaplev(np.arange(-8,8+1))
                 self.set_cbticks(np.arange(-8,8+2,2))
             elif 'seascyc' in flags:
                 self.set_cmaplev(np.arange(-6,6+1,1))
                 self.set_cmaplev(np.arange(-6,6+1,1))
         return self

     def vapor(self):
         flags = self.get_flags()
         self.set_units(' ') # ADD UNITS!
         self.set_varname('vapor')
         self.set_tit('Specific Humidity')
         self.set_cmap(cm.RdBu_r)
         if 'anom' in flags:
             if 'amean' in flags:
                 self.set_cmaplev(np.arange(-5e-3,5e-3+5e-4,5e-4))
                 self.set_cbticks(np.arange(-5e-3,5e-3+1e-3,1e-3))
             elif 'seascyc' in flags:
                 self.set_cmaplev(np.arange(-5e-3,5e-3+5e-4,5e-4))
                 self.set_cbticks(np.arange(-5e-3,5e-3+1e-3,1e-3))
         else:
             if 'amean' in flags:
                 self.set_cmap(cm.Blues)
                 self.set_cmaplev(np.arange(0,0.02+0.002,0.002))
                 self.set_cbticks(np.arange(0,0.02+0.002,0.002))
             elif 'seascyc' in flags:
                 self.set_cmaplev(np.arange(-0.01,0.01+0.001,0.001))
                 self.set_cbticks(np.arange(-0.01,0.01+0.002,0.002))
         return self

     def ice(self):
         flags = self.get_flags()
         self.set_units(' ')
         self.set_varname('ice')
         self.set_tit('Ice')
         self.set_cmap(cm.Blues_r)
         if 'anom' in flags:
             if 'amean' in flags:
                 self.set_cmaplev(np.arange(-1,1+0.1,0.1))
                 self.set_cbticks(np.arange(-1,1+0.2,0.2))
             elif 'seascyc' in flags:
                 self.set_cmaplev(np.arange(-1,1+0.1,0.1))
                 self.set_cbticks(np.arange(-1,1+0.2,0.2))
         else:
             if 'amean' in flags:
                 self.set_cmaplev(np.arange(0,1+0.05,0.05))
                 self.set_cbticks(np.arange(0,1+0.1,0.1))
                 self.set_cbextmode('max')
             elif 'seascyc' in flags:
                 self.set_cmaplev(np.arange(0,1+0.05,0.05))
                 self.set_cbticks(np.arange(0,1+0.1,0.1))
         return self

     def cloud(self):
         flags = self.get_flags()
         self.set_units(' ')
         self.set_varname('cloud')
         self.set_tit('Clouds')
         self.set_cmap(cm.Greys_r)
         if 'anom' in flags:
             if 'amean' in flags:
                 self.set_cmaplev(np.arange(-0.5,0.5+0.05,0.05))
                 self.set_cbticks(np.arange(-0.5,0.5+0.1,0.1))
             elif 'seascyc' in flags:
                 self.set_cmaplev(np.arange(-0.5,0.5+0.05,0.05))
                 self.set_cbticks(np.arange(-0.5,0.5+0.1,0.1))
         else:
             if 'amean' in flags:
                 self.set_cmaplev(np.arange(0,1+0.05,0.05))
                 self.set_cbticks(np.arange(0,1+0.1,0.1))
                 self.set_cbextmode('neither')
             elif 'seascyc' in flags:
                 self.set_cmaplev(np.arange(-1,1+0.1,0.1))
                 self.set_cbticks(np.arange(-1,1+0.2,0.2))
         return self

     def assign_var(self):
         name = self.get_defname()
         if name in self.defvar:
             return eval('self.{}().set_param()'.format(name))
         else:
             return self

     def set_param(self):
         flags = self.get_flags()
         if 'amean' in flags:
             txt='amean'
             tit = 'Annual Mean'
         elif 'seascyc' in flags:
             txt='seascyc'
             tit = 'Seasonal Cycle'
             self.set_cmap(cm.RdBu_r)
             self.set_cbextmode('both')
         else:
             txt=''
             tit = ''
             self.set_cmaplev(12)

         if 'variat' in flags:
             tit2='Change Rate'
             self.set_units('%')
             self.set_cmap(cm.PuOr_r)
             self.set_cmaplev(np.arange(-100,100+10,10))
             self.set_cbticks(np.arange(-100,100+20,20))
             self.set_cbextmode('both')
         elif 'anom' in flags:
             tit2= 'Anomaly'
             self.set_cmap(cm.RdBu_r)
             self.set_cbextmode('both')
         else:
             tit2= ''

         self.set_varname('.'.join([self.get_varname(),txt]))
         self.set_tit(' '.join([self.get_tit(),tit,tit2]))
         return self

# LIBRARIES
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from cdo import Cdo
import os
import warnings
import sys
from datetime import datetime as dtime
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec

class Dataset(xr.Dataset):
    '''
    Wrapper for xarray.Dataset class in order to add user-defined functions

    '''

    def __add__(self,other):
        self=self.copy()
        if check_xarray(other,'Dataset'):
            for var in self:
                if var in [v for v in other]: self[var]=self[var]+other[var]
                else: self[var]=self[var]
        elif check_xarray(other,'DataArray'):
            if other.name not in [v for v in self]:
                raise Exception('Impossible to compute operation. Data variable'+
                                ' names mismatch.')
            for var in self:
                if var == other.name: self[var]=self[var]+other
                else: self[var]=self[var]
        else:
            for var in self:
                self[var]=self[var]+other
        return self

    def __radd__(self,other):
        self=self.copy()
        if check_xarray(other,'DataArray'):
            if other.name not in [v for v in self]:
                raise Exception('Impossible to compute operation. Data variable'+
                                ' names mismatch.')
            self=other+self[other.name]
        else:
            for var in self:
                self[var]=other+self[var]
        return self

    def __sub__(self,other):
        self=self.copy()
        if check_xarray(other,'Dataset'):
            for var in self:
                if var in [v for v in other]: self[var]=self[var]-other[var]
                else: self[var]=self[var]
        elif check_xarray(other,'DataArray'):
            if other.name not in [v for v in self]:
                raise Exception('Impossible to compute operation. Data variable'+
                                ' names mismatch.')
            for var in self:
                if var == other.name: self[var]=self[var]-other
                else: self[var]=self[var]
        else:
            for var in self:
                self[var]=self[var]-other
        return self

    def __rsub__(self,other):
        self=self.copy()
        if check_xarray(other,'DataArray'):
            if other.name not in [v for v in self]:
                raise Exception('Impossible to compute operation. Data variable'+
                                ' names mismatch.')
            self=other-self[other.name]
        else:
            for var in self:
                self[var]=other-self[var]
        return self

    def __mul__(self,other):
        self=self.copy()
        if check_xarray(other,'Dataset'):
            for var in self:
                if var in [v for v in other]: self[var]=self[var]*other[var]
                else: self[var]=self[var]
        elif check_xarray(other,'DataArray'):
            if other.name not in [v for v in self]:
                raise Exception('Impossible to compute operation. Data variable'+
                                ' names mismatch.')
            for var in self:
                if var == other.name: self[var]=self[var]*other
                else: self[var]=self[var]
        else:
            for var in self:
                self[var]=self[var]*other
        return self

    def __rmul__(self,other):
        self=self.copy()
        if check_xarray(other,'DataArray'):
            if other.name not in [v for v in self]:
                raise Exception('Impossible to compute operation. Data variable'+
                                ' names mismatch.')
            self=other*self[other.name]
        else:
            for var in self:
                self[var]=other*self[var]
        return self

    def __truediv__(self,other):
        self=self.copy()
        if check_xarray(other,'Dataset'):
            for var in self:
                if var in [v for v in other]: self[var]=self[var]/other[var]
                else: self[var]=self[var]
        elif check_xarray(other,'DataArray'):
            if other.name not in [v for v in self]:
                raise Exception('Impossible to compute operation. Data variable'+
                                ' names mismatch.')
            for var in self:
                if var == other.name: self[var]=self[var]/other
                else: self[var]=self[var]
        else:
            for var in self:
                self[var]=self[var]/other
        return self

    def __rtruediv__(self,other):
        self=self.copy()
        if check_xarray(other,'DataArray'):
            if other.name not in [v for v in self]:
                raise Exception('Impossible to compute operation. Data variable'+
                                ' names mismatch.')
            self=other/self[other.name]
        else:
            for var in self:
                self[var]=other/self[var]
        return self

    def __floordiv__(self,other):
        self=self.copy()
        if check_xarray(other,'Dataset'):
            for var in self:
                if var in [v for v in other]: self[var]=self[var]//other[var]
                else: self[var]=self[var]
        elif check_xarray(other,'DataArray'):
            if other.name not in [v for v in self]:
                raise Exception('Impossible to compute operation. Data variable'+
                                ' names mismatch.')
            for var in self:
                if var == other.name: self[var]=self[var]//other
                else: self[var]=self[var]
        else:
            for var in self:
                self[var]=self[var]//other
        return self

    def __rfloordiv__(self,other):
        self=self.copy()
        if check_xarray(other,'DataArray'):
            if other.name not in [v for v in self]:
                raise Exception('Impossible to compute operation. Data variable'+
                                ' names mismatch.')
            self=other//self[other.name]
        else:
            for var in self:
                self[var]=other//self[var]
        return self

    def __pow__(self,other):
        self=self.copy()
        if check_xarray(other,'Dataset'):
            for var in self:
                if var in [v for v in other]: self[var]=self[var]**other[var]
                else: self[var]=self[var]
        elif check_xarray(other,'DataArray'):
            if other.name not in [v for v in self]:
                raise Exception('Impossible to compute operation. Data variable'+
                                ' names mismatch.')
            for var in self:
                if var == other.name: self[var]=self[var]**other
                else: self[var]=self[var]
        else:
            for var in self:
                self[var]=self[var]**other
        return self

    def __rpow__(self,other):
        self=self.copy()
        if check_xarray(other,'DataArray'):
            if other.name not in [v for v in self]:
                raise Exception('Impossible to compute operation. Data variable'+
                                ' names mismatch.')
            self=other**self[other.name]
        else:
            for var in self:
                self[var]=other**self[var]
        return self

    def __mod__(self,other):
        self=self.copy()
        if check_xarray(other,'Dataset'):
            for var in self:
                if var in [v for v in other]: self[var]=self[var]%other[var]
                else: self[var]=self[var]
        elif check_xarray(other,'DataArray'):
            if other.name not in [v for v in self]:
                raise Exception('Impossible to compute operation. Data variable'+
                                ' names mismatch.')
            for var in self:
                if var == other.name: self[var]=self[var]%other
                else: self[var]=self[var]
        else:
            for var in self:
                self[var]=self[var]%other
        return self

    def __rmod__(self,other):
        self=self.copy()
        if check_xarray(other,'DataArray'):
            if other.name not in [v for v in self]:
                raise Exception('Impossible to compute operation. Data variable'+
                                ' names mismatch.')
            self=other%self[other.name]
        else:
            for var in self:
                self[var]=other%self[var]
        return self

    def __getitem__(self, key):
        """Access variables or coordinates this dataset as a
        :myfuncs:class:`~__main__.DataArray`.

        Indexing with a list of names will return a new ``Dataset`` object.
        """
        from xarray.core import utils

        if utils.is_dict_like(key):
            return DataArray(self.isel(**key))

        if utils.hashable(key):
            return DataArray(self._construct_dataarray(key))
        else:
            return Dataset(self._copy_listed(np.asarray(key)),attrs=self.attrs)

    def plotall(self, projection = None, levels = None, cmap = None,
                outpath = None, statistics=True, title = None,
                cbar_kwargs = None, coast_kwargs = None, land_kwargs = None,
                save_kwargs = None):
        '''
        Plots all the variables of the Dataset using DataArray.plotvar function.

        '''

        def _check_length(x,def_len):
            x = [x] if not isinstance(x,list) else x
            if len(x) > 1:
                if len(x) != def_len:
                    raise Exception('All properties must be lists of properties '+
                                    'values and must have\nlength equal to the '+
                                    'number of variables in the Dataset')
                else:
                    return x
            else:
                return x*def_len

        vars=[v for v in self]
        projection = _check_length(projection,len(vars))
        levels = _check_length(levels,len(vars))
        cmap = _check_length(cmap,len(vars))
        outpath = _check_length(outpath,len(vars))
        statistics = _check_length(statistics,len(vars))
        title = _check_length(title,len(vars))
        cbar_kwargs = _check_length(cbar_kwargs,len(vars))
        coast_kwargs = _check_length(coast_kwargs,len(vars))
        land_kwargs = _check_length(land_kwargs,len(vars))
        save_kwargs = _check_length(save_kwargs,len(vars))

        for var,pr,lv,cm,out,st,tit,cb_kw,co_kw,la_kw,sv_kw in zip(self,projection, \
                        levels,cmap,outpath,statistics,title,cbar_kwargs, \
                        coast_kwargs,land_kwargs,save_kwargs):
            plt.figure()
            self[var].plotvar(projection=pr,levels=lv,cmap=cm,outpath=out,statistics=st,
                        title=tit,cbar_kwargs=cb_kw,coast_kwargs=co_kw,
                        land_kwargs=la_kw,save_kwargs=sv_kw)


    def annual_mean(self,copy=True,update_attrs=True):
        return annual_mean(self,copy=copy,update_attrs=update_attrs)

    def seasonal_cycle(self,copy=True,update_attrs=True):
            return seasonal_cycle(self,copy=copy,update_attrs=update_attrs)

    def anomalies(self,base=None,copy=True,update_attrs=True):
        return anomalies(self,x_base=base,copy=copy,update_attrs=update_attrs)

    def average(self, dim=None, weights=None,**kwargs):
        if not check_xarray(self, 'Dataset'):
            exception_xarray(type='Dataset')
        return self.apply(average, dim=dim, weights=weights,**kwargs)

    def global_mean(self,copy=True,update_attrs=True):
        return global_mean(self,copy=copy,update_attrs=update_attrs)

    def rms(self,copy=True,update_attrs=True):
        return rms(self,copy=copy,update_attrs=update_attrs)

    def to_celsius(self,copy=True):
        def func(x):
            try: return x.to_celsius()
            except: return x
        if copy: self = self.copy()
        return self.apply(lambda x: func(x),keep_attrs=True)


class DataArray(xr.DataArray):
    '''
    Wrapper for xarray.DataArray class in order to add user-defined functions

    '''

    def __add__(self,other):
        attrs=self.attrs
        return DataArray(xr.DataArray(self)+other,attrs=attrs)

    def __radd__(self,other):
        attrs=self.attrs
        return DataArray(other+xr.DataArray(self),attrs=attrs)

    def __sub__(self,other):
        attrs=self.attrs
        return DataArray(xr.DataArray(self)-other,attrs=attrs)

    def __rsub__(self,other):
        attrs=self.attrs
        return DataArray(other-xr.DataArray(self),attrs=attrs)

    def __mul__(self,other):
        attrs=self.attrs
        return DataArray(xr.DataArray(self)*other,attrs=attrs)

    def __rmul__(self,other):
        attrs=self.attrs
        return DataArray(other*xr.DataArray(self),attrs=attrs)

    def __truediv__(self,other):
        attrs=self.attrs
        return DataArray(xr.DataArray(self)/other,attrs=attrs)

    def __rtruediv__(self,other):
        attrs=self.attrs
        return DataArray(other/xr.DataArray(self),attrs=attrs)

    def __floordiv__(self, other):
        attrs=self.attrs
        return DataArray(xr.DataArray(self)//other,attrs=attrs)

    def __floordiv__(self,other):
        attrs=self.attrs
        return DataArray(other//xr.DataArray(self),attrs=attrs)

    def __pow__(self,other):
        attrs=self.attrs
        return DataArray(xr.DataArray(self)**other,attrs=attrs)

    def __rpow__(self,other):
        attrs=self.attrs
        return DataArray(other**xr.DataArray(self),attrs=attrs)

    def __mod__(self,other):
        attrs=self.attrs
        return DataArray(xr.DataArray(self)%other,attrs=attrs)

    def __rmod__(self,other):
        attrs=self.attrs
        return DataArray(other%xr.DataArray(self),attrs=attrs)

    def plotvar(self, projection = None, levels = None, cmap = None,
                outpath = None, statistics=True, title = None,
                cbar_kwargs = None,
                coast_kwargs = None,
                land_kwargs = None,
                save_kwargs = None):

        '''
        Plots GREB variables with associated color maps, scales and projections.

        '''

        def _get_var(x):
            keys = x.attrs.keys()
            name = x.name
            if 'long_name' in keys:
                title = x.attrs['long_name']
            else:
                title = x.name
            if 'units' in keys:
                units = x.attrs['units']
            else:
                units = ''
            if 'annual_mean' in keys:
                title = title + ' Annual Mean'
                name=name+'.amean'
            if 'seasonal_cycle' in keys:
                title = title + ' Seasonal Cycle'
                name=name+'.seascyc'
                cmap = cm.RdBu_r
            if 'anomalies' in keys:
                title = title + ' Anomalies'
                name=name+'.anom'
            return title,name,units

        if projection is None: projection = ccrs.Robinson()
        if cmap is None: cmap = self.get_param()['cmap']
        if title is None: title = _get_var(self)[0]
        name = _get_var(self)[1]
        units = _get_var(self)[2]
        if levels is None: levels = self.get_param()['levels']
        cbticks = self.get_param()['cbticks']
        extend = self.get_param()['extend']

        if cbar_kwargs is not None:
            cbar_kwargs = {'orientation':'horizontal', 'extend':extend, 'label':units,
                           'ticks':cbticks, **cbar_kwargs}
        else:
            cbar_kwargs = {'orientation':'horizontal', 'extend':extend, 'label':units,
                           'ticks':cbticks}

        if land_kwargs is not None:
            land_kwargs = {'edgecolor':'face', 'facecolor':'black', **land_kwargs}
        else:
            land_kwargs = {'edgecolor':'face', 'facecolor':'black'}

        if coast_kwargs is not None:
            coast_kwargs = {**coast_kwargs}
        else:
            coast_kwargs = {}
        if self.name == 'cloud':
            coast_kwargs = {'edgecolor':[0,.5,0.3],**coast_kwargs}

        if save_kwargs is not None:
            save_kwargs = {'dpi':300, 'bbox_inches':'tight', **save_kwargs}
        else:
            save_kwargs = {'dpi':300, 'bbox_inches':'tight'}

        plt.axes(projection=projection)
        self.to_contiguous_lon().plot.contourf(transform=ccrs.PlateCarree(),
        levels = levels,
        extend= extend,
        cmap = cmap,
        cbar_kwargs=cbar_kwargs)

        plt.gca().add_feature(cfeature.COASTLINE,**coast_kwargs)
        if (self.name == 'tocean'):
            plt.gca().add_feature(cfeature.NaturalEarthFeature('physical', 'land', '110m'),
                                  **land_kwargs)
        plt.title(title)
        if statistics:
            txt = ('gmean = {:.3f}'+'\n'+'rms = {:.3f}').format(self.global_mean().values,self.rms().values)
            plt.text(1.05,1,txt,verticalalignment='top',horizontalalignment='right',
                     transform=plt.gca().transAxes,fontsize=6)
        if outpath is not None:
            plt.savefig(os.path.join(outpath,'.'.join([name, 'png'])),
                        format = 'png',**save_kwargs)
            plt.close()

    def get_param(self):
        '''
        Function to set parameter for plotting

        '''

        keys=self.attrs.keys()
        name=self.name

        # TATMOS
        if name == 'tatmos':
            cmap = cm.RdBu_r
            extend = 'both'
            if 'anomalies' in keys:
                levels = np.arange(-2,2+0.2,0.2)
                cbticks = np.arange(-2,2+0.4,0.4)
            else:
                if 'annual_mean' in keys:
                    levels = np.arange(223,323+5,5)
                    cbticks = np.arange(223,323+10,10)
                elif 'seasonal_cycle' in keys:
                    levels = np.arange(-20,20+2,2)
                    cbticks = np.arange(-20,20+4,4)
        # TSURF
        elif name == 'tsurf':
            cmap = cm.RdBu_r
            extend = 'both'
            if 'anomalies' in keys:
                levels = np.arange(-2,2+0.2,0.2)
                cbticks = np.arange(-2,2+0.4,0.4)
            else:
                if 'annual_mean' in keys:
                    levels = np.arange(223,323+5,5)
                    cbticks = np.arange(223,323+10,10)
                elif 'seasonal_cycle' in keys:
                    levels = np.arange(-20,20+2,2)
                    cbticks = np.arange(-20,20+4,4)
        # TOCEAN
        elif name == 'tocean':
            cmap = cm.RdBu_r
            extend = 'both'
            if 'anomalies' in keys:
                levels = np.arange(-1,1+0.1,0.1)
                cbticks = np.arange(-1,1+0.2,0.2)
            else:
                if 'annual_mean' in keys:
                    levels = np.arange(273,303+5,3)
                    cbticks = np.arange(273,303+10,3)
                elif 'seasonal_cycle' in keys:
                    levels = np.arange(-1,1+1e-1,1e-1)
                    cbticks = np.arange(-1,1+2e-1,2e-1)
        # PRECIP
        elif name == 'precip':
            cmap = cm.GnBu
            extend = 'both'
            if 'anomalies' in keys:
                cmap = cm.RdBu_r
                levels = np.arange(-1,1+0.1,0.1)
                cbticks = np.arange(-1,1+0.2,0.2)
            else:
                if 'annual_mean' in keys:
                    extend = 'max'
                    levels = np.arange(0,9+1,1)
                    cbticks = np.arange(0,9+1,1)
                elif 'seasonal_cycle' in keys:
                    cmap = cm.RdBu_r
                    levels = np.arange(-6,6+1,1)
                    cbticks = np.arange(-6,6+1,1)
        # EVA
        elif name == 'eva':
            cmap = cm.GnBu
            extend = 'both'
            if 'anomalies' in keys:
                cmap = cm.RdBu_r
                levels = np.arange(-1,1+0.1,0.1)
                cbticks = np.arange(-1,1+0.2,0.2)
            else:
                if 'annual_mean' in keys:
                    cmap = cm.Blues
                    levels = np.arange(0,10+1,1)
                    cbticks = np.arange(0,10+1,1)
                elif 'seasonal_cycle' in keys:
                    cmap = cm.RdBu_r
                    levels = np.arange(-3,3+0.5,0.5)
                    cbticks = np.arange(-3,3+0.5,0.5)
        # QCRCL
        elif name == 'qcrcl':
            cmap = cm.RdBu_r
            extend = 'both'
            if 'anomalies' in keys:
                levels = np.arange(-1,1+0.1,0.1)
                cbticks = np.arange(-1,1+0.2,0.2)
            else:
                if 'annual_mean' in keys:
                    levels = np.arange(-8,8+1,1)
                    cbticks = np.arange(-8,8+2,2)
                elif 'seasonal_cycle' in keys:
                    levels = np.arange(-6,6+1,1)
                    cbticks = np.arange(-6,6+1,1)
        # VAPOR
        elif name == 'vapor':
            cmap = cm.RdBu_r
            extend = 'both'
            if 'anomalies' in keys:
                levels = np.arange(-5e-3,5e-3+5e-4,5e-4)
                cbticks = np.arange(-5e-3,5e-3+1e-3,1e-3)
            else:
                if 'annual_mean' in keys:
                    cmap = cm.Blues
                    levels = np.arange(0,0.02+0.002,0.002)
                    cbticks = np.arange(0,0.02+0.002,0.002)
                elif 'seasonal_cycle' in keys:
                    levels = np.arange(-0.01,0.01+0.001,0.001)
                    cbticks = np.arange(-0.01,0.01+0.0012,0.002)
        # ICE
        elif name == 'ice':
            cmap = cm.Blues_r
            extend = 'max'
            if 'anomalies' in keys:
                cmap = cm.RdBu_r
                extend = 'both'
                levels = np.arange(-1,1+0.1,0.1)
                cbticks = np.arange(-1,1+0.2,0.2)
            else:
                if 'annual_mean' in keys:
                    levels = np.arange(0,1+0.05,0.05)
                    cbticks = np.arange(0,1+0.1,0.1)
                elif 'seasonal_cycle' in keys:
                    cmap = cm.RdBu_r
                    extend = 'both'
                    levels = np.arange(0,1+0.05,0.05)
                    cbticks = np.arange(0,1+0.1,0.1)
        # CLOUD
        elif name == 'cloud':
            cmap = cm.Greys_r
            extend = 'neither'
            if 'anomalies' in keys:
                cmap = cm.RdBu_r
                extend = 'both'
                levels = np.arange(-0.5,0.5+0.05,0.05)
                cbticks = np.arange(-0.5,0.5+0.1,0.1)
            else:
                if 'annual_mean' in keys:
                    levels = np.arange(0,1+0.05,0.05)
                    cbticks = np.arange(0,1+0.1,0.1)
                elif 'seasonal_cycle' in keys:
                    cmap = cm.RdBu_r
                    extend = 'both'
                    levels = np.arange(-1,1+0.1,0.1)
                    cbticks = np.arange(-1,1+0.2,0.2)
        # SOLAR
        # not yet implemented

        else:
            levels = None
            cbticks = None
            extend = None
            cmap = None
        return {'levels':levels,'cbticks':cbticks,'extend':extend,'cmap':cmap}

    def to_contiguous_lon(self):
        '''
        Function to close the longitude coord (for plotting)

        '''
        return xr.concat([self, self.sel(lon=0).assign_coords(lon=360.)], dim='lon')

    def annual_mean(self,copy=True,update_attrs=True):
        return annual_mean(self,copy=copy,update_attrs=update_attrs)

    def seasonal_cycle(self,copy=True,update_attrs=True):
        return seasonal_cycle(self,copy=copy,update_attrs=update_attrs)

    def anomalies(self,base=None,copy=True,update_attrs=True):
        return anomalies(self,x_base=base,copy=copy,update_attrs=update_attrs)

    def average(self, dim=None, weights=None,**kwargs):
        return average(self, dim=dim, weights=weights,**kwargs)

    def global_mean(self,copy=True,update_attrs=True):
        return global_mean(self,copy=copy,update_attrs=update_attrs)

    def rms(self,copy=True,update_attrs=True):
        return rms(self,copy=copy,update_attrs=update_attrs)

    def to_celsius(self,copy=True):
        if copy: self = self.copy()
        if self.attrs['units'] == 'K':
            self.attrs['units'] = 'C'
            attrs=self.attrs
            newarray=self-273.15
            newarray.attrs = attrs
            return newarray
        elif self.attrs['units'] == 'C':
            return self
        else:
            raise Exception('Cannot convert to Celsius.\n{} '.format(self.name)+
                            'does not have temperature units.')

class constants:
    '''
    Class to wrap all the constants for GREB model, along with the default working
    folders.
    '''

    def __init__(self):
        pass

    @staticmethod
    def t():
        bin2netCDF(constants.cloud_def_file())
        time=xr.open_dataset(constants.cloud_def_file()+'.nc').time
        os.remove(constants.cloud_def_file()+'.nc')
        return time

    @staticmethod
    def lat():
        return np.arange(-88.125,88.125+3.75,3.75)

    @staticmethod
    def lon():
        return np.arange(0,360,3.75)

    @staticmethod
    def dx():
        return len(constants.lon())

    @staticmethod
    def dy():
        return len(constants.lat())

    @staticmethod
    def dt():
        return len(constants.t())

    @staticmethod
    def time():

        return time

    @staticmethod
    def greb_folder():
        return r'/Users/dmar0022/university/phd/greb-official'

    @staticmethod
    def figures_folder():
        return constants.greb_folder()+'/figures'

    @staticmethod
    def output_folder():
        return constants.greb_folder()+'/output'

    @staticmethod
    def input_folder():
        return constants.greb_folder()+'/input'

    @staticmethod
    def scenario_2xCO2(years_of_simulation=50):
        return constants.output_folder()+'/scenario.exp-20.2xCO2_{}yrs'.format(years_of_simulation)

    @staticmethod
    def cloud_def_file():
        return constants.greb_folder()+'/input/isccp.cloud_cover.clim'

    @staticmethod
    def solar_def_file():
        return constants.greb_folder()+'/input/solar_radiation.clim'

    @staticmethod
    def cloud_folder():
        return constants.greb_folder()+'/artificial_clouds'

    @staticmethod
    def solar_folder():
        return constants.greb_folder()+'/artificial_solar_radiation'

    @staticmethod
    def cloud_figures_folder():
        return constants.cloud_folder()+'/art_clouds_figures'

    @staticmethod
    def control_def_file():
        return constants.output_folder()+'/control.default'

    @staticmethod
    def to_greb_grid(x, method='cubic'):
        '''
        Regrid data to GREB lat/lon grid.

        Arguments
        ----------
        x : xarray.DataArray or xarray.Dataset
            Data to be regridded.

        Parameters
        ----------
        method: str
            Method for the interpolation.
            Can be chosen between: 'linear' (default), 'nearest', 'zero',
                                   'slinear', 'quadratic', 'cubic'.

        Returns
        ----------
        New xarray.Dataset or xarray.DataArray regridded into GREB lat/lon grid.

        '''

        greb=from_binary(constants.control_def_file()).mean('time')
        return x.interp_like(greb,method=method)

    @staticmethod
    def to_greb_indexes(lat,lon):
        '''
        Convert lat/lon from degrees to GREB indexes

        Arguments
        ----------
        lat : float or array of floats
            latitude point or array of latitude points.
        lon : float or array of floats
            longitude point or array of longitude points.
            lat and lon must be the same lenght

        Returns
        ----------
        GREB model Indexes corrisponding to the lat/lon couples.

        '''

        lat = np.array(lat)
        lon = np.array(lon)
        if np.any(lat<-90) or np.any(lat>90):
            raise ValueError('lat value must be between -90 and 90 degrees')
        lon=np.array(lon)
        if np.any(lon<0) or np.any(lon>360):
            raise ValueError('lon value must be between 0 and 360 degrees')
        lat_def = constants.lat().tolist()
        lon_def = constants.lon().tolist()
        i = [lat_def.index(min(lat_def, key=lambda x:abs(x-la))) for la in lat] \
            if len(lat.shape) == 1 else lat_def.index(min(lat_def, key=lambda x:abs(x-lat)))
        j = [lon_def.index(min(lon_def, key=lambda x:abs(x-lo))) for lo in lon] \
            if len(lon.shape) == 1 else lon_def.index(min(lon_def, key=lambda x:abs(x-lon)))
        return i,j

    @staticmethod
    def to_greb_time(date_str, fmt = '%y-%m-%d'):
        '''
        Convert a datestring time to GREB time specification

        Arguments
        ----------
        date_str : datestr
            Datestr of time to convert

        Parameters
        ----------
        fmt : str
            date_str format specification

        Returns
        ----------
        GREB model time specificatio for the date_str in input.

        '''

        return dtime.strptime(date_str,fmt).toordinal()*24+24

    @staticmethod
    def from_greb_time(greb_timenum,fmt = None):
        '''
        Convert a GREB time specification to datestr.

        Arguments
        ----------
        greb_timenum : int
            GREB time ordinal

        Parameters
        ----------
        fmt : str
            format specification for the datestr in output.

        Returns
        ----------
        datetime.datetime object for the GREB model time ordinal in input.
        if fmt is provided, returns a datestr.

        '''

        import math
        timenum = math.ceil((greb_timenum/24)-1)
        if fmt is None:
            return dtime.fromordinal(timenum)
        elif isinstance(fmt,str):
            return dtime.fromordinal(timenum).strftime(fmt)
        else:
            raise Exception('"fmt" must be either None or a valid date format')
            return

    @staticmethod
    def shape_for_bin(type='cloud'):
        if type == 'cloud':
            # 'Shape must be in the form (tdef,ydef,xdef)'
            return (constants.dt(),constants.dy(),constants.dx())
        elif type == 'solar':
            return (constants.dt(),constants.dy(),1)
        else: raise Exception('type must be either "cloud" or "solar"')

    @staticmethod
    def to_shape_for_bin(data,type='cloud'):
        def_sh = constants.shape_for_bin(type)
        sh=data.shape
        if len(sh) != 3: raise Exception('data must be 3D, in the form {}x{}x{}'.format(def_sh[0],def_sh[1],def_sh[2]))
        if len(set(sh)) != 3: raise Exception('data shape must be in the form {}x{}x{}'.format(def_sh[0],def_sh[1],def_sh[2]))
        if ((sh[0] not in def_sh) or (sh[1] not in def_sh) or (sh[2] not in def_sh)):
            raise Exception('data shape must be in the form {}x{}x{}'.format(def_sh[0],def_sh[1],def_sh[2]))
        if sh != def_sh:
            indt=sh.index(def_sh[0])
            indy=sh.index(def_sh[1])
            indx=sh.index(def_sh[2])
            data = data.transpose(indt,indy,indx)
        return data

    @staticmethod
    def get_years_of_simulation(sc_filename):
        '''
        Gets the number of years of simulations for the specified scenario file.

        Arguments
        ----------
        sc_filename : str
            Path to the scenario file

        Returns
        ----------
        int
           Number of years of simulations

        '''

        if 'yrs' not in sc_filename.split('_')[-1]:
            raise Exception('Could not understand the number of years of simulation.'+
                            '\nNumber of years of simulation N must be at the end of'+
                            ' sc_filename in the form "_Nyrs"')
        else:
            return (sc_filename.split('_')[-1])[:-3]

    @staticmethod
    def get_art_forcing_filename(sc_filename,forcing=None):
        '''
        Gets the artificial cloud filename used to obtain the scenario filename in input.

        Arguments
        ----------
        sc_filename : str
            Path to the scenario file

        Parameters
        ----------
        forcing : str
           Type of forcing to retrieve. Can be set to "cloud" or "solar".
           If not set, the forcing type will be tried to be understood from the
           scenario filename.

        Returns
        ----------
        str
           Path to the artificial cloud

        '''

        sc_filename = rmext(os.path.split(sc_filename)[1])
        if 'yrs' in sc_filename.split('_')[-1]:
            sc_filename = '_'.join(sc_filename.split('_')[:-1])
        if forcing is None:
            if 'exp-930.geoeng.' in sc_filename:
                txt='exp-930.geoeng.'
                forcing='cloud'
            elif 'exp-931.geoeng.' in sc_filename:
                txt='exp-931.geoeng.'
                forcing='solar'
            else:
                raise Exception('Invalid scenario filename.\nSpecify "forcing",'+
                                ' or the scenario filename must contain either '+
                                '"exp-930.geoeng." or "exp-931.geoeng.".')
        elif forcing == 'cloud':
            txt='exp-930.geoeng.'
        elif forcing == 'solar':
            txt='exp-931.geoeng.'
        else: raise Exception('Supported forcings are "cloud" or "solar".')
        if txt in sc_filename:
            art_forcing_name = sc_filename[sc_filename.index(txt)+len(txt):]
            if '.iter' in sc_filename:
                return os.path.join(eval('constants.{}_folder()'.format(forcing)),'cld.artificial.iteration_'+'_'.join(sc_filename.split('_')[1:]),art_forcing_name)
            else:
                return os.path.join(eval('constants.{}_folder()'.format(forcing)), art_forcing_name)
        elif ('exp-20.2xCO2' in sc_filename) or ('control.default' in sc_filename):
            return eval('constants.{}_def_file()'.format(forcing))
        else:
            raise Exception('Invalid scenario filename.\nThe scenario filename'+
                            ' must contain "{}".'.format(txt))

    @staticmethod
    def get_scenario_filename(forcing_filename,years_of_simulation=50):
        '''
        Gets the scenario filename from either an artifial cloud or solar forcing
        filename.

        Arguments
        ----------
        forcing_filename : str
            Path to the forcing file

        Parameters
        ----------
        years_of_simulation : int
           Number of years for which the forcing simulation has been run

        Returns
        ----------
        str
           Path to the output scenario

        '''

        txt1='cld.artificial'
        txt2='sw.artificial'
        forcing_filename = rmext(forcing_filename)
        forcing_filename_ = os.path.split(forcing_filename)[1]
        if txt1 in forcing_filename_:
            sc_name = 'scenario.exp-930.geoeng.'+forcing_filename_+'_{}yrs'.format(years_of_simulation)
        elif txt2 in forcing_filename_:
            sc_name = 'scenario.exp-931.geoeng.'+forcing_filename_+'_{}yrs'.format(years_of_simulation)
        elif (forcing_filename == constants.cloud_def_file()) or (forcing_filename == constants.solar_def_file()):
            sc_name = 'scenario.exp-20.2xCO2'+'_{}yrs'.format(years_of_simulation)
        else:
           raise Exception('The forcing file must contain either "cld.artificial" or "sw.artificial"')
        return os.path.join(constants.output_folder(),sc_name)

    @staticmethod
    def days_each_month():
        return np.array([31,28,31,30,31,30,31,31,30,31,30,31])

def input_(def_input,argv=1):
    '''
    Function to set default inputs when running a script from Atom,
    but still allowing those input to be set as arguments when running the script
    from the command line.

    Arguments
    ----------
    def_input : -
        Default input to be set

    Parameters
    ----------
    argv: Int
        Position of the input in the arguments when launching the script from the
        command line.
        argv must be an integer >= 1

    Returns
    ----------
    -
        Returns the default input if the script is run in Atom, or if launched
        from the command line with no argument in the position pointed by argv;
        returns the argument input if, when launching the script from the command
        line, there is an argument in the position pointed by argv.

    '''

    if (argv < 1 or np.all([not isinstance(argv,int),not isinstance(argv,np.int64),not isinstance(argv,np.int32)])):
        raise Exception('argv must be an integer greater than 0')
    try:
        input=sys.argv[argv]
        if ((argv == 1 and input == '-f') or (argv==2 and os.path.splitext(input)[1]=='.json')):
            return rmext(def_input) if isinstance(def_input,str) else def_input
        else:
            return rmext(input) if isinstance(def_input,str) else type(def_input)(input)
    except(IndexError): return rmext(def_input) if isinstance(def_input,str) else def_input

def ignore_warnings():
    '''
    Suppress all the warning messages
    '''

    if not sys.warnoptions:
        warnings.simplefilter("ignore")

def from_binary(filename,time_group=None,parse=True):
    """
    Read binary file into an xarray.Dataset object.

    Arguments
    ----------
    filename : str
        Path to the ".bin" file to open

    Parameters
    ----------
    time_group : str
        Time grouping method to be chosen between: '12h','day','month','year','season'.
        If chosen, the retrieved data belonging to the same time_group will be
        averaged.
        If "time_group" is smaller than the data time-resolution, a spline
        interpolation is performed.
    parse: Bool
        Set to True (default) if you want the output to be parsed with the custom
        "parse_greb_var" function, otherwise set to False.

    Returns
    ----------
    xarray.Dataset
        Dataset containing all the variables in the binary file.

    """
    if time_group not in ['12h','day','month','year','season',None]:
        raise Exception('time_group must be one of the following:\n'+\
                        '"12h","day","month","year","season"')
    filename = rmext(filename)
    bin2netCDF(filename)
    data=xr.open_dataset(filename+'.nc')
    os.remove(filename+'.nc')
    attrs = data.attrs
    if parse: data = parse_greb_var(data)
    t_res = np.timedelta64(data.time.values[1]-data.time.values[0],'D').item().total_seconds()/(3600*12)
    if t_res > 62:
        raise Exception('Impossible to group data by "{}".\n'.format(time_group)+
                        'Could not understand the time resolution of the data.')

    if time_group is not None:
        attrs['grouped_by'] = time_group
        for var in data: data._variables[var].attrs['grouped_by'] = time_group
        interp=False
        if time_group == '12h':
            nt=730
            time_group = 'month'
            interp=True
        elif time_group == 'day':
            nt=365
            time_group = 'dayofyear'
            interp=True
        data = data.groupby('time.{}'.format(time_group)).mean(dim='time',keep_attrs=True).rename({'{}'.format(time_group):'time'})
        if interp:
            data = data.interp(time=np.linspace(data.time[0]-0.5,data.time[-1]+0.5,nt),method='cubic',kwargs={'fill_value':'extrapolate'}).assign_coords(time=constants.t()[::int(730/nt)])
    return Dataset(data,attrs=attrs)

def rmext(filename):
    """
    Remove the .bin or .ctl extension at the end of the filename.
    If none of those extensions is present, returns filename.

    Arguments
    ----------
    filename : str
        Path to remove the extension from

    Returns
    ----------
    str
        New path with ".bin" or ".ctl" extension removed.

    """

    path,ext = os.path.splitext(filename)
    if ext not in ['.ctl','.bin','.']: path = path+ext
    return path

def bin2netCDF(file):
    """
    Convert a binary (".bin") file to a netCDF (".nc") file.

    Arguments
    ----------
    file : str
        Path of the file (with or without ".bin") to convert to netCDF.

    Returns
    ----------
    None
        Creates a new netCDF file with the same name as the original binary

    """

    filename = rmext(file)
    cdo = Cdo() # Initialize CDO
    cdo.import_binary(input = filename+'.ctl', output = filename+'.nc',
                      options = '-f nc')

def exception_xarray(type = None,varname = 'x'):
    '''
    Prescribed xarray exception.

    Parameters
    ----------
    type : str
       type of xarray object: 'DataArray' or 'Dataset'
    varname : str
        name of the variable to display in the exception

    Returns
    ----------
    ValueError Exception

    '''

    if type is not None:
        if type.lower() == 'dataarray':
            raise ValueError('{} must be an xarray.DataArray object'.format(varname))
        elif type.lower() == 'dataset':
            raise ValueError('{} must be an xarray.Dataset object'.format(varname))
    raise ValueError('{} must be either an xarray.DataArray or xarray.Dataset object'.format(varname))

def check_xarray(x,type=None):
    '''
    Check if the argument is an xarray object.

    Arguments
    ----------
    x : xarray.Dataset or xarray.DataArray object
       array to be checked

    Parameters
    ----------
    type : str
       type of xarray object: 'DataArray' or 'Dataset'
    varname : str
       name of the variable to display in the exception

    Returns
    ----------
    Bool

    '''

    da = isinstance(x,xr.DataArray)
    ds = isinstance(x,xr.Dataset)
    if type is not None:
        if type.lower() == 'dataarray': return da
        elif type.lower() == 'dataset': return ds
    return np.logical_or(da,ds)


def parse_greb_var(x,update_attrs=True):
    '''
    Corrects GREB model output variables and adds units label

    Arguments
    ----------
    x : xarray.Dataset or xarray.DataArray object
       array of GREB output variables to be parsed

    Parameters
    ----------
    update_attrs : Bool
        If set to True (default), the new DataArray/Dataset will have an attribute
        as a reference that it was parsed with the "parse_var" function.

    Returns
    ----------
    xarray.Dataset or xarray.DataArray depending on the argument's type

    '''

    def _parsevar(x,update_attrs=None):
        name = x.name
        # TATMOS,TSURF,TOCEAN
        if name == 'tatmos':
            x.attrs['long_name']='Atmospheric Temperature'
            x.attrs['units']='K'
        elif name == 'tsurf':
            x.attrs['long_name']='Surface Temperature'
            x.attrs['units']='K'
        elif name == 'tocean':
            x.attrs['long_name']='Ocean Temperature'
            x.attrs['units']='K'
        elif name == 'precip':
            x.attrs['long_name']='Precipitation'
            x.attrs['units']='mm/day'
            x*=-86400
        elif name == 'eva':
            x.attrs['long_name']='Evaporation'
            x.attrs['units']='mm/day'
            x*=-86400
        elif name == 'qcrcl':
            x.attrs['long_name']='Circulation'
            x.attrs['units']='mm/day'
            x*=-86400
        elif name == 'vapor':
            x.attrs['long_name']='Specific Humidity'
            x.attrs['units']=''
        elif name == 'ice':
            x.attrs['long_name']='Ice'
            x.attrs['units']=''
        elif name == 'cloud':
            x.attrs['long_name']='Clouds'
            x.attrs['units']=''
        elif name == 'solar':
            x.attrs['long_name']='SW Radiation'
            x.attrs['units']='W/m2'

        if update_attrs:
            x.attrs['parse_greb_var']='Parsed with parse_greb_var function'
        return x

    if 'parse_greb_var' in x.attrs: return x
    if check_xarray(x,'dataarray'):
        return DataArray(_parsevar(x,update_attrs).squeeze())
    elif check_xarray(x,'dataset'):
        x.apply(lambda a: _parsevar(a,update_attrs),keep_attrs=True)
        if update_attrs:
            x.attrs['parse_greb_var']='Parsed with parse_greb_var function'
        return Dataset(x,attrs=x.attrs).squeeze()
    else: exception_xarray()

def average(x, dim=None, weights=None,**kwargs):
    """
    weighted average for DataArrays

    Arguments
    ----------
    x : xarray.DataArray
        array to compute the average on

    Parameters
    ----------
    dim : str or sequence of str, optional
        Dimension(s) over which to apply average.
    weights : DataArray
        weights to apply. Shape must be broadcastable to shape of x.

    Returns
    ----------
    reduced : DataArray
        New DataArray with average applied to its data and the indicated
        dimension(s) removed.

    """

    if not check_xarray(x,'DataArray'): exception_xarray('DataArray')
    attrs=x.attrs
    if weights is None:
        return x.mean(dim,**kwargs)
    else:
        if not check_xarray(weights,'DataArray'):
            exception_xarray(type='DataArray',varname='weights')

        # if NaNs are present, we need individual weights
        if not x.notnull().all():
            total_weights = weights.where(x.notnull()).sum(dim=dim,**kwargs)
        else:
            total_weights = weights.sum(dim,**kwargs)
        numerator = xr.apply_ufunc(lambda a,b: a*b,x, weights,**kwargs).sum(dim,**kwargs)
        return DataArray(xr.apply_ufunc(lambda a,b: a/b,numerator, total_weights,**kwargs),attrs=attrs)

def rms(x,copy=True,update_attrs=True):
    '''
    Compute the root mean square error over "lat" and "lon" dimension.

    Arguments
    ----------
    x : xarray.Dataset or xarray.DataArray object
       array to compute the rms on

    Parameters
    ----------
    copy : Bool
       set to True (default) if you want to return a copy of the argument in
       input; set to False if you want to overwrite the input argument.
    update_attrs : Bool
        If set to True (default), the new DataArray/Dataset will have an attribute
        as a reference that the "rms" function has been applied to it.

    Returns
    ----------
    xarray.Dataset or xarray.DataArray

    New Dataset or DataArray object with rms applied to its "lat" and "lon"
    dimension.

    '''

    if not check_xarray(x): exception_xarray()
    if 'rms' in x.attrs:return x
    if 'global_mean' in x.attrs:
        raise Exception('Cannot perform rms on a variable on which global mean has already been performed')
    if copy: x = x.copy()
    func=DataArray
    if check_xarray(x,'Dataset'):
        if update_attrs:
            for var in x: x[var].attrs['rms'] = 'Computed root mean square'
        func=Dataset
    attrs=x.attrs
    gm=global_mean(x**2,update_attrs=False)
    if update_attrs:
        attrs['rms'] = 'Computed root mean square'
    return func(xr.apply_ufunc(lambda x: np.sqrt(x),gm,keep_attrs=True),attrs=attrs)

def annual_mean(x,copy=True,update_attrs=True):
    '''
    Compute the mean over 'time' dimension.

    Arguments
    ----------
    x : xarray.Dataset or xarray.DataArray object
       array to compute the annual mean on

    Parameters
    ----------
    copy : Bool
       set to True (default) if you want to return a copy of the argument in
       input; set to False if you want to overwrite the input argument.
    update_attrs : Bool
        If set to True (default), the new DataArray/Dataset will have an attribute
        as a reference that the annual_mean function has been applied to it.

    Returns
    ----------
    xarray.Dataset or xarray.DataArray

    New Dataset or DataArray object with average applied to its "time" dimension.

    '''

    if not check_xarray(x): exception_xarray()
    if 'annual_mean' in x.attrs: return x
    if 'seasonal_cycle' in x.attrs:
        raise Exception('Cannot perform annual mean on a variable on which seasonal cycle has already been performed')
    if copy: x = x.copy()
    if update_attrs:
        x.attrs['annual_mean'] = 'Computed annual mean'
        if check_xarray(x,'Dataset'):
            for var in x: x._variables[var].attrs['annual_mean'] = 'Computed annual mean'
    return x.mean(dim='time',keep_attrs=True).squeeze()

def global_mean(x,copy=True,update_attrs=True):
    '''
    Compute the global mean over 'lat' and 'lon' dimension.
    The average over 'lat' dimension will be weigthed with cos(lat).

    Arguments
    ----------
    x : xarray.Dataset or xarray.DataArray object
       array to compute the global mean on

    Parameters
    ----------
    copy : Bool
       set to True (default) if you want to return a copy of the argument in
       input; set to False if you want to overwrite the input argument.
    update_attrs : Bool
        If set to True (default), the new DataArray/Dataset will have an attribute
        as a reference that the "global_mean" function has been applied to it.

    Returns
    ----------
    xarray.Dataset or xarray.DataArray

    New Dataset or DataArray object with average applied to its "lat" and
    "lon" dimension. The average along "lat" dimesnion is weighted with cos(lat)
    weights.

    '''

    if not check_xarray(x): exception_xarray()
    if 'global_mean' in x.attrs: return x
    if 'rms' in x.attrs:
        raise Exception('Cannot perform global mean on a variable on which rms has already been performed')
    if copy: x = x.copy()
    if update_attrs:
        x.attrs['global_mean'] = 'Computed global mean'
        if check_xarray(x,'Dataset'):
            for var in x: x._variables[var].attrs['global_mean'] = 'Computed global mean'
    weights = np.cos(np.deg2rad(x.lat))
    return x.average(dim='lat',weights=weights,keep_attrs=True).mean('lon',keep_attrs=True).squeeze()

def seasonal_cycle(x,copy=True,update_attrs=True):
    '''
    Compute the seasonal cycle (DJF-JJA) over time dimension

    Arguments
    ----------
    x : xarray.Dataset or xarray.DataArray object
       array to compute the seasonal cycle on

    Parameters
    ----------
    copy : Bool
       set to True (default) if you want to return a copy of the argument in
       input; set to False if you want to overwrite the input argument.
    update_attrs : Bool
        If set to True (default), the new DataArray/Dataset will have an attribute
        as a reference that the "seasonal_cycle" function has been applied to it.

    Returns
    ----------
    xarray.Dataset or xarray.DataArray

    New Dataset or DataArray object with seasonal cycle applied to its "time" dimension.

    '''

    if not check_xarray(x): exception_xarray()
    if 'seasonal_cycle' in x.attrs: return x
    if 'annual_mean' in x.attrs:
        raise Exception('Cannot perform seasonal cycle on a variable on which annual mean has already been performed')
    if 'global_mean' in x.attrs:
        raise Exception('Cannot perform annual mean on a variable on which global mean has already been performed')
    if 'rms' in x.attrs:
        raise Exception('Cannot perform seasonal cycle on a variable on which rms has already been performed')
    if copy: x = x.copy()
    if update_attrs:
        x.attrs['seasonal_cycle'] = 'Computed seasonal cycle'
        if check_xarray(x,'Dataset'):
            for var in x: x._variables[var].attrs['seasonal_cycle'] = 'Computed seasonal cycle'
    x_seas=x.groupby('time.season').mean(dim='time',keep_attrs=True).squeeze()
    return (x_seas.sel(season='DJF')-x_seas.sel(season='JJA'))/2

def anomalies(x,x_base=None,copy=True,update_attrs=True):
    '''
    Compute anomalies of x with respect to x_base (x-x_base).

    Arguments
    ----------
    x : xarray.Dataset or xarray.DataArray object
       array to compute the anomalies on
    x_base : xarray.Dataset or xarray.DataArray object
       array to compute the anomalies from.
       x and x_base variables and dimensions must match.

    Parameters
    ----------
    copy : Bool
       set to True (default) if you want to return a copy of the argument in
       input; set to False if you want to overwrite the input argument.
    update_attrs : Bool
        If set to True (default), the new DataArray/Dataset will have an attribute
        as a reference that the "anomalies" function has been applied to it.

    Returns
    ----------
    xarray.Dataset or xarray.DataArray

    New Dataset or DataArray object being the difference between x and x_base

    '''

    def fun(y):
        attrs = y.attrs
        newy=np.repeat(y,(x.time.shape[0])/12,axis=0).assign_coords(time=x.time.values)
        newy.attrs = attrs
        return newy

    if not check_xarray(x): exception_xarray()
    if x_base is None:
        if 'grouped_by' in x.attrs:
            x_base = from_binary(constants.control_def_file(),x.attrs['grouped_by'])
        else:
            x_base = from_binary(constants.control_def_file()).apply(fun,keep_attrs=True)
        # Change to Celsius if needed
        temp = ['tsurf','tocean','tatmos']
        if check_xarray(x,'DataArray'):
            if x.name in temp:
                if x.attrs['units'] == 'C': x_base = x_base.to_celsius(copy=False)
        else:
            vars=[d for d in x]
            for t in temp:
                if t in vars:
                    if x[t].attrs['units'] == 'C': x_base = x_base.to_celsius(copy=False)
    else:
        if not check_xarray(x_base): exception_xarray()
    if 'annual_mean' in x.attrs: x_base = annual_mean(x_base)
    if 'seasonal_cycle' in x.attrs: x_base = seasonal_cycle(x_base)
    if 'global_mean' in x.attrs: x_base = global_mean(x_base)
    if 'rms' in x.attrs: x_base = rms(x_base)
    if copy: x = x.copy()
    if update_attrs:
        x.attrs['anomalies'] = 'Anomalies'
        if check_xarray(x,'Dataset'):
            for var in x: x._variables[var].attrs['anomalies'] = 'Anomalies'
    _check_units(x,x_base)
    return x-x_base

def to_Robinson_cartesian(lat,lon,lon_center = 0):
    '''
    Convert lat/lon points to Robinson Projection.

    Arguments
    ----------
    lat : float or array of floats
        latitude point or array of latitude points.
    lon : float or array of floats
        longitude point or array of longitude points.
        lat and lon must be the same lenght

    Parameters
    ----------
    lon_center : float
        center meridiane of the Robinson projection

    Returns
    ----------
    float or array of floats
        Robinson projection projected points

    '''

    from scipy.interpolate import interp1d
    center = np.deg2rad(lon_center)
    lat=np.array(lat)
    if np.any(lat<-90) or np.any(lat>90):
        raise ValueError('lat value must be between -90 and 90 degrees')
    lon=np.array(lon)
    if np.any(lon<0) or np.any(lon>360):
        raise ValueError('lon value must be between 0 and 360 degrees')
    lon = np.deg2rad(lon)
    R = 6378137.1
    lat_def = np.arange(0,95,5)
    X_def= [1,0.9986,0.9954,0.9900,0.9822,0.9730,0.9600,0.9427,0.9216,0.8962,
        0.8679,0.8350,0.7986,0.7597,0.7186,0.6732,0.6213,0.5722,0.5322]
    Y_def= [0,0.0620,0.1240,0.1860,0.2480,0.3100,0.3720,0.4340,0.4958,0.5571,
        0.6176,0.6769,0.7346,0.7903,0.8435,0.8936,0.9394,0.9761,1.0000]

    iX = interp1d(lat_def, X_def, kind='cubic')
    iY = interp1d(lat_def, Y_def, kind='cubic')
    x = 0.8487*R*iX(np.abs(lat))*(lon-lon_center)
    y = 1.3523*R*iY(np.abs(lat))
    x=np.where((lon % 360) > 180,-x,x)
    y=np.where(lat < 0,-y,y)

    return x,y

def multidim_regression(x,y,x_pred=None,axis=-1,multivariate=False):
    '''
    Performs Linear Regression over multi-dimensional arrays.
    It doesn't loop over the dimensions but makes use of np.einsum to perform inner products.

    Arguments
    ----------
    x : array of features to apply linear regression to.
        The shape must be (M,N,...)
    y : array of examples to train the linear regression.
        The shape must be (M,1)


    Parameters
    ----------
    x_pred : array of floats
        array of points on which to perform the prediction
    axis : int
        dimension along which the regression will be performed
    multivariate : bool
        set to True if a multivariate regression is required.
        In this case, the multiple features axis will be the one specified
        by "axis" + 1.

    Returns
    ----------
    If x_pred is provided, it returns an array with the predicted values.
    Otherwise, it will return a function to be applied to the prediction values.

    '''

    def check_var(x):
        if not isinstance(x,np.ndarray): x = np.array([x])
        if len(x.shape) == 1: x= x.reshape([x.shape[0],1])
        return x

    def check_pred(x):
        if not isinstance(x,np.ndarray): x = np.array([x])
        if len(x.shape) == 1: x = x.reshape([1,x.shape[0]])
        return x

    def check_axis(x,axis,multivariate):
        if axis == -1:
            if multivariate:
                if len(x.shape) > 2:
                    axis = -2
                else:
                    axis = 0
        if multivariate:
            multivariate = axis+1
            if multivariate >= len(x.shape):
                raise Exception('Dimension mismatch')
        else: multivariate = False

        return axis,multivariate

    def check_xy(x,y,axis,multivariate):
        if len(x.shape)!=len(y.shape):
            y = np.expand_dims(y,axis=axis+1)
        dim1 = list(x.shape)
        dim2 = list(y.shape)
        if multivariate:
            del dim1[multivariate]
            del dim2[multivariate]
        if not np.all(dim1==dim2):
            raise Exception('x and y dimensions mismatch!')
        return y

    def check_xpred(x,x_pred,axis):
        if len(x.shape)!=len(x_pred.shape):
            x_pred = np.expand_dims(x_pred,axis=axis)
        dim1  = list(x.shape)
        dim2 = list(x_pred.shape)
        del dim1[axis]
        del dim2[axis]
        if not np.all(dim1==dim2):
            raise Exception('x and x_pred dimensions mismatch!')
        return x_pred

    def transpose_(V):
        m=np.arange(len(V.shape)).tolist()
        m = m[:-2] + [m[-1]] + [m[-2]]
        return V.transpose(m)

    def to_X(x,axis,multivariate):
        X = to_Y(x,axis,multivariate)
        return np.insert(X,0,1,axis = -1)

    def to_Y(x,axis,multivariate):
        m=np.arange(len(x.shape)).tolist()
        try:
            m.remove(axis)
        except(ValueError):
            del m[axis]
        if multivariate:
            try:
                m.remove(multivariate)
            except(ValueError):
                del m[multivariate]
            X = np.transpose(x,m+[axis,multivariate])
        else:
            X = np.transpose(x,m+[axis])[...,np.newaxis]
        return X

    def dot_(x,y):
        if len(x.shape) > 2:
            m1 = np.arange(len(x.shape)).tolist()
            m2 = m1[:-2] + [m1[-1]] + [m1[-1]+1]
            m3 = m1[:-1] + [m1[-1]+1]
            return np.einsum(x,m1,y,m2,m3)
        else:
            return np.dot(x,y)

    x = check_var(x)
    y = check_var(y)
    x_pred = check_pred(x_pred)
    axis,multivariate = check_axis(x,axis,multivariate)
    y = check_xy(x,y,axis,multivariate)
    if x_pred is not None:
        x_pred = check_xpred(x,x_pred,axis)
        X_pred = to_X(x_pred,axis,multivariate)
    Y=to_Y(y,axis,multivariate)
    X=to_X(x,axis,multivariate)

    if len(X.shape) > 2:
        THETA=dot_(np.linalg.inv(dot_(transpose_(X),X)),dot_(transpose_(X),Y))
        if x_pred is None:
            return lambda t: dot_(to_X(t,axis,multivariate),THETA).squeeze()
        else:
            return dot_(X_pred,THETA).squeeze()
    else:
        THETA=np.linalg.inv(X.T.dot(X)).dot(X.T.dot(Y))
        if x_pred is None:
            return lambda t: to_X(t,axis,multivariate).dot(THETA)
        else:
            return x_pred.dot(THETA)



def create_bin_ctl(path,vars):
    '''
    Creates '.bin' and '.ctl' file from Dictionary.

    Arguments
    ----------
    path : str
        complete path for the new '.bin' and '.ctl' files.
    vars : dictionary
        vars must be in the form {"namevar1":var1,"namevar2":var2,...,"namevarN":varN}
        var1,var2,...varN must have the same shape

    Returns
    ----------
    -
        Creates '.bin' and '.ctl' file from Dictionary.

    '''

    def _create_bin(path,vars):
        path = rmext(path)
        with open(path+'.bin','wb') as f:
            for v in vars: f.write(v)

    def _create_ctl(path, varnames = None, xdef = None,
                   ydef = None, zdef = 1, tdef = None):
        path = rmext(path)
        if not isinstance(varnames,list): varnames = [varnames]
        nvars = len(varnames)
        name = os.path.split(path)[1]+'.bin'
        with open(path+'.ctl','w+') as f:
            f.write('dset ^{}\n'.format(name))
            f.write('undef 9.e27\n')
            f.write('xdef  {} linear 0 3.75\n'.format(xdef))
            f.write('ydef  {} linear -88.125 3.75\n'.format(ydef))
            f.write('zdef   {} linear 1 1\n'.format(zdef))
            f.write('tdef {} linear 00:00Z1jan2000  12hr\n'.format(tdef))
            f.write('vars {}\n'.format(nvars))
            for v in varnames:
                f.write('{0}  1 0 {0}\n'.format(v))
            f.write('endvars\n')

    if not isinstance(vars,dict):
        raise Exception('vars must be a Dictionary type in the form: ' +
                        '{"namevar1":var1,"namevar2":var2,...,"namevarN":varN}')
    varnames = list(vars.keys())
    nvars = len(varnames)
    varvals = list(vars.values())
    l=[v.shape for v in varvals]
    if not ( l.count(l[0]) == len(l) ):
        raise Exception('var1,var2,...,varN must be of the same size')
    varvals = [constants.to_shape_for_bin(v,type=n) for v,n in zip(varvals,varnames)]
    varvals=[np.float32(v.copy(order='C')) for v in varvals]
    tdef,ydef,xdef = varvals[0].shape
    # WRITE CTL FILE
    _create_ctl(path, varnames = varnames, xdef=xdef,ydef=ydef,tdef=tdef)
    # WRITE BIN FILE
    _create_bin(path,vars = varvals)

def create_clouds(time = None, longitude = None, latitude = None, value = 1,
                  cloud_base = None, outpath = None):
    '''
    Create an artificial cloud matrix file from scratch or by modifying an
    existent cloud matrix.

    Parameters
    ----------
    time : array of str
      Datestr for the extent of the 'time' coordinate, in the form
      [time_min, time_max].
      Default datestr format is '%m-%d' (e.g. '03-04' is 4th March); year
      is automatically set at 2000. To specify your own format
      (for month and day) use the form: [time_min,time_max,format].
      If time is not provided, the default GREB time is used
      (see constants.t() function).

    longitude : array of float
      Extent of the 'lon' coordinate, in the form [lon_min, lon_max].
      Format is E-W degrees -> -180° to 180° (e.g. [-10,70] is from 10E to 70W).
      If longitude is not provided, the default GREB longitude is used
      (see constants.lon() function).

    latitude : array of float
      Extent of the 'lat' coordinate, in the form [lat_min, lat_max].
      Format is S-N degrees -> -90° to 90° (e.g. [-20,40] is from 20S to 40N).
      If latitude is not provided, the default GREB latitude is used
      (see constants.lat() function).

    value : DataArray, nd.array or callable
      Cloud value to be assigned to the dimensions specified in time, latitude
      and longitude. If no dimension is specified, it needs to be the exact matrix
      for cloud values.
      If callable, equals the function to be applied element-wise to the
      "cloud_base" (e.g. "lambda x: x*1.1" means cloud_base scaled by 1.1).

    cloud_base : xarray.DataArray, np.ndarray or str
      Array of the cloud to be used as a reference for the creation of the
      new matrix or full path to the file ('.bin' and '.ctl' files).

    outpath : str
      Full path where the new cloud file ('.bin' and '.ctl' files)
      is saved.
      If not provided, the following default path is chosen:
      '/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial'

    Returns
    ----------
    -
      Creates artificial cloud file ('.bin' and '.ctl' files).

    '''
    def check_lon(min,max):
        if (min*max) > 0:
            return (min<max)
        else:
            return (min>max)
    def switch_lon(x):
        if isinstance(x,list):
            if len(x) == 1:
                return 360+x if x<0 else x
            else:
                return [360+k if k<0 else k for k in x]
        else:
            return 360+x if x<0 else x
    # Define constants
    def_t=constants.t()
    def_lat=constants.lat()
    def_lon=constants.lon()
    dt = constants.dt()
    dx = constants.dx()
    dy = constants.dy()
    # Check coordinates and constrain them
    # TIME
    if time is not None:
        t_exc = '"time" must be an int or date_string in the form [time_min,time_max]\n'+\
              'The date_string must have the format "%m-%d" (e.g. "03-04" for 4th March).\n'+\
              'To specify your own format use the form: [time_min,time_max,format]'
        fmt = '%y-%m-%d'
        if not isinstance(time,list):
            if (isinstance(time,float) or isinstance(time,int) or isinstance(time,str)):
                time = [time]
            else:
                raise Exception(t_exc)
        if len(time) == 1:
            if isinstance(time[0],str):
                t_min = t_max = to_greb_time('00-'+time[0])
            else:
                t_min = t_max = int(time[0])
        elif len(time) == 2:
            if isinstance(time[0],str):
                t_min = to_greb_time('00-'+time[0])
                t_max = to_greb_time('00-'+time[1])
            else:
                t_min = int(time[0])
                t_max = int(time[1])
        elif len(time) == 3:
            if isinstance(time[0],str):
                t_min = to_greb_time('00-'+time[0],'%y-'+time[2])
                t_max = to_greb_time('00-'+time[1],'%y-'+time[2])
            else:
                raise Exception(t_exc)
        else:
            raise Exception(t_exc)
        ind_t=np.where((def_t>=t_min) & (def_t<=t_max))[0]
    else:
        ind_t=np.where((def_t>=def_t.min()) & (def_t<=def_t.max()))[0]
    # LONGITUDE
    if longitude is not None:
        lon_exc = '"longitude" must be a number or in the form [lon_min,lon_max]'
        if (isinstance(longitude,float) or isinstance(longitude,int)):
            longitude = [longitude]
        if isinstance(longitude,list):
            if len(longitude) > 2:
                raise Exception(lon_exc)
            else:
                if np.any(list(map(lambda l: (l > 180 or l < -180),longitude))):
                        raise Exception('"longitude" must be in the range [-180÷180]')
                lon_min,lon_max = switch_lon(longitude)
        else:
            raise Exception(lon_exc)
        if check_lon(lon_min,lon_max):
            ind_lon=np.where((def_lon>=lon_min) & (def_lon<=lon_max))[0]
        else:
            ind_lon=np.where((def_lon>=lon_min) | (def_lon<=lon_max))[0]
    else:
        ind_lon=np.where((def_lon>=def_lon.min()) & (def_lon<=def_lon.max()))[0]
    # LATITUDE
    if latitude is not None:
        lat_exc = '"latitude" must be a number or in the form [lat_min,lat_max]'
        if (isinstance(latitude,float) or isinstance(latitude,int)):
            latitude = [latitude]
        if isinstance(latitude,list):
            if len(latitude) > 2:
                raise Exception(lat_exc)
            else:
                if np.any(list(map(lambda l: (l > 90 or l < -90),latitude))):
                        raise Exception('"latitude" must be in the range [-90÷90]')
                lat_min,lat_max = latitude
        else:
            raise Exception(lat_exc)
        if lat_min < lat_max:
            ind_lat=np.where((def_lat>=lat_min) & (def_lat<=lat_max))[0]
        else:
            ind_lat=np.where((def_lat>=lat_min) | (def_lat<=lat_max))[0]
    else:
        ind_lat=np.where((def_lat>=def_lat.min()) & (def_lat<=def_lat.max()))[0]
    if cloud_base is not None:
        if isinstance(cloud_base,str):
            data=data_from_binary(cloud_base)['cloud']
        elif isinstance(cloud_base,np.ndarray):
            data = cloud_base
        elif isinstance(cloud_base,xr.DataArray):
            data = cloud_base.values
        else:
            raise Exception('"cloud_base" must be a xrray.DataArray or numpy.ndarray'+
                            'matrix of the cloud data, or a valid path to the cloud file.')
        data = constants.to_shape_for_bin(data)
    else:
        data = np.zeros((dt,dy,dx))
    # Change values
    if (isinstance(value,float) or isinstance(value,int) or isinstance(value,np.ndarray)):
        data[ind_t[:,None,None],ind_lat[:,None],ind_lon] = value
    if isinstance(value,xr.DataArray):
        data[ind_t[:,None,None],ind_lat[:,None],ind_lon] = value.values
    elif callable(value):
        data[ind_t[:,None,None],ind_lat[:,None],ind_lon] = value(data[ind_t[:,None,None],ind_lat[:,None],ind_lon])
    else:
        raise Exception('"value" must be a number, numpy.ndarray, xarray.DataArray or function to apply to the "cloud_base" (e.g. "lambda x: x*1.1")')
    # Correct value above 1 or below 0
    data=np.where(data<=1,data,1)
    data=np.where(data>=0,data,0)
    # Write .bin and .ctl files
    vars = {'cloud':data}
    if outpath is None:
        outpath=constants.cloud_folder()+'/cld.artificial.ctl'
    create_bin_ctl(outpath,vars)

def create_solar(time = None, latitude = None, value = 1,
                  solar_base = None, outpath = None):
    '''
    Create an artificial solar matrix file from scratch or by modifying an
    existent solar matrix.

    Parameters
    ----------
    time : array of str
      Datestr for the extent of the 'time' coordinate, in the form
      [time_min, time_max].
      Default datestr format is '%m-%d' (e.g. '03-04' is 4th March); year
      is automatically set at 2000. To specify your own format
      (for month and day) use the form: [time_min,time_max,format].
      If time is not provided, the default GREB time is used
      (see constants.t() function).

    latitude : array of float
      Extent of the 'lat' coordinate, in the form [lat_min, lat_max].
      Format is S-N degrees -> -90° to 90° (e.g. [-20,40] is from 20S to 40N).
      If latitude is not provided, the default GREB latitude is used
      (see constants.lat() function).

    value : float or callable
      Solar value to be assigned to the dimensions specified in time and
      latitude.
      If callable, equals the function to be applied element-wise to the
      "solar_base" (e.g. "lambda x: x*1.1" means solar_base scaled by 1.1).

    solar_base : np.ndarray or str
      Array of the solar to be used as a reference for the creation of the
      new matrix or full path to the file ('.bin' and '.ctl' files).

    outpath : str
      Full path where the new cloud file ('.bin' and '.ctl' files)
      is saved.
      If not provided, the following default path is chosen:
      '/Users/dmar0022/university/phd/greb-official/artificial_solar_radiation/sw.artificial'

    Returns
    ----------
    -
      Creates artificial solar file ('.bin' and '.ctl' files).

    '''

    # Define constants
    def_t=constants.t()
    def_lat=constants.lat()
    dt = constants.dt()
    dy = constants.dy()
    # Check coordinates and constrain them
    # TIME
    if time is not None:
        t_exc = '"time" must be an int or date_string in the form [time_min,time_max]\n'+\
              'The date_string must have the format "%m-%d" (e.g. "03-04" for 4th March).\n'+\
              'To specify your own format use the form: [time_min,time_max,format]'
        fmt = '%y-%m-%d'
        if not isinstance(time,list):
            if (isinstance(time,float) or isinstance(time,int) or isinstance(time,str)):
                time = [time]
            else:
                raise Exception(t_exc)
        if len(time) == 1:
            if isinstance(time[0],str):
                t_min = t_max = to_greb_time('00-'+time[0])
            else:
                t_min = t_max = int(time[0])
        elif len(time) == 2:
            if isinstance(time[0],str):
                t_min = to_greb_time('00-'+time[0])
                t_max = to_greb_time('00-'+time[1])
            else:
                t_min = int(time[0])
                t_max = int(time[1])
        elif len(time) == 3:
            if isinstance(time[0],str):
                t_min = to_greb_time('00-'+time[0],'%y-'+time[2])
                t_max = to_greb_time('00-'+time[1],'%y-'+time[2])
            else:
                raise Exception(t_exc)
        else:
            raise Exception(t_exc)
        ind_t=np.where((def_t>=t_min) & (def_t<=t_max))[0]
    else:
        ind_t=np.where((def_t>=def_t.min()) & (def_t<=def_t.max()))[0]
    # LATITUDE
    if latitude is not None:
        lat_exc = '"latitude" must be a number or in the form [lat_min,lat_max]'
        if (isinstance(latitude,float) or isinstance(latitude,int)):
            latitude = [latitude]
        if isinstance(latitude,list):
            if len(latitude) > 2:
                raise Exception(lat_exc)
            else:
                if np.any(list(map(lambda l: (l > 90 or l < -90),latitude))):
                        raise Exception('"latitude" must be in the range [-90÷90]')
                lat_min,lat_max = latitude
        else:
            raise Exception(lat_exc)
        if lat_min < lat_max:
            ind_lat=np.where((def_lat>=lat_min) & (def_lat<=lat_max))[0]
        else:
            ind_lat=np.where((def_lat>=lat_min) | (def_lat<=lat_max))[0]
    else:
        ind_lat=np.where((def_lat>=def_lat.min()) & (def_lat<=def_lat.max()))[0]
    if solar_base is not None:
        if isinstance(solar_base,str):
            data=data_from_binary(solar_base)['solar']
        elif isinstance(solar_base,np.ndarray):
            data = solar_base
        else:
            raise Exception('"solar_base" must be a valid .ctl or .bin file or a numpy.ndarray matrix of the solar radiation data')
        data = constants.to_shape_for_bin(data,type='solar')
    else:
        data = np.zeros((dt,dy,1))
    # Change values
    if (isinstance(value,float) or isinstance(value,int) or isinstance(value,np.ndarray)):
        data[ind_t[:,None,None],ind_lat[:,None],0] = value
    elif callable(value):
        data[ind_t[:,None,None],ind_lat[:,None],0] = value(data[ind_t[:,None,None],ind_lat[:,None],0])
    else:
        raise Exception('"value" must be a number, numpy.ndarray or function to apply to the "solar_base" (e.g. "lambda x: x*0.9")')
    # Correct value below 0
    data=np.where(data>=0,data,0)
    # Write .bin and .ctl files
    vars = {'solar':data}
    if outpath is None:
        outpath=constants.solar_folder()+'/sw.artificial.ctl'
    create_bin_ctl(outpath,vars)

def data_from_binary(filename,parse=False,time_group=None):
    # 1st version, quicker but not precise on time corrections
    '''
    Get data from a binary ('.bin') file.

    Arguments
    ----------
    filename : str
        Path to the binary ('.bin') file.

    Parameters
    ----------
    parse: Bool
        Set to True if you want the output to be parsed with the custom
        "parse_greb_var" function, otherwise set to False (default).
    time_group : str
        Time grouping method to be chosen between: '12h','day','month','year','season'.
        If chosen, the retrieved data belonging to the same time_group will be
        averaged.
        If "time_group" is smaller than the data time-resolution, a spline
        interpolation is performed.

    Returns
    ----------
    Dictionary
        Dictionary of the data stored in the binary, in the form:
        {'varname1':var1,'varname2':var2,...,'varnameN':varN}

    '''

    # CHECK FLAGS
    if time_group not in ['12h','day','month','year','season',None]:
        raise Exception('time_group must be one of the following:\n'+
                        '"12h","day","month","year","season".')
    # If flag is not "raw" use _data_from_binary (more precise)
    def _data_from_binary(filename,parse=None,time_group=None):
    # 2nd version, slower but precise on time corrections
        data = from_binary(filename,parse=parse,time_group=time_group)
        keys = [d for d in data]
        vals = [data[k].values for k in keys]
        dic = dict(zip(keys,vals))
        return dic

    if parse or time_group is not None:
        return _data_from_binary(filename,parse=parse,time_group=time_group)
    filename = rmext(filename)
    with open(filename+'.ctl','r') as f:
        b=f.read().split('\n')
    ind = np.where(list(map(lambda x: 'vars' in x.split(),b)))[0][0]
    vars=int(b[ind].split()[1])
    dt = int(b[np.where(list(map(lambda x: 'tdef' in x.split(),b)))[0][0]].split()[1])
    dx = int(b[np.where(list(map(lambda x: 'xdef' in x.split(),b)))[0][0]].split()[1])
    dy = int(b[np.where(list(map(lambda x: 'ydef' in x.split(),b)))[0][0]].split()[1])
    keys = []
    for i in np.arange(vars):
        keys.append(b[ind+1+i].split()[0])
    with open(filename+'.bin','rb') as f:
        v = np.fromfile(f,dtype=np.float32).reshape(dt,vars,dy,dx).transpose(1,0,2,3)
        vals=[v[i,...] for i in np.arange(vars)]
    dic = dict(zip(keys,vals))
    return dic

def plot_annual_cycle(coord,*data,legend=True, title='Annual Cycle',
                      draw_point_flag = True):
    '''
    Plot annual cycle for a specific point

    Arguments
    ----------
    coord : tuple
        Tuple of the lat/lon values for the point to plot.
    data : DataArray
        DataArray of the data you want to plot. Further DataArrays can be added
        after the first to overlay multiple data plots for comparison.
        (e.g. plot_annual_cicle(...,data1,data2,..,dataN,...))

    Parameters
    ----------
    legend: Bool
        Set to True (default) if you want the legend to be displayed in the plot.
    var : str
        If clouds are being plotted, can be set to 'cloud' in order to plot the
        values with the proper axes extent.
    draw_point_flag : Bool
        Set to True (default) if you want to plot the position of the specified
        coordinates on the earth.

    Returns
    ----------
    -
        Graph of the annual cycle, for the specified point and data in input.

    '''

    from matplotlib.patheffects import Stroke
    import matplotlib.dates as mdates
    import matplotlib.patches as mpatches

    def draw_point(lat,lon,ax=None):
         x,y = to_Robinson_cartesian(lat,lon)
         patch = lambda x,y: mpatches.Circle((x,y), radius=6e5, color = 'red',
                                                      transform=ccrs.Robinson())
         ax = plt.axes(projection=ccrs.Robinson()) if ax is None else plt.gca()
         ax.stock_img()
         ax.add_patch(patch(x,y))

    i,j=constants.to_greb_indexes(*coord)
    x=constants.t().tolist()
    x=[constants.from_greb_time(a) for a in x]
    for ind,d in enumerate(data):
        if not check_xarray(d,'DataArray'):
            exception_xarray(type = 'DataArray',varname='all data')
        y=d.isel(lat=i,lon=j)
        plt.plot(x,y,label = '{}'.format(ind+1))
    if legend: plt.legend(loc = 'lower left',bbox_to_anchor=(0,1.001))
    plt.grid()
    plt.title(title,fontsize=15)

    if data[0].name == 'cloud':
        plt.ylim([-0.02,1.02])
        m1,m2=plt.xlim()
        plt.hlines(0,m1-100,m2+100,linestyles='--',colors='black',linewidth=0.7)
        plt.hlines(1,m1-100,m2+100,linestyles='--',colors='black',linewidth=0.7)
        plt.xlim([m1,m2])
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))

    if draw_point_flag:
        # Create an inset GeoAxes showing the location of the Point.
        sub_ax = plt.axes([0.8, 0.9, 0.2, 0.2], projection=ccrs.Robinson())
        sub_ax.outline_patch.set_path_effects([Stroke(linewidth=1.5)])
        draw_point(*coord,sub_ax)

def plot_clouds_and_tsurf(*cloudfiles, years_of_simulation=50, coords = None,
                          labels = None):
    '''
    Plot the annual cycle of clouds along with the tsurf response, for the
    specified points.

    Arguments
    ----------
    cloudfiles : str
        Path to the clouds data

    Parameters
    ----------
    years_of_simulation: int
        Number of years for which the forcing simulation has been run
    coords : tuple or list of tuples.
        Lat/Lon coordinates of the point(s) to plot. If not provided the following
        default points will be plotted:
        [(42,12.5),(-37.8,145),(-80,0),(80,0),(0,230)]
    labels : str or list of str
        Legend labels for the plot.

    Returns
    ----------
    -
        Graph(s) of the clouds and tsurf response annual cycle, for the specified
        point(s) and data in input.

    '''
    import matplotlib.ticker as ticker

    cloud = [from_binary(f,time_group='12h').cloud for f in cloudfiles]
    cloud_ctr = from_binary(constants.cloud_def_file(),time_group='12h').cloud
    tfiles = [constants.get_scenario_filename(f,years_of_simulation=years_of_simulation) for f in cloudfiles]
    tsurf = [from_binary(f,time_group='12h').tsurf for f in tfiles]
    tsurf_ctr = from_binary(constants.control_def_file(),time_group='12h').tsurf

    cloud_anomaly = [c.anomalies(cloud_ctr) for c in cloud]
    tsurf_anomaly = [t.anomalies(tsurf_ctr) for t in tsurf]
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
        plot_annual_cycle(coord,*tsurf_anomaly,draw_point_flag=False)
        ax2.set_ylim([-5,5])
        ax2.set_title('tsurf anomaly annual cycle',fontsize=10)
        ax2.get_legend().remove()
        for tick in ax2.xaxis.get_major_ticks(): tick.label.set_fontsize(6.5)
        ax2.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))

        ax3 = plt.subplot(gs[1, 0])
        plot_annual_cycle(coord,*cloud,draw_point_flag=False)
        ax3.set_ylim([0,1])
        ax3.set_title('cloud annual cycle',fontsize=10)
        ax3.get_legend().remove()
        for tick in ax3.xaxis.get_major_ticks(): tick.label.set_fontsize(6.5)

        ax4 = plt.subplot(gs[1,1])
        plot_annual_cycle(coord,*tsurf,draw_point_flag=False)
        ax4.set_ylim([223,323])
        ax4.set_title('tsurf annual cycle',fontsize=10)
        ax4.get_legend().remove()
        for tick in ax4.xaxis.get_major_ticks(): tick.label.set_fontsize(6.5)
        ax4.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.0f'))

        axP = plt.gcf().axes[1]
        axP.set_position([0.265, 0.95, 0.5, 0.15])

def _check_units(x1,x2):
    '''
    Check units matching between Datarrays or Datasets
    '''

    if not np.all([check_xarray(x1),check_xarray(x2)]):
        raise Exception('Input arrays must be xarray.DataArray or xarray.Dataset')
    exc = 'Units don''t match!'
    if check_xarray(x1,'DataArray'):
        if check_xarray(x2,'DataArray'):
            if x1.attrs['units'] != x2.attrs['units']:
                raise Exception(exc)
        else:
            if x1.attrs['units'] != x2[x1.name].attrs['units']:
                raise Exception(exc)
    else:
        if check_xarray(x2,'DataArray'):
            for var in x1:
                if var == x2.name:
                    if x1[var].attrs['units'] != x2.attrs['units']:
                        raise Exception(exc)
        else:
            for var in set([d for d in x1])&set([d for d in x2]):
                if x1[var].attrs['units'] != x2[var].attrs['units']:
                    raise Exception(exc)

# ============================================================================ #
# ============================================================================ #
# ============================================================================ #
# ============================================================================ #

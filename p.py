from myfuncs import *
from myfuncs import _check_units

def fun(y):
    attrs = y.attrs
    newy=np.repeat(y,(x.time.shape[0])/12,axis=0).assign_coords(time=x.time.values)
    newy.attrs = attrs
    return newy


x=from_binary(constants.scenario_2xCO2())
x_base=from_binary(constants.control_def_file())



# x_base=from_binary(constants.control_def_file())
x_base = None
copy=True
update_attrs=True

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

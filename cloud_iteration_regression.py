# LIBRARIES
from greb_climatevar import * # Import self defined classes and function
ignore_warnings()
from scipy import interpolate

def subtract_each_2(v):
    l=[]
    for a,b in zip(np.arange(v.shape[0]-1),np.arange(2,v.shape[0]+2-1)):
        l.append(a); l.append(b)
    dv=-np.subtract.reduceat(v,l[:-1])[::2]
    return dv

def spline_interp(y):
    mdays=np.array([31,28,31,30,31,30,31,31,30,31,30,31])
    y=y[np.cumsum(mdays*2)-1]
    y=np.insert(y,0,y[0])
    y=np.append(y,y[-1])
    x = (constants.t()/24)[np.cumsum(mdays*2)-1]-15
    x=np.insert(x,0,x[0]-30)
    x=np.append(x,x[-1]+30)
    spl= interpolate.UnivariateSpline(x, y,k=3,s=0)
    x_=constants.t()/24
    y_=spl(x_)
    return y_

# define files
control_fname = constants.control_def_file()
t_old_init_fname = '/Users/dmar0022/university/phd/greb-official/output/scenario.exp-20.2xCO2'
t_new_init_fname = '/Users/dmar0022/university/phd/greb-official/output/scenario.exp-930.geoeng.cld.artificial.frominput_x1.1'
cld_old_init_fname = constants.cloud_file()
cld_new_init_fname = get_art_cloud_filename(t_new_init_fname)
niter=input_(1)
time = input_('monthly_regression',2)

t_fname = lambda n: '/Users/dmar0022/university/phd/greb-official/output/scenario.exp-930.geoeng.cld.artificial.iter{}_{}'.format(n,time)
cld_fname = lambda n: get_art_cloud_filename(t_fname(n))
t=lambda n,t: data_from_binary(t_fname(n),t)['tsurf']
cld=lambda n,t: data_from_binary(cld_fname(n),t)['cloud']

# #========================================================================== #
# # ANNUAL MEAN DATA
if time == 'annual_regression':
    CLD = np.zeros([niter+1,48,96])
    T = np.zeros([niter+1,48,96])
    T[0,...]=data_from_binary(t_old_init_fname)['tsurf'].mean(axis=0)
    T[1,...]=data_from_binary(t_new_init_fname)['tsurf'].mean(axis=0)
    CLD[0,...]=data_from_binary(cld_old_init_fname)['cloud'].mean(axis=0)
    CLD[1,...]=data_from_binary(cld_new_init_fname)['cloud'].mean(axis=0)
    if niter>1:
        for n in np.arange(1,niter):
            T[n+1,...] = (t(n,'raw').mean(axis=0))
            CLD[n+1,...] = (cld(n,'raw').mean(axis=0))
            CLD_base=cld(niter-1,'raw')
    else:
        CLD_base=data_from_binary(cld_new_init_fname)['cloud']

elif time == 'monthly_regression':
    mdays=np.array([31,28,31,30,31,30,31,31,30,31,30,31])
    CLD = np.zeros([niter+1,12,48,96])
    T = np.zeros([niter+1,12,48,96])
    T[0,...]=data_from_binary(t_old_init_fname,'monthly')['tsurf']
    T[1,...]=data_from_binary(t_new_init_fname,'monthly')['tsurf']
    CLD[0,...]=data_from_binary(cld_old_init_fname,'monthly')['cloud']
    CLD[1,...]=data_from_binary(cld_new_init_fname,'monthly')['cloud']
    if niter>1:
        for n in np.arange(1,niter):
            T[n+1,...] = t(n,'monthly')
            CLD[n+1,...] = cld(n,'monthly')
            CLD_base=cld(niter-1,'raw')
    else:
        CLD_base=data_from_binary(cld_new_init_fname,'raw')['cloud']

dT = subtract_each_2(T)
dCLD = subtract_each_2(CLD)
Tc = data_from_binary(control_fname,'monthly')['tsurf']
dT_c = T[-1,...]-Tc

if niter > 1:
    dCLD_new = multidim_regression(dT,dCLD,dT_c,axis=0)
else:
    THETA=(dCLD/dT).squeeze()
    dCLD_new = -THETA*dT_c

if time == 'monthly_regression':
    dCLD_new = np.repeat(dCLD_new,mdays*2,axis=0)
    s=dCLD_new.shape
    dCLD_new_int = np.zeros([*s])
    for i in np.arange(s[1]):
        for j in np.arange(s[2]):
            dCLD_new_int[:,i,j]=spline_interp(dCLD_new[:,i,j])
    dCLD_new = dCLD_new_int

new_cloud = (CLD_base+dCLD_new).squeeze()

new_name = '/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial.iter{}_{}'.format(niter,time)
create_clouds(value = new_cloud,cloud_base=None, outpath=new_name)

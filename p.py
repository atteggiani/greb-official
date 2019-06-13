# LIBRARIES
from greb_climatevar import * # Import self defined classes and function
ignore_warnings()

def sub_each_n(v,n=2,axis=0):
    l=[]
    for a,b in zip(np.arange(v.shape[axis]-1),np.arange(n,v.shape[axis]+n-1)):
        l.append(a); l.append(b)
    dv=-np.subtract.reduceat(v,l[:-1])[::n]
    return dv

# define files
control_fname = constants.control_def_file()
t_old_init_fname = '/Users/dmar0022/university/phd/greb-official/output/scenario.exp-20.2xCO2'
t_new_init_fname = '/Users/dmar0022/university/phd/greb-official/output/scenario.exp-930.geoeng.cld.artificial.frominput_x1.1'
cld_old_init_fname = constants.cloud_file()
cld_new_init_fname = get_art_cloud_filename(t_new_init_fname)
niter=input_(1,5)
time = input_('annual',6)

t_fname = lambda n: '/Users/dmar0022/university/phd/greb-official/output/scenario.exp-930.geoeng.cld.artificial.iter{}_{}'.format(n,time)
cld_fname = lambda n: get_art_cloud_filename(t_fname(n))
t=lambda n,t: data_from_binary(t_fname(n),t)['tsurf']
cld=lambda n,t: data_from_binary(cld_fname(n),t)['cloud']
dot_ = lambda x,y: np.einsum('abcd,abdf->abcf',x,y)

time = 'monthly'
niter = 20
# #========================================================================== #
# # ANNUAL MEAN DATA
if time == 'annual_regress':
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

    dT = sub_each_n(T)
    dCLD = sub_each_n(CLD)
    Tc = data_from_binary(control_fname)['tsurf'].mean(axis=0)
    dT_c = T[-1,...]-Tc

    if niter > 1:
        X = np.insert(dT[:,np.newaxis].transpose([2,3,0,1]),0,1,axis=3)
        y = dCLD[:,np.newaxis].transpose([2,3,0,1])
        THETA=dot_(np.linalg.inv(dot_(X.transpose([0,1,3,2]),X)),dot_(X.transpose([0,1,3,2]),y))
        X_pred = np.insert(dT_c[np.newaxis,np.newaxis,:].transpose([2,3,0,1]),0,1,axis=2)
        Y_pred = dot_(THETA.transpose([0,1,3,2]),X_pred)
        new_cloud = (CLD[-1,...]-Y_pred).squeeze()
        CLD_base=CLD_base[...,np.newaxis,np.newaxis]
    else:
        THETA=(dCLD/dT).squeeze()
        Y_pred = THETA*dT_c

    new_cloud = (CLD_base-Y_pred).squeeze()

if time == 'monthly':
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
            CLD_base=cld(niter-1,'monthly')
    else:
        CLD_base=data_from_binary(cld_new_init_fname,'monthly')['cloud']

    # dT = sub_each_n(T)
    # dCLD = sub_each_n(CLD)
    # Tc = data_from_binary(control_fname)['tsurf'].mean(axis=0)
    # dT_c = T[-1,...]-Tc





# i=20;j=50
# x=np.insert(dT[:,i,j].reshape(niter,1),0,1,axis=1)
# y=dCLD[:,i,j].reshape(niter,1)
# x_pred = np.insert(dT_c[i,j,np.newaxis],0,1,axis=0).reshape(2,1)
# plt.scatter(x[:,1],y)
# theta=np.linalg.inv(x.T.dot(x)).dot(x.T.dot(y))
# y_pred = theta.T.dot(x_pred)
# xxx=np.insert(np.arange(-2,2,0.1).reshape(40,1),0,1,axis=1)
# yyy=xxx.dot(theta)
# plt.scatter(x[:,1],y,c='blue')
# plt.plot(xxx[:,1],yyy,color='red')
# plt.scatter(x_pred[1,:],y_pred,c='red')

new_name = '/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial.iter{}_{}'.format(niter,time)
create_clouds(value = new_cloud,cloud_base=None, outpath=new_name)

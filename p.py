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
t=lambda n: data_from_binary(t_fname(n))['tsurf']
cld=lambda n: data_from_binary(cld_fname(n))['cloud']
CLD = np.zeros([niter+1,48,96])
T = np.zeros([niter+1,48,96])

# #========================================================================== #
# # ANNUAL MEAN DATA
if time == 'annual':
    T[0,...]=data_from_binary(t_old_init_fname)['tsurf'].mean(axis=0)
    T[1,...]=data_from_binary(t_new_init_fname)['tsurf'].mean(axis=0)
    CLD[0,...]=data_from_binary(cld_old_init_fname)['cloud'].mean(axis=0)
    CLD[1,...]=data_from_binary(cld_new_init_fname)['cloud'].mean(axis=0)
    if niter>1:
        for n in np.arange(1,niter):
            T[n+1,...] = (t(n).mean(axis=0))
            CLD[n+1,...] = (cld(n).mean(axis=0))
    dT = sub_each_n(T)
    dCLD = sub_each_n(CLD)
    Tc = data_from_binary(control_fname)['tsurf'].mean(axis=0)
    dT_c = T[-1,...]-Tc

linv_ = lambda A: np.linalg.solve(A.T.dot(A), A.T)
dot_ = lambda x,y: np.einsum('abcd,abdf->abcf',x,y)
X = np.insert(dT[:,np.newaxis].transpose([2,3,0,1]),0,1,axis=3)
y = dCLD[:,np.newaxis].transpose([2,3,0,1])
THETA=dot_(np.linalg.inv(dot_(X.transpose([0,1,3,2]),X)),dot_(X.transpose([0,1,3,2]),y))

i=4;j=22
X_=np.insert(dT[:,i,j].reshape(20,1),0,1,axis=1)
y_=dCLD[:,i,j].reshape(20,1)
theta=np.linalg.inv(X_.T.dot(X_)).dot(X_.T.dot(y_))
theta
THETA[i,j,...]
xx=np.arange(-2.5,0.5+0.1,0.1).reshape(31,1)
yy=np.dot(np.insert(xx,0,1,axis=1),theta)
plt.scatter(X,y)
plt.plot(xx,yy)

a=np.arange(12).reshape(1,2,3,2)
b=np.arange(4).reshape(1,2,2,1)
a[0,0,...].dot(b[0,0,...])
a[0,1,...].dot(b[0,1,...])
a.transpose([0,1,3,2]),a)

r_cld = dCLD/dT
dCLD_new = -r_cld*(t_new_am-t_c_am)
new_cloud = dCLD_new+CLD[-1,...]

new_name = '/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial.iter{}_{}'.format(niter,time)
create_clouds(value = new_cloud,cloud_base=None, outpath=new_name)

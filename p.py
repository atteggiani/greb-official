from myfuncs import *
import matplotlib.colors as colors

r_cld=from_binary('r_calibration').r
data_filename=os.path.join(constants.output_folder(),
                 'scenario.exp-930.geoeng.cld.artificial.iter20_50yrs')
data=from_binary(data_filename)[['tsurf','precip']]
anomalies=data.anomalies()
a=anomalies.annual_mean().tsurf
b=anomalies.seasonal_cycle().tsurf
c=anomalies.annual_mean().precip

cm0=cm.Spectral_r
col1=cm0(np.linspace(0,0.4,102))
w1=np.array(list(map(lambda x: np.linspace(x,1,26),col1[-1]))).transpose()
col2=cm0(np.linspace(0.6,1,102))
w2=np.array(list(map(lambda x: np.linspace(1,x,26),col2[0]))).transpose()
cols=np.vstack([col1,w1,w2,col2])
my_cmap = colors.LinearSegmentedColormap.from_list('my_colormap', cols)

a.plotvar(levels=np.arange(-1,1+0.01,0.01),cmap=my_cmap,
          cbar_kwargs={'ticks':np.arange(-1,1+0.2,0.2)})

c.plotvar(levels=np.arange(-0.1,0.1+0.001,0.001),cmap=my_cmap,
          cbar_kwargs={'ticks':np.arange(-0.1,0.1+0.02,0.02)})

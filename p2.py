#!python
from myfuncs import *
import matplotlib.colors as colors
from pylab import *
from numpy import outer

def plot_cb(cmap=None):
    rc('text', usetex=False)
    a=transpose(outer(arange(0,1,0.01),ones(5)))
    figure(figsize=(10,5))
    subplots_adjust(top=0.8,bottom=0.05,left=0.01,right=0.99)
    subplot(111)
    axis("off")
    imshow(a,aspect='auto',cmap=cmap,origin="lower")

col1=cm.Spectral(np.linspace(0,0.4,102))
w1=np.array(list(map(lambda x: np.linspace(x,1,26),col1[-1]))).transpose()
col2=cm.Spectral(np.linspace(0.6,1,102))
w2=np.array(list(map(lambda x: np.linspace(1,x,26),col2[0]))).transpose()
cols=np.vstack([col1,w1,w2,col2])
my_cmap = colors.LinearSegmentedColormap.from_list('my_colormap', cols)

plot_cb(cmap=cm.Spectral)
plot_cb(cmap=my_cmap)

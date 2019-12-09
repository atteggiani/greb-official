from myfuncs import *

a=from_binary('./r_calibration.bin').r
a.annual_mean().plotvar(cmap=cm.viridis,
                        levels=np.arange(-10,0+0.2,0.2))
a.global_mean().plot()

b=from_binary('/Users/dmar0022/Desktop/dietmar_script/data/greb.cloud.sensitivity.best-guess.gad').rcld
b.annual_mean().plotvar(cmap=cm.viridis,
                        levels=np.arange(-10,0+0.2,0.2))
b.global_mean().plot()                        

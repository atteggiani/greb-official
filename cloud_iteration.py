import warnings
warnings.filterwarnings("ignore")
import myfuncs as my
import numpy as np 
import os
from argparse import ArgumentParser

t_init_fname = my.GREB.output_folder()+'/scenario.exp-930.geoeng.2xCO2.cld.artificial.frominput_x1.1_50yrs'

# niter=1
# t_fname = t_init_fname
# ocean_flag = ""
# corr = 0.15

# PARSE ARGUMENTS
parser=ArgumentParser()
parser.add_argument('--it',type=int)
parser.add_argument('-t','--t_init',type=str)
parser.add_argument('-c','--corr',type=np.float)
parser.add_argument('-o','--ocean',action="store_true")
args=parser.parse_args()
niter=args.it
t_fname=args.t_init
ocean_flag = "_ocean" if args.ocean else ""
corr=args.corr

r_cld=my.GREB.from_binary(my.GREB.greb_folder()+'/r_calibration_cloud').r

folder = my.GREB.cloud_folder()+'/cld.artificial.iteration{}'.format(ocean_flag)
os.makedirs(folder,exist_ok=True)

if niter == 1:
    cld_fname = my.GREB.get_art_forcing_filename(t_fname,'cloud')
else:
    cld_fname = my.GREB.get_art_forcing_filename(t_fname,'cloud',output_path=folder)
cld_base = my.GREB.from_binary(cld_fname).cloud

dt = my.GREB.from_binary(t_fname).tsurf.anomalies()

ny=1
dt = dt.isel(time=slice(-12*ny,None)).group_by('12h')
dCLD_new = -(corr/r_cld)*(dt)
dCLD_new=dCLD_new.where(np.abs(r_cld)>=1,0) # Correction for small r_cld

# If ocean_flag is active, change clouds only over ocean
if ocean_flag is "_ocean":
    new_cloud = np.where(my.GREB.land_ocean_mask(),dCLD_new+cld_base,cld_base)
else:
    new_cloud = dCLD_new+cld_base

new_name = os.path.join(folder,'cld.artificial.iter{}{}'.format(niter,ocean_flag))
my.GREB.create_clouds(value = new_cloud, outpath=new_name)

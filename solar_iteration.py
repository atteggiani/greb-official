import warnings
warnings.filterwarnings("ignore")
import myfuncs as my
import numpy as np 
import os
from argparse import ArgumentParser

t_init_fname = my.GREB.output_folder()+'/scenario.exp-931.geoeng.2xCO2.sw.artificial.frominput_x0.98_50yrs'

# niter=1
# t_fname = t_init_fname
# ocean_flag = ""
# corr=0.2

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

r_sw=my.GREB.from_binary(my.GREB.greb_folder()+'/r_calibration_solar').r

folder = my.GREB.solar_folder()+'/sw.artificial.iteration{}'.format(ocean_flag)
os.makedirs(folder,exist_ok=True)

if niter == 1:
    sw_fname = my.GREB.get_art_forcing_filename(t_fname,'solar')
else:
    sw_fname = my.GREB.get_art_forcing_filename(t_fname,'solar',output_path=folder)
sw_base = my.GREB.from_binary(sw_fname).solar

dt = my.GREB.from_binary(t_fname).tsurf.anomalies()

ny=1
dt = dt.isel(time=slice(-12*ny,None)).group_by('12h')
dsw_new = -(corr/r_sw)*(dt)
dsw_new=dsw_new.where(r_sw!=1,0) # Correction for small r_sw
dsw_new=dsw_new.mean('lon')
# If ocean_flag is active, change clouds only over ocean
if ocean_flag is "_ocean":
    new_solar = np.where(my.GREB.land_ocean_mask(),dsw_new+sw_base,sw_base)
else:
    new_solar = dsw_new+sw_base

new_name = os.path.join(folder,'sw.artificial.iter{}{}'.format(niter,ocean_flag))
my.GREB.create_solar(value = new_solar, outpath=new_name)

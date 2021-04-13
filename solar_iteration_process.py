import warnings
warnings.filterwarnings("ignore")
from myfuncs import GREB as greb
import numpy as np 
import os
from argparse import ArgumentParser

t_init_fname = greb.output_folder()+'/scenario.exp-931.geoeng.2xCO2.sw.artificial.frominput_x0.98_50yrs'

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

S_sw=greb.from_binary(os.path.join(greb.greb_folder(),'S_sensitivity/solar/Ssw')).S

folder = os.path.join(greb.solar_folder(),f'sw.artificial.iteration{ocean_flag}_{corr}corr')
os.makedirs(folder,exist_ok=True)

if niter == 1:
    sw_fname = greb.get_art_forcing_filename(t_fname,'solar')
else:
    sw_fname = greb.get_art_forcing_filename(t_fname,'solar',output_path=folder)
sw_base = greb.from_binary(sw_fname).solar

dt = greb.from_binary(t_fname).tsurf.anomalies()

ny=1
dt = dt.isel(time=slice(-12*ny,None)).group_by('12h')
dsw_new = -(corr/S_sw)*(dt)
# dsw_new=dsw_new.where(S_sw!=1,0) # Correction for small S_sw
# If ocean_flag is active, change solar only over ocean
if ocean_flag == "_ocean":
    new_solar = np.where(greb.land_ocean_mask(),dsw_new+sw_base,sw_base)
else:
    new_solar = dsw_new+sw_base

new_name = os.path.join(folder,f'sw.artificial.iter{niter}{ocean_flag}_{corr}corr')
greb.create_solar(value = new_solar, outpath=new_name)

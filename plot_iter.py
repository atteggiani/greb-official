# LIBRARIES
import warnings
warnings.filterwarnings("ignore")
from argparse import ArgumentParser
import myfuncs as my 
from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt
import os
import numpy as np

parser=ArgumentParser()
parser.add_argument('-f','--forcing',type=str,default="cloud")
parser.add_argument('-o','--ocean', action='store_true')
parser.add_argument('-e','--exp',type=str,default="930")
parser.add_argument('-i','--init',type=str,
                    default=my.GREB.output_folder()+'scenario.exp-930.geoeng.2xCO2.cld.artificial.frominput_x1.1_50yrs')
parser.add_argument('-a','--all', action='store_true') # If included plot all iteration, otherwise plots only the last
parser.add_argument('-c','--corr',type=np.float)
args=parser.parse_args()

art_forcing_type=args.forcing
ocean_flag = "_ocean" if args.ocean else ""
exp_num = args.exp
filename_first_correction = args.init
plot_all = args.all
corr=args.corr
ntimesteps = 30*12

if art_forcing_type == "cloud":
    shortname='cld'
    art_forcing_folder=my.GREB.cloud_folder()
elif art_forcing_type == "solar":
    shortname='sw'
    art_forcing_folder=my.GREB.solar_folder()
else:
    raise Exception("Artificial forcing type must be either 'cloud' or 'solar'.")

exp_name = my.GREB.get_exp_name(exp_num)
sim_years = my.GREB.get_years_of_simulation(filename_first_correction)

rms_a = []
rms_s = []

name_base = os.path.split(my.GREB.control_def_file())[1]

filename_original = my.GREB.scenario_2xCO2()
data = my.GREB.from_binary(filename_original)
rms_a.append(data.annual_mean().anomalies().rms().tsurf.values)
rms_s.append(data.seasonal_cycle().anomalies().rms().tsurf.values)

data = my.GREB.from_binary(filename_first_correction)
rms_a.append(data.annual_mean().anomalies().rms().tsurf.values)
rms_s.append(data.seasonal_cycle().anomalies().rms().tsurf.values)

# Setting figures output directories
outdir=os.path.join(my.GREB.figures_folder(),
        'scenario.{}.{}.artificial.iteration{}_{}yrs_{}corr'.format(exp_name,shortname,ocean_flag,sim_years,corr))
os.makedirs(outdir,exist_ok=True)      
niter = 1
filename = lambda it: os.path.join(my.GREB.output_folder(),
        'scenario.{}.{}.artificial.iter{}{}_{}yrs'.format(exp_name,shortname,it,ocean_flag,sim_years))

while os.path.isfile(my.rmext(filename(niter))+'.bin'):
    print('-- Iter. {}'.format(niter))
    # Import data
    data = my.GREB.from_binary(filename(niter))
    rms_a.append(data.annual_mean(ntimesteps).anomalies().rms().tsurf.values)
    rms_s.append(data.seasonal_cycle(ntimesteps).anomalies().rms().tsurf.values)
    if (plot_all) or not os.path.isfile(my.rmext(filename(niter+1))+'.bin'):
        art_forcing_filename = my.GREB.get_art_forcing_filename(filename(niter),forcing = art_forcing_type, output_path = art_forcing_folder+'/{}.artificial.iteration'.format(shortname))
        # Setting figures output directories
        outdir_abs=os.path.join(outdir,'iter{}'.format(niter),'absolute')
        outdir_diff=os.path.join(outdir,'iter{}'.format(niter),'diff_'+name_base)
        # Creating figures output directories
        os.makedirs(outdir_abs,exist_ok=True)
        os.makedirs(outdir_diff,exist_ok=True)

        art_forcing = my.GREB.from_binary(art_forcing_filename); art_forcing=art_forcing[next(iter(art_forcing))]

        print('   Plotting Iter. {} ...'.format(niter))
        # ANNUAL MEAN
        data[['tsurf','precip']].annual_mean(ntimesteps).plotall(outpath=outdir_abs)
        plt.figure() ; art_forcing.annual_mean(ntimesteps).plotvar(outpath=os.path.join(outdir_abs,"{}.amean.png".format(art_forcing_type)))
        data[['tsurf','precip']].annual_mean(ntimesteps).anomalies().plotall(outpath=outdir_diff)
        plt.figure() ; art_forcing.annual_mean(ntimesteps).anomalies().plotvar(outpath=os.path.join(outdir_diff,"{}.amean.anom.png".format(art_forcing_type)))

        # SEASONAL CYCLE
        data[['tsurf','precip']].seasonal_cycle(ntimesteps).plotall(outpath=outdir_abs)
        plt.figure() ; art_forcing.seasonal_cycle(ntimesteps).plotvar(outpath=os.path.join(outdir_abs,"{}.seascyc.png".format(art_forcing_type)))
        data[['tsurf','precip']].seasonal_cycle(ntimesteps).anomalies().plotall(outpath=outdir_diff)
        plt.figure() ; art_forcing.seasonal_cycle(ntimesteps).anomalies().plotvar(outpath=os.path.join(outdir_diff,"{}.seascyc.anom.png".format(art_forcing_type)))

    niter += 1

print('\nPlotting rms...')
# plot rms annual mean
plt.figure()
plt.plot(np.arange(1,niter+2),rms_a,linewidth=1.5,color='Red')
plt.title('Improvement Annual Mean')
plt.xlabel('N. Iteration')
plt.ylabel('rms')
plt.xlim([1,niter+1])
plt.xticks(ticks=np.arange(1,niter+2),labels=['O','O*']+np.arange(1,niter).tolist())
plt.ylim(bottom=0)
plt.gca().yaxis.set_minor_locator(MultipleLocator(0.1))
plt.grid(which='both')
plt.savefig(outdir+'/improvement_amean.png')

# plot rms seasonal cycle
plt.figure()
plt.plot(np.arange(1,niter+2),rms_s,linewidth=1.5,color='Red')
plt.title('Improvement Seasonal Cycle')
plt.xlabel('N. Iteration')
plt.ylabel('rms')
plt.xlim([1,niter+1])
plt.xticks(ticks=np.arange(1,niter+2),labels=['O','O*']+np.arange(1,niter).tolist())
plt.ylim(bottom=0)
plt.gca().yaxis.set_minor_locator(MultipleLocator(0.1))
plt.grid(which='both')
plt.savefig(outdir+'/improvement_seascyc.png')

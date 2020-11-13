# LIBRARIES
import warnings
warnings.filterwarnings("ignore")
from argparse import ArgumentParser
from myfuncs import * # Import self defined classes and function
from matplotlib.ticker import MultipleLocator

parser=ArgumentParser()
parser.add_argument('-f','--forcing',type=str,default="cloud")
parser.add_argument('-o','--ocean', action='store_true')
parser.add_argument('-e','--exp',type=str,default="930")
parser.add_argument('-i','--init',type=str,
                    default=Constants.greb.output_folder()+'scenario.exp-930.geoeng.2xCO2.cld.artificial.frominput_x1.1_50yrs')
parser.add_argument('-a','--all', action='store_true') # If included plot all iteration, otherwise plots only the last
args=parser.parse_args()

art_forcing_type=args.forcing
ocean_flag = "_ocean" if args.ocean else ""
exp_num = args.exp
filename_first_correction = args.init
plot_all = args.all

if art_forcing_type == "cloud":
    shortname='cld'
    art_forcing_folder=Constants.greb.cloud_folder()
elif art_forcing_type == "solar":
    shortname='sw'
    art_forcing_folder=Constants.greb.solar_folder()
else:
    raise Exception("Artificial forcing type must be either 'cloud' or 'solar'.")

exp_name = Constants.greb.get_exp_name(exp_num)
sim_years = Constants.greb.get_years_of_simulation(filename_first_correction)

rms_a = []
rms_s = []

name_base = os.path.split(Constants.greb.control_def_file())[1]

filename_original = Constants.greb.scenario_2xCO2()
data = from_binary(filename_original)
rms_a.append(data.annual_mean().anomalies().rms().tsurf.values)
rms_s.append(data.seasonal_cycle().anomalies().rms().tsurf.values)

data = from_binary(filename_first_correction)
rms_a.append(data.annual_mean().anomalies().rms().tsurf.values)
rms_s.append(data.seasonal_cycle().anomalies().rms().tsurf.values)

# Setting figures output directories
outdir=os.path.join(Constants.greb.figures_folder(),
        'scenario.{}.{}.artificial.iteration{}_{}yrs'.format(exp_name,shortname,ocean_flag,sim_years))
niter = 1
filename = lambda it: os.path.join(Constants.greb.output_folder(),
        'scenario.{}.{}.artificial.iter{}{}_{}yrs'.format(exp_name,shortname,it,ocean_flag,sim_years))

while os.path.isfile(rmext(filename(niter))+'.bin'):
    print('-- Iter. {}'.format(niter))
    # Import data
    data = from_binary(filename(niter))
    rms_a.append(data.annual_mean().anomalies().rms().tsurf.values)
    rms_s.append(data.seasonal_cycle().anomalies().rms().tsurf.values)
    if (plot_all) or not os.path.isfile(rmext(filename(niter+1))+'.bin'):
        art_forcing_filename = Constants.greb.get_art_forcing_filename(filename(niter),forcing = art_forcing_type, output_path = art_forcing_folder+'/{}.artificial.iteration'.format(shortname))
        # Setting figures output directories
        outdir_abs=os.path.join(outdir,'iter{}'.format(niter),'absolute')
        outdir_diff=os.path.join(outdir,'iter{}'.format(niter),'diff_'+name_base)
        # Creating figures output directories
        os.makedirs(outdir_abs,exist_ok=True)
        os.makedirs(outdir_diff,exist_ok=True)

        art_forcing = from_binary(art_forcing_filename); art_forcing=art_forcing[next(iter(art_forcing))]

        print('   Plotting Iter. {} ...'.format(niter))
        # ANNUAL MEAN
        data[['tsurf','precip']].annual_mean().plotall(outpath=outdir_abs)
        plt.figure() ; art_forcing.annual_mean().plotvar(outpath=os.path.join(outdir_abs,"{}.amean.png".format(art_forcing_type)))
        data[['tsurf','precip']].annual_mean().anomalies().plotall(outpath=outdir_diff)
        plt.figure() ; art_forcing.annual_mean().anomalies().plotvar(outpath=os.path.join(outdir_diff,"{}.amean.anom.png".format(art_forcing_type)))

        # SEASONAL CYCLE
        data[['tsurf','precip']].seasonal_cycle().plotall(outpath=outdir_abs)
        plt.figure() ; art_forcing.seasonal_cycle().plotvar(outpath=os.path.join(outdir_abs,"{}.seascyc.png".format(art_forcing_type)))
        data[['tsurf','precip']].seasonal_cycle().anomalies().plotall(outpath=outdir_diff)
        plt.figure() ; art_forcing.seasonal_cycle().anomalies().plotvar(outpath=os.path.join(outdir_diff,"{}.seascyc.anom.png".format(art_forcing_type)))

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

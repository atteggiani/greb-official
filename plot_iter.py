# LIBRARIES
from myfuncs import * # Import self defined classes and function
from matplotlib.ticker import MultipleLocator

r_fixed_flag = input_('_nf')
filename_first_correction = input_(r'/Users/dmar0022/university/phd/greb-official/output/scenario.exp-930.geoeng.cld.artificial.frominput_x1.1_50yrs',2)
try: sim_years = constants.get_years_of_simulation(filename_first_correction)
except: sim_years = None
sim_years = input_(sim_years,3)

rms_a = []
rms_s = []

filename_base = constants.control_def_file()
name_base = os.path.split(filename_base)[1]
data_base =  from_binary(filename_base)

filename_original = constants.scenario_2xCO2()
data = from_binary(filename_original)
rms_a.append(data.annual_mean().anomalies(data_base).rms().tsurf.values)
rms_s.append(data.seasonal_cycle().anomalies(data_base).rms().tsurf.values)

data = from_binary(filename_first_correction)
rms_a.append(data.annual_mean().anomalies(data_base).rms().tsurf.values)
rms_s.append(data.seasonal_cycle().anomalies(data_base).rms().tsurf.values)

# Setting figures output directories
outdir=os.path.join(constants.figures_folder(),
                    'scenario.exp-930.geoeng.cld.artificial.iteration_monthly{}_{}yrs'.format(r_fixed_flag,sim_years))


niter = 1
filename = os.path.join(constants.output_folder(),
                        'scenario.exp-930.geoeng.cld.artificial.iter{}_monthly{}_{}yrs'.format(niter,r_fixed_flag,sim_years))
while os.path.isfile(rmext(filename)+'.bin'):
    # Setting figures output directories
    outdir_abs=os.path.join(outdir,'iter{}'.format(niter),'absolute')
    outdir_diff=os.path.join(outdir,'iter{}'.format(niter),'diff_'+name_base)
    # Creating figures output directories
    os.makedirs(outdir_abs,exist_ok=True)
    os.makedirs(outdir_diff,exist_ok=True)

    # Import data
    data = from_binary(filename)

    print('Plotting Iter. {}...'.format(niter))
    # ANNUAL MEAN
    rms_a.append(data.annual_mean().anomalies(data_base).rms().tsurf.values)
    data[['tsurf','precip']].annual_mean().plotall(outpath=outdir_abs)
    data[['tsurf','precip']].annual_mean().anomalies(data_base).plotall(outpath=outdir_diff)
    # SEASONAL CYCLE
    rms_s.append(data.seasonal_cycle().anomalies(data_base).rms().tsurf.values)
    data[['tsurf','precip']].seasonal_cycle().plotall(outpath=outdir_abs)
    data[['tsurf','precip']].seasonal_cycle().anomalies(data_base).plotall(outpath=outdir_diff)

    niter += 1
    filename = os.path.join(constants.output_folder(),
                            'scenario.exp-930.geoeng.cld.artificial.iter{}_monthly{}_{}yrs'.format(niter,r_fixed_flag,sim_years))
print('Plotting rms...')
# plot rms_a
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
plt.close()

# plot rms_s
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
plt.close()

print('Done!!!')

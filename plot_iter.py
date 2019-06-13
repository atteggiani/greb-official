# LIBRARIES
from greb_climatevar import * # Import self defined classes and function
ignore_warnings()

time = input_('monthly',1)

niter = 1
rms = []

filename_base = r'/Users/dmar0022/university/phd/greb-official/output/control.default'
name_base = os.path.split(filename_base)[1]
outfile_base = filename_base + '.nc'
bin2netCDF(filename_base)
data_base = parsevar(iris.load(outfile_base))

filename_original = r'/Users/dmar0022/university/phd/greb-official/output/scenario.exp-20.2xCO2'
bin2netCDF(filename_original)
data = parsevar(iris.load(filename_original+'.nc'))
ts = data[[v.var_name for v in data].index('tsurf')]
TS=plot_param.from_cube(ts).to_annual_mean().to_anomalies(data_base)
rms.append(TS.rms())
os.remove(filename_original+'.nc')

filename_first_correction = r'/Users/dmar0022/university/phd/greb-official/output/scenario.exp-930.geoeng.cld.artificial.frominput_x1.1'
bin2netCDF(filename_first_correction)
data = parsevar(iris.load(filename_first_correction+'.nc'))
ts = data[[v.var_name for v in data].index('tsurf')]
TS=plot_param.from_cube(ts).to_annual_mean().to_anomalies(data_base)
rms.append(TS.rms())
os.remove(filename_first_correction+'.nc')

filename = r'/Users/dmar0022/university/phd/greb-official/output/scenario.exp-930.geoeng.cld.artificial.iter{}_{}'.format(str(niter),time)
while os.path.isfile(rmext(filename)+'.bin'):
    # Read scenario and base file
    filename_art_cloud=get_art_cloud_filename(filename)
    name = os.path.split(filename)[1]
    outfile = filename + '.nc'
    name_art_cloud = os.path.split(filename_art_cloud)[1]

    # Setting figures output directories
    outdir=os.path.join('/Users/dmar0022/university/phd/greb-official/figures',name)
    outdir_diff=os.path.join(outdir,'diff_'+name_base)

    # Creating figures output directories
    os.makedirs(outdir_diff,exist_ok=True)

    # Converting bin file to netCDF
    bin2netCDF(filename)

    # Importing the data cube
    data = parsevar(iris.load(outfile))

    ts = data[[v.var_name for v in data].index('tsurf')]
    TS=plot_param.from_cube(ts).to_annual_mean().to_anomalies(data_base)
    rms.append(TS.rms())
    # # plot annual mean
    plt.figure()
    TS.assign_var().plot(outpath=outdir_diff)
    # # plot seasonal cycle
    plt.figure()
    plot_param.from_cube(ts).to_seasonal_cycle().to_anomalies(data_base).assign_var().plot(outpath=outdir_diff)
    os.remove(outfile)
    niter += 1
    filename = r'/Users/dmar0022/university/phd/greb-official/output/scenario.exp-930.geoeng.cld.artificial.iter{}_{}'.format(str(niter),time)
os.remove(outfile_base)

# plot rms
plt.figure()
plt.plot(np.arange(1,niter+2),rms,linewidth=1.5,color='Red')
plt.title('Algorithm improvement')
plt.xlabel('N. Iteration')
plt.ylabel('rms')
plt.xlim([1,niter+1])
plt.xticks(ticks=np.arange(1,niter+2),labels=['O','O*']+np.arange(1,niter).tolist())
plt.ylim(ymin=0)
plt.savefig(outdir+'/improvement_'+name+'.png')

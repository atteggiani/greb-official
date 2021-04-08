import warnings
warnings.simplefilter("ignore")
from myfuncs import GREB as greb
import numpy as np
from itertools import islice,product as iproduct, count
import concurrent.futures as cf
# import time
import os
from argparse import ArgumentParser

parser=ArgumentParser()
parser.add_argument('--nlat',type=int,default=10)
parser.add_argument('--nlon',type=int,default=20)
args=parser.parse_args()
nlat=args.nlat
nlon=args.nlon

def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result

def main(bound):
    l,ll = bound[0],bound[1]
    sw_name = 'sw.artificial.lat.{:.0f}_{:.0f}lon.{:.0f}_{:.0f}'.format(l[0],l[1],ll[0],ll[1])
    greb.create_solar(latitude=l, longitude=ll,
                    time=['2000-12-01','2000-02-28'],
                    value = lambda x: x - 0.1,
                    outpath=os.path.join(output_folder,f"{sw_name}_DJF"))
    greb.create_solar(latitude=l, longitude=ll,
                    time=['2000-03-01','2000-05-31'],
                    value = lambda x: x - 0.1,
                    outpath=os.path.join(output_folder,f"{sw_name}_MAM"))
    greb.create_solar(latitude=l, longitude=ll,
                    time=['2000-06-01','2000-08-31'],
                    value = lambda x: x - 0.1,
                    outpath=os.path.join(output_folder,f"{sw_name}_JJA"))
    greb.create_solar(latitude=l, longitude=ll,
                    time=['2000-09-01','2000-11-30'],
                    value = lambda x: x - 0.1,
                    outpath=os.path.join(output_folder,f"{sw_name}_SON"))

tot=nlat*nlon
lat=greb.lat()[np.round(np.linspace(0, greb.dy() - 1, nlat+1)).astype(int)]
lon=np.append(greb.lon(),360.)[np.round(np.linspace(0, greb.dx(), nlon+1)).astype(int)]
output_folder = greb.solar_folder()+'/S_sensitivity'
os.makedirs(output_folder,exist_ok=True)
n=count(1)
bounds=iproduct(window(lat),window(lon))
print(f'0/{tot}',end="\r")
if __name__ == '__main__':
    with cf.ProcessPoolExecutor() as executor:
        for _ in executor.map(main, bounds):
            print(f'{next(n)}/{tot}',end="\r")



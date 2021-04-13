import warnings
warnings.simplefilter("ignore")
from myfuncs import GREB as greb
import myfuncs as my
import numpy as np
from itertools import islice,product as iproduct, count
import concurrent.futures as cf
import time
import os
from argparse import ArgumentParser
import matplotlib.cm as cm

greb.create_solar(value=lambda x:x*0.5,tridimensional=True,outpath=os.path.join(greb.solar_folder(),"test3D"))

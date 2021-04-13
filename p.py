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

a=greb.from_binary("/Users/dmar0022/university/phd/greb-official/S_sensitivity/solar/Ssw.bin").S
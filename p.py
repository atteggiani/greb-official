# LIBRARIES
from greb_climatevar import * # Import self defined classes and function
ignore_warnings()

# Read scenario and base file
filename = r'/Users/dmar0022/university/phd/greb-official/output/scenario.exp-930.geoeng.cld.artificial.frominputX1.1'
filename_base = r'/Users/dmar0022/university/phd/greb-official/output/control.default'
# filename_art_cloud = '/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial.frominputX1.1'

filename = input_file(filename,1)
filename_base = input_file(filename_base,2)

# Read artificial cloud (if any)
filename_art_cloud=get_art_cloud_filename(filename)
if filename_art_cloud: filename_art_cloud=input_file(filename_art_cloud,3)

create_clouds(longitude=...,latitude=..., value = lambda x: x*1.1, cloud_base = constants.cloud_file())
data_from_binary('/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial.frominputX1.1')['cloud'] - \
data_from_binary('/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial')['cloud']

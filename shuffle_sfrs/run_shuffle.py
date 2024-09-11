#import MyShuffle as shuffle
import MyShuffle_shuffle_sat_group_ps as shuffle
import importlib
importlib.reload(shuffle)
import sys
from multiprocessing import Pool
import numpy as np
import time

start_time = time.time()

initial_seed = int(sys.argv[1])
final_seed = int(sys.argv[2])

def string2number(string):
	number = float(string)
	if number.is_integer():
		return int(number)
	else:
		return round(number, 1)

logMmin = string2number(sys.argv[3])
logMmax = string2number(sys.argv[4])
Nsplit= string2number(sys.argv[5])
Nsplit2= string2number(sys.argv[6])
#shuffler = shuffle.Shuffler(ps_type="gal", object2shuffle="gal")
#shuffler.bin_data(mhalo_min=12.5)

shuffler = shuffle.Shuffler(ps_type="group", object2shuffle="sat",include_bh=True, include_halo_structure=True, include_msat_sum=True, include_conc_proxy=True)

start_read = time.time()
#shuffler.bin_data(mhalo_min=logMmin, mhalo_max=logMmax)
#shuffler.bin_data(mhalo_min=logMmin)
#shuffler.bin_data(mhalo_max=logMmax)
shuffler.bin_data()

end_read = time.time()

time_read = end_read - start_read
print(f"Time taken to read: {time_read} s")


seeds = np.arange(initial_seed, final_seed)

def shuffle(seed):
	shuffler.shuffle_in_bins(seed=seed, Nsplit=Nsplit, split_property="msat_sum", Nsplit2=Nsplit2, split_property2="dMdyn", split_test=False)

pool = Pool()
results = pool.map(shuffle, seeds)
pool.close()

end_time = time.time()

time_taken = end_time - start_time
print(f"Total time taken: {time_taken} s")


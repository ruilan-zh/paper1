import numpy as np
from collections import Counter
import random
import os
import h5py
from multiprocessing import Process



class Shuffler:
	def __init__(self, ps_type, object2shuffle, snapnum=40, boxsize=205, include_bh=False, include_conc=False):

		if ps_type not in ["gal", "cent", "group"]:
			raise Exception('ps_type has to be one of "gal", "cent" or "group"')

		if ps_type == "cent":
			if object2shuffle != "cent":
				raise Exception('For ps_type="cent", object2shuffle must equal "cent"')
		elif ps_type == "group":
			if object2shuffle != "group":
				raise Exception('For ps_type="group", object2shuffle must equal "group"')
		elif ps_type == "gal":
			if object2shuffle not in ["gal", "cent", "sat"]:
				raise Exception('For ps_type="gal", object2shuffle has to be one of "gal", "cent" or "sat"')




		self.ps_type = ps_type
		self.object2shuffle = object2shuffle
		self.snapnum = snapnum
		self.boxsize=boxsize
		self.include_bh = include_bh
		self.include_conc = include_conc

		self.mhalo_main = None
		self.mhalo_binned = None



		

	def read_tng(self):
	
		base_dir = f"/cosma7/data/dp004/dc-zhan5/TNG/snap{self.snapnum}/SubhaloFlag_all/mvir"
		ihalo_dir = f"{base_dir}/ihalo"
		if self.include_bh:
			ihalo_dir = f"{base_dir}/ihalo/bh_mass"
			
		if self.ps_type == "group":
			# Read positions of groups (including SFR=0)
			print("Reading", f"{ihalo_dir}/sfr-halomass_sum.txt")
			tng_data_sum = np.loadtxt(f"{ihalo_dir}/sfr-halomass_sum.txt")
			mask_min_sum = tng_data_sum[:,1] > 10
			ihalo_tng_sum = tng_data_sum[:,0][mask_min_sum]
			mhalo_tng_sum = tng_data_sum[:,1][mask_min_sum]
			pos_tng_sum = tng_data_sum[:,2:5][mask_min_sum]
			sfr_tng_sum = tng_data_sum[:,5][mask_min_sum]

			ihalo_main = ihalo_tng_sum
			mhalo_main = mhalo_tng_sum
			pos_main = pos_tng_sum
			sfr_main = sfr_tng_sum
		else:
			# Read positions of central subhalos with nonzero SFR
			print("Reading", f"{ihalo_dir}/sfr-halomass_central.txt")
			tng_data1 = np.loadtxt(f"{ihalo_dir}/sfr-halomass_central.txt")

			mask_min = tng_data1[:,1] > 10
			ihalo_tng1 = tng_data1[:,0][mask_min]
			mhalo_tng1 = tng_data1[:,1][mask_min]
			pos_tng1 = tng_data1[:,2:5][mask_min]
			sfr_tng1 = tng_data1[:,5][mask_min]
			if self.include_bh:
				bh_tng1 = tng_data1[:,6][mask_min]

			# Read positions of central subhalos with zero SFR
			print("Reading", f"{ihalo_dir}/sfr-cent_0sfr.txt")
			tng_data2 = np.loadtxt(f"{ihalo_dir}/sfr-cent_0sfr.txt")

			mask_min2 = tng_data2[:,1] > 10
			ihalo_tng2 = tng_data2[:,0][mask_min2]
			mhalo_tng2 = tng_data2[:,1][mask_min2]
			pos_tng2 = tng_data2[:,2:5][mask_min2]
			sfr_tng2 = tng_data2[:,5][mask_min2]
			if self.include_bh:
				bh_tng2 = tng_data2[:,6][mask_min2]


			# Concatenate arrays of central subhalos with zero and nonzero SFR
			ihalo_main = np.concatenate((ihalo_tng1,ihalo_tng2))
			mhalo_main = np.concatenate((mhalo_tng1,mhalo_tng2))
			pos_main = np.concatenate((pos_tng1,pos_tng2))
			sfr_main = np.concatenate((sfr_tng1,sfr_tng2))
			if self.include_bh:
				bh_main = np.concatenate((bh_tng1,bh_tng2))
		 
	   
			if self.ps_type != "cent":
				# Read absolute positions of the satellite subhalos (relative to box)
				print("Reading", f"{ihalo_dir}/sfr-halomass_satellite.txt")
				tng_data_sat_abs = np.loadtxt(f"{ihalo_dir}/sfr-halomass_satellite.txt")

				mask_min = tng_data_sat_abs[:,1] > 10
				ihalo_tng_sat_abs = tng_data_sat_abs[:,0][mask_min]
				mhalo_tng_sat_abs = tng_data_sat_abs[:,1][mask_min]
				pos_tng_sat_abs = tng_data_sat_abs[:,2:5][mask_min]
				sfr_tng_sat_abs = tng_data_sat_abs[:,5][mask_min]
				
				self.ihalo_sat_abs = ihalo_tng_sat_abs.astype(int)
				self.mhalo_sat_abs = mhalo_tng_sat_abs
				self.pos_sat_abs = pos_tng_sat_abs
				self.sfr_sat_abs = sfr_tng_sat_abs

					
				if self.object2shuffle != "cent":
					# Read positions of satellite subhalos relative to their corresponding central subhalo
					print("Reading", f"{ihalo_dir}/sfr-halomass_satellite_relative.txt")
					tng_data_sat_rel = np.loadtxt(f"{ihalo_dir}/sfr-halomass_satellite_relative.txt")
					mask_min = tng_data_sat_rel[:,1] > 10
					ihalo_tng_sat_rel = tng_data_sat_rel[:,0][mask_min]
					mhalo_tng_sat_rel = tng_data_sat_rel[:,1][mask_min]
					pos_tng_sat_rel = tng_data_sat_rel[:,2:5][mask_min]
					sfr_tng_sat_rel = tng_data_sat_rel[:,5][mask_min]
					
					self.ihalo_sat_rel = ihalo_tng_sat_rel.astype(int)
					self.mhalo_sat_rel = mhalo_tng_sat_rel
					self.pos_sat_rel = pos_tng_sat_rel
					self.sfr_sat_rel = sfr_tng_sat_rel
		
		
		self.ihalo_main = ihalo_main.astype(int)
		self.mhalo_main = mhalo_main
		self.pos_main = pos_main
		self.sfr_main = sfr_main
		if self.include_bh:
			self.bh_mass_main = bh_main
			
			
			
		if self.include_conc:
			basePath = '/cosma7/data/dp004/dc-zhan5/TNG300-1'
			halo_path = f"{basePath}/postprocessing/halo_structure"
			fname_halo = f"{halo_path}/halo_structure_0{self.snapnum}.hdf5"
			f = h5py.File(fname_halo, 'r')
			c200c_all = np.array(f["c200c"])
			c200c = c200c_all[self.ihalo_main]
			#c200c = np.where(np.isnan(c200c), -1, c200c)
			self.conc_main = c200c
			
			

		

	def create_mask(self, mhalo_min, mhalo_max, sfr_min, sfr_max, bh_mass_min, bh_mass_max):
		mass_mask = (self.mhalo_main > mhalo_min) & (self.mhalo_main < mhalo_max)
		if sfr_min is None:
			sfr_mask = (self.sfr_main < sfr_max)
		else:
			sfr_mask = (self.sfr_main < sfr_max) & (self.sfr_main > sfr_min)

		if self.include_bh:
			if bh_mass_min is None:
				bh_mask = self.bh_mass_main < bh_mass_max
			else:
				bh_mask = (self.bh_mass_main < bh_mass_max) & (self.bh_mass_main > bh_mass_min)

			main_mask = mass_mask & sfr_mask & bh_mask
		else:
			main_mask = mass_mask & sfr_mask

		return main_mask

	def bin_data(self, dp=1, mhalo_min=0, mhalo_max=20, sfr_max = 5, sfr_min=None, bh_mass_max=20, bh_mass_min=None):
		if self.mhalo_main is None:
			self.read_tng()
		self.mask_main = self.create_mask(mhalo_min, mhalo_max, sfr_min, sfr_max, bh_mass_min, bh_mass_max)

		
		if mhalo_min == 0:
			if mhalo_max != 20:
				mhalo_mask_name = f"logMmax{mhalo_max}"
			else:
				mhalo_mask_name = ""
		else:
			if mhalo_max != 20:
				mhalo_mask_name = f"logM{mhalo_min}-{mhalo_max}"
			else:
				mhalo_mask_name = f"logMmin{mhalo_min}"

		if sfr_max == 5:
			if sfr_min == None:
				sfr_mask_name = ""
			else:
				sfr_mask_name = f"logSFRmin{sfr_min}"
		else:
			if sfr_min == None:
				sfr_mask_name = f"logSFRmax{sfr_max}"
			else:
				sfr_mask_name = f"logSFR{sfr_min}-{sfr_max}"

		if bh_mass_max == 20:
			if bh_mass_min == None:
				bh_mask_name = ""
			else:
				bh_mask_name = f"logMBHmin{bh_mass_min}"
		else:
			if bh_mass_min == None:
				bh_mask_name = f"logMBHmax{bh_mass_max}"
			else:
				bh_mask_name = f"logMBH{bh_mass_min}-{bh_mass_max}"



		self.mask_main_name = f"{mhalo_mask_name}/{sfr_mask_name}/{bh_mask_name}"
		
		# Bin the data according to their mass
		dlogM = 1/10**dp
		print(dlogM)
		mhalo_bins = np.round(np.arange(8, 15, dlogM),dp)
		print(len(mhalo_bins))

		ihalo_binned = []
		mhalo_binned = []
		sfr_binned = []
		pos_binned = []
		conc_binned = []
		count1 = 0
		for i, mhalo_val in enumerate(mhalo_bins):
			#mask_bin = np.round(self.mhalo_main[self.mask_main], dp) == np.round(mhalo_val, dp) 
			mask_bin = (self.mhalo_main[self.mask_main] > mhalo_val) & (self.mhalo_main[self.mask_main] < mhalo_val+dlogM)

			ihalo_binned.append(self.ihalo_main[self.mask_main][mask_bin]) 
			count1 += len(self.ihalo_main[self.mask_main][mask_bin])
			mhalo_binned.append(self.mhalo_main[self.mask_main][mask_bin])
			sfr_binned.append(self.sfr_main[self.mask_main][mask_bin])
			pos_binned.append(self.pos_main[self.mask_main][mask_bin])
			if self.include_conc:
				conc_binned.append(self.conc_main[self.mask_main][mask_bin])






		self.ihalo_binned = ihalo_binned
		self.mhalo_binned = mhalo_binned
		self.sfr_binned = sfr_binned
		self.pos_binned = pos_binned
		self.conc_binned = conc_binned
		
		self.ihalo_masked = np.concatenate(ihalo_binned)
		
		
		

	def shuffle_in_bins(self, seed=0, do_shuffle=True, do_polyfit=False, odir="/cosma7/data/dp004/dc-zhan5/shuffled", N_conc_split=1, split_test=False
):
		#initial_seed = seeds[0]
		#final_seed = seeds[-1]

		## N_conc_split gives the number of groups split into by concentration
		## 1 means split into one group (i.e. no split)

		if not isinstance(N_conc_split, int):
			raise ValueError("N_conc_split argument must be an integer.")
		if N_conc_split < 1:
			raise ValueError("N_conc_split argument must be 1 or greater")

		if self.mhalo_binned is None:
			self.bin_data()

		# Shuffle the objects

		count_cent = 0
		count_sat = 0
		#for seed in range(initial_seed,final_seed):
		random.seed(seed)

		shuffled_sfrs = []
		shuffled_ihalo = []

		polyfit_list = []

		for ibin in range(len(self.mhalo_binned)):
			if len(self.sfr_binned[ibin]) > 0:
				indices = np.arange(0,len(self.sfr_binned[ibin]),1) 
				random.shuffle(indices) # shuffle order of halos in bin

				if do_shuffle:
					if do_polyfit:
						mask = np.isinf(self.sfr_binned[ibin]) == False 
						if (np.sum(mask) > 0) and len(self.sfr_binned[ibin]) > 1: # Make sure there are at least 2 halos with nonzero SFR
							# Compute best fit line using nonzero SFRs only
							a, b = np.polyfit(self.mhalo_binned[ibin][mask], self.sfr_binned[ibin][mask], 1) # Find line of best fit in bin
							polyfit_list.append((a,b))

							sfr_diff = np.array(self.sfr_binned[ibin] - (a*self.mhalo_binned[ibin]  + b)) # Compute difference between SFR and line of best fit for each galaxy

							shuffled_sfrs.append(sfr_diff[indices] + (a*self.mhalo_binned[ibin]  + b)) # shuffle the differences, then add difference on to best fit value for given halo mass
							shuffled_ihalo.append(np.array(self.ihalo_binned[ibin])[indices])
						else: 
							# If fewer than 2 nonzero SFRs in bin, then just keep SFRs as they are
							shuffled_sfrs.append(np.array(self.sfr_binned[ibin]))
							shuffled_ihalo.append(np.array(self.ihalo_binned[ibin]))
					else: 
						# Just shuffle in bins normally
						if N_conc_split == 1:
							shuffled_sfrs.append(np.array(self.sfr_binned[ibin])[indices]) 
							shuffled_ihalo.append(np.array(self.ihalo_binned[ibin])[indices])
						else:
							#conc_median = np.median(np.array(self.conc_binned[ibin]))
							conc_not_nan_mask = np.isnan(self.conc_binned[ibin]) == False
							conc_nan_mask = np.isnan(self.conc_binned[ibin]) == True
			
							
							indices_orig = np.arange(0, len(self.conc_binned[ibin]))
							indices_shuffled = np.arange(0, len(self.conc_binned[ibin]))
							#print("indices_orig: ", indices_orig)
							
							#conc_median = np.median(np.array(self.conc_binned[ibin][conc_not_nan_mask]))
							#percentiles_list = [0, 25, 50, 75, 100]
							
							intervals = 100/N_conc_split
							percentiles_list = np.arange(0,101, intervals)
							not_nan_concs = np.array(self.conc_binned[ibin][conc_not_nan_mask])
							conc_percentiles = np.percentile(not_nan_concs, percentiles_list)
							# interpolation="higher" means that instead of taking average between two middle values, I take the higher one
							
							bin_assignments_not_nan = np.tile(np.arange(N_conc_split),len(not_nan_concs)//N_conc_split + 1)[:len(not_nan_concs)]
							random.shuffle(bin_assignments_not_nan)

							bin_assignments = np.arange(0, len(self.conc_binned[ibin]))
							bin_assignments[conc_not_nan_mask] = bin_assignments_not_nan


							

							for ip in range(N_conc_split):

								if split_test is False:
									if ip == 0:
										percentile_mask = conc_not_nan_mask & (self.conc_binned[ibin] < conc_percentiles[ip+1])
									elif ip == N_conc_split - 1: # Last bin
										percentile_mask =  conc_not_nan_mask & (self.conc_binned[ibin] >= conc_percentiles[ip])
									else:
										percentile_mask = conc_not_nan_mask & (self.conc_binned[ibin] >= conc_percentiles[ip]) & (self.conc_binned[ibin]  < conc_percentiles[ip+1]) # the percentile value is the higher one - that value is included in next bin
									indices_percentiles = indices_orig[percentile_mask]
									random.shuffle(indices_percentiles)
									indices_shuffled[percentile_mask] = indices_percentiles
								else:
									indices_mask =  bin_assignments == ip
									indices_in_bin = indices_orig[indices_mask]
									random.shuffle(indices_in_bin)
									indices_shuffled[indices_mask] = indices_in_bin
									



								

							indices_nan = indices_orig[conc_nan_mask]
							random.shuffle(indices_nan)
							indices_shuffled[conc_nan_mask] = indices_nan
							#print("indices_shuffled_low", indices_shuffled)


							
							print(percentiles_list)
							
							shuffled_sfrs.append(np.array(self.sfr_binned[ibin])[indices_shuffled]) 
							shuffled_ihalo.append(np.array(self.ihalo_binned[ibin])[indices_shuffled])
							
							

				else:
					# No shuffling (for tests)
					shuffled_sfrs.append(np.array(self.sfr_binned[ibin]))
					shuffled_ihalo.append(np.array(self.ihalo_binned[ibin]))   
			else:
				# If no halos in bin
				shuffled_sfrs.append([])
				shuffled_ihalo.append([])
				polyfit_list.append(None)
		print("Shuffling halos done")

		if self.object2shuffle == "gal" or self.object2shuffle == "sat":
			print("Shuffling satellites")
			# shuffle satellites
			new_sat_pos = np.empty_like(self.pos_sat_rel)
			new_sat_sfr = np.empty_like(self.sfr_sat_rel)
			new_sat_mhalo = np.empty_like(self.mhalo_sat_rel)
			index_prev = 0


			
			for ibin in range(len(self.mhalo_binned)):
				if len(self.sfr_binned[ibin]) > 0:
					### We want to match satellites to central galaxies with the same ihalo (the position of the central galaxy will have changed if we have shuffled ###
					### We want to add on the relative position of the satellite to this new central position, so we get new satellite positions relative to the box ###
					### First we only consider satellites corresponding to centrals that have been shuffled (ihalo_binned[ibin] and shuffled_ihalo[ibin] only includes centrals we want to shuffle - those that are included in mask)
					if do_shuffle:
						cent_ihalos_in_bin = shuffled_ihalo[ibin]
					else:
						cent_ihalos_in_bin = self.ihalo_binned[ibin]


					# Find satellite galaxies corresponding to centrals in bin
					mask_sat = np.isin(self.ihalo_sat_rel, cent_ihalos_in_bin)
					n_sat_in_bin = np.sum(mask_sat)

					if n_sat_in_bin > 0:
						sort_indices = np.argsort(cent_ihalos_in_bin)
						cent_ihalos_in_bin_sorted = cent_ihalos_in_bin[sort_indices]

						pos_binned_sorted = self.pos_binned[ibin][sort_indices]

						pos_sat_in_bin = self.pos_sat_rel[mask_sat] + pos_binned_sorted[np.searchsorted(cent_ihalos_in_bin_sorted, self.ihalo_sat_rel[mask_sat])]
	# np.searchsorted returns first index in cent_ihalos_in_bin_sorted which corresponds to self.ihalo_sat_rel[mask_sat] 



						index_next = index_prev+n_sat_in_bin
						new_sat_pos[index_prev:index_next] = pos_sat_in_bin
						new_sat_sfr[index_prev:index_next] = self.sfr_sat_rel[mask_sat]
						new_sat_mhalo[index_prev:index_next] = self.mhalo_sat_rel[mask_sat]

						index_prev = index_next
			nsat_shuffle = index_next
			nsat_tot = len(self.sfr_sat_rel)
			print("Total number of satellites in box:", nsat_tot)		
			print("Number of satellites shuffled:", nsat_shuffle)
			mask_large = new_sat_pos[:nsat_shuffle] > 205
			mask_small = new_sat_pos[:nsat_shuffle] < 0
			n_out = np.sum(mask_large) + np.sum(mask_small)
			print("Nsat outside of box:", n_out)
			new_sat_pos[:nsat_shuffle] = np.where(mask_large, new_sat_pos[:nsat_shuffle] - 205, new_sat_pos[:nsat_shuffle])
			new_sat_pos[:nsat_shuffle] = np.where(mask_small, new_sat_pos[:nsat_shuffle] + 205, new_sat_pos[:nsat_shuffle])

			if nsat_shuffle != nsat_tot:
				## Some satellites will not have been selected if they don't correspond to centrals in ihalo_binned - some centrals might have been excluded by self.mask_main
				#shuffled_cent_ihalos = np.concatenate(self.ihalo_binned)
				# self.ihalo_masked includes all halos that are to be shuffled
				# We want to find the ihalo_sat which are not shuffled (therefore invert = True)
				mask_not_shuffled_sats = np.isin(self.ihalo_sat_abs, self.ihalo_masked, invert=True) 
				print("Number of satellites not shuffled:", np.sum(mask_not_shuffled_sats))
				assert nsat_tot- nsat_shuffle == np.sum(mask_not_shuffled_sats)
				## Add satellites which have not been shuffled
				new_sat_pos[nsat_shuffle:nsat_tot] = self.pos_sat_abs[mask_not_shuffled_sats]
				new_sat_sfr[nsat_shuffle:nsat_tot] = self.sfr_sat_abs[mask_not_shuffled_sats]
				new_sat_mhalo[nsat_shuffle:nsat_tot] = self.mhalo_sat_abs[mask_not_shuffled_sats]

		if do_shuffle:
			shuffle_name =""
		else:
			shuffle_name="_not_shuffled"
		
		if N_conc_split == 1:
			conc_split_name = ""
		else:
			#conc_split_name = "conc_split2"
			if split_test == False:
				conc_split_name = f"conc_split_nan/conc_split{N_conc_split}"
			else:
				conc_split_name = f"conc_split_nan/test_split{N_conc_split}"


		odir1 =f"{odir}/logM10_dlogM0.1_snap{self.snapnum}/changed_bins/{self.ps_type}_ps/shuffle_{self.object2shuffle}/{self.mask_main_name}/{conc_split_name}"
		if not os.path.exists(odir1):
			try:
				os.makedirs(odir1)
			except FileExistsError:
				        pass
		fname = f"{odir1}/seed{seed}{shuffle_name}.txt"

		f_out = open(fname, "w")


		print("# log10(mass[Msun/h]) x[Mpc/h] y[Mpc/h] z[Mpc/h] log10(sfr[Msun/yr])", file=f_out)
		# Print shuffled halos

		# Either central or group
		for ibin in range(len(self.mhalo_binned)):
			if len(self.sfr_binned[ibin]) > 0:
				for ihalo in range(len(self.sfr_binned[ibin])):
					if self.object2shuffle == "sat":
						# If we are shuffling satellites only, keep central the same
						sfr1 = self.sfr_binned[ibin][ihalo]
					else:
						sfr1 = shuffled_sfrs[ibin][ihalo]

					if sfr1 > -5:
						print(self.mhalo_binned[ibin][ihalo], self.pos_binned[ibin][ihalo][0], self.pos_binned[ibin][ihalo][1], self.pos_binned[ibin][ihalo][2], sfr1, file=f_out)
						count_cent += 1


		if self.ps_type == "gal":
			## If including satellites
			if self.object2shuffle == "cent":
				## If only shuffling centrals then we can keep satellites as they are
				for i in range(len(self.mhalo_sat_abs)):
					print(self.mhalo_sat_abs[i], self.pos_sat_abs[i][0], self.pos_sat_abs[i][1], self.pos_sat_abs[i][2], self.sfr_sat_abs[i], file=f_out)
			else:
				## If satellite positions have been changed
				for i in range(nsat_tot):
					#if (new_sat_mhalo[i] > 10) :
					#print(new_sat_mhalo[i], new_sat_pos[i][0], new_sat_pos[i][1], new_sat_pos[i][2], new_sat_sfr[i], file = f_out)
					print(new_sat_mhalo[i], new_sat_pos[i][0], new_sat_pos[i][1], new_sat_pos[i][2], new_sat_sfr[i], file = f_out)
					count_sat += 1


		

		# Print unshuffled halos (if mask_main is not empty)
		mhalo_tng_min = self.mhalo_main[~self.mask_main]
		pos_tng_min = self.pos_main[~self.mask_main]
		sfr_tng_min = self.sfr_main[~self.mask_main]
		for i in range(len(mhalo_tng_min)):
			if sfr_tng_min[i] > -5:
				print(mhalo_tng_min[i], pos_tng_min[i][0],pos_tng_min[i][1],pos_tng_min[i][2], sfr_tng_min[i], file = f_out)
		
		f_out.close()
		print("Written to ", fname)

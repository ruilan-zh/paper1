import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '/cosma/home/dp004/dc-zhan5')
import os

import MyHaloPS as ps
import importlib
importlib.reload(ps)

#arr = np.arange(-3, -2, 0.1)
#arr = np.arange(10, 11.6, 0.1)
#index = int(sys.argv[2])
#sfr_lim = arr[index]

snapnum=40
ihalo = True
#sim = "tng100-1"
boxsize_eagle = 100*0.6777
sim = "tng300-1"
SubhaloFlag=False
metallicity=False
#tng_dir = "/cosma7/data/dp004/dc-zhan5/tng-sfr"
#tng_dir = f"/cosma7/data/dp004/dc-zhan5/TNG/snap{snapnum}/ihalo/test"
if sim == "tng100-1":
    tng_dir = f"/cosma8/data/dp004/dc-zhan5/TNG/tng100-1/snap{snapnum}"
elif sim == "tng300-1":
    #tng_dir = f"/cosma7/data/dp004/dc-zhan5/TNG/snap{snapnum}/SubhaloFlag=1/mvir/w_metallicity"
    #tng_dir = f"/cosma7/data/dp004/dc-zhan5/TNG/snap{snapnum}/SubhaloFlag_all/mfof"
    if SubhaloFlag is False:
        if ihalo is True:
            tng_dir = f"/cosma7/data/dp004/dc-zhan5/TNG/snap{snapnum}/SubhaloFlag_all/mvir/ihalo"
            if metallicity:
                tng_dir = f"/cosma7/data/dp004/dc-zhan5/TNG/snap{snapnum}/SubhaloFlag_all/mvir/ihalo/SubhaloGasMetallicitySfrWeighted"
        else:
            tng_dir = f"/cosma7/data/dp004/dc-zhan5/TNG/snap{snapnum}/SubhaloFlag_all/mvir"
            #tng_dir = f"/cosma7/data/dp004/dc-zhan5/TNG/snap{snapnum}/SubhaloFlag_all/mfof"
    else:
        if ihalo is True:
            tng_dir = f"/cosma7/data/dp004/dc-zhan5/TNG/snap{snapnum}/SubhaloFlag=1/mvir/ihalo"
else:
    raise CustomError(f"{sim} simulation not recognised")


#tng_dir = f"/cosma7/data/dp004/dc-zhan5/TNG/snap{snapnum}/mvir/w_metallicity"
#tng_dir = f"/cosma7/data/dp004/dc-zhan5/TNG/snap{snapnum}/w_metallicity_cent_flag=1"
halo_type="group"


if halo_type == "gal":
    tng_data1 = np.loadtxt(f"{tng_dir}/sfr-halomass_central.txt")
    tng_data2 = np.loadtxt(f"{tng_dir}/sfr-halomass_satellite.txt")


    #tng_data1 = np.loadtxt(f"{tng_dir}/sfr-cent-tng.txt")
    #tng_data2 = np.loadtxt(f"{tng_dir}/sfr-sat-tng.txt")


    if ihalo is False:
        mhalo_tng1 = tng_data1[:,0]
        pos_tng1 = tng_data1[:,1:4]
        sfr_tng1 = tng_data1[:,4]

        mhalo_tng2 = tng_data2[:,0]
        pos_tng2 = tng_data2[:,1:4]
        sfr_tng2 = tng_data2[:,4]
    else:
        mhalo_tng1 = tng_data1[:,1]
        pos_tng1 = tng_data1[:,2:5]
        sfr_tng1 = tng_data1[:,5]

        mhalo_tng2 = tng_data2[:,1]
        pos_tng2 = tng_data2[:,2:5]
        sfr_tng2 = tng_data2[:,5]

    
    """
    mask = (mhalo_tng1 >10.5) #& (sfr_tng > -1.5)
    mhalo_tng1 = mhalo_tng1[mask]
    pos_tng1 = pos_tng1[mask]
    sfr_tng1 = sfr_tng1[mask]
    mask = (mhalo_tng2 < 13.5) #& (sfr_tng > -1.5)
    mhalo_tng2 = mhalo_tng2[mask]
    pos_tng2 = pos_tng2[mask]
    sfr_tng2 = sfr_tng2[mask]
    """

    """
    mhalo_tng1 = tng_data1[:,1]
    pos_tng1 = tng_data1[:,2:5]
    sfr_tng1 = tng_data1[:,5]

    mhalo_tng2 = tng_data2[:,1]
    pos_tng2 = tng_data2[:,2:5]
    sfr_tng2 = tng_data2[:,5]
    """
    

    mhalo_tng = np.concatenate((mhalo_tng1, mhalo_tng2))
    pos_tng = np.concatenate((pos_tng1, pos_tng2))
    sfr_tng = np.concatenate((sfr_tng1, sfr_tng2))

    mask = (mhalo_tng > 10) 
    #mask = (sfr_tng > sfr_lim)#(mhalo_tng <    13.5) & 
    mhalo_tng = mhalo_tng[mask]
    pos_tng = pos_tng[mask]
    sfr_tng = sfr_tng[mask]


elif halo_type == "group":
    #tng_data1 = np.loadtxt(f"{tng_dir}/sfr-group-tng.txt")
    #tng_data1 = np.loadtxt(f"{tng_dir}/sfr-cent-tng.txt")
    #tng_data1 = np.loadtxt(f"shuffled_data/snap{snapnum}/sfr-gal_logM10_polyfit0.1.txt")
    #tng_data1 = np.loadtxt("eagle_in_tng_data/eagle_sfrs_in_tng_cent.txt")
    #tng_data1 = np.loadtxt(f"SHAM_LF/sfr-cent-shuffled_logM10_all_seed0_snap99_logSFR>-3.txt")
    #tng_data1 = np.loadtxt(f"{tng_dir}/sfr-halomass_sum.txt")
    #tng_data1 = np.loadtxt(f"halo_exclusion/random_halo_exclusion_2R=0.6.txt")
    #tng_data1 = np.loadtxt(f"halo_exclusion/random_seed0.txt")
    tng_data1 = np.loadtxt(f"{tng_dir}/sfr-halomass_sum.txt")
    
    if ihalo is True:
        mhalo_tng1 = tng_data1[:,1]
        pos_tng1 = tng_data1[:,2:5]
        sfr_tng1 = tng_data1[:,5]
    else:
        mhalo_tng1 = tng_data1[:,0]
        pos_tng1 = tng_data1[:,1:4]
        sfr_tng1 = tng_data1[:,4]

    mask = (mhalo_tng1 > 10) #& (sfr_tng1 < 2) 
    #logMmax = 13.6
    #mask = (mhalo_tng1 > 0) & (mhalo_tng1 < logMmax)
    #mask = sfr_tng1 < -3
   
    mhalo_tng = mhalo_tng1[mask]
    pos_tng = pos_tng1[mask]
    sfr_tng = sfr_tng1[mask]
    
    #mask14 = np.argwhere(mhalo_tng > 14)
    seed = 2
    
    #seed = int(sys.argv[2])
    #np.random.seed(seed)
    #for ihalo in mask14:
#       sfr_tng[ihalo] = np.random.normal(2.4, 0.2)
    #sfr_tng = np.where(mhalo_tng < 14, sfr_tng, 2.55)

    """
    mask = sfr_tng1 > -3
    mhalo_tng = mhalo_tng1
    pos_tng = pos_tng1
    sfr_tng = np.where(mask, sfr_tng1, -3)
    """
    
elif halo_type == "cent":
    tng_data1 = np.loadtxt(f"{tng_dir}/sfr-halomass_central.txt")
    #tng_data1 = np.loadtxt(f"{tng_dir}/SubhaloFlag_central=1/sfr-halomass_central.txt")
    #tng_data1 = np.loadtxt(f"shuffled_data/snap{snapnum}/sfr-cent_logM10_polyfit0.1.txt")
    #tng_data1 = np.loadtxt(f"shuffled_data/snap{snapnum}/sfr-cent_logM10_0.1.txt")
    if ihalo is True:
        mhalo_tng1 = tng_data1[:,1]
        pos_tng1 = tng_data1[:,2:5]
        sfr_tng1 = tng_data1[:,5]
    else:
        mhalo_tng1 = tng_data1[:,0]
        pos_tng1 = tng_data1[:,1:4]
        sfr_tng1 = tng_data1[:,4]

    #mhalo_tng1 = tng_data1[:,0]
    #pos_tng1 = tng_data1[:,1:4]
    #sfr_tng1 = tng_data1[:,4]

    #mask = (pos_tng1[:,0] < boxsize_eagle)& (pos_tng1[:,1] < boxsize_eagle)& (pos_tng1[:,2] < boxsize_eagle) & (sfr_tng1 > -3)
    mask = mhalo_tng1 > 10


    mhalo_tng = mhalo_tng1[mask]
    pos_tng = pos_tng1[mask]
    sfr_tng = sfr_tng1[mask]

elif halo_type == "sat" or halo_type =="sat_sum":
    if halo_type == "sat":
        tng_data1 = np.loadtxt(f"{tng_dir}/sfr-halomass_satellite.txt")
    elif halo_type =="sat_sum":
        tng_data1 = np.loadtxt(f"{tng_dir}/sat_sfr_sum_logM10.txt")

        if number_density:
            tng_data1 = np.loadtxt(f"{tng_dir}/nsubs_w_sfr.txt")
    #tng_data1 = np.loadtxt(f"halo_exclusion/random_halo_exclusion_2R=0.6_nsat15.txt")
    #tng_data1 = np.loadtxt(f"{tng_dir}/sfr-halomass_central.txt")
    
    if ihalo is True:
        mhalo_tng1 = tng_data1[:,1]
        pos_tng1 = tng_data1[:,2:5]
        sfr_tng1 = tng_data1[:,5]
    else:
        mhalo_tng1 = tng_data1[:,0]
        pos_tng1 = tng_data1[:,1:4]
        sfr_tng1 = tng_data1[:,4]

    #mask = (mhalo_tng1 > logMmin) 
    #logMmax = 13.6
    if number_density:
        if halo_type == "sat_sum":
            sfr_tng1 -= 1
    mask = (mhalo_tng1 > 10) 
    
    #mask = (mhalo_tng1 > logMmin) & (mhalo_tng1 < logMmax)
    #mask = sfr_tng1 < -3

    mhalo_tng = mhalo_tng1[mask]
    pos_tng = pos_tng1[mask]
    sfr_tng = sfr_tng1[mask]


z = 1.5


mpc = 3.0856775814671914e24
from astropy.cosmology import Planck15
from astropy import units as u
h = 0.6774

d_A_cm = Planck15.angular_diameter_distance(z).to(u.cm).value # proper angular diameter distance [cm]
print("d_A:", d_A_cm, "cm")
#d_A_cm = Planck15.angular_diameter_distance(z).value*mpc # proper angular diameter distance [cm]

D_A = d_A_cm * (1+z) # comoving
print("d_A:", d_A_cm, "cm")

res = 6.2
pixlen = res /(60*60)
pixlen_rad = pixlen * 2 * np.pi / 360
pixlen_cm = pixlen_rad * d_A_cm * (1+z)
pixlen_mpc_h = pixlen_cm * h / mpc
print("pixlen: ", pixlen_mpc_h, "Mpc/h")

pixsize = pixlen*pixlen
pixsize_sr = pixsize / (180/np.pi)**2 # convert from deg2 to sr

#boxsize_tng = 75
#boxsize_tng = 100*0.6777
if sim == "tng300-1":
    boxsize_tng = 205
elif sim == "tng100-1":
    boxsize_tng = 75
    #boxsize_tng = boxsize_eagle

else:
    raise CustomError(f"{sim} simulation not recognised")
Nmesh = int(boxsize_tng/pixlen_mpc_h)
#Nmesh = 8988
print("Nmeshxy:", Nmesh)
Nmesh+=1
print("Nmeshxy:", Nmesh)
pixlen_mpc_h = boxsize_tng / (Nmesh)
print("New pixlen:", pixlen_mpc_h, "Mpc/h")

boxsize = Nmesh * pixlen_mpc_h
print("Boxsize:", boxsize, "Mpc/h")

#Nmesh = 2247
#Nmesh=8


l_l = Planck15.luminosity_distance(z).to(u.cm).value
print("l_l", l_l)

cspeed = 2.998e10 # [cm/s]
lambda_rest = 6563e-8 # [cm]
print("lambda rest:", lambda_rest)
nu_rest = cspeed / lambda_rest
dnu_dz = nu_rest / (1+z)**2

r = Planck15.comoving_distance(z)
print(r)

H0 = 3.226e-18 # multiply little h by this [s]
H = Planck15.H(z).to(u.Hz)
print("H:", H)





L = sfr_tng - np.log10(4.4*10**-42)
print(L[0])
extinction = 1
V = H.value * pixsize_sr * pixlen_cm / (lambda_rest * (1+z)**2) 
I_nu = 10**23 * 10**(L-extinction/2.5) / (4 * np.pi * l_l**2 * V) # [Jy/sr] where Jy = 10^-23 erg s-1 cm-2 Hz-1
#I_nu = 10**6 * 10**(L-extinction/2.5) / (4 * np.pi * l_l**2 * V) # [nW/m^2/sr] 
nu_obs = nu_rest * (1+z)
print("nu_obs", nu_obs)
nu_I_nu = nu_obs * I_nu

V = Nmesh**3 * H.value * pixsize_sr * pixlen_cm / (lambda_rest * (1+z)**2) 
I_mean = np.sum(10**23 * 10**(L-extinction/2.5) / (4 * np.pi * l_l**2 * V)) # [Jy/sr] where Jy = 10^-23 erg s-1 cm-2 Hz-1
#I_mean = np.sum(10**6 * 10**(L-extinction/2.5) / (4 * np.pi * l_l**2 * V)) #[nW/m^2/sr] 
nu_I_mean = nu_obs * I_mean

print("I_mean:", I_mean)
print("nu*I_mean:", nu_I_mean)



#print(type(I_nu))
#I_nu = I_nu.astype(np.float64)
#I_nu = np.log10(I_nu)




nhalo = len(mhalo_tng)

halocat = np.empty(nhalo, dtype=[("Position", ("f8", 3)), ("I_nu", "f8"), ("Mass", "f8")])
halocat["I_nu"] = np.array(I_nu)
halocat["Position"] = np.array(pos_tng)
#halocat["Mass"] = np.array(10**mhalo_tng)

ps_dict = {
    "Nhalo": nhalo,
    "halocat": halocat
}


from nbodykit.source.catalog import ArrayCatalog
from nbodykit.lab import *
        
arraycat = ArrayCatalog(ps_dict["halocat"])

interp = "tsc"
#interp = "nearest"
#interp = "cic"
#weight = "Weight"
weight = "I_nu"
if interp == "nearest":
    mesh = arraycat.to_mesh(resampler="nearest", BoxSize=boxsize, Nmesh=Nmesh, weight=weight, interlaced=True)
else:
    mesh = arraycat.to_mesh(resampler=interp, BoxSize=boxsize, Nmesh=Nmesh, weight=weight, compensated=True, interlaced=True)
# resampler="tsc" means that the triangular shaped cloud mass assignment function is used
# compensated=True deconvolves the effects of interpolation

print("cp2")

#nyq = np.pi*Nmesh/boxsize
#kmax = np.log10(nyq/2)

# Compute 3D power spectrum
kmax=10
dk = 0
r = FFTPower(mesh, mode='1d', dk=dk, kmin=0.01, kmax=kmax)
Pk = r.power
#print(Pk)
k = Pk.coords
#print(k)

ncore = int(sys.argv[1])
print("ncores:", ncore)

print(Pk.attrs["shotnoise"])
Pk.attrs["shotnoise"] = Pk.attrs["shotnoise"]*ncore
shotnoise = ps.compute_shotnoise(halocat["I_nu"], boxsize, dim=3)
print("3d", shotnoise)

#halops_dicts[mass]["tng_3d"] = pinocchio_dict
import pickle
#odir=f"ps_data/snap{snapnum}/mvir/Nmesh{Nmesh}"
#odir=f"ps_data/snap{snapnum}/mvir/tng100-1"
odir=f"ps_data/snap{snapnum}/mvir"

#fname = f"{odir}/snap{snapnum}/shuffled/ps-intensity-cent-logM10_dlogM0.1_seed0.pickle"
#fname = f"{odir}/snap{snapnum}/mvir/shuffled/logM10_dlogM0.1/group/seed{seed}.pickle"
#fname = f"{odir}/snap{snapnum}/mvir/ps-intensity-sum_logM10.pickle"
#fname = f"{odir}/snap{snapnum}/mvir/halo_exclusion/2R=0.6_nsat15.pickle"
if not os.path.exists(odir):
    os.makedirs(odir,exist_ok=True)
    print("Directory created: ", odir)


#fname = f"{odir}/ps-intensity-cent_logM10.pickle"
fname = f"{odir}/ps-intensity-{halo_type}_logM10_dk0_kmax10.pickle"
#fname = f"{odir}/logM{logMmax}.pickle"
#fname = f"{odir}/logSFR2.pickle"
#fname = f"{odir}/seed0.pickle"
with open(fname, "wb") as f: 
    pickle.dump(I_mean,f)
    pickle.dump(Pk,f)
print("Written to ", fname)

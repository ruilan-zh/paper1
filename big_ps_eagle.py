import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '/cosma/home/dp004/dc-zhan5')
import os

import MyHaloPS as ps
import importlib
importlib.reload(ps)

eagle_dir = "/cosma8/data/dp004/dc-zhan5/eagle-sfr/mvir/snap28"

halo_type="cent"
snapnum=99

if halo_type == "gal":
    eagle_data1 = np.loadtxt(f"{eagle_dir}/sfr-cent-eagle.txt")
    eagle_data2 = np.loadtxt(f"{eagle_dir}/sfr-sat-eagle.txt")


    mhalo_eagle1 = eagle_data1[:,1]
    pos_eagle1 = eagle_data1[:,2:5]
    sfr_eagle1 = eagle_data1[:,5]

    mhalo_eagle2 = eagle_data2[:,1]
    pos_eagle2 = eagle_data2[:,2:5]
    sfr_eagle2 = eagle_data2[:,5]


    mhalo_eagle = np.concatenate((mhalo_eagle1, mhalo_eagle2))
    pos_eagle = np.concatenate((pos_eagle1, pos_eagle2))
    sfr_eagle = np.concatenate((sfr_eagle1, sfr_eagle2))
    
    mask = mhalo_eagle > 10
    mhalo_eagle = mhalo_eagle[mask]
    pos_eagle = pos_eagle[mask]
    sfr_eagle = sfr_eagle[mask]

elif halo_type == "group":
    #eagle_data1 = np.loadtxt(f"SHAM_LF/sfr-cent-renormalised0.5.txt")
    #eagle_data1 = np.loadtxt(f"SHAM_LF/eagle/sfr-cent-shuffled_single_mass_logM12_all_seed0.txt")
    #eagle_data1 = np.loadtxt("eagle_in_tng_data/tng_sfrs_in_eagle_cent_tng_all_lim-3.txt")
    #eagle_data1 = np.loadtxt(f"SHAM_LF/invented_Gaussian_SFR_func/sfr-cent-invented-gaussian.txt")
    #eagle_data1 = np.loadtxt(f"SHAM_LF/sfr-cent-double-inventedTNG0.5.txt")
    #eagle_data1 = np.loadtxt(f"{eagle_dir}/sfr-cent-eagle_com.txt")
    #eagle_data1 = np.loadtxt(f"shuffle_SFRs/sfr-cent-eagle-shuffled3.txt")
    eagle_data1 = np.loadtxt(f"{eagle_dir}/sfr-group-eagle.txt")
    mhalo_eagle1 = eagle_data1[:,1]
    pos_eagle1 = eagle_data1[:,2:5]
    sfr_eagle1 = eagle_data1[:,5]

    mask = mhalo_eagle1 > 10
    mhalo_eagle = mhalo_eagle1[mask]
    pos_eagle = pos_eagle1[mask]
    sfr_eagle = sfr_eagle1[mask]
elif halo_type == "cent":
    eagle_data1 = np.loadtxt(f"{eagle_dir}/sfr-cent-eagle.txt")
    #eagle_data1 = np.loadtxt(f"SHAM_LF/sfr-cent-renormalised0.25.txt")

    mhalo_eagle1 = eagle_data1[:,1]
    pos_eagle1 = eagle_data1[:,2:5]
    sfr_eagle1 = eagle_data1[:,5]

    mask = mhalo_eagle1 > 10
    mhalo_eagle = mhalo_eagle1[mask]
    pos_eagle = pos_eagle1[mask]
    sfr_eagle = sfr_eagle1[mask]




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

#boxsize_eagle = 75
#boxsize_eagle = 100*0.6777
#boxsize_eagle = 205
boxsize_eagle = 100*0.6777

Nmesh = int(boxsize_eagle/pixlen_mpc_h)
print("Nmeshxy:", Nmesh)
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





L = sfr_eagle - np.log10(4.4*10**-42)
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





nhalo = len(mhalo_eagle)

halocat = np.empty(nhalo, dtype=[("Position", ("f8", 3)), ("I_nu", "f8"), ("Mass", "f8")])
halocat["I_nu"] = np.array(I_nu)
halocat["Position"] = np.array(pos_eagle)
halocat["Mass"] = np.array(10**mhalo_eagle)

ps_dict = {
    "Nhalo": nhalo,
    "halocat": halocat
}


from nbodykit.source.catalog import ArrayCatalog
from nbodykit.lab import *
        
arraycat = ArrayCatalog(ps_dict["halocat"])

interp = "tsc"
#weight = "Weight"
weight = "I_nu"
if interp == "nearest":
    mesh = arraycat.to_mesh(resampler="nearest", BoxSize=boxsize, Nmesh=Nmesh, weight=weight)
else:
    mesh = arraycat.to_mesh(resampler=interp, BoxSize=boxsize, Nmesh=Nmesh, weight=weight, compensated=True, interlaced=True)
# resampler="tsc" means that the triangular shaped cloud mass assignment function is used
# compensated=True deconvolves the effects of interpolation

# Number of halos
#Nobjects = halops_dicts[mass]["Nhalo"]
# shot noise
#shotnoise = one_plus_delta.attrs["shotnoise"]

# Compute 3D power spectrum
#pinocchio_dict = ps.my_3dpower(delta_r, Nmesh, boxsize_eagle, shotnoise)
r = FFTPower(mesh, mode='1d', dk=0.05, kmin=0.01)
Pk = r.power
#print(Pk)
k = Pk.coords
#print(k)

ncore = int(sys.argv[1])
print("ncores:", ncore)

Pk.attrs["shotnoise"] = Pk.attrs["shotnoise"]*ncore


#pinocchio_dict["delta_r"] = delta_r

odir=f"ps_data/snap{snapnum}/mvir/eagle"
#halops_dicts[mass]["eagle_3d"] = pinocchio_dict
import pickle
if not os.path.exists(odir):
    os.makedirs(odir,exist_ok=True)
    print("Directory created: ", odir)

fname = f"{odir}/ps-intensity-{halo_type}.pickle"

#fname = f"{odir}/snap{snapnum}/eagle/logM/ps-intensity-gal_logM10.5.pickle"
with open(fname, "wb") as f: 
    pickle.dump(I_mean,f)
    pickle.dump(Pk,f)
print("Written to ", fname)

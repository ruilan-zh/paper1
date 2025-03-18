import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '/cosma/home/dp004/dc-zhan5')
import os

import MyHaloPS as ps
import importlib
importlib.reload(ps)


tng_dir = "/cosma7/data/dp004/dc-zhan5/tng-sfr"

halo_type="group"

if halo_type == "gal":
    tng_data1 = np.loadtxt(f"{tng_dir}/sfr-cent-tng.txt")
    tng_data2 = np.loadtxt(f"{tng_dir}/sfr-sat-tng.txt")
    #tng_data1 = np.loadtxt(f"{tng_dir}/sfr-cent-tng-100-1.txt")
    #tng_data2 = np.loadtxt(f"{tng_dir}/sfr-sat-tng-100-1.txt")

    #tng_data1 = np.loadtxt(f"sfr-cent-eagle_com.txt")
    #tng_data2 = np.loadtxt(f"sfr-sat-eagle_cop.txt")


    mhalo_tng1 = tng_data1[:,0]
    pos_tng1 = tng_data1[:,1:4]
    sfr_tng1 = tng_data1[:,4]

    mhalo_tng2 = tng_data2[:,0]
    pos_tng2 = tng_data2[:,1:4]
    sfr_tng2 = tng_data2[:,4]

    mhalo_tng = np.concatenate((mhalo_tng1, mhalo_tng2))
    pos_tng = np.concatenate((pos_tng1, pos_tng2))
    sfr_tng = np.concatenate((sfr_tng1, sfr_tng2))
elif halo_type == "group":
    #tng_data1 = np.loadtxt(f"{tng_dir}/sfr-group-tng.txt")
    #tng_data1 = np.loadtxt(f"toy_model/logM11-11.1/weight1.txt")
    #tng_data1 = np.loadtxt(f"toy_model/logM11-11.5/logM11-11.5_weight1_2_random.txt")
    tng_data1 = np.loadtxt(f"toy_model/logM11-11.1/weight1_5_random_seed4.txt")
    #tng_data1 = np.loadtxt(f"toy_model/logM11-11.1/weight1(25)_5(75)_cprox.txt")
    #tng_data1 = np.loadtxt(f"toy_model/logM11-11.1/weight5_1_cprox.txt")
    mhalo_tng1 = tng_data1[:,0]
    pos_tng1 = tng_data1[:,1:4]
    sfr_tng1 = tng_data1[:,4]

    mask = mhalo_tng1 > 0
    #mask = sfr_tng1 < -3

    mhalo_tng = mhalo_tng1[mask]
    pos_tng = pos_tng1[mask]
    sfr_tng = sfr_tng1[mask]

    """
    mask = sfr_tng1 > -3
    mhalo_tng = mhalo_tng1
    pos_tng = pos_tng1
    sfr_tng = np.where(mask, sfr_tng1, -3)
    """
    
elif halo_type == "cent":
    tng_data1 = np.loadtxt(f"{tng_dir}/sfr-cent-tng.txt")
    #tng_data1 = np.loadtxt(f"SHAM_LF/sfr-cent-renormalised0.25.txt")

    mhalo_tng1 = tng_data1[:,0]
    pos_tng1 = tng_data1[:,1:4]
    sfr_tng1 = tng_data1[:,4]

    mask = mhalo_tng1 > 11
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
boxsize_tng = 205
Nmesh = int(boxsize_tng/pixlen_mpc_h)
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





"""
nhalo = len(mhalo_tng)

x = np.random.random(nhalo)*boxsize
y = np.random.random(nhalo)*boxsize
z = np.random.random(nhalo)*boxsize
"""

"""
distances_squared = (x[:, np.newaxis] - x) ** 2 + (y[:, np.newaxis] - y) ** 2 + (z[:, np.newaxis] - z) ** 2
distances = np.sqrt(distances_squared)

distances[np.tril_indices(nhalos)] = np.inf

threshold = 0.5
mask = np.all(distances > threshold, axis=1)
"""

"""
mask = np.array([True]*nhalo)

 
for a in range(nhalo):
    for b in range(a+1, nhalo):
        dist = np.sqrt((x[b]-x[a])**2 + (y[b]-y[a])**2 + (z[b]-z[a])**2)
        if dist < 0.1:
            mask[a] = False

print(np.sum(mask))
pos_random = np.vstack((x, y, z)).T[mask]
"""

nhalo = len(mhalo_tng)
halocat = np.empty(nhalo, dtype=[("Position", ("f8", 3)), ("I_nu", "f8"), ("Mass", "f8")])
#halocat = np.empty(nhalo, dtype=[("Position", ("f8", 3))])
halocat["Position"] = np.array(pos_tng)
halocat["I_nu"] = np.array(sfr_tng)
#halocat["Mass"] = np.array(10**mhalo_tng)

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
    mesh = arraycat.to_mesh(resampler=interp, BoxSize=boxsize, Nmesh=Nmesh, weight=weight, compensated=True)
# resampler="tsc" means that the triangular shaped cloud mass assignment function is used
# compensated=True deconvolves the effects of interpolation

# Number of halos
#Nobjects = halops_dicts[mass]["Nhalo"]
# shot noise
#shotnoise = one_plus_delta.attrs["shotnoise"]

# Compute 3D power spectrum
#pinocchio_dict = ps.my_3dpower(delta_r, Nmesh, boxsize_tng, shotnoise)
r = FFTPower(mesh, mode='1d', dk=0.05, kmin=0.01)
Pk = r.power
#print(Pk)
k = Pk.coords
#print(k)
ncore = int(sys.argv[1])
print("ncores:", ncore)

Pk.attrs["shotnoise"] = Pk.attrs["shotnoise"]*ncore

odir=f"ps_data/snap40/mvir/toy_model/logM11-11.1"
if not os.path.exists(odir):
    os.makedirs(odir,exist_ok=True)
    print("Directory created: ", odir)


#pinocchio_dict["delta_r"] = delta_r

#halops_dicts[mass]["tng_3d"] = pinocchio_dict
import pickle
#with open(f"{odir}/weight1.pickle", "wb") as f:
with open(f"{odir}/weight1_5_random_seed4.pickle", "wb") as f:
#with open(f"{odir}/weight5_1_cprox.pickle", "wb") as f:
#with open(f"{odir}/weight1(25)_5(75)_cprox.pickle", "wb") as f:
    pickle.dump(I_mean,f)
    pickle.dump(Pk,f)

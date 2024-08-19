import numpy as np
import matplotlib.pyplot as plt
import pickle
import sys
sys.path.insert(0, '/cosma/home/dp004/dc-zhan5')
import os


import MyHaloPS as ps
import importlib
importlib.reload(ps)

#object2shuffle="cent"
object2shuffle=sys.argv[5]

#logM_range="logM11-11.5"
logM_range=sys.argv[3]
#logM_range="logMmin13"
sfr_range=""
bh_range=""
#conc_split="split_nan/msat_sum_split2"
#conc_split="split_nan/conc_split100"
#conc_split="split_nan/test_split10000"
conc_split=sys.argv[4]
#conc_split=""
changed_bins=True
if changed_bins==True:
    changed_bins="changed_bins"
else:
    changed_bins=""
do_shuffle=True
if do_shuffle:
    shuffle_name=""
else:
    shuffle_name="_not_shuffled"

snapnum=40
is_logps = False

tng_dir = f"/cosma7/data/dp004/dc-zhan5/TNG/snap{snapnum}/SubhaloFlag_all/mvir"

nfile=1
seed = int(sys.argv[2])
if nfile==2:
    tng_data1 = np.loadtxt(f"{tng_dir}/sfr-halomass_central.txt")
    tng_data2 = np.loadtxt(f"{tng_dir}/sfr-halomass_satellite.txt")

    mhalo_tng1 = tng_data1[:,0]
    pos_tng1 = tng_data1[:,1:4]
    sfr_tng1 = tng_data1[:,4]

    mhalo_tng2 = tng_data2[:,0]
    pos_tng2 = tng_data2[:,1:4]
    sfr_tng2 = tng_data2[:,4]

    mhalo_tng = np.concatenate((mhalo_tng1, mhalo_tng2))
    pos_tng = np.concatenate((pos_tng1, pos_tng2))
    sfr_tng = np.concatenate((sfr_tng1, sfr_tng2))

    #mask = mhalo_tng > 10
    mask = (mhalo_tng > 12.5) & (mhalo_tng < 13) 

    mhalo_tng = mhalo_tng[mask]
    pos_tng = pos_tng[mask]
    sfr_tng = sfr_tng[mask]

elif nfile==1:
    #tng_data1 = np.loadtxt(f"{tng_dir}/sfr-halomass_sum.txt")
    #tng_data1 = np.loadtxt(f"{tng_dir}/sfr-halomass_central.txt")
    #tng_data1 = np.loadtxt(f"/snap7/scratch/dp004/dc-zhan5/shuffled/sfr-gal-logM10_dlogM0.1_snap40/seed{seed}.txt")
    tng_data1 = np.loadtxt(f"/cosma7/data/dp004/dc-zhan5/shuffled/logM10_dlogM0.1_snap40/{changed_bins}/gal_ps/shuffle_{object2shuffle}/{logM_range}/{sfr_range}/{bh_range}/{conc_split}/seed{seed}{shuffle_name}.txt")
    #tng_data1 = np.loadtxt(f"/cosma8/data/dp004/dc-zhan5/shuffled/logM10_dlogM0.1_snap40/cent_ps/shuffle_cent/seed{seed}.txt")
    #tng_data1 = np.loadtxt(f"/cosma8/data/dp004/dc-zhan5/assignment_schemes/gaussian/tng_median_std/upper_std/seed{seed}.txt")
    #tng_data1 = np.loadtxt(f"/cosma8/data/dp004/dc-zhan5/assignment_schemes/gaussian/tng_linear_mean/changed_sfr_func/all/sigma=0.2/seed{seed}.txt")
    #tng_data1 = np.loadtxt(f"/cosma8/data/dp004/dc-zhan5/assignment_schemes/gaussian/tng_linear_mean/changed_sfr_func/nonzero/interped/quenched_tests/0.8/set_to_-5/seed{seed}.txt")
    #tng_data1 = np.loadtxt(f"/cosma8/data/dp004/dc-zhan5/invented/sigma0/seed{seed}.txt")
#	tng_data1 = np.loadtxt(f"/cosma8/data/dp004/dc-zhan5/invented/2sigma/0.4_0.2/seed{seed}_mean.txt")
    #tng_data1 = np.loadtxt(f"/cosma8/data/dp004/dc-zhan5/invented/sigma0.2/seed{seed}.txt")
    mhalo_tng1 = tng_data1[:,0]
    pos_tng1 = tng_data1[:,1:4]
    sfr_tng1 = tng_data1[:,4]

    mask = (mhalo_tng1 > 10) & (sfr_tng1 > -100)
    #mask = sfr_tng1 < -3

    mhalo_tng = mhalo_tng1[mask]
    pos_tng = pos_tng1[mask]
    sfr_tng = sfr_tng1[mask]
    print("sum sfr:", np.sum(10**sfr_tng))

    """
    mask = sfr_tng1 > -3
    mhalo_tng = mhalo_tng1
    pos_tng = pos_tng1
    sfr_tng = np.where(mask, sfr_tng1, -3)
    """
    




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
print("original Nmeshxy:", Nmesh)
Nmesh = Nmesh + 1
print("new Nmeshxy:", Nmesh)
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





L = sfr_tng + np.log10(2.27*10**41)
print(L[0])
extinction = 1
V = H.value * pixsize_sr * pixlen_cm / (lambda_rest * (1+z)**2) 
#I_nu = 10**23 * 10**(L-extinction/2.5) / (4 * np.pi * l_l**2 * V) # [Jy/sr] where Jy = 10^-23 erg s-1 cm-2 Hz-1
I_nu = 10**6 * 10**(L-extinction/2.5) / (4 * np.pi * l_l**2 * V) # [nW/m^2/sr] 
nu_obs = nu_rest * (1+z)
print("nu_obs", nu_obs)
nu_I_nu = nu_obs * I_nu

V = Nmesh**3 * H.value * pixsize_sr * pixlen_cm / (lambda_rest * (1+z)**2) 
#I_mean = np.sum(10**23 * 10**(L-extinction/2.5) / (4 * np.pi * l_l**2 * V)) # [Jy/sr] where Jy = 10^-23 erg s-1 cm-2 Hz-1
I_mean = np.sum(10**6 * 10**(L-extinction/2.5) / (4 * np.pi * l_l**2 * V)) #[nW/m^2/sr Hz-1] 
nu_I_mean = nu_obs * I_mean # [nW/m^2/sr] 


print("I_mean:", I_mean)
print("nu*I_mean:", nu_I_mean)


#print(type(I_nu))
#I_nu = I_nu.astype(np.float64)
#I_nu = np.log10(I_nu)


print("min_I_nu:", min(I_nu))
print("max_I_nu:", max(I_nu))

log_nu_I_nu = np.log10(nu_I_nu.astype("float"))

print("min log(I_nu):", min(log_nu_I_nu))
print("max log(I_nu):", max(log_nu_I_nu))
print("mean log(I_nu):", np.mean(log_nu_I_nu))



nhalo = len(mhalo_tng)

halocat = np.empty(nhalo, dtype=[("Position", ("f8", 3)), ("I_nu", "f8"), ("Mass", "f8")])
#halocat["I_nu"] = np.array(I_nu)
if is_logps:
    halocat["I_nu"] = log_nu_I_nu+10
else:
    halocat["I_nu"] = nu_I_nu
halocat["Position"] = np.array(pos_tng)
halocat["Mass"] = np.array(10**mhalo_tng)

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

# VID
one_plus_delta = mesh.paint(mode='real')
mesh_vals = nu_I_mean * one_plus_delta.value.flatten()
mean_mesh_vals = np.mean(mesh_vals)
print("mean_mesh_vals: ", mean_mesh_vals)
print("max_mesh_vals: ", np.max(mesh_vals))
print("min_mesh_vals: ", np.min(mean_mesh_vals))
print("min_nu_I: ", np.min(nu_I_nu[nu_I_nu > 0]))
log_mesh_vals = np.log10(mesh_vals[mesh_vals > 0])
bin_edges1=np.arange(0,3)
nu_I_nu_hist, bin_edges = np.histogram(log_mesh_vals, density=True, bins=50)


# Number of halos
#Nobjects = halops_dicts[mass]["Nhalo"]
# shot noise
#shotnoise = one_plus_delta.attrs["shotnoise"]

# Compute 3D power spectrum
# fundamental mode of the box is 2pi/Lbox 
fundamental_mode = 2*np.pi / boxsize
print("fundamental mode: ", fundamental_mode)
r = FFTPower(mesh, mode='1d', dk=0.05, kmin=0.01)
#r = FFTPower(mesh, mode='1d', dk=1, kmin=0.01)
Pk = r.power
#print(Pk)
k = Pk.coords
#print(k)
ncore = int(sys.argv[1])
print("ncores:", ncore)

Pk.attrs["shotnoise"] = Pk.attrs["shotnoise"]*ncore


#pinocchio_dict["delta_r"] = delta_r

#halops_dicts[mass]["tng_3d"] = pinocchio_dict
#odir = f"ps_data/snap{snapnum}/mvir/assignment_schemes/gaussian/tng_median_std/upper_std"
#odir = f"ps_data/snap{snapnum}/mvir/assignment_schemes/gaussian/tng_linear_mean/changed_sfr_func/all/sigma=0.2"
#odir = f"ps_data/snap{snapnum}/mvir/assignment_schemes/gaussian/tng_linear_mean/changed_sfr_func/nonzero/interped/quenched_tests/0.8/set_to_-5"
#odir = f"ps_data/snap{snapnum}/mvir"
#odir = f"ps_data/snap{snapnum}/mvir/invented/sigma0"
#odir = f"ps_data/snap{snapnum}/mvir/invented/2sigma/0.4_0.2/mean"
#odir = f"ps_data/snap{snapnum}/mvir/invented/sigma0.2"
#odir = f"ps_data/snap{snapnum}/mvir/shuffled/logM10_dlogM0.1/gal_ps/shuffle_gal"
odir = f"ps_data/snap{snapnum}/mvir/shuffled/logM10_dlogM0.1/{changed_bins}/gal_ps/shuffle_{object2shuffle}/{logM_range}/{sfr_range}/{bh_range}/{conc_split}"
#odir = f"ps_data/snap{snapnum}/mvir/shuffled/logM10_dlogM0.1/cent_ps/shuffle_cent"

fname = f"{odir}/seed{seed}{shuffle_name}.pickle"

if nfile==2:
    odir = f"ps_data/snap{snapnum}/mvir"
    #fname = f"{odir}/ps-intensity-gal_logM10.pickle"
    fname = f"{odir}/ps-intensity-gal_logM12.5-13.pickle"

if not os.path.exists(odir):
    os.makedirs(odir,exist_ok=True)
    print("Directory created: ", odir)



with open(fname, "wb") as f: 
    pickle.dump(nu_I_mean,f)
    pickle.dump(Pk,f)
print("Written to ", fname)

odir_vid = f"{odir}/VID"
if not os.path.exists(odir_vid):
    try:
        os.mkdir(odir_vid)
        print("Directory created: ", odir_vid)
    except FileExistsError:
        pass


fname1 = f"{odir_vid}/seed{seed}.pickle"
#fname1 = f"{odir_vid}/intensity-sum_logM10.pickle"
with open(fname1, "wb") as f: 
    pickle.dump(bin_edges,f)
    pickle.dump(nu_I_nu_hist,f)
print("Written to ", fname1)

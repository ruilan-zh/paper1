
from astropy.cosmology import Planck15
from astropy import units as u
from nbodykit.source.catalog import ArrayCatalog
from nbodykit.lab import *

snapnum=40
z = 1.5
boxsize_tng = 205

### Read in halo catalogue
tng_dir = f"/cosma7/data/dp004/dc-zhan5/TNG/snap{snapnum}/SubhaloFlag_all/mvir/ihalo"
tng_data = np.loadtxt(f"{tng_dir}/sfr-halomass_sum.txt")

ihalo = True
if ihalo is True:
    plus_index = 1
else:
    plus_index = 0

mhalo_tng1 = tng_data1[:,0+plus_index]
pos_tng1 = tng_data1[:,1+plus_index:4+plus_index]
sfr_tng1 = tng_data1[:,4+plus_index]

mask = (mhalo_tng1 > 10) 

mhalo_tng = mhalo_tng1[mask]
pos_tng = pos_tng1[mask]
sfr_tng = sfr_tng1[mask]

### Convert SFRs to intensities ###
from astropy.cosmology import Planck15
from astropy import units as u

h = 0.6774

d_A_cm = Planck15.angular_diameter_distance(z).to(u.cm).value # proper angular diameter distance [cm]
print("d_A:", d_A_cm, "cm")

D_A = d_A_cm * (1+z) # comoving
print("d_A:", d_A_cm, "cm")

### Determine pixel size
res = 6.2 # width of pixel in arcseconds
pixlen_deg = res /(60*60) # width of pixel in degrees
pixlen_rad = pixlen_deg * 2 * np.pi / 360
pixlen_cm = pixlen_rad * d_A_cm * (1+z)
pixlen_mpc_h = pixlen_cm * h / mpc


### From pixel size, compute number of mesh cells in a direction
Nmesh = int(boxsize_tng/pixlen_mpc_h)

# Change Nmesh to make pixel sizes a bit smaller so that an integer number can fit in the box
Nmesh+=1
pixlen_mpc_h = boxsize_tng / (Nmesh)
pixlen_cm = pixlen_mpc/ (h / mpc)
pixlen_rad = pixlen_cm /(d_A_cm * (1+z))
pixlen_deg = pixlen_rad / (2 * np.pi / 360)


pixsize = pixlen_deg*pixlen_deg
pixsize_sr = pixsize / (180/np.pi)**2 # convert from deg2 to sr

boxsize = Nmesh * pixlen_mpc_h 

### Compute quantities required for computation of intensity
l_l = Planck15.luminosity_distance(z).to(u.cm).value

cspeed = 2.998e10 # [cm/s]
lambda_rest = 6563e-8 # [cm]

nu_rest = cspeed / lambda_rest
dnu_dz = nu_rest / (1+z)**2

H = Planck15.H(z).to(u.Hz)

### Convert SFR to luminosity
L = sfr_tng - np.log10(4.4*10**-42)
extinction = 1

### Convert to intensity

V_pix = H.value * pixsize_sr * pixlen_cm / (lambda_rest * (1+z)**2)  
I_nu = 10**6 * 10**(L-extinction/2.5) / (4 * np.pi * l_l**2 * V_pix) # [nW/m^2/sr] 

nu_obs = nu_rest * (1+z)
nu_I_nu = nu_obs * I_nu

### Compute mean intensity
V_box = Nmesh**3 * H.value * pixsize_sr * pixlen_cm / (lambda_rest * (1+z)**2) 
I_mean = np.sum(10**6 * 10**(L-extinction/2.5) / (4 * np.pi * l_l**2 * V_box)) #[nW/m^2/sr] 
nu_I_mean = nu_obs * I_mean






### Paint onto mesh using nbodykit ###

### Convert to array catalog 
nhalo = len(mhalo_tng)

halocat = np.empty(nhalo, dtype=[("Position", ("f8", 3)), ("I_nu", "f8"), ("Mass", "f8")])
halocat["I_nu"] = np.array(I_nu)
halocat["Position"] = np.array(pos_tng)

ps_dict = {
    "Nhalo": nhalo,
    "halocat": halocat
}

arraycat = ArrayCatalog(ps_dict["halocat"])

### Create mesh object
interp = "tsc"
weight = "I_nu"
if interp == "nearest":
	mesh = arraycat.to_mesh(resampler="nearest", BoxSize=boxsize, Nmesh=Nmesh, weight=weight, interlaced=True)
else:
	mesh = arraycat.to_mesh(resampler=interp, BoxSize=boxsize, Nmesh=Nmesh, weight=weight, compensated=True, interlaced=True)
# resampler="tsc" means that the triangular shaped cloud mass assignment function is used
# compensated=True deconvolves the effects of interpolation

### Compute power spectrum ###
r = FFTPower(mesh, mode='1d', dk=0.05, kmin=0.01)
Pk = r.power

fname="power_spectrum.pickle"
with open(fname, "wb") as f: 
    pickle.dump(I_mean,f) 
    pickle.dump(Pk,f)
print("Written to ", fname)

# Pk["power"].real gives the power
# Pk["k"] gives the k values

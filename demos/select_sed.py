import os
import outObj as ob
from outObj import nColors, getColors
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LogNorm, LinearSegmentedColormap
from matplotlib import cm, gridspec, patches
import matplotlib.ticker as ticker

mpl.rc('axes', labelsize=22, titlesize=22, linewidth=3)
mpl.rc('xtick', labelsize=20, direction='in', top=True)
mpl.rc('xtick.major', size=12, width=3, top=True)
mpl.rc('xtick.minor', visible=True, size=8, width=2, top=True)
mpl.rc('ytick', labelsize=20, direction='in', right=True)
mpl.rc('ytick.major', size=12, width=3, right=True)
mpl.rc('ytick.minor', visible=True, size=8, width=2, right=True)
mpl.rc('font', size=22, family='serif', style='normal', variant='normal', stretch='normal', weight='heavy')
mpl.rc('legend', labelspacing=0.1, handlelength=2, fontsize=16)


# --- read in data files ---
dir_sxp = '../sxp-ssp/'
model_prefix = 'ZAU'
zau_sxp = ob.allmods(dir_sxp, model_prefix)

logZGrid = zau_sxp.logZ_vals
tageGrid = zau_sxp.age_vals
lsun = 3.839e+33

def parse_seds(tage, logZ, sedFile):

    """
    Parses ascii file in the `sed` directory to return the SED for the desired value in tage and logZ

    Args:
        tage (float): age in yrs
        logZ (float): log10 of metallicity in solar units
        sedFile (string): path to file to parse

    Returns:
        wav, spec (arrays): wavelength (Angstroms) and spectra (erg/s/Hz/Msun) for desired model
    """

    sedlam = np.loadtxt(sedFile)
    seds = np.array([val for line in sedlam for val in line])
    lam = seds[:15000] # select wavelength grid
    spec = seds[15000:] # select spec grid

    ilogZ = np.abs(logZGrid - logZ).argmin()
    itage = np.abs(tageGrid - tage).argmin()
    specselect = np.array(
        spec[ilogZ*len(lam)*len(tageGrid)+itage*len(lam):
            ilogZ*len(lam)*len(tageGrid)+(len(lam)*(itage+1))
        ])
    specselect *= lsun

    return lam, specselect


if __name__ == "__main__":

    # adjust defintions and function calls here as needed

    # plot single metallicity for all ages
    logZ = -1
    sedFile = '../sed/FSPS-bpass-massScal_XRB-sirfvartheta.ascii'
    for tage in tageGrid:
        lam, spec = parse_seds(tage, logZ, sedFile)
        plt.plot(np.log10(lam), spec,
                 label=r'{0:.0f} Myr'.format(tage/1.e6))
        plt.annotate(r'{0:.2g} Zsun'.format(10**logZ), size=18,
                    xy=(0.95, 0.85), xycoords='axes fraction', ha='right', va='bottom')
    plt.ylim([10**-28,10**-16])
    plt.xlim([0, 8.0])
    plt.semilogy()
    plt.ylabel('Fnu [erg/s/Hz/Msun]')
    plt.xlabel('log(Wave [Angstrom])')
    plt.legend(loc=4)
    plt.tight_layout()
    plt.show()

    # plot all metallicities for a single age
    tage = 5e+6
    zcolors = nColors(len(logZGrid),
                      minv = 0.3, maxv = 1, cname = 'plasma_r')
    for i in range(len(logZGrid)):
        lam, spec = parse_seds(tage, logZGrid[i], sedFile)
        plt.plot(np.log10(lam), spec,
                 label=r'{0:.2g} Zsun'.format(10**logZGrid[i]),
                 color=zcolors[i])
        plt.annotate(r'{0:.0f} Myr'.format(tage/1.e6), size=18,
                    xy=(0.95, 0.85), xycoords='axes fraction', ha='right', va='bottom')
    plt.ylim([10**-28,10**-16])
    plt.xlim([0, 8.0])
    plt.semilogy()
    plt.ylabel('Fnu [erg/s/Hz/Msun]')
    plt.xlabel('log(Wave [Angstrom])')
    plt.legend(loc=4)
    plt.tight_layout()
    plt.show()

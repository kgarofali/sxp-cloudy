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

# --- basic function for plotting grids ---
def make_emline_diagnostic(gridP, gridS, xattr, yattr, xlab, ylab, cval):

    """
    plots a set of grids for chosen emission line diagnostic

    Args:
        gridP (object): primary grid to be plotted
        gridS (object): secondary grid to be plotted (appears as faded lines)
        xattr (string): line ratio for the abscissa. This string must be defined in load_lines() in outObj.py to be recognized.
        yattr (string): line ratio for the ordinate. This string must be defined in load_lines() in outObj.py to be recognized.
        xlab (string): xaxis label
        ylab (string): yaxis label
        cval (float): "constant" value for plotting the grid; here this is age in units of yrs.

    Returns:
        Six figures showing the full model grids in logU and logZ at the selected cval (age) for a set of emission line diagnostics shown in Garofali et al. 2024. 
    """

    fig, ax = plt.subplots(1, 1, figsize=(8,8))
    ucolors = nColors(len(gridP.logU_vals),
                      minv = 0.2, maxv = 1.0, cname = 'Blues')
    zcolors = nColors(len(gridP.logZ_vals),
                      minv = 0.3, maxv = 1, cname = 'plasma_r')


    Xp,Yp,Zpx = gridP.group_mods(zval = xattr, yval = 'logU',
                                 const = 'age', cval = cval)
    Xp,Yp,Zpy = gridP.group_mods(zval = yattr, yval = 'logU',
                               const = 'age', cval = cval)
    Xs,Ys,Zsx = gridS.group_mods(zval = xattr, yval = 'logU',
                                   const = 'age', cval = cval)
    Xs,Ys,Zsy = gridS.group_mods(zval = yattr, yval = 'logU',
                                 const = 'age', cval = cval)

    for i in range(Xp.shape[0]):
        # SXP + SSP, lines of constant logU
        ax.plot(Zpx[i,:], Zpy[i,:], lw=3, color=ucolors[i])
        # SSP, lines of constant logU
        ax.plot(Zsx[i,:], Zsy[i,:], '--', lw=3, alpha=0.3, color=ucolors[i])
    for i in range(Xp.shape[1]):
        # SXP + SSP, lines of constant logZ
        ax.plot(Zpx[:,i], Zpy[:,i], lw=3, color=zcolors[i])
        # SSP, lines of constant logZ
        ax.plot(Zsx[:,i], Zsy[:,i], '--', lw=3, alpha=0.3, color=zcolors[i])

    ax.plot(Zpx[-1,0], Zpy[-1,0], '*', markersize=18, color='k')
    ax.annotate(r'{0:.0f} Myr'.format(cval/1.e6), size=24,
                xy=(0.98, 0.02), xycoords='axes fraction', ha='right', va='bottom')
    plt.xlabel(xlab, labelpad=7)
    plt.ylabel(ylab, labelpad=7)
    plt.tight_layout()
    plt.show()

# --- read in data files ---
dir_sxp = '../sxp-ssp/'
model_prefix = 'ZAU'
zau_sxp = ob.allmods(dir_sxp, model_prefix)
dir_ssp = '../ssp/'
zau_ssp = ob.allmods(dir_ssp, model_prefix)

# --- call plotting function for lines of interest ---
make_emline_diagnostic(zau_sxp, zau_ssp,
                       'log_OIII_CIII', 'log_HeIIu_CIII',
                       r'${\rm log(O~III]}~\lambda1661,6/{\rm C~III]}~\lambda1907,9)$',
                       r'${\rm log(He~II}~\lambda1640/{\rm C~III]}~\lambda1907,9)$', cval = 20e+6)
make_emline_diagnostic(zau_sxp, zau_ssp,
                       'log_NIIb_Ha', 'log_HeII_Hb',
                       r'${\rm log([N~II]}~\lambda6584/{\rm H}\alpha$)', r'${\rm log(He~II}~\lambda4686/{\rm H}\beta$)',
                       cval = 20e+6)
make_emline_diagnostic(zau_sxp, zau_ssp,
                        'log_OIVi_NeIIIia', 'log_NeIIIia_NeIIi',
                        r'${\rm log([O~IV]}~25.9\mu{\rm m}/{\rm [Ne~III]}~15.56\mu{\rm m}$)',
                        r'${\rm log([Ne~III]}~15.56\mu{\rm m}/{\rm [Ne~II]}~12.81\mu{\rm m}$)', cval = 20e+6)
make_emline_diagnostic(zau_sxp, zau_ssp,
                       'log_CIV_OIII', 'log_OIII_CIII',
                       r'${\rm log~(C~IV}~\lambda1548,51/{\rm O~III]}~\lambda1661,6)$',
                       r'${\rm log(O~III]}~\lambda1661,6/{\rm [C~III]}~\lambda1907,10)$', cval = 20e+6)
make_emline_diagnostic(zau_sxp, zau_ssp,
                       'log_NeV_NeIIIb', 'log_OIIIb_Hb',
                       r'${\rm log~([Ne~V]}~\lambda3426/{\rm [Ne~III]}~\lambda3870)$',
                       r'${\rm log~([O~III]}~\lambda 5007/{\rm H}\beta)$',
                       cval = 20e+6)
make_emline_diagnostic(zau_sxp, zau_ssp,
                       'log_NeVia_NeIIIia','log_NeIIIia_NeIIi',
                       r'${\rm log([Ne~V]}~14.3\mu{\rm m}/{\rm [Ne~III]}~15.56\mu{\rm m}$)',
                       r'${\rm log([Ne~III]}~15.56\mu{\rm m}/{\rm [Ne~II]}~12.81\mu{\rm m}$)', cval = 20e+6)

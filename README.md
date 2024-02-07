# sxp-cloudy

This repository contains results for nebular line emission due to the composite simple stellar population (SSP) and simple X-ray population (SXP) models presented in Garofali et al. 2023. The photoionization simulations were performed using ```Cloudy``` v17.02, and a modified version of ```cloudyfsps```: http://nell-byler.github.io/cloudyfsps/

The output presented here is meant to enable quick inspection of the simulated nebular line emission due to the composite models for user-defined line diagnostics. We also provide Table A.1 (nebular line list) in machine readable format. For detailed descriptions of the models and assumptions therein, please see Garofali et al. 2024. For questions about the simulation output, please contact kristen DOT garofali AT nasa DOT gov.

## sxp-ssp

This directory contains the simulation results for the full suite of composite SXP + SSP models.

The ```ZAU.pars``` file contains one line for each point in the full grid of models. The columns are as follows: model number (1-147), logZ (solar units), age (Myr), logU, logR (cm), logQ (s^-1), nH (cm^-3), and the stopping criteria (the same for all simulations, corresponding to when the ionized fraction falls to 1%).

There is one ```ZAUXX.lineflux``` file per point in the grid, where XX refers to the model number (corresponding to the number in the first column of the ```ZAU.pars``` file). In each .lineflux file, the columns are as follows: vacuum wavelength (Angstroms), emergent line emission (erg/s) emitted by a full spherical shell.  

## ssp

This directory contains the simulation results for the SSP-only models (no SXP contribution). The file names and column information are the same as above.

## sed

This directory contains a file with the combined SXP + SSP SEDs that were used as input for the Cloudy simulations presented in Garofali et al. 2024. This file therefore contains a fixed set of SXP + SSP SEDs at a select set of burst ages and metallicities, and relies on the BPASS models for the SSP spectra. The header of this file includes relevant information for parsing the file. The grid is defined by pairings of burst age and metallicity with 21 separate SEDs (7 age x 3 logZ). Each SED has length 15000 in wavelength and Fnu, where wavelength is in Angstroms, and Fnu is in units Lsun/Hz/Msun (where Lsun = 3.839e+33). After the header entries, there is a block that lists the age-metallicity pairings, where age is in units of yrs, and metallicity is listed as logZ relative to solar. After this block comes the wavelength array (recorded once, units Angstroms), and then each SED for the 21 age-logZ pairs.

The _SXP-only_ SEDs can be accessed via [FSPS](https://github.com/cconroy20/fsps/tree/master/SPECTRA/xrb) in the```SPECTRA/xrb``` directory. Here, the wavelength array is recorded in a separate file (```.lambda```) and the SEDs for all ages are recorded in separate files as a function of metallicity (```.spec```). As described in Section 5.4 of Garofali et al. 2024, the grids in FSPS are of a larger size (10 age x 11 logZ).

## demos

This directory contains example code (```plot_grids.py```) for plotting the full suite of simulated nebular line emission as a grid for user-defined emission line diagnostics. The ```plot_grids.py``` demo can be run from the command line or in an interactive python environment. Running the code will interactively produce images for six emission line diagnostics corresponding to figures presented in Garofali et al. 2024; closing one figure will automatically advance to the next figure. The user can follow these examples to create their own emission line diagnostics for different lines and/or produce grids for different burst ages. This code is adapted from existing functions in ```cloudyfsps```. For full functionality in interpreting and plotting simulation results, it is recommended that the user install and familiarize themselves with ```cloudyfsps```; however, the code presented here will work as a standalone for quick visualizations.

This directory also contains example code (```select_sed.py```) for parsing the file in the ```sed``` directory to select and plot an SED for a particular point in the grid (i.e., in terms of burst age and stellar metallicity). This code can also be used with slight modifications to select SEDs from the ```.spec``` files in FSPS.

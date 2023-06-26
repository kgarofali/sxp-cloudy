# sxp-cloudy

This repository contains results for nebular line emission due to the composite simple stellar population (SSP) and simple X-ray population (SXP) photoionization models as presented in Garofali et al. 2023. The photoionization simulations are performed using ```Cloudy``` v17.02, and associated file i/o relies on a modified version of ```cloudyfsps```: http://nell-byler.github.io/cloudyfsps/

The simulation output presented here is meant to enable quick inspection of the composite SXP + SSP nebular line emission in grid form for different nebular emission line diagnostics, which can then be compared to other photoionization or shock ionization model grids, or observational samples.

For detailed descriptions of the models and assumptions therein, please see Garofali et al. 2023. For questions about the simulation output, please contact kristen DOT garofali AT nasa DOT gov.

## sxp-ssp

This directory contains the simulation results for the composite SXP + SSP models.

The ```ZAU.pars``` file contains one line for each point in the grid. The columns are as follows: model number (1-147), logZ (solar units), age (Myr), logU, logR (cm), logQ (s^-1), nH (cm^-3), and the stopping criteria (the same for all simulations, corresponding to when the ionized fraction falls to 1%).

There is one ```ZAUXX.lineflux``` file per grid point, where XX == the model number (corresponding to the first column in the ```ZAU.pars``` file). In the .lineflux files, the columns are as follows: vacuum wavelength (Angstroms), line luminosity (erg/s).

## ssp

This directory contains the simulation results for the SSP models only (no SXP contribution). The file names and column information are the same as above.

## demos

This directory contains example code for plotting the nebular line emission results as a grid for various emission line diagnostics. The code presented here is adapted from existing functions in ```cloudyfsps```. For full functionality in interpreting and plotting simulation results, it is recommended that the user install and familiarize themselves with ```cloudyfsps```; however, the code presented here will work as a standalone for quick visualizations.

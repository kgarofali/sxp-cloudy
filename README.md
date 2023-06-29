# sxp-cloudy

This repository contains results for nebular line emission due to the composite simple stellar population (SSP) and simple X-ray population (SXP) models presented in Garofali et al. 2023. The photoionization simulations were performed using ```Cloudy``` v17.02, and a modified version of ```cloudyfsps```: http://nell-byler.github.io/cloudyfsps/

The output presented here is meant to enable quick inspection of the simulated nebular line emission due to the composite models for user-defined line diagnostics. We also provide Table A.1 (nebular line list) in machine readable format. For detailed descriptions of the models and assumptions therein, please see Garofali et al. 2023. For questions about the simulation output, please contact kristen DOT garofali AT nasa DOT gov.

## sxp-ssp

This directory contains the simulation results for the full suite of composite SXP + SSP models.

The ```ZAU.pars``` file contains one line for each point in the full grid of models. The columns are as follows: model number (1-147), logZ (solar units), age (Myr), logU, logR (cm), logQ (s^-1), nH (cm^-3), and the stopping criteria (the same for all simulations, corresponding to when the ionized fraction falls to 1%).

There is one ```ZAUXX.lineflux``` file per point in the grid, where XX refers to the model number (corresponding to the number in the first column of the ```ZAU.pars``` file). In each .lineflux file, the columns are as follows: vacuum wavelength (Angstroms), emergent line emission (erg/s) emitted by a full spherical shell.  

## ssp

This directory contains the simulation results for the SSP-only models (no SXP contribution). The file names and column information are the same as above.

## demos

This directory contains example code (```plot_grids.py```) for plotting the full suite of simulated nebular line emission as a grid for user-defined emission line diagnostics. The ```plot_grids.py``` demo can be run from the command line or in an interactive python environment. Running the code will interactively produce images for six emission line diagnostics corresponding to figures presented in Garofali et al. 2023; closing one figure will automatically advance to the next figure. The user can follow these examples to create their own emission line diagnostics for different lines and/or produce grids for different burst ages.

The code presented here is adapted from existing functions in ```cloudyfsps```. For full functionality in interpreting and plotting simulation results, it is recommended that the user install and familiarize themselves with ```cloudyfsps```; however, the code presented here will work as a standalone for quick visualizations.

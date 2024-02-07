#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mpl_colors
from matplotlib import cm as cmx


c = 2.9979e18 #ang/s
lsun = 3.839e33 #erg/s
planck = 6.626e-27
pc_to_cm = 3.08568e18

def getColors(vals, cname='CMRmap', minv=0.05, maxv=0.8, cmap=None,
              set_bad_vals=False, return_cNorm=False,
              logNorm=False, Ncol=100, return_cmap=False):
    '''
    sM = getColors(arr, cname='jet', minv=0.0, maxv=1.0)
    sM,cNorm = getColors(arr, cmap=cubehelix.cmap(), return_cNorm=True)
    '''
    if cmap is None:
        cmap = plt.get_cmap(cname)
    new_cmap = mpl_colors.LinearSegmentedColormap.from_list('trunc({0}, {1:.2f}, {2:.2f})'.format(cmap.name, minv, maxv), cmap(np.linspace(minv, maxv, Ncol)))
    if set_bad_vals:
        new_cmap.set_bad('white', alpha=1.0)
    if logNorm:
        cNorm = mpl_colors.LogNorm(vmin=vals.min(), vmax=vals.max())
    else:
        cNorm = mpl_colors.Normalize(vmin=vals.min(), vmax=vals.max())
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=new_cmap)
    if return_cNorm:
        return scalarMap, cNorm
    if return_cmap:
        color_list = new_cmap(np.linspace(minv, maxv, Ncol))
        cmap_name = new_cmap.name+str(Ncol)
        return new_cmap.from_list(cmap_name, color_list, Ncol)
    else:
        scalarMap.set_array(vals)
        return scalarMap

def nColors(n, **kwargs):
    '''
    n_colors(50, minv=0.5, maxv=1.0, cname='Blues')
    '''
    sM = getColors(np.linspace(0.0, 1.0), **kwargs)
    colors = [sM.to_rgba(v) for v in np.linspace(0.0, 1.0, n)]
    return colors

class modObj(object):
    '''
    '''
    def __init__(self, dir_, prefix, parline, **kwargs):
        '''
        this needs to be called from other class or given
        a line from a ".pars" file
        [0]modnum; [1]logZ; [2]age; [3]logU; [4]logR; [5]logQ
        '''
        self.modnum = int(parline[0])
        self.logZ = parline[1]
        self.age = parline[2]
        self.logU = parline[3]
        self.logR = parline[4]
        self.logQ = parline[5]
        self.nH = parline[6]
        try:
            self.efrac = parline[7]
        except IndexError:
            self.efrac = -1.0
        try:
            self.fbhb = parline[8]
        except IndexError:
            self.fbhb = 0.0

        self.logq = np.log10((10.0**self.logQ)/(np.pi*4.0*self.nH*(10.0**self.logR)**2.0))
        self.fl = '{}{}{}'.format(dir_, prefix, self.modnum)
        self.load_lines()
        return
    def add_lines(self, lines):
        line_info = np.genfromtxt(self.fl+'.lineflux')
        lam, flu = line_info[:,0], line_info[:,1]
        for name, wav in list(lines.items()):
            matchind = np.argmin(np.abs(lam-wav))
            self.__setattr__(name, flu[matchind])
        return
    def load_lines(self, **kwargs):
        lines = {'Lya':1215.67,
                 'Ha':6564.723,
                 'Hb':4862.763,
                 'HeIIu': 1640.43,
                 'HeII':4687.024,
                 'CIIIua': 1906.68,
                 'CIIIub': 1908.73,
                 'CIVa': 1548.19,
                 'CIVb': 1550.78,
                 'NIIa':6549.959,
                 'NIIb':6585.369,
                 'OIIa': 3727.118,
                 'OIIb': 3730.119,
                 'OIIIua': 1660.81,
                 'OIIIub': 1666.00,
                 'OIIIa': 4960.37,
                 'OIIIb':5008.314,
                 'OIVi': 258906.4,
                 'NeIIi': 128137.9,
                 'NeIIIb':3869.917,
                 'NeIIIia': 155553.7,
                 'NeV': 3427.066,
                 'NeVia': 143269.2,
                 'SIIa':6718.396,
                 'SIIb':6732.78,
                }

        self.lines = dict(names=np.array(list(lines.keys())), wavs=np.array(list(lines.values())))

        line_info = np.genfromtxt(self.fl+'.lineflux')
        lam, flu = line_info[:,0], line_info[:,1]
        for name, wav in list(lines.items()):
            matchind = np.argmin(np.abs(lam-wav))
            self.__setattr__(name, flu[matchind])
        def logify(a,b):
            with np.errstate(divide='ignore'):
                return np.log10(a/b)

        #
        self.log_HeII_Hb = logify(self.HeII, self.Hb)
        self.log_HeIIu_CIII = logify(self.HeIIu, (self.CIIIua + self.CIIIub))
        #
        self.log_CIII_HeIIu = logify((self.CIIIua + self.CIIIub), self.HeIIu)
        self.log_CIV_OIII = logify((self.CIVa + self.CIVb),
                                   (self.OIIIub + self.OIIIua))
        self.log_CIV_CIII = logify((self.CIVa + self.CIVb),
                                   (self.CIIIua + self.CIIIub))
        #
        self.log_NII_Ha = logify(self.NIIa+self.NIIb, self.Ha)
        self.log_NIIb_Ha = logify(self.NIIb, self.Ha)
        #
        self.log_OIIIb_Hb = logify(self.OIIIb, self.Hb)
        self.log_OIII_Hb = logify((self.OIIIb + self.OIIIa), self.Hb)
        self.log_OIII_CIII = logify((self.OIIIua + self.OIIIub),
                                    (self.CIIIua + self.CIIIub))
        self.log_OIIIub_HeIIu = logify(self.OIIIub,self.HeIIu)
        self.log_OIVi_NeIIIia = logify(self.OIVi, self.NeIIIia)
        #
        self.log_NeV_NeIIIb = logify(self.NeV, self.NeIIIb)
        self.log_NeIIIia_NeIIi = logify(self.NeIIIia, self.NeIIi)
        self.log_NeVia_NeIIIia = logify(self.NeVia, self.NeIIIia)
        self.log_NeIIIb_OII = logify(self.NeIIIb, self.OIIa + self.OIIb)

        return


class allmods(object):
    '''
    mods = outobj.allmods(dir, prefix)
    '''
    def __init__(self, dir_, prefix, **kwargs):
        self.modpars = np.genfromtxt('{}{}.pars'.format(dir_, prefix))
        self.load_mods(dir_, prefix, **kwargs)
        self.set_pars()
        self.set_arrs()

    def load_mods(self, dir_, prefix, **kwargs):
        mods = []
        for par in self.modpars:
            mod = modObj(dir_, prefix, par, **kwargs)
            mods.append(mod)
        self.__setattr__('mods', mods)
        self.__setattr__('nmods', len(mods))
        return
    def set_pars(self):
        self.logZ_vals = np.unique(self.modpars[:,1])
        self.age_vals = np.unique(self.modpars[:,2])
        self.logU_vals = np.unique(self.modpars[:,3])
        self.logR_vals = np.unique(self.modpars[:,4])
        self.logQ_vals = np.unique(self.modpars[:,5])
        self.nH_vals = np.unique(self.modpars[:,6])
        try:
            self.efrac_vals = np.unique(self.modpars[:,7])
        except IndexError:
            self.efrac_vals = np.array([-1.0])
        try:
            self.fbhb_vals = np.unique(self.modpars[:,8])
        except IndexError:
            self.fbhb_vals = np.array([0.0])
    def set_arrs(self):
        iterstrings = ['logZ', 'age', 'logU', 'logR', 'logQ', 'nH',
                       'efrac','fbhb']
        for i in iterstrings:
            vals = np.array([mod.__getattribute__(i) for mod in self.mods])
            self.__setattr__(i, vals)
    def add_arrs(self, *args):
        for item in args:
            try:
                vals = np.array([mod.__getattribute__(item) for mod in self.mods])
                self.__setattr__(item, vals)
            except AttributeError:
                continue
        return
    def add_lines(self, linedict={}):
        '''
        self.add_lines(linedict={'O3':1666.0})
        '''
        [mod.add_lines(linedict) for mod in self.mods]
        return
    def group_mods(self, xval='logZ', yval='age', zval='NIIb',
                   const='logU', cval=-2.0, make_cut=False, **kwargs):
        grid_x = self.__getattribute__(xval+'_vals')
        grid_y = self.__getattribute__(yval+'_vals')
        if make_cut:
            xlims = kwargs.get('xlims', (-1.0, 0.1))
            ylims = kwargs.get('ylims', (0.0, 10.e6))
            grid_x = grid_x[(grid_x >= xlims[0]) & (grid_x <= xlims[1])]
            grid_y = grid_y[(grid_y >= ylims[0]) & (grid_y <= ylims[1])]
        X, Y = np.meshgrid(grid_x, grid_y)
        Z = np.zeros_like(X)
        for index, x in np.ndenumerate(Z):
            mind = [i for i in range(self.nmods)
                    if (self.mods[i].__getattribute__(xval) == X[index]
                        and self.mods[i].__getattribute__(yval) == Y[index]
                        and self.mods[i].__getattribute__(const) == cval)]
            try:
                Z[index] = self.mods[mind[0]].__getattribute__(zval)
            except AttributeError:
                print('not a valid attribute.')
        if xval == 'age':
            X*=1.0e-6
        if yval == 'age':
            Y*=1.0e-6
        return X,Y,Z

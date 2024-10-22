import numpy as np
from sympy import *
import pandas as pd

# Defining the Observables
q = Symbol('q')
omega = Symbol('\Omega')
sigma = Symbol('\Sigma')
sigmatot = Symbol('Sigma_tot')
sigmasfr = Symbol('Sigma_SFR')
T = Symbol('T')

# Defining the Constants
calpha = Symbol('C_alpha')
gamma = Symbol('gamma')
boltz = Symbol('k_B')
mu = Symbol('mu')
mu0 = Symbol('Mu_0')
mh = Symbol('m_H')
G = Symbol('G')
xio = Symbol('xi_0')
delta = Symbol('\delta')
mstar = Symbol('m_*')
cl = Symbol('C_l')
kappa = Symbol('kappa')
E51 = Symbol('E_51')
Rk = Symbol('R_k')
zet = Symbol('zeta')
psi = Symbol('psi')
kalpha = Symbol('K_alpha')
Gamma = Symbol('Gamma')
eta = Symbol('eta')
Nsb = Symbol('N_sb')
bet = Symbol('beta')
alphak = Symbol('alpha_k')
Gamma = Symbol('Gamma')
A = Symbol('A')
K = Symbol('K')


# Defining the general parameters
u = Symbol('u')
tau = Symbol('tau')
l = Symbol('l')
max_mach = Symbol('M')
n = Symbol('n')
nu = Symbol('nu')

# You can select any combination of regimes as described in the regimes.py file,
# or  you can select one of the moel given in the manuscript and use model_seletor function to obtain the corresponding regimes.
#from regimes import hreg, lreg, ureg, taureg, alphareg 
from model_generator import model_gen_regime, model_selector

model = 'Model Alt 2'
for r in ['a','b']:
    hreg, lreg, ureg, taureg = model_selector(model,r)
    alphareg='regime 1'

    quantities = model_gen_regime(hreg, lreg, ureg, taureg, alphareg)

    # conversion factors and physical constants used to convert all quantities to cgs units for consistency
    g_Msun = 1.989e33  # solar mass in g
    cgs_G = 6.674e-8  # gravitational constant in cgs units
    g_mH = 1.6736e-24  # mass of hydrogen atom in grams
    cgs_kB = 1.3807e-16  # boltzmann constant in cgs units
    pc_kpc = 1e3  # number of pc in one kpc
    cm_kpc = 3.086e+21  # number of centimeters in one parsec
    cm_pc = cm_kpc/pc_kpc
    cm_km = 1e5  # number of cm in one km
    s_yr = (365*24*60*60)
    s_Myr = 1e+6*s_yr  # number of seconds in one megayear



    # Reading the Constant values
    gval, clval, xioval, mstarval, deltaval, e51val, kaval, Gammaval, Caval, Rkval, muval, mu0val, etaval = tuple(
        np.genfromtxt('constants.in', delimiter='=', dtype=np.float64)[:, -1])

    # List of tuples for substituting the values in the symbol. 
    # The firt element of each tuple is the symbol for which the value needs to be substituted
    # The second element is the numerical value which is stored in constants.in file
    const = [(boltz, cgs_kB), (mh, g_mH), (G, cgs_G), (gamma, gval),
            (calpha, Caval), (Rk, Rkval), (mu, muval), (cl,
                                                clval), (xio, xioval), (mstar, mstarval*g_Msun),
            (delta, deltaval), (E51, e51val), (kalpha, kaval), (Gamma, Gammaval), (mu0, mu0val), (eta, etaval),
            (Nsb, 1),(zet,10),(bet,8),(K,0.3),(psi,1),(A,1.414)]

    ks_leroy = (1e-9/(365*24*60*60))/(10*g_Msun*(cm_pc)**(-2))**(0.4)
    ks_paper2 = 1.102e-15

    idx = 1
    print(str(model)+str(r))
    print('              a                  b')

    for idx in [4,5,6]:
        final_quantity = quantities[idx]
        quantity_string = ['h', 'l', 'u', 'tau',
                        'biso', 'bani', 'Bbar', 'tanpB']

        # values subsituted for the observables. They are set to typical values observed in a galaxy
        variables = [(sigmatot, 175*g_Msun/(cm_pc)**2),# (sigma, 5*g_Msun/(cm_pc)**2), (sigmasfr, sfr),
                        (omega, 20*cm_km/cm_kpc), (q, 1), (T, 1e+4)]
        # the final substituents are the physical constants and the observables
        final = const + variables
        final_quan_val = final_quantity.subs(final)
        #store the quantity chosen
        quantity_chosen = quantity_string[idx]

        # #printing the quantity in cgs units
        # print(f'The quantity {quantity_chosen} for the above given values is {float(final_quan_val):.3} in cgs units')

        ks = simplify(final_quan_val.subs(sigma,(sigmasfr/K)**(1/1.4)))

        coef = ks.subs([(sigmasfr,1),(K,1e-16)])
        obs = sigmasfr
        b = (diff(log(ks), obs)*obs).subs(obs, 1)
        conv_fact = (g_Msun*((s_yr)**(-1))*((cm_kpc)**(-2))*1e-3)**(b)
        a = float(coef*conv_fact)*1e6
        print(quantity_string[idx]+': ',a,b)
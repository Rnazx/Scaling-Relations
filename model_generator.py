# import libraries
import numpy as np
import matplotlib.pyplot as plt
from sympy import *
from fractions import Fraction

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
kalpha = Symbol('K_alpha')
Gamma = Symbol('Gamma')

# Defining the general parameters
u = Symbol('u')
tau = Symbol('tau')
l = Symbol('l')
mach = Symbol('M')
n = Symbol('n')
nu = Symbol('nu')

# conversion factors
pc_kpc = 1e3  # number of pc in one kpc
cm_kpc = 3.086e+21  # number of centimeters in one parsec
cm_km = 1e5  # number of cm in one km
s_Myr = 1e+6*(365*24*60*60)  # number of seconds in one megayear


###################################################################################################
########################### Function to generate the model###########################################
#################################################################################################
def model_gen(model_no, let='a', not_ren=True, alphareg=1):
    cs = (gamma*boltz*T/(mu*mh))**Rational(1/2)
    # Function to return the expression of l given the model number

    def choose_lreg(h, model_no):
        # dependence of gas density on scale height(h)
        rho = sigma/(2*h)
        # number density
        n = rho/(mu*mh)
        # If we include correlation length from the supernovae model from Chamandy et. al. (2020)
        if [3, 4].count(model_no) > 0:
            lsn = 0.14*cm_kpc*(E51)**Fraction(16, 51) * \
                (n/0.1)**Fraction(-19, 51)*(cs/(cm_km*10))**Fraction(-1, 3)
            l = ((Gamma-1)/Gamma)*cl*lsn
            l = simplify(l)
        # Minimalistic model for l in model 1 and 2. Turbulence is driven at the maximum scale (h)
        else:
            l = simplify(cl*h)
            lsn = simplify(cl*h)
        return l, lsn, n
    # if condition to check whether turbulent velocity follows minimalistic condition
    if model_no == 1:
        u = mu0*cs
        # model for h
        h = ((u**2)/(3*pi*G*sigmatot))
        # call the function which chooses the regime for l
        l, lsn, n = choose_lreg(h, model_no)
        # mach number is u/cs
        mach = mu0
    else:
        # The letter through which subsonic regime is chosen
        if let == 'a':
            if model_no == 4:
                # alternate model for the scale height
                h = cs/omega
            else:
                # base model for the scale height
                h = (cs**2)/(3*pi*G*sigmatot)
            # supernova rate as a function of h
            nu = (delta*sigmasfr)/(2*h*mstar)
            # choose l as a function of h
            l, lsn, n = choose_lreg(h, model_no)
            # turbulent velocity according to Chamandy et. al. (2020)
            usn = ((4*pi/3)*l*lsn**3*cs**2*nu)**Fraction(1, 3)
            u = simplify(usn)
            h = simplify(h)
            # mach is max(1, u/cs) which is 1 in subsonic case
            mach = 1

        else:
            # The letter through which supersonic regime is chosen
            # first define h as a symbol as we have to solve an equation (analytically)
            h = Symbol('h')
            # The expressions are defined the same as for the subsonic case
            nu = (delta*sigmasfr)/(2*h*mstar)
            l, lsn, n = choose_lreg(h, model_no)
            u = ((4*pi/3)*l*lsn**3*cs**2*(nu))**Fraction(1, 3)
            # substitute h = 1 in the expression for u (Refer manual for further details)
            usn = u.subs(h, 1)
            if model_no == 4:
                # collect the exponents of h and bring it to the RHS to solve for h
                h = simplify(((usn)/(omega))**(1/(1-diff(log(u), h)*h)))
            else:
                # collect the exponents of h and bring it to the RHS to solve for h
                h = simplify(((usn**2)/(3*pi*G*sigmatot))
                             ** (1/(1-2*diff(log(u), h)*h)))
            # Finally substitute h in l, nu and u
            l, lsn, n = choose_lreg(h, model_no)
            nu = (delta*sigmasfr)/(2*h*mstar)
            u = simplify(((4*pi/3)*l*lsn**3*cs**2*(nu))**Fraction(1, 3))
            # mach is max(1, u/cs) which is u/cs in supersonic case
            mach = u/cs
    # eddy turnover time
    taue = simplify(l/u)
    # Models 1 and 2 do not take into consideration teh effect of supernovae in the correlation time
    # so we set the renovation time as the eddy turnover time
    if model_no == 2 or model_no == 1:
        taur = taue
    # expression for the supernovae renovation time
    else:
        taur = simplify(6.8*s_Myr*(1/4)*(nu*cm_kpc**3*s_Myr/50)**(-1)*(E51)**Fraction(-16, 17)
                        * (n/0.1)**Fraction(19, 17)*(cs/(cm_km*10)))  # does not work if model no = 2
    # not_ren checks if the regime of correlation time is  is eddy turnover time or renovation time
    # True means eddy turnover time, False means renovation time
    if not_ren == False:
        tau = taue
    else:
        tau = taur

    # after solving for h we put it into the other expressions
    #define rho again for the supersonic case as we have to input the final expression for h
    rho = sigma/(2*h)
    # Magnetic field considering equipartition
    Beq = u*(4*pi*rho)**Rational(1/2)

    #Expression for the isotropic magnetic field from Federrath et. al. (2011)
    #mach is max(1, u/cs)
    biso = (Beq*(xio**(1/2)))/mach
    biso = simplify(biso)
    biso = biso.powsimp(force=True)

    #Expression for the anisotropic magnetic field considering differential rotation
    bani = biso*(Rational(2/3)*q*omega*tau)**Rational(1/2)
    bani = simplify(bani)
    bani = bani.powsimp(force=True)

    # Expression for the mean magnetic field from Dynamo theory
    Rk = Symbol('R_k')
    eta = (1/3)*tau*u**2
    #Three regimes for alpha_k are chosen and scaling relations can be found for each regime
    alphak1 = calpha*tau**2*u**2*omega/h
    alphak2 = calpha*tau*u**2/h
    alphak3 = kalpha*u
    if alphareg == 1:
        alphak = alphak1
    elif alphareg == 2:
        alphak = alphak2
    else:
        alphak = alphak3
    # Substitute alpha_k in the reynolds numbers
    Ralpha = alphak*h/eta
    Romega = -q*omega*h**2/eta
    #Dynamo numbers
    Dk = Ralpha*Romega
    Dc = -(pi**5)/32
    # Final expression for mean magnetic field after some approximations
    Bbar = (pi*Beq*l*(Rk*(Dk/Dc))**Rational(1/2))/h
    Bbar = simplify(Bbar)

    # Expression for the pitch angle of the mean magnetic field
    tanpB = -((pi**2)*tau*(u**2))/(12*q*omega*(h**2))
    tanpB = simplify(tanpB)
    # Substitute tau and l in tanpB
    tanpB = tanpB.subs([(tau, tau), (l, l)])
    tanpB = simplify(tanpB)

    # Expression for the pitch angle of the mean magnetic field
    tanpb = 1/(1+q*omega*tau)

    #Put all the expression in a single list
    quantities = [h, l, u, tau, biso, bani, Bbar, tanpB, tanpb]

    return quantities

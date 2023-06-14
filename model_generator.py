#import libraries
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

# Defining the general parameters
u = Symbol('u')
tau = Symbol('tau')
l = Symbol('l')
mach = Symbol('M')
n = Symbol('n')
nu = Symbol('nu')

#conversion factors
pc_kpc = 1e3  # number of pc in one kpc
cm_kpc = 3.086e+21  # number of centimeters in one parsec
cm_km = 1e5  # number of cm in one km
s_Myr = 1e+6*(365*24*60*60)  # number of seconds in one megayear

# Defining the expressions
cs = (gamma*boltz*T/(mu*mh))**Rational(1/2)


###################################################################################################
###########################Function to generate the model###########################################
#################################################################################################
def model_gen(model_no, let, tbool = True, alphareg = 1):
    def find_hlut(model_no, let):
        def choose_lreg(h, model_no):
            rho = sigma/(2*h)
            n = rho/((14/11)*mh)
            if [3, 4].count(model_no)>0 :
                lsn = 0.14*cm_kpc*(E51)**Fraction(16, 51) * (n/0.1)**Fraction(-19, 51)*(cs/(cm_km*10))**Fraction(-1, 3)
                l = (3/10)*lsn
                l = simplify(l)
            else:
                l = simplify(cl*h)
                lsn = simplify(h)
            return l, lsn, n
        if model_no ==1:
            u = mu0*cs
        else:
            if let == 'a':
                if model_no == 4:
                    h = cs/omega
                else: 
                    h = (cs**2)/(3*pi*G*sigmatot)
                nu = (delta*sigmasfr)/(2*h*mstar)
                l, lsn, n = choose_lreg(h, model_no)
                usn = ((4*pi/3)*l*lsn**3*cs**2*nu)**Fraction(1, 3)
                u = simplify(usn)
                h = simplify(h)
                mach = 1
                
            else:
                h = Symbol('h')
                nu = (delta*sigmasfr)/(2*h*mstar)
                l, lsn, n = choose_lreg(h, model_no)
                u = ((4*pi/3)*l*lsn**3*cs**2*(nu))**Fraction(1, 3)
                usn = u.subs(h, 1)
                if model_no == 4:
                    h = simplify(((usn)/(omega))**(1/(1-diff(log(u), h)*h)))
                else:
                    h = simplify(((usn**2)/(3*pi*G*sigmatot))**(1/(1-2*diff(log(u), h)*h)))
                l, lsn, n = choose_lreg(h, model_no)
                nu = (delta*sigmasfr)/(2*h*mstar)
                u = simplify(((4*pi/3)*l*lsn**3*cs**2*(nu))**Fraction(1, 3))
                mach = u/cs
        taue = simplify(l/u)
        if model_no ==2: taur = taue
        else : taur = simplify(6.8*s_Myr*(1/4)*(nu*cm_kpc**3*s_Myr/50)**(-1)*(E51)**Fraction(-16, 17) * (n/0.1)**Fraction(19, 17)*(cs/(cm_km*10)))# does not work if model no = 2
        if model_no ==2 or tbool == False:
            tau = taue
        else :
            tau = taur
        return [h, l ,u, tau, nu, n, cs, mach, taue, taur]
    h, l, u, tau, nu, n, cs, mach, taue, taur = find_hlut(model_no, let)
    rho = sigma/(2*h)
    Beq = u*(4*pi*rho)**Rational(1/2)
    biso = (Beq*(xio**(1/2)))/mach
    biso = simplify(biso)
    biso = biso.powsimp(force=True)

    bani = biso*(Rational(2/3)*q*omega*tau*(1+(q*omega*tau)/2))**Rational(1/2)#
    bani = simplify(bani)
    bani = bani.powsimp(force=True)

    Rk = Symbol('R_k')
    eta = (1/3)*tau*u**2
    alphak1 = calpha*tau**2*u**2*omega/h
    alphak2 = calpha*tau*u**2/h
    alphak3 = kalpha*u
    if alphareg == 1:
        alphak = alphak1
    elif alphareg == 2:
        alphak = alphak2
    else :
        alphak = alphak3
    Ralpha = alphak*h/eta
    Romega = -q*omega*h**2/eta
    Dk = Ralpha*Romega
    Dc = -(pi**5)/32
    rho = sigma/(2*h)
    Beq = (4*pi*rho)**Rational(1/2)*u
    Bbar = (pi*Beq*l*(Rk*(Dk/Dc-1))**Rational(1/2))/h
    Bbar = simplify(Bbar)
    #Bbar = Bbar.powsimp(force=True)

    tanpb = -((pi**2)*tau*(u**2))/(12*q*omega*(h**2))
    tanpb = simplify(tanpb)
    tanpb = tanpb.subs([(tau, tau), (l, l)])
    tanpb = simplify(tanpb)

    tanpbm = 1/(1+q*omega*tau)

    quantities = [ h, l, u, tau, biso, bani, Bbar, tanpb,tanpbm, nu, n, cs, alphak, Dk, Dc, omega*tau,  kalpha*h/(calpha*tau*u), alphak1, alphak2, alphak3,  taue, taur]

    return quantities

# import libraries
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

# conversion factors
pc_kpc = 1e3  # number of pc in one kpc
cm_kpc = 3.086e+21  # number of centimeters in one parsec
cm_km = 1e5  # number of cm in one km
s_Myr = 1e+6*(365*24*60*60)  # number of seconds in one megayear


###################################################################################################
########################### Function to generate the model###########################################
#################################################################################################

######################################################################################################
#Model generator based on the regime

def model_gen_regime(hreg, lreg, ureg, taureg, alphareg='regime 1'):
    cs = (gamma*boltz*T/(mu*mh))**Rational(1/2)

    # Function to return the expression of l given the regime
    def choose_lreg(h, lreg):
        nu = (delta*sigmasfr)/(2*h*mstar)
        # dependence of gas density on scale height(h)
        rho = sigma/(2*h)
        # number density
        n = rho/(mu*mh)
        # If we include correlation length from the supernovae model from Chamandy and Shukurov (2020)
        #Model S
        #fsb = 0
        if lreg == 'isolated supernova-driven':
            ls = psi*0.14*cm_kpc*(E51)**(16/51) * \
                (n/0.1)**(-19/51)*(cs/(cm_km*10))**(-1/3)
            nu = nu
            l = ((Gamma-1)/Gamma)*cl*ls
            l = (l)
        #fsb = 1, Nsb is set to 1 later on as it does not affect the scaling relations
        elif lreg == 'superbubble-driven':
            #Eqn 10 Chamandy and Sukurov (2020)
            Rsb = 0.53*cm_kpc*(eta/0.1)**(1/3)*(Nsb/100)**(1/3)*(E51)**(1/3)*(n/0.1)**(-1/3)*(cs/(cm_km*10))**(-2, 3)
            ls = psi*Rsb
            nu = nu/Nsb
            l = ((Gamma-1)/Gamma)*cl*ls
            l = (l)
        # Minimalistic model for l in model Alt 1 and 2. Turbulence is driven at the maximum scale (h)
        elif lreg == 'maximum scale-driven':
            l = psi*(cl*h)
            ls = psi*(cl*h)
        else:
            raise ValueError("Invalid correlation length (l) regime input")
        return l, ls, n, nu
    # Function to return the expression of u given the regime.
    def choose_ureg(h, ureg):
        # We first choose l according to the regime
        l, ls, n, nu = choose_lreg(h, lreg)
        # If u is set equal to the sound speed cs
        #Model 1
        if ureg == 'sound speed' :
            u = mu0*cs
        #If the regime is supernovae driven, the expression for u is taken from Chamandy and Shukurov (2020)
        #Models 2 and 3
        elif ureg == 'supenovae/superbubble-driven':
            u = ((4*pi/3)*l*ls**3*cs**2*(nu))**(1/3)
        else:
            raise ValueError("Invalid turbulent velocity (u) regime input")          
        return l,ls,u,n,nu
    # Edge case where in the expression for h, we assume u<<cs (w = u^2 +cs^2)
    if hreg == 'subsonic':
        h = (cs**2)/(3*pi*G*((sigmatot/zet)))
    # Edge case where in the expression for h, we assume u>>cs
    # This case is slightly more complicate since u indirectly depends on h through l
    # Hence we need to algebraically solve the equation 
    elif hreg == 'supersonic':
        #First define h as a symbol
        h = Symbol('h')
        #Solve for l and u as a function of h which is just a symbol
        l,ls,u,n,nu = choose_ureg(h, ureg)
        # define a new quantity us where h is set to 1 in the expression for u
        us = u.subs(h, 1)
        # The standard expression for h raised to the power of 1/(1-2*(exponent of h in u))
        h = ((us**2)/(3*pi*G*(sigmatot/zet)))**(1/(1-2*diff(log(u), h)*h))#exponent is found by differentiating the log
    #alternate expression for h
    elif hreg == 'cs/omega':
        h = cs/omega
    else:
        raise ValueError("Invalid scale height (h) regime input")
    l,ls,u,n,nu = choose_ureg(h, ureg)
    # Define max_mach as max(1,u/cs) which will be used later on in the expression for b_iso
    if hreg == 'supersonic':
        max_mach = u/(A*cs)
    else:
        max_mach = 1
    # Regime for the turbulence correlation time
    # If the regime for tau is eddy turnover time
    if taureg == 'eddy turnover time':
        tau = (l/u)
    # If the regime for tau is supernovae renovation time
    # The quantities are all converted to cgs units for standardization
    elif taureg == 'supernovae/superbubble renovation time':
        tau = ((4/3)*pi*nu*(ls**3))**(-1) # does not converge if model no = 2
    # after solving for h we put it into the other expressions
    #define rho again for the supersonic case as we have to input the final expression for h
    else: 
        raise ValueError("Invalid correlation time regime input")
    rho = sigma/(2*h)
    
    # Magnetic field considering equipartition
    Beq = bet*u*(4*pi*rho)**Rational(1/2)
    
    #Expression for the isotropic magnetic field from Federrath et. al. (2011)
    #max_mach is max(1, u/cs)
    biso = (Beq*(xio**(1/2)))/max_mach# change the name
    #biso = biso.powsimp(force=True)

    #Expression for the anisotropic magnetic field considering differential rotation
    bani = biso*((2/3)*q*omega*tau)**(1/2)# mention the approximations
    #bani = bani.powsimp(force=True)
    # Expression for the mean magnetic field from Dynamo theory
    Rk = Symbol('R_k')
    eta_t = (1/3)*tau*u**2
    #Three regimes for alpha_k are chosen and scaling relations can be found for each regime
    # Refer to equation 19 from manuscript
    alphak1 = calpha*tau**2*u**2*omega/h
    alphak2 = calpha*tau*u**2/h
    alphak3 = kalpha*u
    if alphareg == 'regime 1':
        alphak = alphak1
    elif alphareg == 'regime 2':
        alphak = alphak2
    else:
        alphak = alphak3
    # Substitute alpha_k in the reynolds numbers
    Ralpha = alphak*h/eta_t
    Romega = -q*omega*h**2/eta_t
    #Dynamo numbers
    Dk = Ralpha*Romega
    Dc = -(pi**5)/32
    # Final expression for mean magnetic field after some approximations
    Bbar = (K*pi*Beq*(l/h)*(Rk*(Dk/Dc))**(0.5))

    # Expression for the pitch angle of the mean magnetic field
    tanpB = -((pi**2)*tau*(u**2))/(12*q*omega*(h**2))
    # Substitute tau and l in tanpB
    tanpB = tanpB.subs([(tau, tau), (l, l)])# change the names

    # Expression for the pitch angle of the random magnetic field
    tanpb = 1/(1+q*omega*tau)

    #Put all the expression in a single list
    quantities = [h, l, u, tau, biso, bani, Bbar, tanpB]

    return quantities

################################################################################################################
#you can select one of the moel given in the manuscript and use model_seletor function to obtain the corresponding regimes.
def model_selector(model = 'Model S',subreg = 'a'):
    if model == 'Model S':
        lreg='isolated supernova-driven'
        ureg='supenovae/superbubble-driven'
        if subreg == 'a' : 
            hreg='subsonic'
            taureg='eddy turnover time'
        elif subreg == 'b':
            hreg='supersonic'
            taureg='eddy turnover time'
        elif subreg == 'c':
            hreg='subsonic'
            taureg='supernovae/superbubble renovation time'
        elif subreg == 'd':
            hreg='supersonic'
            taureg='supernovae/superbubble renovation time'
        else:
            print('enter a valid subregime')
    elif model == 'Model Alt 2':
        lreg='maximum scale-driven'
        ureg='supenovae/superbubble-driven'
        if subreg == 'a' : 
            hreg='subsonic'
            taureg='eddy turnover time'
        elif subreg == 'b':
            hreg='supersonic'
            taureg='eddy turnover time'
        else:
            print('enter a valid subregime')
    elif model == 'Model Alt 1':
        lreg='maximum scale-driven'
        ureg='sound speed'
        hreg=  'subsonic' #**does not matter as both give same answer**
        taureg='eddy turnover time'
    else:
        print('enter a valid model')
    return hreg, lreg, ureg, taureg

##############################################################################################################
#model generator based on model no
def model_gen(model_no, let = 'a', alphareg=1):
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
        max_mach = mu0
    else:
        # The letter through which subsonic regime is chosen
        if let == 'a' or let =='c':
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
            # turbulent velocity according to Chamandy and Shukurov (2020)
            usn = ((4*pi/3)*l*lsn**3*cs**2*nu)**Fraction(1, 3)
            u = simplify(usn)
            h = simplify(h)
            # max_mach is max(1, u/cs) which is 1 in subsonic case
            max_mach = 1

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
            # max_mach is max(1, u/cs) which is u/cs in supersonic case
            max_mach = u/cs
    
    # Models Alt 1 and Alt 2 do not take into consideration the effect of supernovae in the correlation time
    # so we set the renovation time as the eddy turnover time
    # eddy turnover time
    if let == 'a' or let == 'b':
        tau = simplify(l/u)
    # expression for the supernovae renovation time
    else:
        tau = simplify(6.8*s_Myr*(1/4)*(nu*cm_kpc**3*s_Myr/50)**(-1)*(E51)**Fraction(-16, 17)
                        * (n/0.1)**Fraction(19, 17)*(cs/(cm_km*10)))  # does not work if model Alt 2
    # after solving for h we put it into the other expressions
    #define rho again for the supersonic case as we have to input the final expression for h
    rho = sigma/(2*h)
    # Magnetic field considering equipartition
    Beq = u*(4*pi*rho)**Rational(1/2)

    #Expression for the isotropic magnetic field from Federrath et. al. (2011)
    #max_mach is max(1, u/cs)
    biso = (Beq*(xio**(1/2)))/max_mach# change the name
    biso = simplify(biso)
    biso = biso.powsimp(force=True)
    
    #Expression for the anisotropic magnetic field considering differential rotation
    bani = biso*(Rational(2/3)*q*omega*tau)**Rational(1/2)# mention the approximations
    bani = simplify(bani)
    bani = bani.powsimp(force=True)

    # Expression for the mean magnetic field from Dynamo theory
    Rk = Symbol('R_k')
    eta_t = (1/3)*tau*u**2
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
    Ralpha = alphak*h/eta_t
    Romega = -q*omega*h**2/eta_t
    #Dynamo numbers
    Dk = Ralpha*Romega
    Dc = -(pi**5)/32
    # Final expression for mean magnetic field after some approximations
    Bbar = (pi*Beq*l*(Rk*(Dk/Dc))**(1/2))/h
    Bbar = simplify(Bbar)

    # Expression for the pitch angle of the mean magnetic field
    tanpB = -((pi**2)*tau*(u**2))/(12*q*omega*(h**2))
    tanpB = simplify(tanpB)
    # Substitute tau and l in tanpB
    tanpB = tanpB.subs([(tau, tau), (l, l)])# change the names
    tanpB = simplify(tanpB)

    # Expression for the pitch angle of the random magnetic field
    tanpb = 1/(1+q*omega*tau)

    #Put all the expression in a single list
    quantities = [h, l, u, tau, biso, bani, Bbar, tanpB, tanpb]

    return quantities

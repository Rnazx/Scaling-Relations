# Scaling Relations Finder
A general framework to find the scaling relations between magnetic field properties and observables for a model of galactic magnetic fields
### Libraries Used
* sympy
* matplotlib
* ipywidgets
## Code Description
Mean and random components of the magnetic field are modelled based on the following observables:
![obs](https://github.com/Rnazx/Scaling-Relations/assets/42196798/bb3e29fe-9bc9-4374-876b-fe5da0455514)

The turbulence and magnetic field models are solved in the [jupyter notebook](https://github.com/Rnazx/Scaling-Relations/blob/master/scaling_relations.ipynb). Different regimes of the model can be chosen in the notebook from the python widgets. 
* The model for the scale height is inpired by [Forbes et. al. (2012)](https://ui.adsabs.harvard.edu/abs/2012ApJ...754...48F/abstract) is given by
```math
  h= \frac{\zeta w^2}{3\pi G \Sigma_{tot}},
```
where $1\lesssim\zeta\lesssim20$ is a parameter and $w=\max(u,c_\mathrm{s}$.
An alternative model is also included where 
```math
  h= \frac{c_s}{\Omega}
```
* For the turbulent correlation length we have a choice between a minimalistic model which assumes that the turbulence is driven at the maximum scale $h$ and another model based on [Chamandy \& Shukurov (2020)](https://ui.adsabs.harvard.edu/abs/2020Galax...8...56C/abstract) which assumes supernovae predominately drive turbulence.
*  Similarly the turbulent velocity $u$ has a minimalistic regime where it is set equal to the sound speed $c_\mathrm{s}$ and another regime where the model for $u$ is taken from [Chamandy \& Shukurov (2020)](https://ui.adsabs.harvard.edu/abs/2020Galax...8...56C/abstract). Here $h$ depends on $u$ but $u$ can also depend on $h$ through $\nu$ and $l$. To obtain an expression for $h$, an expression for $u$ is found in terms of $h$ and then is substituted back to obtain a relation between the right-hand-side (RHS) and $h$. 
* Let us say RHS $=Hh^\beta$ where $H$ contains the other quantities which are independent of $h$. Thus $h = H^{1/(1-\beta)}$. This algorithm is implemented in Sympy to obtain an expression for $h$. The value of $\beta$ is found using $\beta = \partial \log(u)/\partial \log(h)$.
* Finally the turbulence correlation time has two regimes. The eddy turnover time $\tau = l/u$ or the renovation time of the flow ([Chamandy \& Shukurov 2020)](https://ui.adsabs.harvard.edu/abs/2020Galax...8...56C/abstract).
* These expressions are finally substituted into the magnetic field model to obtain the following quantities:
 ![mag](https://github.com/Rnazx/Scaling-Relations/assets/42196798/2abb8bf5-9a63-4916-9846-ff2a17305ef5).
* Finally the scaling relations for all the quantities are found using 
```math
  \frac{\partial \log(quantity)}{\partial \log(observable)}
```

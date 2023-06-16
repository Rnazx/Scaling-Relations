# Scaling Relations Finder
A general framework to find the scaling relations for a model for galactic magnetic fields based on observables
### Libraries Used
* sympy
* matplotlib
* ipywidgets
## Code Description
Mean and random components of the magnetic field are modelled based on the following observables
![obs](https://github.com/Rnazx/Scaling-Relations/assets/42196798/bb3e29fe-9bc9-4374-876b-fe5da0455514)

For different regimes of the model, the turbulence and magnetic field models are solved in the [jupyter notebook](https://github.com/Rnazx/Scaling-Relations/blob/master/scaling_relations.ipynb). Different regimes of the model can be chosen in the notebook from the python widgets. 
* The model for the scale height inpired by Forbes et. al. (2012) is given by
```math
  h= \frac{w^2}{3\pi G \Sigma_{tot}}
```
where $`w`$ is chosen to be $`u`$ which is the turbulent velocity or $`c_s`$ which is the sound speed depending on whether the turbulence is subsonic or supersonic.
An alternate model is also included where 
```math
  h= \frac{c_s}{\Omega}
```
* For the turbulent correlation length we have a choice between a minimalistic model which assumes that the turbulence is driven at the maximum scale and another model based on [Chamandy et. al. (2020)](https://arxiv.org/abs/2007.14159) which assumes supernovae predominately drive turbulence.
*  Similarly the turbulent velocity has a minimalistic regime where it is set equal to the sound speed $`c_s`$ and another regime where the model for $`u`$ is taken from [Chamandy et. al. (2020)](https://arxiv.org/abs/2007.14159). Here $`h`$ depends on $`u`$ but, 
$`u`$ can also depend on $`h`$ through $\nu$ and through $`l`$. To obtain an expression for $`h`$, an expression for u is found in terms of h and then is substituted back to obtain a relation between the RHS and h. 
* Let us say RHS $=Hh^\beta$ where $H$ contains the other quantities which are independent of $`h`$. Thus $h = H^{\frac{1}{1-\beta}}$. This algorithm is implemented in Sympy to obtain an expression for h. The value of $\beta$ is found using the following $`\beta = \frac{\partial log(u)}{\partial log(h)}`$
* Finally the turbulence correlation time has two regimes. The eddy turnover time $`\tau = l/u`$ and anohter regime based on [Chamandy et. al. (2020)](https://arxiv.org/abs/2007.14159)
* These expressions are finally substituted into the magnetic field model to obtain the following quantities
 ![mag](https://github.com/Rnazx/Scaling-Relations/assets/42196798/2abb8bf5-9a63-4916-9846-ff2a17305ef5)
* Finally the scaling relations for all the quantities are found using 
```math
\frac{\partial log(quantity)}{\partial log(observable)}
```

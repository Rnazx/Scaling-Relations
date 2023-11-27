
# Scaling Relations Finder
A general framework to find the scaling relations between magnetic field properties and observables for a model of galactic magnetic fields
### Libraries Used
* sympy
* numpy
* matplotlib
* pandas
* ipywidgets

 If these packages are not available in your Python interpreter, you can run
```
pip install -r requirements.txt
```
## Code Overview
Mean and random components of the magnetic field are modelled based on the following observables:
![obs](https://github.com/Rnazx/Scaling-Relations/assets/42196798/bb3e29fe-9bc9-4374-876b-fe5da0455514)

The turbulence and magnetic field models are solved in the [jupyter notebook](example.ipynb). Different regimes of the model can be chosen in the notebook from the python widgets. 
* The model for the scale height is inpired by [Forbes et. al. (2012)](https://ui.adsabs.harvard.edu/abs/2012ApJ...754...48F/abstract) is given by
```math
  h= \frac{\zeta w^2}{3\pi G \Sigma_{tot}},
```
where $1\lesssim\zeta\lesssim20$ is a parameter and $w=\max(u,c_\mathrm{s})$.
An alternative model is also included where 
```math
  h= \frac{c_s}{\Omega}
```
* For the turbulent correlation length, we have a choice between a minimalistic model, which assumes that the turbulence is driven at the maximum scale $h$ and another model based on [Chamandy \& Shukurov (2020)](https://ui.adsabs.harvard.edu/abs/2020Galax...8...56C/abstract) which assumes supernovae predominately drive turbulence.
*  Similarly, the turbulent velocity $u$ has a minimalistic regime where it is set equal to the sound speed $c_\mathrm{s}$ and another regime where the model for $u$ is taken from [Chamandy \& Shukurov (2020)](https://ui.adsabs.harvard.edu/abs/2020Galax...8...56C/abstract). Here $h$ depends on $u$ but $u$ can also depend on $h$ through $\nu$ and $l$. To obtain an expression for $h$, an expression for $u$ is found in terms of $h$ and then is substituted back to obtain a relation between the right-hand-side (RHS) and $h$. 
* Let us say RHS $=Hh^\beta$ where $H$ contains the other quantities which are independent of $h$. Thus $h = H^{1/(1-\beta)}$. This algorithm is implemented in Sympy to obtain an expression for $h$. The value of $\beta$ is found using $\beta = \partial \log(u)/\partial \log(h)$.
* The turbulence correlation time has two regimes. The eddy turnover time $\tau = l/u$ or the renovation time of the flow ([Chamandy \& Shukurov 2020)](https://ui.adsabs.harvard.edu/abs/2020Galax...8...56C/abstract).
* These expressions are finally substituted into the magnetic field model to obtain the following quantities:
 ![mag](https://github.com/Rnazx/Scaling-Relations/assets/42196798/2abb8bf5-9a63-4916-9846-ff2a17305ef5).
* Finally, the scaling relations for all the quantities are found using 
```math
  \frac{\partial \log(quantity)}{\partial \log(observable)}
```
## Instructions to run the code
* This repository consists of two main routines. All the expressions are symbolically evaluated in the [model_generator.py](model_generator.py) file using the model_gen function. This function takes in information about the regimes described in the manuscript.
* This function is then used in the [jupyter notebook file](example.ipynb) to find the  expression per the chosen regime. We have seven different regimes, as described in the manuscript. The regimes are automatically chosen from the selection in the widgets. The following are the steps needed to find the scaling relations.
* Detailed instructions are available in the order of the blocks of code in the [jupyter notebook file](example.ipynb).
* A non-interactive version of the notebook is also available [here](example_non_interactive.ipynb). The information about the regime for each turbulence parameter is stored in [regimes.py](regimes.py). A description of the regimes corresponding to each model in the manuscript is also available in the same file.
* To find the scaling relation as per the manuscript, run [manuscript_models.ipynb](manuscript_models.ipynb). Running the single block of code will open an interactive window which lets you select the model you are interested in and finds the scaling relations in real-time.

## Model Results
The final scaling relations are plotted for each model. The value of the exponent is given in the legends. The links below for each model will direct you to the scaling relation plots for that particular model.
</details>

<!-- Center align the content -->
<div align="center">

<!-- Create an HTML table with 3 rows -->
<table style="border-collapse: collapse; width: 100%;">
    <tr>
        <!-- Empty cell for the top row -->
        <tr></tr>
        <!-- Button for the top row -->
        <td align="center" colspan="8">
            <a href="scaling_relation_plots/Model_Alt1/quantity%20plots.md" style="display: inline-block; text-align: center; width: 100px; padding: 10px; border: 1px solid #ccc; background-color: #f0f0f0;">
                Model Alt 1
            </a>
        </td>
    </tr>
    <tr>
        <!-- Button for the second row -->
        <td align="center" colspan="4">
            <a href="scaling_relation_plots/Model_Alt2a/quantity%20plots.md" style="display: inline-block; text-align: center; width: 100px; padding: 10px; border: 1px solid #ccc; background-color: #f0f0f0;">
                Model Alt 2a
            </a>
        </td>
        <!-- Button for the second row -->
        <td align="center" colspan="4">
            <a href="scaling_relation_plots/Model_Alt2b/quantity%20plots.md" style="display: inline-block; text-align: center; width: 100px; padding: 10px; border: 1px solid #ccc; background-color: #f0f0f0;">
                Model Alt 2b
            </a>
        </td>
    </tr>
    <tr>
        <!-- Button for the third row -->
        <td align="center" colspan="2">
            <a href="scaling_relation_plots/Model_Sa/quantity%20plots.md" style="display: inline-block; text-align: center; width: 100px; padding: 10px; border: 1px solid #ccc; background-color: #f0f0f0;">
                Model Sa
            </a>
        </td>
        <!-- Button for the third row -->
        <td align="center" colspan="2">
            <a href="scaling_relation_plots/Model_Sb/quantity%20plots.md" style="display: inline-block; text-align: center; width: 100px; padding: 10px; border: 1px solid #ccc; background-color: #f0f0f0;">
                Model Sb
            </a>
        </td>
        <!-- Button for the third row -->
        <td align="center" colspan="2">
            <a href="scaling_relation_plots/Model_Sc/quantity%20plots.md" style="display: inline-block; text-align: center; width: 100px; padding: 10px; border: 1px solid #ccc; background-color: #f0f0f0;">
                Model Sc
            </a>
        </td>
      <td align="center" colspan="2">
            <a href="scaling_relation_plots/Model_Sd/quantity%20plots.md" style="display: inline-block; text-align: center; width: 100px; padding: 10px; border: 1px solid #ccc; background-color: #f0f0f0;">
                Model Sd
            </a>
        </td>
    </tr>
    
</table>

</div>

'''
##############################################################################################
This file consists of the regimes for the turbulence quantities h, l, u, tau, alpha_k
##############################################################################################
The regime for h can be any one of the following: copy any one of them and paste it in value for hreg variable
'subsonic', 'supersonic', 'cs/omega'
'''
hreg='subsonic'
'''
The regime for l can be any one of the following: copy any one of them and paste it in value for lreg variable
'maximum scale-driven', 'isolated supernova-driven', 'superbubble-driven'
'''
lreg='isolated supernova-driven'
'''
The regime for u can be any one of the following: copy any one of them and paste it in value for ureg variable
'sound speed', 'supenovae/superbubble-driven'
'''
ureg='supenovae/superbubble-driven'
'''
The regime for tau can be any one of the following: copy any one of them and paste it in value for taureg variable
'eddy turnover time', 'supernovae/superbubble renovation time'
'''
taureg='eddy turnover time'
'''
The regime for tau can be any one of the following: copy any one of them and paste it in value for alphareg variable
'regime 1', 'regime 2', 'regime 3'
'''
alphareg='regime 1'

'''
#################################################################################################
NOTE: The regimes for each of the model described in the manuscript is as follows
Model S:
lreg='isolated supernovae-driven'
ureg='supenovae/superbubble-driven'
--> a   
    hreg='subsonic'
    taureg='eddy turnover time'
--> b
    hreg='supersonic'
    taureg='eddy turnover time'
--> c
    hreg='subsonic'
    taureg='supernovae/superbubble renovation time'
--> d
    hreg='supersonic'
    taureg='supernovae/superbubble renovation time'
Model Alt 2:
lreg='maximum scale-driven'
ureg='supenovae/superbubble-driven'
--> a   
    hreg='subsonic'
    taureg='eddy turnover time'
--> b
    hreg='supersonic'
    taureg='eddy turnover time'
Model Alt 1:
lreg='maximum scale-driven'
ureg='sound speed'
hreg=**does not matter as both give same answer**
taureg='eddy turnover time'
#####################################################################################################
'''
## Py_XPPCALL Example

# import some modules including Py_XPPCALL
import matplotlib.pylab as plt
import numpy as np
from xppcall import xpprun, read_pars_values_from_file

# check if parameters with label 'p' will work
# add function to change inits.

# Let's check what are the parameters of the model
pars = read_pars_values_from_file('simple.ode')
print pars


"""
# Note: XPPAUT is not case sensitive. In Py_XPPCALL, the names of parameters and variables were chosen to be in lower case.

# Let's plot solution for membrane potential with parameters specified in .ODE file
npa, vn = xpprun('hh.ode', clean_after=True)
plt.figure()
plt.plot(npa[:,0], npa[:, 1+vn.index('v')])

# Let's modify constant input current
npa, vn = xpprun('hh.ode', parameters={'i':20.0}, clean_after=True)
plt.figure()
plt.plot(npa[:,0], npa[:, 1+vn.index('v')])


# Example of an optimization using fmin from SciPy
from scipy.optimize import fmin

# define desired V graph
target_v = -80.0+20*npa[:,0]*(np.sign(-npa[:,0]+4)+1)
plt.figure()
plt.plot(npa[:,0], target_v)

# define objective_func we want to minimize
def objective_func(x, target=target_v):
    try:
        npa, vn = xpprun('hh.ode', parameters={'i':x[0]}, clean_after=True)
        computed = npa[:, 1+vn.index('v')]
        return np.mean( (computed-target)**2 )
    except:
        return 1e10 # return huge error if something went wrong

xopt = fmin(objective_func, [20.0]) # find new parameters
npa, vn = xpprun('hh.ode', parameters={'i':xopt[0]}, clean_after=True)
plt.figure()
plt.plot(npa[:,0], npa[:, 1+vn.index('v')], label='fit')
plt.plot(npa[:,0], target_v, label='target')
plt.legend()
"""

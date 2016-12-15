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



# Note: XPPAUT is not case sensitive. In Py_XPPCALL, the names of parameters and variables were chosen to be in lower case.

# Let's plot solution for membrane potential with parameters specified in .ODE file
npa, vn = xpprun('simple.ode', clean_after=True)
t = npa[:,0]
sv = npa[:,1:]

fig = plt.figure()
ax1 = fig.add_subplot(121)
ax1.plot(sv[:,vn.index('x')],sv[:,vn.index('y')])

# Let's modify constant input current
npa, vn = xpprun('simple.ode', parameters={'a':20.0}, clean_after=True)
t = npa[:,0]
sv = npa[:,1:]

ax2 = fig.add_subplot(122)
ax2.plot(sv[:,vn.index('x')],sv[:,vn.index('y')])


# example with different initial conditions



plt.show()

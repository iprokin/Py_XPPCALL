## Py_XPPCALL Example

# import some modules including Py_XPPCALL
import matplotlib.pylab as plt
import numpy as np
from xppcall import xpprun, read_pars, read_inits, read_numerics

# check if parameters with label 'p' will work
# add function to change inits.

# Let's check what are the parameters of the model
pars = read_pars('simple.ode')
print pars


inits = read_inits('simple.ode')
print inits

numerics = read_numerics('simple.ode')
print numerics

# Note: XPPAUT is not case sensitive. In Py_XPPCALL, the names of parameters and variables were chosen to be in lower case.

# Let's plot a solution with default parameters and inits specified in the .ODE file
npa, vn = xpprun('simple.ode', clean_after=False)
t = npa[:,0]
sv = npa[:,1:]

fig = plt.figure(figsize=(10,5))
ax1 = fig.add_subplot(121)
ax1.plot(sv[:,vn.index('u')],sv[:,vn.index('v')],lw=2)
ax1.set_xlim([-1.05,1.05])
ax1.set_ylim([-1.05,1.05])
ax1.set_title('q=1')

# Let's modify one of the parameters
npa, vn = xpprun('simple.ode', parameters={'q':5.0}, clean_after=False)
t = npa[:,0]
sv = npa[:,1:]

ax2 = fig.add_subplot(122)
ax2.plot(sv[:,vn.index('u')],sv[:,vn.index('v')],lw=2)
ax2.set_xlim([-1.05,1.05])
ax2.set_ylim([-1.05,1.05])
ax2.set_title('q=5')

fig.suptitle('Lambda-Omega System')

# example with different initial conditions
npa, vn = xpprun('simple.ode', inits={'u':-.1,'v':-.2}, clean_after=True)
t = npa[:,0]
sv = npa[:,1:]

fig = plt.figure()

ax3 = fig.add_subplot(111)
ax3.plot(sv[:,vn.index('u')],sv[:,vn.index('v')])

ax3.set_xlim([-1.05,1.05])
ax3.set_ylim([-1.05,1.05])
ax3.set_title('Lambda-Omega System')

plt.show()

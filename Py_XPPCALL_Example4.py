"""
another example with the other init syntax + array init

"""

# import some modules including Py_XPPCALL
import matplotlib.pylab as plt
import numpy as np
from xppcall import xpprun, read_pars, read_inits, read_numerics

# check if parameters with label 'p' will work
# add function to change inits.

# Let's check what are the parameters of the model
pars = read_pars('simple2.ode')
print 'pars',pars

# print inits
inits = read_inits('simple2.ode')
print 'default inits',inits

# print options
numerics = read_numerics('simple2.ode')
print 'numerics', numerics


# example with different initial conditions
npa, vn = xpprun('simple2.ode', inits={'u':-.1,'v':-.2}, clean_after=False)
t = npa[:,0]
sv = npa[:,1:]

fig = plt.figure()

ax3 = fig.add_subplot(111)
ax3.plot(sv[:,vn.index('u')],sv[:,vn.index('v')])

ax3.set_xlim([-1.05,1.05])
ax3.set_ylim([-1.05,1.05])
ax3.set_title('Lambda-Omega System')

plt.show()

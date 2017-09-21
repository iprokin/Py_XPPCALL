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
pars = read_pars('schnakenberg.ode')
print 'pars',pars

# print inits
inits = read_inits('schnakenberg.ode')
print 'default inits',inits

# print options
numerics = read_numerics('schnakenberg.ode')
print 'numerics', numerics


# run ODE and get solution with default inits

# Let's plot a solution with default parameters and inits specified in the .ODE file
npa, vn = xpprun('schnakenberg.ode', clean_after=True)
t = npa[:,0]
sv = npa[:,1:] #(501 time steps, 202 variables)

# the way that xpp defined the ODEs, the varnames alternate like u0,v0,u1,v1,u2,v2,... u99,v99,u100,v100

#print np.shape(sv)

fig = plt.figure(figsize=(10,5))
ax1 = fig.add_subplot(121)
ax1.set_title('default inits and params')
ax1.plot(sv[:,0],sv[:,1],lw=2)
#ax1.set_xlim([-1.05,1.05])
#ax1.set_ylim([-1.05,1.05])
#ax1.set_title('q=1')


# modify a param
npa, vn = xpprun('schnakenberg.ode', parameters={'a':5}, clean_after=True)
t = npa[:,0]
sv = npa[:,1:]

ax2 = fig.add_subplot(122)
ax2.set_title('default inits and new param (a)')
ax2.plot(sv[:,0],sv[:,1],lw=2)
#ax2.set_xlim([-1.05,1.05])
#ax2.set_ylim([-1.05,1.05])
#ax2.set_title('q=5')




# now let's modify an entire array of initial conditions
# the index number must correspond to the number in the xpp array. e.g. if 
# init u[3..100] then we must define a list with 98 elements
npa, vn = xpprun('schnakenberg.ode', inits={'u':[1.,2.]}, clean_after=False)
t = npa[:,0]
sv = npa[:,1:]


fig2 = plt.figure(figsize=(10,5))
ax1 = fig2.add_subplot(121)
ax1.set_title('new inits with default params')
ax1.plot(sv[:,0],sv[:,1],lw=2)

npa, vn = xpprun('schnakenberg.ode', inits={'u':[1.,2.]}, parameters={'a':5}, clean_after=True)
t = npa[:,0]
sv = npa[:,1:]


ax2 = fig2.add_subplot(122)
ax2.set_title('new inits with new param (a)')
ax2.plot(sv[:,0],sv[:,1],lw=2)

"""
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
"""
plt.show()

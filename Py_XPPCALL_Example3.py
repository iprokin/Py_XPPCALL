# import some modules including Py_XPPCALL
import matplotlib.pylab as plt
import numpy as np
from xppcall import xpprun, read_pars, read_inits, read_numerics

# load file with partially defined initial conditions and define new initial conditions
npa, vn = xpprun('simple_partial_inits.ode', inits={'u':-.1,'v':-.2}, clean_after=True)
t = npa[:,0]
sv = npa[:,1:]


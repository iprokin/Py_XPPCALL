[XPPAUT](http://www.math.pitt.edu/~bard/xpp/xpp.html) is a great
software for the analysis of dynamical systems. Many mathematical models
have been implemented with XPPAUT (\*.ODE file format) \[search for
examples at <http://senselab.med.yale.edu/modeldb/>\]. These
implementations could be used to reproduce computational experiments and
to quickly test ideas related to them. For instance, one could perform
the sensitivity analysis of model’s parameters or parameters’ space
searches. However, due to the graphical nature of XPPAUT, the batch
modification of parameters of these models is problematic. 

Here I describe the solution for this problem using simple python module
**Py\_XPPCALL** that I have written to interface with XPPAUT. It allows
you to batch-modify model’s parameters and returns corresponding
solutions. An analogous software exists,
<https://github.com/jsnowacki/xppy>, however little documentation is
available.

Py\_XPPCALL is easy to use and does not require installation. Simply put
**xppcall.py** to your python path or current folder.

### An example of usage with Hodgkin-Huxley neuron model for numerical optimization

I extracted the ODE source code of Hodgkin-Huxley model  from the
example at the website of
XPPAUT <http://www.math.pitt.edu/~bard/bardware/tut/newstyle.html#hh>. I
saved it as hh.ode. I put it to the same folder where I have xppcall.py
and ran python from there. 

``` {.python}
## Py_XPPCALL Example

# import some modules including Py_XPPCALL
import matplotlib.pylab as plt
import numpy as np
from xppcall import xpprun, read_pars_values_from_file

# Let's check what are the parameters of the model
pars = read_pars_values_from_file('hh.ode')
print pars
```

``` {style="line-height:16.25px;color:rgb(0,0,0)"}
Out[]: 

    {'c': '1',
     'gk': '36',
     'gl': '.3',
     'gna': '120',
     'i': '0',
     'vk': '-77',
     'vl': '-54.4',
     'vna': '50'}
```

``` {.python}
# Note: XPPAUT is not case sensitive. In Py_XPPCALL, the names of parameters and variables were chosen to be in lower case.

# Let's plot solution for membrane potential with parameters specified in .ODE file
npa, vn = xpprun('hh.ode', clean_after=True)
plt.figure()
plt.plot(npa[:,0], npa[:, 1+vn.index('v')])
```

``` {style="line-height:16.25px;color:rgb(0,0,0)"}
Out[]:
```

[![](py_xppcall-a-python-binding-to-xppaut/1.png)](py_xppcall-a-python-binding-to-xppaut/1.png)

``` {.python}
# Let's modify constant input current
npa, vn = xpprun('hh.ode', parameters={'i':20.0}, clean_after=True)
plt.figure()
plt.plot(npa[:,0], npa[:, 1+vn.index('v')])
```

``` {style="line-height:16.25px;color:rgb(0,0,0)"}
Out[]:
```

[![](py_xppcall-a-python-binding-to-xppaut/2.png)](py_xppcall-a-python-binding-to-xppaut/2.png)

``` {.python}
# Example of an optimization using fmin from SciPy
from scipy.optimize import fmin

# define desired V graph
target_v = -80.0+20*npa[:,0]*(np.sign(-npa[:,0]+4)+1)
plt.figure()
plt.plot(npa[:,0], target_v)
```

``` {style="line-height:16.25px;color:rgb(0,0,0)"}
Out[]:
```

``` {.python}
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
```

``` {style="line-height:16.25px;color:rgb(0,0,0)"}
Out[]:
```

![](py_xppcall-a-python-binding-to-xppaut/4.png)

### Congrats! We got a pretty good fit.

Notes:

-All initial conditions must be initialized using the init command, e.g. "init x=2,y=1".

-This script currently does not support initialization of arrays (e.g., "init x[0..10]=1"), or the syntax "x(0)=2".

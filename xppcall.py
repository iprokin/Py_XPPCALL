# -*- coding: utf-8 -*-

# (ɔ) Py_XPPCALL - a python binding to amazing XPPAUT
#
#     Copyright 2015 Ilya Prokin
#     https://sites.google.com/site/ilyaprokin/
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>

import os
import subprocess
import numpy as np
import re
from random import random



def file_to_lines(filepath):
    with open(filepath,"r") as f:
        content = f.readlines()
    return content

def search_state_vars_in_srclines(srclines):
    """
    srclines - an ODE-file's content read into the list of strings,

    return:
    the list of names of found state variables
    """
    der=[]; aux=[]
    for line in srclines:
        so=re.search('^ *d([a-zA-Z0-9_]+)/dt[ \t]*=|^ *([a-zA-Z0-9_]+)\'[ \t]*=|^ *aux +([a-zA-Z0-9_]+) *=', line, flags=re.IGNORECASE)
        if so is not None:
            if so.group(1) is not None:
                der.append(so.group(1).lower())
            elif so.group(2) is not None:
                der.append(so.group(2).lower())
            else:
                aux.append(so.group(3).lower())
    return der+aux

def read_numerics_settings(srclines, num_names=None):
    """ srclines - an ODE-file content in the list of strings,
    if num_names is None all non-default numerical parameters will be read
    num_names - the list of numerical options

    return:
    the dict of parameters, where keys=num_names, values are parsed from srclines
    """
    vars_list=[]
    i_num_lines = np.nonzero([re.search('^ *(@) (.+)$', line, flags=re.IGNORECASE) is not None for line in srclines])[0]
    for i in i_num_lines:
        vars_list+=re.findall('([a-z0-9_]+) *= *([0-9\.e\-\+]+)', srclines[i].lower(), flags=re.IGNORECASE)
    d = dict(vars_list)
    if num_names is None:
        return d
    else:
        return {pn:d[pn] for pn in num_names}

def read_numerics_settings_from_file(filepath, num_names=None):
    """
    filepath - path to a .ode file
    num_names - the list of numerical options
    if num_names is None all non-default numerical options will be read

    return:
    the dict of parameters, where keys=pars_names, values are parsed from .ode file
    """
    return read_numerics_settings(file_to_lines(filepath), num_names=num_names)



def read_pars_values(srclines, pars_names=None):
    """ srclines - an ODE-file content in the list of strings,
    if pars_names is None all parameters will be read
    pars_names - the list of parameters names

    return:
    the dict of parameters, where keys=pars_names, values are parsed from srclines
    """
    vars_list=[]
    i_par_lines = np.nonzero([re.search('^ *(parameters|par|param|params|p) (.+)$', line, flags=re.IGNORECASE) is not None for line in srclines])[0]
    for i in i_par_lines:
        vars_list+=re.findall('([a-z0-9_]+) *= *([0-9\.e\-\+]+)', srclines[i].lower(), flags=re.IGNORECASE)
    d = dict(vars_list)
    if pars_names is None:
        return d
    else:
        return {pn:d[pn] for pn in pars_names}

def read_pars_values_from_file(filepath, pars_names=None):
    """
    filepath - path to a .ode file
    pars_names - the list of parameters names
    if pars_names is None all parameters will be read

    return:
    the dict of parameters, where keys=pars_names, values are parsed from .ode file
    """
    return read_pars_values(file_to_lines(filepath), pars_names=pars_names)

def change_parameters_in_ode_and_save(srclines, parameters, newfilepath):
    """
    srclines - an ODE-file content in the list of strings,
    parameters - the dict of parameters to set up new values, all keys in low register!
    newfilepath - path to a new ODE file with modified parameters
    """
    lparameters = {pn.lower():(lambda x: repr(x) if not isinstance(x,str) else x)(pv) for pn,pv in parameters.iteritems()}
    pnames = lparameters.keys()
    def repl_in_par(matchobj):
        mog = matchobj.group(1).lower()
        if mog in pnames:
           return matchobj.group(1)+matchobj.group(2)+lparameters[mog]
        else:
           return matchobj.group(0)
    i_par_lines = np.nonzero([re.search('^ *(parameters|par|param|params|p) (.+)$', line, flags=re.IGNORECASE) is not None for line in srclines])[0]
    nsrclines=srclines[:]
    for i in i_par_lines:
        nsrclines[i] = re.sub('([a-z0-9_]+)( *= *)([0-9\.e\-\+]+)', repl_in_par, nsrclines[i], flags=re.IGNORECASE)
    nsrc = ''.join(nsrclines)
    with open(newfilepath, 'w') as f:
        f.write(nsrc)


def read_init_values(srclines, init_names=None):
    """ srclines - an ODE-file content in the list of strings,
    if init_names is None all parameters will be read
    init_names - the list of parameters names

    return:
    the dict of parameters, where keys=pars_names, values are parsed from srclines
    """
    vars_list=[]
    i_init_lines = np.nonzero([re.search('^ *(init) (.+)$', line, flags=re.IGNORECASE) is not None for line in srclines])[0]
    for i in i_init_lines:

        vars_list+=re.findall('([a-z0-9_]+) *= *([0-9\.e\-\+]+)', srclines[i].lower(), flags=re.IGNORECASE)
    d = dict(vars_list)
    if init_names is None:
        return d
    else:
        return {pn:d[pn] for pn in init_names}

def read_init_values_from_file(filepath, init_names=None):
    """
    filepath - path to a .ode file
    init_names - the list of parameters names
    if init_names is None all parameters will be read

    return:
    the dict of parameters, where keys=pars_names, values are parsed from .ode file
    """
    return read_init_values(file_to_lines(filepath), init_names=init_names)

def change_inits_in_ode_and_save(srclines, inits, newfilepath):
    """
    srclines - an ODE-file content in the list of strings,
    inits - the dict of inits to set up new values, all keys in low register!
    newfilepath - path to a new ODE file with modified inits
    """
    linits = {pn.lower():(lambda x: repr(x) if not isinstance(x,str) else x)(pv) for pn,pv in inits.iteritems()}
    pnames = linits.keys()
    def repl_in_par(matchobj):
        mog = matchobj.group(1).lower()
        if mog in pnames:
           return matchobj.group(1)+matchobj.group(2)+linits[mog]
        else:
           return matchobj.group(0)
    i_par_lines = np.nonzero([re.search('^ *(init) (.+)$', line, flags=re.IGNORECASE) is not None for line in srclines])[0]
    nsrclines=srclines[:]
    for i in i_par_lines:
        nsrclines[i] = re.sub('([a-z0-9_]+)( *= *)([0-9\.e\-\+]+)', repl_in_par, nsrclines[i], flags=re.IGNORECASE)
    nsrc = ''.join(nsrclines)
    with open(newfilepath, 'w') as f:
        f.write(nsrc)




def xpprun(filepath, xppname='xppaut', postfix='_tmp', parameters=None, inits=None, clean_after=False):
    """
    A simple interface to xppaut. It runs xpp in a silent mode 'xpp some_ode_file.ode -silent'
    and analyses the result of computation, a file produced by xpp (output.dat by default).
    It also allows you to modifiy parameters of the XPP model when parameters provided as a dict - parameters.
    In the dict of parameters, a key is the name of a parameter to be modified, the corresponding value is a new numerical value of the parameter.

    Ex.: In .ode file you have
    'par x=5.6' and want to change it from python.
    You need to create the dictionary of parameters where
    parameters['x']=10.1. If you evoke function with keyword argument parameters=parameters,
    the value of x would be set to 10.1.
    If you pass the dict of parameters, then the new .ode will be created from your original .ode and xppaut will be run with it.

    Input:

    filepath - path to ode file. Ex.: /home/user/xppfile.ode (Linux), D:/some_folder/xppfile.ode (Windows)
    xppname - name of xpp as you call it from Terminal
    postfix - the postfix of new .ode file made out of original
    parameters - the dict of parameters to be modified
    clean_after - if True temporary .ode file (with modified parameters) would be deleted after computations

    Output: tuple (out, vn) or None

    out - numpy.array where out[:,0] is time, and out[:,1:] is the matrix with solutions for model variables
    vn - the list with the names of variables that allow you to search for a data row in the matrix by a variable's name
    To plot variable with name NaCl in ode vs. time, run
    plt.plot(npa[:,0], npa[:, 1+vn.index('NaCl')])

    """
    srclines = file_to_lines(filepath)
    path, filename = os.path.split(filepath)
    name, ext = os.path.splitext(filename)
    wd = os.getcwd()
    rndid=''; rndid2=''; newfilepath=''


    if (parameters is not None) or (inits is not None):
        rndid='_rndid'+str(int(random()*1e15))
        filename = name+postfix+rndid+ext # change to new file
        newfilepath = os.path.join(path, filename)
        if parameters is not None:
            change_parameters_in_ode_and_save(srclines, parameters, newfilepath)
        if inits is not None:
            change_inits_in_ode_and_save(srclines, inits, newfilepath)
    

    if path!='':
        os.chdir(path)
    outputfile = 'output%s.dat'%(rndid+rndid2)
    outputfilepath = os.path.join(path, outputfile)

    try:
        res = subprocess.check_output("%s %s -silent -outfile %s" % (xppname, filename, outputfile), stderr=subprocess.STDOUT, shell=True)
        os.chdir(wd)
        out = np.genfromtxt(outputfilepath, delimiter=' ')
        vn = search_state_vars_in_srclines(srclines)
        ret = out, vn
    except:
        ret = None

    if clean_after:
        if os.path.isfile(outputfilepath):
            os.remove(outputfilepath)
        if newfilepath!='':
            os.remove(newfilepath)
    return ret

read_pars = read_pars_values_from_file
read_inits = read_init_values_from_file
read_numerics = read_numerics_settings_from_file

if __name__ == "__main__":
    pass

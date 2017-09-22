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


# initial condition regex. The syntax differs depending on scalar or array.
# if scalar inits, we have 'init v=*' or 'v(0)=*'
# if array init, we have 'init v[0..10]=*' or 'v[0..10](0)=*'

# scalar inits
init_re_sc1 = '^ *(init) (.+)$'
init_re_sc2 = '^ *(.+ *\( *0 *\) *.+)$'
init_re_ar1 = '^ *(init) (.+ *\[[0-9]+\.\.[0-9]+\] *.+)$'
#init_re_ar1b = '^ *(init) (.+ *\[[0-9]+\.\.[0-9]+\] *.+)$'
init_re_ar2 = '^ *(.+ *\[[0-9]+\.\.[0-9]+\] *\( *0 *\) *.+)$'

# array inits coming soon...

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
    the dict of numerical options, where keys=num_names, values are parsed from srclines
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
    the dict of numerical options, where keys=num_names, values are parsed from .ode file
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

    vars_list_sc1=[];vars_list_sc2=[];vars_list_ar1=[];vars_list_ar2=[];vars_list_ar3=[]
    i_init_lines = np.nonzero([re.search(init_re_sc1+'|'+\
                                         init_re_sc2+'|'+\
                                         init_re_ar1+'|'+\
                                         init_re_ar2, line, flags=re.IGNORECASE) is not None for line in srclines])[0]

    for i in i_init_lines:
        vars_list_sc1+=re.findall('([a-z0-9_]+) *= *([0-9\.e\-\+]+)',srclines[i].lower(),flags=re.IGNORECASE)
        vars_list_sc2+=re.findall('([a-z0-9_]+\(0\)) *= *([0-9\.e\-\+]+)',srclines[i].lower(),flags=re.IGNORECASE)
        vars_list_ar1+=re.findall('([a-z0-9_]+\[[0-9]+\.\.[0-9]+\]\(0\)) *= *([0-9\.e\-\+]+)',srclines[i].lower(),flags=re.IGNORECASE)
        vars_list_ar2+=re.findall('([a-z0-9_]+\[[0-9]+\.\.[0-9]+\]) *= *([0-9\.e\-\+]+)',srclines[i].lower(),flags=re.IGNORECASE)
        vars_list_ar3+=re.findall('([a-z0-9_]+\[j\]) *= *([0-9\.e\-\+]+)',srclines[i].lower(),flags=re.IGNORECASE)

    # remove '(0)' from vars_list_sc2
    for i in range(len(vars_list_sc2)):
        tup = vars_list_sc2[i]
        var = tup[0]
        var_pruned = var[:-3]
        tup2 = (var_pruned,tup[1])
        vars_list_sc2[i] = tup2

    # remove '(0)' from vars_list_ar1
    for i in range(len(vars_list_ar1)):
        tup = vars_list_ar1[i]
        var = tup[0]
        var_pruned = var[:-3]
        tup2 = (var_pruned,tup[1])
        vars_list_ar1[i] = tup2

    # implement remove '(0)' from vars_list_ar2
    #print vars_list_sc1,vars_list_ar2
    vars_list = vars_list_sc1 + vars_list_sc2 + vars_list_ar1 + vars_list_ar2 + vars_list_ar3
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
        """
        replace scalar inits
        """
        
        mog = matchobj.group(1).lower()
        # if init is used as v(0)=*, account for this fact.
        if matchobj.group(2) == '(0)':

            if mog in pnames:
                return matchobj.group(1)+matchobj.group(2)+matchobj.group(3)+linits[mog]
            else:
                return matchobj.group(0)
        else:

            if mog in pnames:
                return matchobj.group(1)+matchobj.group(3)+linits[mog]
            else:
                return matchobj.group(0)

    def repl_in_ar(matchobj):
        """
        replace array inits
        """

        mog = matchobj.group(1).lower()

        # if init is used as v(0)=*, account for this fact.
        #print matchobj.group(1),'/',matchobj.group(2),'/',matchobj.group(3),'/',matchobj.group(4)

        # get idx limits
        idx = matchobj.group(2)
        idx = idx.split('..')
        low_idx = int(idx[0])
        hi_idx = int(idx[-1])
        idxrange = np.arange(low_idx,hi_idx+1,1)

        #print idx,idxrange

        # if the init contains (0), keep it. no particular reason, but sorta easier this way?
        if matchobj.group(3) == '(0)':
            #print 'sdfjkadsfasfd',mog

            if mog in pnames:
                # collect all inits into one explicit line
                # this is where we convert from v[0..2]=1 syntax to v0=1,v1=1,v2=1 syntax.
                #print mog
                listval = linits[mog][1:-1]
                listval = listval.split(',')

                inits_new = ''
                for i in range(len(idxrange)):
                    #print idxrange[i]
                    inits_new += matchobj.group(1)+str(idxrange[i])+matchobj.group(3)+'='+listval[i]+','

                # trim trailing comma, force newline
                inits_new = inits_new[:-1]

                return inits_new

                #print inits_new
            else:
                return matchobj.group(0)
        else:

            if mog in pnames:
                # collect all inits into one explicit line
                # this is where we convert from v[0..2]=1 syntax to v0=1,v1=1,v2=1 syntax.
                #print mog

                # remove list index brackets '[0,1,2]' -> '0,1,2'
                listval = linits[mog][1:-1]
                listval = listval.split(',')

                inits_new = ''

                for i in range(len(idxrange)):
                    #print idxrange[i]
                    inits_new += matchobj.group(1)+str(idxrange[i])+'='+listval[i]+','

                # trim trailing comma
                inits_new = inits_new[:-1]
                return inits_new
                #return matchobj.group(1)+matchobj.group(2)+linits[mog]
            else:
                return matchobj.group(0)


    # get lines of inits
    i_par_lines = np.nonzero([re.search(init_re_sc1+'|'+\
                                        init_re_sc2,line,flags=re.IGNORECASE) is not None for line in srclines])[0]

    # get lines of array inits
    i_ar_lines = np.nonzero([re.search(init_re_ar1+'|'+\
                                       init_re_ar2,line,flags=re.IGNORECASE) is not None for line in srclines])[0]
    #print i_ar_lines

    # get line of 'done' flag. empty string if it does not exist.
    i_d_line = np.nonzero([re.search('^ *(d)|^ *(done)',line,flags=re.IGNORECASE) is not None for line in srclines])[0]

    # if the done flag position is empty, return -1
    # else return the position number.
    if i_d_line.size == 0:
        i_d_line = -1
    else:
        i_d_line = i_d_line[0]

    # mark which inits exist and which do not.
    dnelist = 'init '
    idx = 0

    # create list for deletion of state variable keys that do not exist
    delete_keys = []

    # cram all inits into one line, to make it easy to check if state variable exists
    combinedlist = ''
    
    for i in range(len(i_par_lines)):
        combinedlist += srclines[i_par_lines[i]]

    # check if user-input initial conditions exist.
    # iterate over user-input initial conditions
    for k in inits:
            
        # if the user-input initial condition is not in the code...
        # verify that this init is in fact a state variable
        if not(k in combinedlist):
            
            vn = search_state_vars_in_srclines(srclines)
            
            if k in vn: # if state variable exists, take note that the init was not defined in the ode script
                dnelist += k+'='+str(inits[k])
            else:
                # if the state variable does not exist in the ODE file, ignore.
                delete_keys.append(k)

    # delete the state variables that do not exist
    for key in delete_keys:
        del inits[key]

    # if there exist user-defined inits (not initialized in the script) that are existing state variables ...
    if dnelist != 'init ':
        # if new inits defined, move done flag to end
        srclines[i_d_line] = ''
        dnelist += '\n'
        srclines.append(dnelist) # add the new inits
        srclines.append('d')
    #print srclines

    nsrclines=srclines[:]
    for i in i_par_lines:
        nsrclines[i] = re.sub('([a-z0-9_]+)( *\( *0 *\) *)?( *= *)([0-9\.e\-\+]+)', repl_in_par, nsrclines[i], flags=re.IGNORECASE)

    for i in i_ar_lines:
        nsrclines[i] = re.sub('([a-z0-9_]+)\[([0-9]+..[0-9]+)\]( *\( *0 *\) *)?( *= *)([0-9\.e\-\+]+)', repl_in_ar, nsrclines[i], flags=re.IGNORECASE)


    nsrc = ''.join(nsrclines)
    with open(newfilepath, 'w') as f:
        f.write(nsrc)


def check_if_in_ode(srclines,inits):
    """
    DEPRECATED 
    
    check whether a set of inits are listed in an ODE
    return {dictonary of existing guys}, {dictionary of nonexisting guys}
    """
    i_par_lines = np.nonzero([re.search(init_re_sc1+'|'+\
                                        init_re_sc2+'|'+\
                                        init_re_ar1+'|'+\
                                        init_re_ar2, line, flags=re.IGNORECASE) is not None for line in srclines])[0]
    return i_par_lines



def xpprun(filepath, version=8, xppname='xppaut', postfix='_tmp', parameters=None, inits=None, clean_after=False):
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
    version - xpp version number. If for example you are running xpp version 6.11, use version=6.
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



    if version < 8:
        # legacy code. Adds compatibility to older xpp versions that do not have command line inputs
        # forwards compatible for now


        if (parameters is not None) or (inits is not None):
            rndid='_rndid'+str(int(random()*1e15))
            filename = name+postfix+rndid+ext # change to new file
            newfilepath = os.path.join(path, filename)
            fullfilename = os.path.join(path, filename)
            if parameters is not None:
                change_parameters_in_ode_and_save(srclines, parameters, newfilepath)
            if inits is not None:
                change_inits_in_ode_and_save(srclines, inits, newfilepath)
        else:
            fullfilename = os.path.join(path, filename)
        
        if path!='':
            os.chdir(path)
        outputfile = 'output%s.dat'%(rndid+rndid2)
        outputfilepath = os.path.join(path, outputfile)

        try:
            res = subprocess.check_output("%s %s -silent -outfile %s" % (xppname, fullfilename, outputfilepath), stderr=subprocess.STDOUT, shell=True)
            os.chdir(wd)
            out = np.genfromtxt(outputfilepath, delimiter=' ')
            vn = search_state_vars_in_srclines(srclines)
            ret = out, vn
        except:
            ret = None


        
    else:
        # if xpp version >= 8, run using command line inputs.

        # clean inputs into cli compatible format
        inputstr = ''

        if (parameters is not None) and (parameters != {}):
            # for each parameter, append to string
            for opt in parameters:
                inputstr += opt+'='+str(parameters[opt])+';'

        # remove trailing semicolon
        inputstr = inputstr[:-1]

        if (inits is not None) and (inits != {}):
            # for each input, append to string
            rndid='_rndid'+str(int(random()*1e15))
            filename = name+postfix+rndid+ext # change to new file
            newfilepath = os.path.join(path, filename)
            fullfilename = os.path.join(path, filename)
            change_inits_in_ode_and_save(srclines, inits, newfilepath)
        else:
            fullfilename = os.path.join(path, filename)


        outputfile = 'output.dat'
        outputfilepath = os.path.join(path, outputfile)

        try:

            res = subprocess.check_output("%s %s -silent -with '%s' -runnow -outfile %s" % (xppname, fullfilename, inputstr,outputfilepath), stderr=subprocess.STDOUT, shell=True)

            os.chdir(wd)

            out = np.genfromtxt(outputfilepath, delimiter=' ')

            vn = search_state_vars_in_srclines(srclines)

            ret = out, vn
            
        except:
            print 'xpp was not called properly. check that xpp is installed and its alias.'
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

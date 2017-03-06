
#loadmat script is based on http://stackoverflow.com/questions/7008608/scipy-io-loadmat-nested-structures-i-e-dictionaries
# printm contains hack from http://stackoverflow.com/questions/3229419/pretty-printing-nested-dictionaries-in-python

import scipy.io as sio
import re
import numpy as np
import pandas as pd

def loadmat(filename,remove_metadata=1):
    '''
    this function should be called instead of direct spio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    ''' 
    if isinstance(filename,str):
        data = sio.loadmat(filename, struct_as_record=False, squeeze_me=True)

        # remove MATLAB metadata
        if remove_metadata:
            keylist = list(data.keys())
            for key in keylist:
                if re.search('^__\w+',key):
                    del data[key]
                    
        return _check_keys(data)

def _check_keys(dict):
    '''
    checks if entries in dictionary are mat-objects. If yes
    todict is called to change them to nested dictionaries
    '''

#     if any(isinstance(dict[key],sio.matlab.mio5_params.mat_struct in dict)):
    for key in dict:
        if isinstance(dict[key], sio.matlab.mio5_params.mat_struct):
            dict[key] = _todict(dict[key])
    return dict        

def _todict(matobj):
    '''
    A recursive function which constructs from matobjects nested dictionaries
    '''
    dict = {}
    for strg in matobj._fieldnames:
        elem = matobj.__dict__[strg]
        if isinstance(elem, sio.matlab.mio5_params.mat_struct):
            dict[strg] = _todict(elem)
        else:
            dict[strg] = elem
    return dict
           
def match_dict(key, var):
    if hasattr(var,'items'):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result

def printm(d, indent=0, indepth=0):
    '''
    Pretty print single variable that is a nested structure from .mat files   
    based on work inspired by: `StackOverflow <http://stackoverflow.com/questions/3229419/pretty-printing-nested-dictionaries-in-python>`_
    '''

    if indepth:
        if isinstance(d, dict):
            for key, value in d.items():
                print('\t' * indent + str(key) + ': ')
                printmat(value, indent+1)

        if isinstance(d,np.ndarray) and d.dtype.names is not None:  # Note: and short-circuits by default
            for n in d.dtype.names:    # This means it's a struct, it's bit of a kludge test.
                print('\t' * indent + str(n) + ': ')
                printmat(d[n][0,0], indent+1)
    else:
        if isinstance(d,str):
            print(d)
            
        else:
            if isinstance(d, dict):
                nlen = len(max(d.keys(), key=len)) + 2
                tlen = len(max([str(type(val)) for val in d.values()],key=len)) + 2
    #             slen = len(max([str(np.size(val)) for val in test.values()],key=len)) + 2

            elif isinstance(d,np.ndarray):
                if d.dtype.names is not None:
                    nlen = len(max(d.dtype.names, key=len))
                    tlen = len(max([str(type(val)) for val in d.values()],key=len)) + 2
                else:
                    return(d)

            for key, value in d.items():
                n = str(key)
                t = str(type(value))

                if isinstance(value,np.ndarray):
                    if np.shape(value)[0] > 1:
                        s = str(np.shape(value))
                    elif np.size(value) > 50:
                        s = str(value)

                elif isinstance(value,str):
                    s = str(value)

                elif isinstance(value,dict):
                    if len(list(value.keys())) > 10:
                        s = '%s keys available' %(len(value))
                    else:
                        s = str(list(value.keys()))

                print('{:>{a}} {:>{b}} {:<{c}}'.format(n,t,s,a=nlen,b=tlen,c=5))

def restrict(array,val1,val2):
    if isinstance(array,np.ndarray):
        for t in range(np.size(array)):
            idx1 = val1 <= array[t]
            idx2 = array[t] <= val2
            array[t] = array[t][idx1*idx2]
        return array

    
def ridx(array,val1,val2):
    if isinstance(array,np.ndarray) and np.size(array[0])>1:
        idx_out = []
        for t in range(np.size(array)):
            idx1 = val1 <= array[t]
            idx2 = array[t] <= val2
            idx_out[t] = idx1*idx2
        idx_out.append(idx)

    elif isinstance(array,np.ndarray):
            idx1 = val1 <= array
            idx2 = array <= val2
            idx_out = idx1*idx2
    return idx_out




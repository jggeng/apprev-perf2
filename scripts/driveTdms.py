import pandas as pd
import re

def filterDataFrame(df, FILTERED, FILTER_NAN):
    if not FILTERED:
        ##DROP USELESS COLUMNS
        #get rid of non-existant CAN 2 bus if file is a DRIVE 1.x file
        df = df[df.columns.drop(list(df.filter(regex='CAN 2')))]

    if FILTER_NAN and not FILTERED:
        #get rid of columns where every value is NaN
        df = df.dropna(axis=1, how='all')

        #get rid of columns where every value is the same in each row
        nunique = df.apply(pd.Series.nunique)
        cols_to_drop = nunique[nunique == 1].index
        df = df.drop(cols_to_drop, axis=1)

    if not FILTERED:
        FILTERED = True #clear FILTERED flag
        ##RENAME USEFUL COLUMNS
        #get rid of slashes and group name up to last (-1) slash, then take channel name
        df = df.rename(lambda x: x.split('/')[-1], axis='columns')
        df = df.rename(lambda x: x.strip(), axis='columns')

        #get rid of quotes
        df = df.rename(lambda x: x.replace("'", ""), axis='columns')

        #replace long identifiers
        df = df.rename(lambda x: x.replace("CAN 1 - ", "C"), axis='columns')

        #get rid of [non ^ letter \w or digit \d ]characters
        df = df.rename(lambda x: re.sub('[^\w\d]','',  x), axis='columns')

        #df = df.rename(lambda x: underscoreToCammelCase(x), axis='columns')
        #df = df.rename(lambda x: re.sub('[\d]','',  x), axis='columns')
        #df = df.rename(lambda x: x.replace(' ','_'), axis='columns')
    return df, FILTERED

def underscoreToCammelCase(us):
    retstr = ''
    cammelNext = False
    digitPrev = False
    for c in us:
        if c == '_':
            cammelNext = True
            digitPrev = False
        elif c.isdigit == True:
            digitPrev = True
            retstr += c
        else:
            if cammelNext == True:
                retstr += c.upper()
                cammelNext = False
            if digitPrev == True:
                digitPrev = False
                retstr = retstr + '_' + c
            else:
                retstr += c
    return(retstr)



'''
import pandas as pd
import matplotlib.pyplot as plt
import nptdms as td
#from nptdms import tdms
import re

from scripts.dtdms import drivetdms
from scripts.wpphist import plot as hist_plot
from scripts.vib_files import getTdmsFilesInPath, getTdmsFilesInFolder
from scripts.driveTdms import underscoreToCammelCase
'''

def global_imports(modulename,shortname = None, asfunction = False):
    if shortname is None: 
        shortname = modulename
    if asfunction is False:
        globals()[shortname] = __import__(modulename)
    else:        
        globals()[shortname] = eval(modulename + "." + shortname)
        
def drive_global_import():
    global_imports("pandas","pd")
    global_imports("matplotlib.pyplot", "plt")
    global_imports("nptdms", "td")
    global_imports("re")
    #global_imports(".scritps.dtdms", "drivetdms", True)
    #global_imports("scripts.wpphist", "hist_plot", True)
    #global_imports(".scripts.vib_files","getTdmsFilesInPath", True)
    #global_imports(".scripts.vib_files","getTdmsFilesInFolder", True)
    #global_imports(".scripts.driveTdms", "underscoreToCammelCase", True)
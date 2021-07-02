# -*- coding: utf-8 -*-
"""
Handy Functions and variables/constants for use at iPython prompt
   call mine() for full list of functions and variables.

Created on Sat Feb  1 15:05:51 2020
     ------ Time-stamp: <2021-07-02T16:53:18.534724-04:00 hedfp> ------
     
@author: Carl Schmiedekamp

2020-04-14 /CS/ adding 'mine()' to list what has been setup by handies.py
                adding atan2P(y,x) to return positive angle.
2020-04-17 /CS/ adding astropy.units as 'u'
2020-07-13 /CS/ removing cdpy1d(), and cdWD()
2020-07-22 /CS/ making astropy and func_timeout optional.
2020-07-25 /CS/ added timeStampStr()
                changed from file date/time to timestamp file as mod. time
                for this module, also added the version from __init__.py.
                Added variable "__version__" which holds the version.
2020-07-29 /CS/ added isInstalled()
2020-08-13 /CS/ added condaEnvName() as a helper function.
2020-08-25 /CS/ added 'line magic' cls to fill screen with 23 blank lines.
                the 'Loading' message is not output if not in IPython or the
                interactive interpreter.
2020-09-02 /CS/ Now sets ipython number precision to 5 digits.
                  (Note: only for expression evaluation output.)
2020-09-13 /CS/ made the height parameter to figsize optional, with the default
                  being 0.75 % of width.
2020-09-22 /CS/ added VURound and round_sig functions,
                VURound needs work if uncertainty can have more than 1 sig.fig.
2020-10-16 /CS/ Add is_ipython(), is_interactive(), and is_commandline() to test
                running environment.
2020-10-30 /CS/ adding astropy.constants as c
2020-11-02 /CS/ added clsall() which clears terminal screen of all characters.
2021-05-05 /CS/ split round_sig into two function, round_sig_limit rounds to zero
                  values that are 'very small'. While round_sig( ) rounds to specified
                  sig.figs.
2021-05-10 /CS/ added is_defined(), which checks if name is defined.

#####

To Do List:
    - check all functions are in mine()
    - use consistant names ex: isIn vs is_in, get_osname vs osname
    - renamed functions from previous versions get aliases like "ii = isInstalled"
        for old names.
    - add function to timestamp current python file
    - Should the 'mine()' function be renamed to info()?

"""
  ## Hoping for some combatibility in python2.7
from __future__ import absolute_import, division
from __future__ import print_function, unicode_literals

  ## These includes should be available on most systems
import math
import codecs
from math import pi, sqrt, cos, sin, tan, floor
from math import acos, asin, atan, atan2, degrees, radians
from math import log, log10, exp

from random import randint

from platform import python_version
import sys, os.path, time, os


import glob, pathlib

from typing import List, Sequence, Any

  ## More for Python 2.7 compatibility
if sys.version_info[0] < 3:
    ## load some stuff so that the code can be more compatible with python3
    def input( str):
        '''' redefine input() for Python 2 so it is compatible with Python 3 version'''
        return raw_input( str)  ## raises warning in python3 but not used in python3



  ### Current rule of thumb: only handies imports from other modules.
from classroom_gizmos.BestByMinBefore import getCCode
from classroom_gizmos.import_install import importInstall as II
from classroom_gizmos.import_install import ckII


def clsall() -> None:
    '''Outputs the ASCII clear screen character.
    This usually deletes all the previoous text in the terminal.'''
    print( '\033[2J', end=None)

def is_online() -> bool:
    '''Returns True if connected to Internet.'''
    from urllib.request import urlopen
    
    try:
        urlopen( 'https://www.google.com/', timeout=20)
        return True
    except:
        return False

def is_ipython() -> bool:
    '''Return True if running in IPython.
    Ref: https://stackoverflow.com/questions/23883394/detect-if-python-script-is-run-from-an-ipython-shell-or-run-from-the-command-li
    '''
    try:
        __IPYTHON__
    except NameError:
        result = False
    else:
        result = True
    return result

# def is_interactive():
#     '''Return True if running interactive interpreter but not IPython.
#     Ref: https://stackoverflow.com/questions/23883394/detect-if-python-script-is-run-from-an-ipython-shell-or-run-from-the-command-li
#     '''
#     import inspect
    
#     if len( inspect.stack()) > 1 and not is_ipython():
#         result = True
#     else:
#         result = False
#     return result

def is_interactive() -> bool:
    '''Return true if interactive python, False if running from command line.
    Ref: https://stackoverflow.com/questions/2356399/tell-if-python-is-in-interactive-mode
    '''
    import sys
    try:
        if sys.ps1:
            inter = True
    except AttributeError:
        inter = False
        if sys.flags.interactive: inter = True
    return inter


def is_commandline() -> bool:
    '''Returns True if running from command line (not ipython, and not interactive
    interpreter.).
    Ref: https://stackoverflow.com/questions/23883394/detect-if-python-script-is-run-from-an-ipython-shell-or-run-from-the-command-li
    '''
    import inspect
    
    if len( inspect.stack()) == 1 :
        result = True
    else:
        result = False
    return result

def is_collab() -> bool:
    '''Returns True if running in Google Colab.
    Ref: https://stackoverflow.com/questions/53581278/test-if-notebook-is-running-on-google-colab'''
    import sys
    return 'google.colab' in sys.modules

def round_sig_limit( x: float, sig: int=6, small_value: float=1.0e-9) -> float:
    ''' Round numbers to sig figs, and zero if less than min. value.
      Modified to to work without limit and created new round_sig_limit()
     Ref: https://stackoverflow.com/questions/3410976/how-to-round-a-number-to-significant-figures-in-python
     '''
    if abs( x)<abs(small_value):  ## return zero for smaller values
        return 0.0
    else:
        return round(x, sig - int(floor(log10(abs(x)))) - 1)

def files_globber( wild_card_file_list: List[str], full: bool=True) -> List[ str]:
    '''
    
      expand wild cards in the files in wild_card_file_list
       and create a single list of path names.
       
       if full flag is True, then full paths are returned,
         otherwise the base names (without directory parts) 
         of the files are returned.
       
       Any duplicate names are removed before returning the list
         of files found.
       For example:
      files_globber( [ './*.txt', '*.txt', ../dir/*.txt'])
       could specify the same list of files, 3 different ways, 
       the duplicates are removed and a file name appears
       once in the output list.  However, different paths to the
       same file, such as those created with the ln command are
       all returned.
    '''

    
    
    full_path_list = []      ## list of full path names found
    filesRel = []   ## wild card expanded file list
    base_name_list = [] ## list of base file name (file part) corresponding
                        ##   to paths in files
                        
    ## Catch single string instead of a list of strings
    # print( f'DBug type of arg is { type(wild_card_file_list)}')
    if type( wild_card_file_list) == str:
        # print( 'DBug converting string to list.')
        file_list = [ wild_card_file_list ]
    else:
        file_list = wild_card_file_list
    
    for f in file_list:
        # print( f'DBug: current file is {f}')
        filesRel += glob.glob( f)
    # print( '\nDBug filesRel: {}'.format( filesRel))
    
    for f in filesRel:
        path = pathlib.Path(f)
        # print( '\nDBug path: {}, Abs: {}'.format(
        #     path, path.absolute()))
        fabs = path.absolute()
        path = str(fabs)
        full_path_list.append( path)
        base =  os.path.basename( path)
        base_name_list.append( base)
    print( '\nDBug files: {}'.format( full_path_list))
    print( f'\nDBug base names: { base_name_list}')
    if full:
        return list( set( full_path_list))  ## remove duplicates and return list
    else:
        return list( set( base_name_list))  ## remove duplicates and return list


def round_sig(x: float, sig: int=6):
    ''' Round numbers to sig figs.
      Modified to to work without limit and created new round_sig_limit()
     Ref: https://stackoverflow.com/questions/3410976/how-to-round-a-number-to-significant-figures-in-python
     '''
    return round(x, sig - int(floor(log10(abs(x)))) - 1)



def VURound( value: float, uncertainty: float, undig: int=1) -> str:
    '''
    Returns a string with rounded value and uncertainty.
    Round value based on uncertainty.
    Uncertainty is rounded up to "undig" sig.figs.
      'undig' is currently fixed at 1
      Based on Javascript function by Carl Schmiedekamp
    '''
    from math import copysign, log10, floor, ceil
    
    #soecial case: uncertanity is zero: return value as string.
    if uncertainty==0:
        return str( value)
    
    sign = copysign( 1,value)
    
    valin = abs( value)
    uncin = abs( uncertainty)
    
    dec = log10(uncin)
    # print('DBug uncin, dec, uncertainty', uncin, dec, uncertainty)
    dec = floor(dec+1)-1
    
    uncmant=uncin*pow(10.0,-1*dec)
    
    if uncmant > 9: ##Fix if rounding up adds another digit.
        dec = dec + 1
        uncmant=uncin*pow(10.0,-1*dec);
    
    if round( uncmant) != uncmant:  ##round larger if sigmant is not integral
        uncmant=int( uncmant+1);
    
    ## for values between .1 and 9999. use 2 part output (also equal to zero)
    if (valin >= .1 and valin <=9999.) or (valin == 0.0):
        if dec > 0:
            nd = 0
        else:
            nd = -dec
            
        fmtstr = '{'+':22.{}f'.format( nd)+'}'
#        print( 'DBug: fmtstr: {}'.format( fmtstr))
        
        if sign < 0:
#            val3p=str(int(valin*pow(10,-dec)+0.5)*pow(10,dec)*sign)
            val3p=fmtstr.format( int(valin*pow(10,-dec)+0.5)*pow(10,dec)*sign).strip()
        else:
#            val3p=str(int(valin*pow(10,-dec)+0.5)*pow(10,dec))
            val3p=fmtstr.format( int(valin*pow(10,-dec)+0.5)*pow(10,dec)).strip()
            
#        print( 'DBug: valin: {}, dec: {}, val3p: {}, nd: {}'.format( valin, dec, val3p, nd))
        
        unc3p = fmtstr.format( uncmant*pow(10,dec) ).strip()
        
        return ('{} '+u"\u00B1"+ ' {}').format( val3p, unc3p)
        
    else:  ##  otherwise use 4 part output
        
        val=int(valin*pow(10,-dec)+0.5)*pow(10,dec)*sign
        if valin >= uncin:
            exp=ceil(log10(valin))-1
        else:
            exp=ceil(log10(uncin))-1
        
        
        nd = -( dec - exp)
        
        if nd < 0:
            nd = 0
            
        fmtstr = '{'+':22.{}f'.format( nd)+'}'
#        print( 'DBug: fmtstr: {}'.format( fmtstr))

        val = fmtstr.format( val*pow(10,-exp)).strip()

        unc=str(uncmant*pow(10,dec-exp));
        unc = fmtstr.format( uncmant*pow(10,dec-exp)).strip()

#        print( 'DBug: val: {}, unc: {}, exp: {}, nd: {}'.format( val, unc, exp, nd))
        
        return ('({} '+u"\u00B1"+ ' {})' + u"\u00D7" +'10^' + '{}').format( val, unc, exp)



def randomLetter() -> str:
    '''
    Generate a single random uppercase ASCII letter

    Returns
    -------
    TYPE
        char.
    '''
    import random
    import string    
    return random.choice(string.ascii_uppercase)

def randomElement( List: Sequence[ Any]=(-1,1)) -> Any:
    '''
    return random element of list/sequence

    '''
    index = randint(0, len( List)-1)
    return List[ index]


def timeStampStr() -> str:
    '''Returns a string with the current time in ISO format.'''
    import datetime
    import time
    
    dt = datetime.datetime.now()
    epoch = dt.timestamp() # Get POSIX timestamp of the specified datetime.
    st_time = time.localtime(epoch) #  Get struct_time for the timestamp. This will be created using the system's locale and it's time zone information.
    tz = datetime.timezone(datetime.timedelta(seconds = st_time.tm_gmtoff)) # Create a timezone object with the computed offset in the struct_time.
    return dt.astimezone(tz).isoformat()

## math.comb is in Python 3.8 
if hasattr( math, "comb" ):
    from math import comb
    from math import comb as nCr
else:
    def nCr(n: int, r: int) -> int:
        ''' calculate number of combinations of r from n items.'''
        f = math.factorial
        return f(n) // f(r) // f(n-r)
    comb = nCr   

def relative_to_full_path( rel_path: str) -> str:
    '''Converts file path, relative to this module's directory, to a full path.
    Ref: https://stackoverflow.com/questions/3718657/how-do-you-properly-determine-the-current-script-directory
    '''
    import inspect
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    path = os.path.dirname(os.path.abspath(filename))
    path = os.path.join( path, rel_path)
    return path

def getTS( rel_path: str) -> str:
    '''Reads first line of specified file, which is expected to be a time-date
    string.
    This is mostly for internal package use.'''
    # here = os.path.abspath(os.path.dirname(__file__))
    # with codecs.open(os.path.join(here, rel_path), 'r') as tsf:
    fpath = relative_to_full_path( rel_path)
    # print( f'DBug: rel_path: { rel_path}, fpath: {fpath}')
    with codecs.open( fpath, 'r') as tsf:
        lines = tsf.read()
    linelist = lines.splitlines()
    return linelist[0]


def read( rel_path: str) -> str:
    '''Reads text file.'''
    # here = os.path.abspath(os.path.dirname(__file__))
    # with codecs.open(os.path.join(here, rel_path), 'r') as fp:
    fpath = relative_to_full_path( rel_path)
    # print( f'DBug: fpath: {fpath}')
    with codecs.open( fpath, 'r') as fp:
        return fp.read()

def get_version(rel_path: str) -> str:
    '''Reads version from specified file. The file path is relative
    to this file. It looks for line that starts with "__version__"'''
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

def is_defined( name:str) -> bool:
    '''
    Tests if string in name is a defined variable, function, etc.

    Parameters
    ----------
    name : str
        Name of object.

    Returns
    -------
    bool
        True if contents of name is name of defined object, else False.

    '''

    return name in locals()



## define cls magic and set precision if in IPython.
if is_ipython() and is_interactive():
    ### set default float precision
    ### Ref: https://stackoverflow.com/questions/10361206/how-to-run-an-ipython-magic-from-a-script-or-timing-a-python-script
    from IPython import get_ipython
    from IPython.core.magic import register_line_magic
            
    ipython = get_ipython()
    ipython.magic( 'precision %0.5g')
            
    ### define clear screen magic (%cls generates 23 blank lines)
    @register_line_magic 
    def cls(line) -> None: 
        '''Defines a 'clear screen' line magic'''
        print( 23*'\n') 
        return

    del cls ## must delete function to make magic visible.
    
    

######  'Welcome Message' on loading  ######

def condaEnvName() -> str:
    '''Gets environment name from python's path.
    Ref:
        https://stackoverflow.com/questions/36539623/how-do-i-find-the-name-of-the-conda-environment-in-which-my-code-is-running'''

    # return Path(sys.executable).as_posix().split('/')[-3]
    return sys.exec_prefix.split(os.sep)[-1]

def ipythonversion() -> str:
    '''gets IPython version or returns None.'''
    try:
        import IPython
        ipv = IPython.version_info
        version = ''
        for n in ipv:
            version += str( n) + '_'
        return version[:-1]  ## remove last '_'
    except:
        return None
 
def in_ipynb() -> bool:
    '''True if running in Jupyter notebook.
    Ref: https://exceptionshub.com/how-can-i-check-if-code-is-executed-in-the-ipython-notebook.html
    Ref: https://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook.
    Currently not definitive in result; returns True in Spyder IPython console.'''

    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter


def ck_installed( pkgname: sys.modules) :
    ''' Checks if package is installed,
        If installed the package is returned,
        Else tries to install pkgname and returns package if installed.
        pkgname is a string with name of package as used in import stmt.
        If install fails, returns None.
        Should be a duplicate of import_install.is_installed().
        Typical Usage:
            astropy = isInstalled( 'astropy') 
            if astropy == None:
                ... 
            else:
                from astropy import units as u
        '''
    try:
        pkg = __import__( pkgname)
        return pkg
    except Exception:
    	return None
ii = ck_installed ## alias

def is_installed( pkgname: sys.modules) -> bool:
    '''Returns True if package is installed.'''
    try:
        __import__( pkgname)
        return True
    except Exception:
    	return False

## check if packages for sound are installed and load once
IPython = ii( 'IPython')
beepy = ii( 'beepy')
 # beepy = None  ## testing
playsoundPkg = ii( 'playsound')
 # playsoundPkg = None; ## testing
simpleaudio = ii( 'simpleaudio')
 # simpleaudio = None ## testing

def beepsound() -> None:
    '''Plays a 'beep' sound when called if a sound package is found, or
    tries terminal beep.
    Sound packages that can be used:
        beepy
        simpleaudio
        Ipython.display.Audio'''
    ## use beep sounds from various possible packages
    if beepy != None:
        beepy.beep( 1)
    elif playsoundPkg != None and os.path.isfile( 'A-Tone-His_Self-1266414414.wav'):
        playsoundPkg.playsound( 'A-Tone-His_Self-1266414414.mp3')
    elif simpleaudio != None and os.path.isfile( 'mixkit-relaxing-bell-chime-3109.wav'):
        wave_obj = simpleaudio.WaveObject.from_wave_file( 'A-Tone-His_Self-1266414414..wav')
        play_obj = wave_obj.play()
        play_obj.wait_done()
    elif IPython != None:
        try:
            # IPython.display.Audio( 'http://www.soundjay.com/button/beep-07.wav', autoplay=True)
            IPython.display.Audio( 'audio/tone_440.wav', autoplay=True)
            # import numpy
            # sr = 22050 # sample rate
            # T = 2.0    # seconds
            # t = numpy.linspace(0, T, int(T*sr), endpoint=False) # time variable
            # x = 0.5*numpy.sin(2*numpy.pi*440*t)  
            # IPython.display.Audio(x, rate=sr) # load a NumPy array
        except ValueError:
            print( '\a')
    else:
        print( '\a')   ## probably won't work, but last attempt.


    
## Get timestamp for package, updated by setup.py.
timestamp = getTS( 'timestamp.txt')
date  = timestamp[0:10]
# print('\nDBug: date: {} TS:\n{}'.format( date, timestamp))

__version__=get_version("__init__.py")

def call( cmd: str):
    import subprocess
    '''Modeled after call function in NANOGrav Sprinng 2020 workshop.
    call() just executes the command in the shell and displays output.
    
    Could have security issues. See subprocess documentation.'''
    subprocess.call( cmd, shell=True)


def mine() -> None:

    '''List (prints) the functions and variables defined in handies.py'''
    
    print('\n classroom_gizmos.handies ver: {}, modified {}'.format(
        __version__, date))
    if is_installed( 'astropy'):
        print('Defining:\n     nowMJD(); mjd2date(), date2mjd(),')
        print('     astropy.units as "u", i.e. u.cm or u.GHz')
        print('     astropy.constants as "c", i.e. c.c or c.au')
        print('     angular_separation() ➞ angular separation between two RA,DEC coords.')
    else:
        print( '** astropy not available; MJD functions, u (units) and c (constants) are not available.')
    print('     cdbn(), osname(), hostname(), call(),')
    if is_installed( 'PyQt5'):
        if is_installed( 'func_timeout'):
            print('     select_file(), select_file_timeout( timeout={}),'.format( sfTimeOut))
        else:
            print('** func_timeout not available; select_file_timeout() ignores timeout.')
            print('     select_file()')
        
    else:
        print( '** PyQt5 is not available; select_file() and select_file_timeout() are not defined.')
    print('     rad(), deg(), sinD(), cosD(), tanD(), asinD(),\n     acosD(), atanD(), atan2D(), atan2P()')
    print("       'D' and 'P' functions work with degrees.")
    print("       'P' inverse functions return only positive angles.")
    print("     Defines nCr() and comb() or imports from math if available.")
    print('     greeks  ➞ a string with greek alphabet.')
    print('     cls or %cls; ipython \'magic\' writes 23 blank lines to clear an area of the screen')
    print('     clsall() function which removes previous text on screen by outputing ascii code.')
    print('     pltsize( width) ➞ resizes plots in matplotlib, units are inches')
    print('     timeStampStr() ➞ returns a readable timestamp string.')
    print('     ck_installed( pkgNameStr) ➞ returns package or None if not installed.')
    print('     is_installed( pkgNameStr) ➞ returns True if package is installed.')
    print('     is_ipython() ➞ True if running in ipython.')
    print('     is_interactive() ➞ True if in interactive interpreter but not in ipython.')
    print('     is_commandline() ➞ True if running from commandline;not interactive nor ipython.')
    print('     is_colab() ➞ True if running from Google Colab.')
    print('     VURound( value, uncertainty) ➞ Rounds value based on uncertainty.')
    print('     round_sig( value, sigfigs) ➞ Rounds value to specified sig.figs.')
    print('     round_sig_limit( value, sigfigs, limit) ➞ Rounds value to specified sig.figs or zero.')
    print('     count_down() ➞ Counts down the specified number of seconds.')
    print('     beepsound() ➞  trys to make sound.')

    print('     randomLetter() ➞ a random uppercase ASCII letter.')
    print('     randomElement( List) ➞ returns random element from list.')
    
    print('     external_addresses()  ➞  external names and IPs')
    print('     externalIP() ➞ external IP')
    print('     local_addresses() ➞ local name and IP')
    
    print('  Functions for portable code:')
    print('     osname(), username(), computername(), pythonversion(),')
    print('     condaversion(), ipythonversion(), in_ipynb(), is_installed()')
    print('     ck_installed(), or ii(),  II()' )
    
    print()

    print('From random imports randint( min, max)')
    print('From BestByMinBefore imports getCCode()')
    print('From import_install imports import_install as II and imports ckII')
    
    print('From math imports:\n     pi, sqrt, degrees, radians,\n     cos, sin, tan, atan2, asin, acos, atan, and\n' + 
      '     log, log10, exp')

    print( '\n     mine() ➞ lists what handies.py defines.')

    print( '\nRequires astropy, PyQt5, and func_timeout packages for full functionality.')
    print( 'beepsound() can use these audio packages if available: beepy, playsound, simpleaudio')
    
##Ref: https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-precision
    # prhints = ('Hint:\n' + 
    #       '     "%precision %g" or %.6g for better number formats.')
    # print(prhints)


def cosD( ang: float) -> float:
    '''Return cosine of angle in degrees.'''
    import math as m
    return m.cos( m.radians( ang))

def sinD( ang: float) -> float:
    '''Return sine of angle in degrees.'''
    import math as m
    return m.sin( m.radians( ang))

def tanD( ang: float) -> float:
    '''Return tangent of angle in degrees.'''
    import math as m
    return m.tan( m.radians( ang))

def asinD( val: float) -> float:
    '''Return inverse sine, in degrees, of val.'''
    import math as m
    return  m.degrees( m.asin( val))

def acosD( val: float) -> float:
    '''Return inverse consine, in degrees, of val.'''
    import math as m
    return m.degrees( m.acos( val))


def atanD( val: float) -> float:
    '''Return inverse tangent, in degrees, of val.'''
    import math as m
    return m.degrees( m.atan( val))


def atan2D( y: float, x: float) -> float:
    '''Return inverse tangent, in degrees, of y/x. (-180 ... 180)'''
    import math as m
    return m.degrees( m.atan2( y, x))

def atan2P( y: float, x: float) -> float:
    '''Return inverse tangent, in degrees, of y/x. (0 .. 360)'''
    ang = atan2D( y, x)
    if ang <0:
        ang = ang + 360
    return ang

rad = radians  ## alias the conversion functions
deg = degrees

greeks = ' Α Β Γ Δ Ε Ζ Η Θ Ι Κ Λ Μ Ν Ξ Ο Π Ρ Σ Τ Υ Φ Χ Ψ Ω  α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ τ υ φ χ ψ ω '

def cdbn( dirname: str, sub=None) -> str:
    '''cd to directory (or subdirectory) who's path is in Env.Var. who's name is passed as
       first argument.  2nd argument specifies a subdirectory relative to
       that named directory. On successful change, returns path of new CWD.'''
    import os
    """ Does cd to directory named in specified environment
        variable.
        Returns current directory (as string) if no error.
        If Error, outputs error msg. and returns False.
        --
        If sub is specified, tries to cd to that subdirectory
        after the cd to the contents of env. var.
    """
    try:
        dir = os.environ[ dirname]
    except KeyError:
        print( dirname, ': not an env. var.')
        return False
    else:
        if os.access( dir, os.R_OK):
            os.chdir( dir)
            if sub==None:
                return os.getcwd()
            else:
                if os.access( sub, os.R_OK):
                    os.chdir( sub)
                    return os.getcwd()
                else:
                    print( '{}: No access!'.format( 
                            os.path.join(dir,sub), dir))
            return False

        else:
            print('[{}] --> {} : No access!'.format( dirname, dir))
            return False



try:   ## These are only defined if astropy is installed.
    import astropy
    from astropy import units as u
    from astropy import constants as c
    import astropy.coordinates.angles as aca
    
    def nowMJD() -> float:
        '''Convert current time to MJD'''
        from astropy.time import Time
        return Time.now().to_value( 'mjd')
    
    def mjd2date( mjd: float) -> str:
        '''Convert MJD to a civil utc date/time'''
        
        from astropy.time import Time
        time = Time( mjd, format='mjd')
        return time.to_datetime()
    
    def date2mjd_( civildate: str) -> float:
        '''Convert specified time to MJD.
        The string in civildate must be recognized by astropy.time.Time,
        and is assumed to be UCT time.
    
        Value returned is float
        
        Usage:
            date2mjd( '2020-05-16T14:10') returns 58985.59027777777778'''
        
        from astropy.time import Time
        return Time( civildate).to_value( 'mjd', 'long')
        
    def date2mjd( civildate: str) -> float:
        '''Convert specified time to MJD.
        The string in civildate must be recognized by astropy.time.Time,
        and is assumed to be UCT time.
        As a special case, if the date/time is followed by UTC offset
        then that is used to shift the date/time to UTC.
        Example: 2019-09-30 20:54:54-04:00 corresponds to 
        UTC of 2019-10-01 00:54:54
    
        Value returned is float
        
        Usage:
            date2mjd( '2020-05-16T14:10') returns 58985.59027777777778
            or
            date2mjd( '2020-05-16T14:10-04:00') returns 58985.756944444444446
            '''
        
        cd = civildate
        offset = 0
        ## check for special case:
        if cd[-3]==':' and ( cd[-6]=='-' or cd[-6]=='+') :
            offset = (int( cd[-5:-3]) + int( cd[-2:])/60 )/24
            if cd[-6]=='+':
                offset = -offset
            cd = cd[:-6]
        
        from astropy.time import Time
        return Time( cd).to_value( 'mjd', 'long')+offset
    
    def angular_separation( RA1: str, DEC1: str, RA2: str, DEC2: str
                           ) -> aca.Angle:
        '''
        Returns angle separation between two coordinates in Astropy 'Angle' units.
    
        Parameters
        ----------
        RA1 : string
            RA coordinate (ex: '5h23m34.5s')
        DEC1 : string
            DEC coordinate (ex: '-69d45m22s')
        RA2 : string
            RA coordinate (ex: '0h52m44.8s')
        DEC2 : string
           DEC coordinate (ex: '-72d49m43s')
    
        Returns
        -------
        Separation angle in Astropy Angle units.
    
        '''
        
        from astropy.coordinates import SkyCoord
        # c1 = SkyCoord('5h23m34.5s', '-69d45m22s', frame='icrs')
        # c2 = SkyCoord('0h52m44.8s', '-72d49m43s', frame='fk5')
        c1 = SkyCoord( RA1, DEC1)
        c2 = SkyCoord( RA2, DEC2)
        sep = c1.separation(c2)
        
        return sep
    
except ImportError:
    print( 'mjd and anglular_separation functions not defined because astropy is not available.')


def pltsize( w: float, h: float=None, dpi: int=150) -> None:
    '''set plot size (matplotlib), size in notebook depends on resolution and
    browser settings. However, doubling the values should double the size.
    dpi is dots-per-inch which also changes plot size in notebooks.
    Default height is .75 times the width.'''
    import matplotlib
    if h==None:
        h = 0.75*w
    matplotlib.rc('figure', figsize=[w,h], dpi=dpi)

def osname() -> str:
    '''Returns name of operating system that Python is running on.'''
    try:
        os = __import__( 'os')
        return os.name
    except ImportError:
        return None


def username() -> str:
    '''Get current username or return "None".'''
    # import getpass
    try:
        getpass = __import__( 'getpass')
        return( getpass.getuser())
    except ImportError:
        return None

def computername() -> str:
    '''Get hostname of current computer or return "None".'''
    try:
        socket = __import__( 'socket')
        return socket.getfqdn()
    except ImportError:
        return None
hostname = computername

def external_addresses() -> List[ str]:
    '''Returns a 3 element list of info about external IP/Hostname.
      ( external hostname,  list of aliased hostnames, list of aliased IPs)
      
    '''
    from requests import get
    import socket
    
    verbose = False  ## set to True for debugging output
    
    ip = 'IP address not found.' ##  To mark failed attempt to get ip address
    
    try:
        ip = get( 'https://checkip.amazonaws.com').text
        if verbose: 
            print( f'from amazonaws.com ip is {ip}')
    except Exception:
        try:
            ip = get( 'https://api.ipify.org').text
            if verbose: 
                print( f'from ipify.org ip is {ip}')
        except Exception:
                ip = get( 'https://ident.me').text
                if verbose: 
                    print( f'from ident.me ip is {ip}')

    else:
        if verbose: 
            print('\nMy public IP address is: {}\n'.format(ip))
    
    ip = ip.rstrip()   ## remove any whitespace at ends of string.

    
    ##  Ref: https://www.programcreek.com/python/example/2611/socket.gethostbyaddr
    if verbose: 
        print( f'DBug ip is {ip}, and its type is {type(ip)}')
    
    try:
        results = socket.gethostbyaddr( ip)
    except Exception as err:
        results = ( str( err), [ None], [ ip])
        
    return results

def local_addresses() -> List[str]:
    ''' returns tuple of local hostname and local IP address'''
    import socket
    hostname = socket.gethostname()
    IP = socket.gethostbyname(hostname)
    return ( hostname, IP)

def externalIP() -> str:
    '''Returns external IP address via call to external_addresses().'''
    return external_addresses()[2][0]

def pythonversion() -> str:
    '''Get version of python or return "None".'''
    try:
        platform = __import__( 'platform')
        return platform.python_version()
    except ImportError:
        return None

def condaversion():
    '''Get version of conda, or return "None".
    Usually returns None!'''
    try:
        conda = __import__( 'conda')
        return conda.__version__
    except ImportError:
        return None  ## to be consistent with the others.

def count_down( t: int=10) -> None:
    '''Count down by seconds. 't' is the number of seconds.
    If beepy is installed, then a sound is made when countdown ends.
    Refs:  
    https://pypi.org/project/beepy/#description
    https://www.codespeedy.com/how-to-create-a-countdown-in-python/
    https://stackoverflow.com/questions/25189554/countdown-clock-0105'''
    while t > 0:
        mins, secs = divmod( int( t), 60)
        timeformat = '{:02d}:{:02d} '.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1
    print('\a\n\nDone!\n\n')
    beepsound()



#>>> File hash code functions 
def base10toN( num: int, n: int) -> str:
    """Change 'num'  to a base-n number.
    Up to base-38 is supported without special notation.
    should be file name safe.
    
     0 <= num  (i.i. non-negative)
     2 <= n <= 38  implemented number bases
    invalid values result in '???' being returned.
    
    C.S.:extended from base 36 to 38
    
    Ref: https://code.activestate.com/recipes/65212-convert-from-decimal-to-any-base-number/
    """
    if num < 0:
        return '???'
    if n < 2 or n > 38:
        return '???'
        
    num_rep={10:'a', 11:'b', 12:'c', 13:'d', 14:'e', 15:'f',
                     16:'g', 17:'h', 18:'i', 19:'j', 20:'k',
                     21:'l', 22:'m', 23:'n', 24:'o', 25:'p',
                     26:'q', 27:'r', 28:'s', 29:'t', 30:'u',
                     31:'v', 32:'w', 33:'x', 34:'y', 35:'z',
                     36:'-', 37:'_'}
    alphalen = 38  ##  number of characters in alphabet
    new_num_string=''
    current=num
    while current!=0:
        remainder=current%n
        if alphalen > remainder > 9:  ## 10 to alphalen - 1 case
            remainder_string=num_rep[remainder]
        elif remainder>=alphalen:     ## error condition
            remainder_string='('+str(remainder)+')'
        else:                         ## 0 to 9 case
            remainder_string=str(remainder)
        new_num_string=remainder_string+new_num_string
        current=int(current/n)
    return new_num_string

def hashstrlist( strlist: List[ str], nc: int=5, ordered: bool=False) -> str:
    '''
    Creates file systems safe hash code of length nc from the list of
    strings in strlist. Typically, strlist is a list of file names.
    The order of the strings does not affect the hash generated unless ordered is True.
    
    uses base10toN
    2019-02-16 /CS/ initial function version
    2021-05-09 /CS/ added 'ordered' flag.
    '''
    import hashlib
    tmplist = strlist.copy()
    if not ordered:
        tmplist.sort()
#    print( 'DBug:\n', strlist,'\n-----\n', tmplist)
    tmp = "".join( tmplist)
#    print( 'DBug:\n', tmp)
    resulthash = int(hashlib.sha256(tmp.encode('utf-8')).hexdigest(), 16) 
    # print( 'DBug resulthash:', resulthash)
    result = resulthash % 38**(nc)
    # print( 'DBug: result:', result)
    result = base10toN( result, 38).upper()
    # print( 'DBug: result:', result)
    
    ## zero fill if length is less than nc
    while len( result) < nc:
        result = '0' + result
    return result

#>>> END File hash code functions        


try:
    import PyQt5  ## used in fdtest module, skip these definitions if Qt5 not available.
    
    ## default timeout (in s) for select_file():
    sfTimeOut = 95

    def select_file( ) -> str:
        ''' Uses fdtest.py to browse for file and return its path.
        WARNING: This function will 'hang' until a file is selected.'''
        
        from classroom_gizmos.fdtest import gui_fname        
        return gui_fname()

    def select_file_timeout( timeout: float=sfTimeOut):
        ''' Uses fdtest.py to browse for file and return its path.
        If the fdtest call takes longer than 'timeout' seconds,
        the attempt is cancelled and None is returned.
        The argument, timeout, sets the number of seconds before time out.
        Note: if func_timeout package is not available, the no timeout
        is used (select_file() is called.)
        '''
        ## trying to do auto-install of func_timeout
        try:
            from func_timeout import func_timeout, FunctionTimedOut
        except ImportError:
            from classroom_gizmos.import_install import ii
            func_timeout = ii( 'func_timeout')
            try:
                from func_timeout import func_timeout, FunctionTimedOut
            except Exception:
                print( 'Timeout is not available.')
                return select_file()
            
        from classroom_gizmos.fdtest import gui_fname
        
        try:
            filename = func_timeout( timeout, gui_fname, args=()).decode("utf-8")
        except FunctionTimedOut:
            outstr = 'select_file cound not complete within '
            outstr += '{} seconds.\n'.format( timeout)
            print( outstr)
            #raise e
            filename = None
            
        return filename
except ImportError:
    print( 'select_file functions not defined because PyQt5 is not available.')

user = username()  ## only output version info for me.
if ( user == 'cws2' or user == 'hedfp') and +\
    is_interactive() and not in_ipynb():
    print( "Loading Carl's handies.py ver: {} {}; Python:{};\n   environment: {}; IPython: {}; is interactive: {};\n is ipython: {}".format( 
            __version__, date, python_version(), condaEnvName(), ipythonversion(), is_interactive(), is_ipython() ) )




if __name__ == "__main__":
    mine()
    
    
    

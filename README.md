# classroom_gizmos


### Easy install:

    pip install -U classroom_gizmos


### handies

A collection of functions (and constants) that are useful on the ipython command line in an introductory physics class.

Needs astropy, PyQt5, and func_timeout packages for some functions. If the packages are not installed, some functions will not be defined.


### import_install

importInstall() function returns the package specified by the string argument.

If the package is not installed, an attempt is made to install it and import is tried again.

### jupyter_file_browser

Implements an ipywidget based file browser for Jupyter notebooks.
(The file_select functions in handies module do not work in notebooks.)

### BestByMinBefore
Used for creating Perl snippits useful for WebAssign scoring algorithms.
<tt>getCCode()</tt> is a 'wizard' innterface that prompts for needed values.

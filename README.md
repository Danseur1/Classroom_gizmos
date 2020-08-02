# classroom_gizmos

### handies

A collection of functions (and constants) that are useful on the ipython command line in an introductory physics class.

Needs astropy, PyQt5, and func_timeout packages for some functions. If the packages are not installed, some functions will not be defined.


Easy install:

    pip install -U classroom_gizmos

### import_install

importInstall() function returns the package specified by the string argument.

If the package is not installed, an attempt is made to install it and import is tried again.

### jupyter_file_browser

Implements an ipywidget based file browser for Jupyter notebooks.
    
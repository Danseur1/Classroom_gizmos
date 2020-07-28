# classroom_gizmos

A collection of functions (and constants) that are useful on the ipython command line in an introductory physics class.

Needs astropy, PyQt5, and func_timeout packages for some functions.

* If astropy is not available, the MJD functions are not defined.
* If PyQt5 is not available, select_file and select_file_timeout are not defined.
* If func_timeout is not available, select_file_timeout() is
    the same as select_file().

Easy install:

    pip install classroom_gizmos
    
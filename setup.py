from setuptools import setup, find_packages
from setuptools.extension import Extension
import re
import numpy as np


def get_cython_version():
    """
    Returns:
        Version as a pair of ints (major, minor)

    Raises:
        ImportError: Can't load cython or find version
    """
    import Cython.Compiler.Main
    match = re.search('^([0-9]+)\.([0-9]+)',
                      Cython.Compiler.Main.Version.version)
    try:
        return map(int, match.groups())
    except AttributeError:
        raise ImportError

# Only use Cython if it is available, else just use the pre-generated files
try:
    cython_version = get_cython_version()
    # Requires Cython version 0.13 and up
    if cython_version[0] == 0 and cython_version[1] < 13:
        raise ImportError
    from Cython.Distutils import build_ext
    source_ext = '.pyx'
    cmdclass = {'build_ext': build_ext}
except ImportError:
    source_ext = '.c'
    cmdclass = {}

ext_modules = [Extension("_imseg_rand_forest", ["imseg/rand_forest/rand_forest" + source_ext,
                                                'imseg/rand_forest/fast_hist.c'],
                         extra_compile_args=['-I', np.get_include(), '-O3']),
               Extension("_imseg_rand_forest_image_features", ['imseg/rand_forest/forest_image_features_aux.c',
                                                               "imseg/rand_forest/forest_image_features" + source_ext],
                         extra_compile_args=['-I', np.get_include(), '-O3'])]
setup(name='imseg',
      cmdclass=cmdclass,
      version='0.0.1',
      packages=find_packages(),
      package_data={'imseg' : ['super_pixels/data/*']},
      author='Brandyn A. White',
      author_email='bwhite@dappervision.com',
      license='GPL',
      url='https://github.com/bwhite/imseg',
      ext_modules=ext_modules)

# ICOS-CP2ERDDAP

put your own configuration file in
~/.config/icp2edd/config.yaml

# to run 'module.__main__' from terminal
$ python3 -m icp2edd

or

$ python3 wrapper.py

# to run test
$ python3 test/test_basic.py


# to set up/update  package library
$ python3 setup.py sdist bdist_wheel

This command should output a lot of text and once completed should generate two files in the
 **dist** directory.
> The tar.gz file is a Source Archive whereas the .whl file is a Built Distribution.
Newer pip versions preferentially install built distributions, but will fall back to source archives
if needed. You should always upload a source archive and provide built archives for the platforms your
 project is compatible with.

# to install package
$ python3 -m pip install PATH_TO_YOUR_PACKAGE/dist/icp2edd.SOME_RELEASE.tar.gz
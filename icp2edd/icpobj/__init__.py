# from https://julienharbulot.com/python-dynamical-import.html
from importlib import import_module
from inspect import isclass
from pathlib import Path
from pkgutil import iter_modules

# set up what symbols in this module will be exported when from <module> import *
# __all__ = []

# First load local Object
module_name = "icpObj"

module = import_module(f"{__name__}.{module_name}")
for attribute_name in dir(module):
    attribute = getattr(module, attribute_name)

    if isclass(attribute):
        # Add the class to this package's variables
        globals()[attribute_name] = attribute
        # __all__.append(attribute_name)

# Then load subpackages
package_dir = Path(__file__).resolve().parent
for (_, module_name, _) in iter_modules([str(package_dir)]):
    module = import_module(f"{__name__}.{module_name}")
    # Add the module to this package's variables
    globals()[module_name] = module
    # __all__.append(module_name)

    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)

        if isclass(attribute):
            # Add the class to this package's variables
            globals()[f"{module_name}.{attribute_name}"] = attribute
    #         # __all__.append(f"{module_name}.{attribute_name}")

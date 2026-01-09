import numpy as np
import matplotlib.pyplot as plt

# import and setup site and windTurbines
import py_wake
from py_wake import BastankhahGaussian
from py_wake.examples.data.iea37._iea37 import IEA37Site, IEA37_WindTurbines
from py_wake.examples.data.hornsrev1 import V80

site = IEA37Site(16)
x, y = [0, 400, 800], [0, 0, 0]
windTurbines = V80()
D = windTurbines.diameter()
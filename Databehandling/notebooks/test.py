import packs
from tkinter import filedialog
import os
import pydicom as pd
import numpy as np
from func import *


LET, dose = accumulate_quantities('LET', Quantity_MAXVAl = None, dosescale = 0.01, return_dose = True)
Qeff = accumulate_quantities('Qeff', Quantity_MAXVAl = None, dosescale = 0.01, return_dose = False)
print("Accumulated quantities found")
files = [dose, LET, Qeff]
names = ['Accumulated_dose', 'Accumulated_LET', 'Accumulated_Qeff']

print("save as dicom files are now runned")
array2Dicom(files, names)
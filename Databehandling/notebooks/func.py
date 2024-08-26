import packs
import os
from tkinter import filedialog
import pydicom as pd
import numpy as np
import copy

def accumulate_quantities(quantity, Quantity_MAXVAl = None, dosescale = 0.01, return_dose = False):
    """
    Accumulates quantities based on patient data.
    Args:
        quantity (str): The quantity to be accumulated.
        Quantity_MAXVAl (float, optional): The maximum value for the quantity. Defaults to None.
        dosescale (float, optional): The scale for filtering doses. Defaults to 0.01.
        return_dose (bool, optional): Whether to return the dose values. Defaults to False.
    Returns:
        numpy.ndarray or tuple: The accumulated quantities. If return_dose is True, returns a tuple of the accumulated quantities and dose values. Otherwise, returns only the accumulated quantities.
    """
    
    
    #find path to patient data
    path = filedialog.askdirectory()  #choose a directory with the patient data
    
    print("Path: ", path)
    print("Quantity: ", quantity)

    dose_files = [file for file in os.listdir(path + '/dcm') if 'RD' in file]  #list of the patient's dose files
    dose_files_path = [path + '/dcm/' + file for file in dose_files]  #list of the patient's dose files with path
    
    quantity_files = [file for file in os.listdir(path + '/dose_output/Brain2') if f'{quantity}' in file]  #list of the patient's dose files
    quantity_files_path = [path + '/dose_output/Brain2/' + file for file in quantity_files]  #list of the patient's dose files with path
    

    sum_dose = 0  #initialize the sum of the dose values
    sum_quantity = 0  #initialize the sum of the quantity values
    for i in range(len(dose_files_path)):
        dsfile = pd.read_file(dose_files_path[i])
        dose = dsfile.pixel_array*dsfile.DoseGridScaling

        quantityfile = pd.read_file(quantity_files_path[i])
        quantity = quantityfile.pixel_array*quantityfile.DoseGridScaling
        
        if Quantity_MAXVAl:
            max_value_index = quantity > Quantity_MAXVAl
            values = quantity[max_value_index]
        
        sum_dose += dose  #sum the dose values
        sum_quantity += quantity*dose
    
    sum_quantity = sum_quantity/sum_dose
    sum_quantity[np.isnan(sum_quantity)] = 0
    
    #filter after dosescale
    filter_index = sum_dose < dosescale*np.max(sum_dose)
    sum_quantity[filter_index] = 0
    sum_dose[filter_index] = 0
    
    if return_dose == True:
        print('Returning dose')
        return sum_quantity, sum_dose
    else:
        return sum_quantity
    
    
def array2Dicom(array, series_description):
    """
    Converts a 3D array into DICOM files.
    Parameters:
    - array (ndarray): The 3D array to be converted into DICOM files.
    - series_description (list): A list of strings representing the description for each DICOM file.
    Returns:
    None
    Raises:
    AssertionError: If the shape of the array slice is not the same as the shape of the pixel data in the DICOM file.
    Notes:
    - This function prompts the user to choose a DICOM file to use as an example.
    - It creates a new DICOM file for each slice in the array, with the specified series description.
    - The DICOM files are saved in the chosen file path.
    """
    
    
    
    #load the dicom file that will be used as an example
    print('## Choose a dicom file to use as an example. Should be RD file for instance')
    dicom_example_path = filedialog.askopenfilename(filetypes=[("DICOM files", "*.dcm")])

    
    for i in range(len(array)):
        array_slice = array[i]
        ds = pd.read_file(dicom_example_path)
        scratch_rtdose = copy.deepcopy(ds)
        scratch_rtdose.SOPInstanceUID = scratch_rtdose.SOPInstanceUID[0:30] + str(np.random.randint(00000,99999)) + scratch_rtdose.SOPInstanceUID[-15:]
        scratch_rtdose.SeriesInstanceUID = scratch_rtdose.SOPInstanceUID[0:54] + str(np.random.randint(00000,99999))
    
    
        scratch_rtdose.BitsAllocated = 16
        scratch_rtdose.BitsStored = 16
        scratch_rtdose.HighBit = 15
        
        #check for the same shape
        assert array_slice.shape == (scratch_rtdose.pixel_array).shape, "not same shape in pixeldata"
        scratch_rtdose.NumberOfFrames = array_slice.shape[0]
        scratch_rtdose.Rows = array_slice.shape[1]
        scratch_rtdose.Columns = array_slice.shape[2]
        dgs =(2**16-1)/np.max(array_slice) #dose grid scaling
        scratch_rtdose.PixelData = (array_slice*dgs).astype(np.uint16)
        scratch_rtdose.DoseGridScaling = 1/dgs
        scratch_rtdose.DoseComment = series_description[i]
        scratch_rtdose.SeriesDescription = series_description[i]
        print(f'## Dicom file created for {series_description[i]}. Choose filename and path to save')
        save_path = filedialog.asksaveasfilename(defaultextension=".dcm", filetypes=[("DICOM files", "*.dcm")])
        scratch_rtdose.save_as(save_path)
    
    print('Dicom files saved')
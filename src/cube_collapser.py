#                             CUBE_COLLAPSER
#
# To collapse PANIC fits cubes.
#
# **inputs**
#   1. Folder /input with original fits slices
#   2. Final image name

####################################################################################

from astropy.io import fits
import os
import numpy as np
import sys

name = sys.argv[1]
date = sys.argv[2]
#name = input('Serie name (ej: FocusSeries_M43_0001): ')
#date = input('Date (YYY-MM-DD): ')


#~~~~      From the cube     ~~~~#
path = os.getcwd()
path_input = os.path.dirname(path)+f'/input/{date}/'
path_output = os.path.dirname(path)+f'/output/{date}/{name}/'

with fits.open(path_input + f'{name}.fits') as hdul:
    img = hdul[0].data

img_collapsed = (np.sum(img, axis=0)).astype(np.float32)
hdr_collapsed = hdul[0].header

img_hdu = fits.PrimaryHDU(img_collapsed,hdr_collapsed)
img_hdu.writeto(path_output + f'{name}_collapsed.fits',overwrite=True)



#~~~~     From the slices     ~~~~#    EDITAR SEGUN DATE Y NAME LOS PATHS
#path = os.path.dirname(path)+f'/output/{name}/originals/'

#total_files = [file for file in os.listdir(path) if file.startswith(f'{name}_')]
#for i in range(len(total_files)):
#    with fits.open(path + f'{name}_{i + 1}.fits') as hdul:
#        img = hdul[0].data
#        header = hdul[0].header
#
#        if i == 0:
#            suma = img
#        else:
#            suma += img
#
#img_sum = fits.PrimaryHDU(suma, header=header)
#hdul = fits.HDUList([img_sum])
#hdul.writeto(path + f'{name}_collapsed.fits', overwrite=True)

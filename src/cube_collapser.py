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

object = input('Cube directory (ej: M43_0001): ')
name = input('Final image name (ej: M43_0001_cube): ')

path = os.getcwd()
path = os.path.dirname(path)+f'/output/{object}/originals/'

total_files = [file for file in os.listdir(path) if file.startswith(f'{object}_')]
for i in range(len(total_files)):
    with fits.open(path + f'{object}_{i + 1}.fits') as hdul:
        img = hdul[0].data
        header = hdul[0].header

        if i == 0:
            suma = img
        else:
            suma += img

img_sum = fits.PrimaryHDU(suma, header=header)
hdul = fits.HDUList([img_sum])
hdul.writeto(path + f'{name}.fits', overwrite=True)

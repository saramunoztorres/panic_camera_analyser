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

name = input('Cube directory (ej: FocusSeries_M43_0001): ')
final_img_name = input('Final image name (ej: FocusSeries_M43_0001_collapse): ')

path = os.getcwd()
path = os.path.dirname(path)+f'/output/{name}/originals/'

total_files = [file for file in os.listdir(path) if file.startswith(f'{name}_')]
for i in range(len(total_files)):
    with fits.open(path + f'{name}_{i + 1}.fits') as hdul:
        img = hdul[0].data
        header = hdul[0].header

        if i == 0:
            suma = img
        else:
            suma += img

img_sum = fits.PrimaryHDU(suma, header=header)
hdul = fits.HDUList([img_sum])
hdul.writeto(path + f'{final_img_name}.fits', overwrite=True)

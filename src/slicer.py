#        SLICER_FITS
#
# Para cortar los cubos fits de PANIC.
#
#  **inputs**
#   1. Carpeta /input con las imagenes fits originales en el mismo dir que este script
#   2. El nombre del objeto (lo pide el programa)
#
#  Se crean fits individuales con el header del cubo original.
#  El nombre de los fits individuales es *'nombre de la serie'+slice_i*,
#  y se guardan en las respectivas carpetas de las series y llamadas por
#  su propio nombre en la carpeta output.
#
####################################################################################

from astropy.io import fits
from astropy.io.fits import Header
import os

path = os.getcwd()

# function to make new directories in the output dir, or to use the existing one
def make_dir(name):
    path_new_dir = os.path.dirname(path)+f'/output/{name}'
    if not os.path.exists(path_new_dir):
        os.makedirs(path_new_dir)
        directory = path_new_dir
    else:
        directory = path_new_dir
    return directory

#
object = input('Objeto de la FocusSerie: ')

total_files = [file for file in os.listdir(os.path.dirname(path)+'/input/') if file.startswith(f'FocusSeries_{object}')]
for i in range(len(total_files)):
    # open fit cube
    focusSerie = f'{object}_{i+1:04d}'

    fit = fits.open(os.path.dirname(path)+f'/input/FocusSeries_{focusSerie}.fits')
    hdr = fit[0].header
    img = fit[0].data
    directory = make_dir(focusSerie)

    # slice and save in different fits
    for slice_index in range(len(img)):
        img_ind = img[slice_index, :, :]
        hdr_ind = Header(cards=hdr.cards)
        slc = fits.PrimaryHDU(data=img_ind, header=hdr_ind)
        slc.writeto(os.path.dirname(path) + f'/output/{focusSerie}/{focusSerie}_slice_{slice_index+1}.fits', overwrite=True)

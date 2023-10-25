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
#  Dos modos disponibles:
#   - Para un solo cubo
#   - Para varios cubos del mismo objeto numerados desde el 1
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

#~~~~     One cube at a time     ~~~~#

focusSerie = input('Focus Serie (ej: M34_0004): ')

hdul = fits.open(os.path.dirname(path)+f'/input/FocusSeries_{focusSerie}.fits')
hdr = hdul[0].header
img = hdul[0].data
dir_focusSerie= make_dir(focusSerie)
dir_originals = make_dir(f'{focusSerie}/originals')

# slice and save in different fits
for slice_index in range(len(img)):
    img_ind = img[slice_index, :, :]
    hdr_ind = Header(cards=hdr.cards)
    slc = fits.PrimaryHDU(data=img_ind, header=hdr_ind)
    slc.writeto(os.path.dirname(path)+f'/output/{focusSerie}/originals/{focusSerie}_{slice_index+1}.fits',overwrite=True)


#~~~~  More than one cube at a time ~~~~#

#object = input('Objeto de la FocusSerie: ')

#total_files = [file for file in os.listdir(os.path.dirname(path)+'/input/') if file.startswith(f'FocusSeries_{object}')]
#for i in range(len(total_files)):
#    focusSerie = f'{object}_{i+1:04d}'
#    # open fit cube
#    hdul = fits.open(os.path.dirname(path)+f'/input/FocusSeries_{focusSerie}.fits')
#    hdr = hdul[0].header
#    img = hdul[0].data
#    directory = make_dir(focusSerie)
#
#    # slice and save in different fits
#    for slice_index in range(len(img)):
#        img_ind = img[slice_index, :, :]
#        hdr_ind = Header(cards=hdr.cards)
#        slc = fits.PrimaryHDU(data=img_ind, header=hdr_ind)
#        slc.writeto(os.path.dirname(path) + f'/output/{focusSerie}/{focusSerie}_slice_{slice_index+1}.fits', overwrite=True)
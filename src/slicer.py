#                                SLICER_FITS
#
# To cut PANIC fits cubes.
#
# **inputs**
#   1. Folder /input with original fits images in the same directory as this script
#   2. Object name (prompted by the program)
#
# Individual fits are created with the header of the original cube.
# The names of the individual fits are 'series name'+i.fits, and they are
# saved in the respective series folders, called by their own names in the
# output folder.
#
# Two available modes:
#   - For a single cube
#   - For multiple cubes of the same object (numbered from 1)

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
#        slc.writeto(os.path.dirname(path) + f'/output/{focusSerie}/{focusSerie}_{slice_index+1}.fits', overwrite=True)
#        ALIGN_IMAGES
#
# This script align the images of the given directory.
#
#  **inputs**
#   1. Object directory (where the images to align are)
#
#  First image is the reference, the second one the objetive.
#  A transformation matrix between the images is calculated and used to create a
#  new image: the objetive image transformed (aligned). Then, the same process is
#  repeated with this new image (objetive aligned) and the next one in the dir.
#
####################################################################################

import matplotlib.pyplot as plt
import numpy as np
from photutils.detection import DAOStarFinder
import astroalign as aa
from astropy.io import fits
from astropy.stats import mad_std
from astropy.visualization import ZScaleInterval, ImageNormalize
import os

##

object = input('Object directory: ')

path = os.getcwd()
path = os.path.dirname(path)+f'/output/{object}/'

# read fits to compare
img_ref = fits.getdata(path + f'{object}_slice_1.fits')
img_obj = fits.getdata(path + f'{object}_slice_2.fits')


# norm
def normalization(img):
    intervalo = ZScaleInterval()
    vmin, vmax = intervalo.get_limits(img)
    norm = ImageNormalize(vmin=vmin, vmax=vmax)
    return norm


total_files = [file for file in os.listdir(path) if file.startswith(f'{object}_slice')]

for i in range(len(total_files) - 1):  # repeat for every fits file in the dir

    print('Img ref: ', i + 1, '\nImg obj: ', i + 2)

    # finding stars
    daofind = DAOStarFinder(fwhm=3.0, threshold=5. * mad_std(img_ref))
    star_ref = daofind(img_ref)
    star_obj = daofind(img_obj)

    # extract coords
    coord_ref = np.array(list(zip(star_ref['xcentroid'], star_ref['ycentroid'])))
    coord_obj = np.array(list(zip(star_obj['xcentroid'], star_obj['ycentroid'])))

    # align by coords
    transf, (img_ref_alin, img_obj_alin) = aa.find_transform(coord_ref, coord_obj)
    print('\nTransformation matrix: \n', transf.params, '\n')

    # align objetive image
    img_alin, footprint = aa.apply_transform(transf, img_ref, img_obj)

    # vis differences
    plt.figure(figsize=(12, 10))
    #plt.subplot(1, 2, 1)
    plt.imshow(img_alin - img_ref, cmap='viridis', origin='lower', norm=normalization(img_alin - img_ref))
    plt.colorbar(label='difference')
    plt.tight_layout()
    plt.show()

    ## vis footprint
    #plt.subplot(1, 2, 2)
    #plt.imshow(footprint, cmap='viridis', origin='lower', norm=normalization(footprint))
    #plt.colorbar(label='footprint')
    #plt.tight_layout()
    #plt.show()

    if i == (len(total_files) - 2):  # break the bucle, bc there are no more img in the dir
        break

    # change images: now img_ref is the aligned one, and img_obj is the next one
    img_ref = img_alin
    img_obj = fits.getdata(path + f'{object}_slice_{i + 3}.fits')

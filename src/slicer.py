from astropy.io import fits
from astropy.io.fits import Header
import os
import time

start = time.time()

path = os.getcwd()

for i in range(9):
    # open fit cube
    focusSerie = f'M34_000{i + 1}'

    fit = fits.open(f'FocusSeries_{focusSerie}.fits')
    hdr = fit[0].header
    img = fit[0].data

    # slice and save in different fits
    for slice_index in range(len(img)):
        img_ind = img[slice_index, :, :]
        hdr_ind = Header(cards=hdr.cards)
        slc = fits.PrimaryHDU(data=img_ind, header=hdr_ind)
        slc.writeto(path + f'/slices_{focusSerie}/slice_{focusSerie}_{slice_index + 1}.fits', overwrite=True)

end = time.time()

print('Ejecution time:', end - start)

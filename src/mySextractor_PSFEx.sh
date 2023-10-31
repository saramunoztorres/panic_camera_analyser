#!/bin/bash

echo -n Serie name, ej: FocusSeries_M34_0011:
read name

echo -n Number of fits: 
read number

cd ..

# 
for ((i=1; i<=$number; i++)); do
    file="${name}_${i}"
    echo Procesing ${file}
    echo Ejecuting sextractor
    sex -c sextractor.sex.panic test_sara/${file}.fits -CATALOG_NAME test_sara/${file}.cat
    echo Ejecuting PSFEx
    cd test_sara/
    psfex -c ../psfex.cfg ${file}.cat 
    cd ..
done

echo Procesing ${name}_collapsed
echo Ejecuting sextractor
sex -c sextractor.sex.panic test_sara/${name}_collapsed.fits -CATALOG_NAME test_sara/${name}_collapsed.cat
echo Ejecuting 
cd test_sara/
psfex -c ../psfex.cfg ${name}_collapsed.cat 

# Copying FWHM to saramunoz@ekbalam:/home/saramunoz/project/panic_camera_analyser/output_PSFEx/
echo Copying FWHM files to saramunoz@ekbalam:/home/saramunoz/project/panic_camera_analyser/output_PSFEx/
scp fwhm_${name}_*.png saramunoz@ekbalam:/home/saramunoz/project/panic_camera_analyser/output_PSFEx/
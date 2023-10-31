#!/bin/bash
# Pipeline from raw cubes to slices and cube collapsed in panic1

echo -n "Serie name (ej: FocusSeries_M34_0002): "
read name

echo -n "Date (YYY-MM-DD): "
read date

#
echo Ejecuting slicer.py
python3 slicer.py ${name} ${date}

#
echo Ejecuting cube_collapser.py
python3 cube_collapser.py ${name} ${date}

#
echo Copying data to @panic1:/home/panic/data2/PSFEx_test/test_sara 
cd ../output/${date}/"${name}" 
scp "${name}_collapsed.fits" saramunoz@panic1:/home/panic/data2/PSFEx_test/test_sara
cd originals/
scp * saramunoz@panic1:/home/panic/data2/PSFEx_test/test_sara
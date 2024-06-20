# BSc-Research-Project

This python program was one of many used for calibrating and analysing spectral profiles of plasma plumes taken from a variety of target material. This example specifically was used for a carbon (graphite) target, with the spectrometer centered at a wavelength of 650nm. It should be noted that the beginning of this code uses Neon and Krypton calibration lamps to calibrate the wavelengths (x-axis of final plots) and  QTH lamp to calibrate the relative intensities measured in the spectrometer (y-axis in the final plot). For different spectrometers, center wavelengths, and calibration lamps, the calculations of emission peaks will have to be adjusted accordingly.

The final spectral profile for the carbon data from this example is shown below:

![screenshot](carbon-650center-plot.jpg)

## How it Works

This program is made to take in .tiff files as data files. These files are pixel arrays (in this case 78x512 pixes) that store a "count" or relative intensity of photons incident on that pixel, and because the light passes through a spectrometer before being detected, the x-axis of this pixel array corresponds to wavelengths.

This program works in three main steps:
1 - Calibrate wavelengths by making a relation between x-pixel number and a wavelength
2 - Calibrate the relative intensities by creating a correction ration from a "known" spectral profile (the QTH lamp)
3 - Apply these calibrations to the real data, plot, and calculate a peak wavelength

Details of these steps can be found below.

## Wavelength Calibration

The first step/cell in the wavelength calibration is to load in the calibration data (three files: the Ne, Kr, and QTH lamp) and put it into 1-D arrays by summing over the y-axis intensities

The next step is to correspond "known" Ne and Kr emission wavelengths to the centroid of the emission peaks seen in the data. The first peak of the Krypton lamp seems to happen around pixel 50, so a centroid of this peak was calculated over the range 40 to 60 (Peak1). This Krypton peak is known to be at a wavelength of 587nm, so one can identify that the pixel value for Peak1 corresponds to a wavelength of 587nm. The same is done for two Neon emission peaks which are known to have wavelengths of 640nm and 703nm. 

Once these three pixel-wavelength calculations have been made, a second degree polynomial fit is made to act as a function relating every pixel to a wavelength which concludes the wavelength calibration.

## Intensity calibration

To calibrate the intensity of the experimental data, the third calibration data file, the QTH lamp, is used. This lamp has a very well known and measured emission spectrum over the wavelength region of interest, so can serve as an indicator of how much your spectrometer is over/under-detecting intensities. 

This calculation starts off by creating an array that corresponds to the NIST polynomial (just the known QTH emission spectrum). This polynomial, along with the measured QTH spectrum are then normalized to unity. Lastly, a "ratio of calibration" is calculated by dividing the MEASURED emission spectrum of the QTH lamp by the EXPECTED/KNOWN emission spectrum (the NIST polynomial). This can then be easily applied to the real data (by dividing the real data by this ratio) to ensure the relative intensities measured by the spectrometer are accurate.

## Analyze Real Data

The last part of this code is to use the two calibrations on the real data, plot it, and calculate the maximum wavelengths.

This is done by loading in the real data, which are three .tiff files plus an extra background .tiff file (an image taken in the dark). The background shot was then subtracted out from the main files, and then for each file a sum over the vertical pixels was done to make each one a 1-D array.

Then the intensity calibration was applied by dividing the real data arrays by the "ratio of calibration", and finally the data was plotted with the wavelenth function as the x-axis.

To calculate the peaks of each emission line, a third degree polynomial fit was applied to the region right around the peak, and the location of the max was recorded. These polynomials can be seen below, along with the data plots and the maximum wavelengths

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 14:48:04 2021

@author: patte
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import imageio
from PIL import Image

#%% Load Calibration data

path = '<PATH_TO_CALIBRATION_DATA>'
os.chdir(path)
list = os.listdir(path)
image = np.zeros([3,78,512])

i = 0
while i<3:
    image[i] = imageio.imread(list[i])
    i += 1
print(image[2])

calib_data = np.zeros([3,512])
i = 0
while i<3:
    j = 0
    while j<78:
        k = 0
        while k<512:
            calib_data[i,k] += image[i,j,k]
            k += 1
        j += 1
#    plt.plot(calib_data[i])
    i += 1

#%% centroid of first peak

start = 40
end = 60
i = start
a = 0
b = 0

while i<end:
    a += i * calib_data[0,i]
    b += calib_data[0,i]
    i += 1

Peak1 = a / b
print(Peak1)

subset1 = calib_data[0,start:end]
plt.plot(range(start,end), subset1)
plt.axvline(x=Peak1, color = 'red')

#%% centroid of second peak

start = 200
end = 225
a = 0
b = 0
i = start
while i<end:
    a += i * calib_data[1,i]
    b += calib_data[1,i]
    i += 1

Peak2 = a / b
print(Peak2)

subset2 = calib_data[1,start:end]
plt.plot(range(start,end), subset2)
plt.axvline(x=Peak2, color = 'red')

#%% centroid of third peak

start = 401
end = 420
a = 0
b = 0
i = start
while i<end:
    a += i * calib_data[1,i]
    b += calib_data[1,i]
    i += 1
Peak3 = a / b
print(Peak3)

subset3 = calib_data[1,start:end]
plt.plot(range(start,end), subset3)
plt.axvline(x=Peak3, color='red')

#%% plot calibration data

plt.title('Calibration Emission Spectra')
plt.xlabel('Pixels')
plt.ylabel('Relative Intensities')
plt.plot(calib_data[0], label='Kr')
plt.plot(calib_data[1], label='Ne')
plt.plot(calib_data[2], label='QTH')
plt.text(32, 1.6e6, '587nm')
plt.text(220, 2.4e6, '640nm')
plt.text(410, 0.4e6, '703nm')
plt.legend()
#plt.savefig('calibration-data.png')

#%% wavelength vs pixel

pixel_peaks = np.array([Peak1,Peak2,Peak3])
wavelength_peaks = np.array([587.1,640.23,703.24])
pixels = np.zeros([512])

i = 0
while i<512:
    pixels[i] = i + 1
    i += 1

wavelength = np.zeros([400])
p = np.polyfit(pixel_peaks,wavelength_peaks,2)
print(p)

i = 0
while i<400:
    P = np.poly1d(p)
    wavelength[i] = P(pixels[i])
    i += 1

plt.title('Wavelength vs Pixel')
plt.xlabel('Pixel')
plt.ylabel('Wavelength (nm)')
plt.plot(wavelength)

#plt.savefig('wavelength_vs_pixel.png')

#%% test peak and wavelength

print(wavelength[252])

#%% NIST polynomial wavelength

import math

A=42.9349188812877
B=-4529.93297732735
C=0.99573376982131
D=93.0152926804316
E=-27811.5953281163
F=-7981163.44240646
G=1444339179.40102
H=0

NIST = np.zeros([400])
i = 0
while i<400:
    NIST[i] = (wavelength[i])**(-5)*(math.exp(A+B/wavelength[i]))*(C+D/wavelength[i]+E/(wavelength[i])**2+F/(wavelength[i])**3+G/(wavelength[i])**4+H/(wavelength[i])**5)
    i += 1

plt.plot(NIST)

#%% normalize NIST and QTH

plt.title('Normalized NIST and QTH Intensities')
plt.xlabel('Pixel')
plt.ylabel('Normalized Relative Intensities')

norm_NIST = np.zeros([400])
i = 0
while i<400:
    norm_NIST[i] = NIST[i] / np.amax(NIST)
    i += 1
plt.plot(norm_NIST, label='NIST')

norm_QTH = np.zeros([512])
j = 0
while j<512:
    norm_QTH[j] = calib_data[2,j] / np.amax(calib_data[2])
    j += 1
plt.plot(norm_QTH, label='QTH')

plt.legend()
#plt.savefig('norm-NIST-QTH.png')

#%% ratio of calibration

ratio = np.zeros([400])
i = 0
while i<400:
    ratio[i] = norm_QTH[i] / norm_NIST[i]
    i += 1

plt.title('Ratio of Calibration')
plt.xlabel('Pixel')
plt.ylabel('Ratio')
plt.plot(ratio)
#plt.savefig('ratio.png')

#%% load real data

path = '<PATH_TO_REAL_DATA>'
os.chdir(path)
list = os.listdir(path)
image3 = np.zeros([4,24,400])

i = 0
while i<4:
    image3[i]=imageio.imread(list[i])
    print(image3[i])
    i += 1

data = np.zeros([4,400])

bg = image3[0]
i = 1
while i<4:
    image3[i]=np.subtract(image3[i],bg)
    i += 1

i = 0
while i<4:
    j = 0
    while j<24:
        k = 0
        while k<400:
            data[i,k] += image3[i,j,k]
            k += 1
        j += 1
    plt.plot(data[i])
    i += 1

#%% calibrate real data

norm_data = np.zeros([3,400])

i = 0
while i<3:
    j = 0
    while j<400:
        norm_data[i,j] = data[i+1,j] / ratio[j]
        j += 1
    i += 1

plt.title('Carbon Centered at 650nm')
plt.xlabel('Wavelength')
plt.ylabel('Relative Intensities')
plt.plot(wavelength, norm_data[2] / 1e5, color='blue', label='d=38cm')  
plt.plot(wavelength, norm_data[0] / 1e5, color='orange', label='d=39cm')
plt.plot(wavelength, norm_data[1] / 1e5, color='green', label='d=40cm')
plt.legend()
#plt.savefig('carbon.center=650.jpg')
b=np.amax(norm_data[1])
print(b)

#%% 3rd degree polynomial fit and plot (around peaks)

data_subsection = np.zeros([3,200])
x_subsection = np.zeros([3,200])
wavelength_subsection = np.zeros([200])
poly = np.zeros([3,200])
maxes = np.zeros([3])


i = 0
while i < 3:
    j = 0
    while j < 200:
        data_subsection[i,j] = norm_data[i,j]
        x_subsection[i,j] = j+1
        if(i == 0):
            wavelength_subsection[j] = wavelength[j]
        j += 1
    a = np.polyfit(x_subsection[i], data_subsection[i], 3) # a[0]*x^2 + a[1]*x + a[2]
    A = np.poly1d(a) # polynomial function with a[i] coefficients (A[x] = a[0]*x^2 + a[1]*x + a[2])
    k = 0
    while k < 200:
        poly[i,k] = A(x_subsection[i,k])
        k += 1
    maxes[i] = np.argmax(poly[i])
    i += 1

i = 0
while i < 3:
    plt.plot(wavelength_subsection, data_subsection[i] / 1e5, color='grey')
    print(wavelength[int(maxes[i])])
    i += 1

plt.title('Polynomial fits and Max Wavelengths')
plt.xlabel('Wavelength (nm)')
plt.plot(wavelength_subsection, poly[0] / 1e5, color = 'orange')
plt.plot(wavelength_subsection, poly[1] / 1e5, color = 'green')
plt.plot(wavelength_subsection, poly[2] / 1e5, color = 'blue')
plt.axvline(x=maxes[0], color = 'orange')
plt.axvline(x=maxes[1], color = 'green')
plt.axvline(x=maxes[2], color = 'blue')
plt.text(603, 3.5, int(wavelength[int(maxes[0])]), color = 'orange')
plt.text(596, 3.5, int(wavelength[int(maxes[1])]), color = 'green')
plt.text(613, 3.5, int(wavelength[int(maxes[2])]), color = 'blue')

#plt.savefig('poly-fit.png')

#%% Plot with max wavelength and calculate temperature

temp = np.zeros([3])
i=0
while i<3:
    temp[i] = 2.898e6 / wavelength[int(maxes[i])]
    print(temp[i])
    i += 1

max_wavelengths = np.zeros([3])
i = 0
while i<3:
    max_wavelengths[i] = wavelength[int(maxes[i])]
    i += 1

plt.title('Carbon Centered at 650nm')
plt.xlabel('Wavelength')
plt.plot(wavelength,norm_data[2],color='blue', label='d=38cm')  
plt.plot(wavelength,norm_data[0],color='orange', label='d=39cm')
plt.plot(wavelength,norm_data[1],color='green', label='d=40cm')
plt.axvline(x=max_wavelengths[0], color='orange')
plt.axvline(x=max_wavelengths[1], color='green')
plt.axvline(x=max_wavelengths[2], color='blue')
plt.legend()

#%% Planck Graph w2

h=6.626e-34
c=3e8
k=1.38e-23
pi=np.pi
def planck(wav, T):
    a = 2.0*h*c**2
    b = h*c/(wav*k*T)
    intensity = a/ ( (wav**5) * (np.exp(b) - 1.0) )
    return intensity

wavelengths = np.arange(436e-9, 650e-9, 1e-9) #for ROI

intensity4727 = planck(wavelengths, 4727.)
intensity4758 = planck(wavelengths, 4758.)
intensity4814 = planck(wavelengths, 4814.)

plt.plot(wavelengths*1e9, intensity4758, color='orange', label='4758K')
plt.plot(wavelengths*1e9, intensity4727, color='green', label='4727K')
plt.plot(wavelengths*1e9, intensity4814, color='blue', label='4814K')

plt.axvline(x=436, color='black',  linestyle='--')
plt.axvline(x=650, color='black', linestyle='--')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity')
plt.title('Region of Interest')
plt.legend()
#plt.savefig('ROI.jpg')


#%%


plt.title('Carbon Centered at 650nm')
plt.plot(wavelength,norm_data[1],color='gray')  
plt.plot(wavelength,norm_data[0],color='gray')
plt.plot(wavelength,norm_data[2],color='gray')

plt.plot(wavelengths*1e9, intensity4727*1.35e-6-1.246e7, linewidth='2', linestyle='--', color='green', label='T=4727K') # 6000K blue line
plt.axvline(x=613, color='green')
plt.plot(wavelengths*1e9, intensity4758*1.35e-6-1.29e7, linewidth='2', linestyle='--', color='orange', label='T=4758K') # 6000K blue line
plt.axvline(x=609, color='orange')
plt.plot(wavelengths*1e9, intensity4814*8.84e-7-8.85e6, linewidth='2',linestyle='--', color='blue', label='T=4814K' ) # 6000K blue line
plt.axvline(x=602, color='blue')
plt.legend()
#plt.savefig('temp_for_carbon.center=650.jpg')

#%%

import seaborn as sns

i=0
y=np.zeros([200])
x=np.zeros([200])
while i<200:
    x[i] = wavelength[i]
    y[i] = norm_data[2,i]
    i += 1
    
a = sns.regplot(x=x, y=y/1e5, data=y, order=3, )
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensities')
plt.axvline(x=613, color='red')
plt.text(614, 4.6, '613nm')
plt.title('Zoomed-In Maximum Wavelength Calculation')
#plt.savefig('mwl.jpg')

b = np.amax(a)
print(b)
#plt.plot(x,y)

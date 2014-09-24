# Simple script written in Python 2.7.1 + NumPy 1.6.1 + SciPy 0.10.0 + matplotlib 1.1.0
# This version works only for SVS data.
# SDR in Python
import os #Miscellaneous operating system interfaces
import pylab as m #For complex arrays
import struct #read binary data
import numpy as np
import pylab #plotting
import scipy.fftpack #FFT
import scipy
from Tkinter import * #GUI Tk
import tkFileDialog

#Open dialog

master = Tk()
master.withdraw() #hiding tkinter window

file_path = tkFileDialog.askopenfilename(title="Open file", filetypes=[("Siemens DICOM file",".IMA"),("All files",".*")])

if file_path != "":
  print "you chose file with path:", file_path

else:
  print "you didn't open anything!"

master.quit()

DICOMfile=file_path
fileHandle = open (DICOMfile, 'rb' ) #open binary file
file=fileHandle.read() #read the content into file variable
#	print fileHandle.read()
#while (fileHandle.readline() == '### ASCCONV END ###'):
#print 'End'

# Search for begin
search_begin = "### ASCCONV BEGIN ###"
index_begin = file.find(search_begin)
#print search_begin, "found at index", index_begin

#Search for end
search_end = "### ASCCONV END ###"
index_end = file.find(search_end)
#print search_end, "found at index", index_end
#print file[index_begin:index_end]

#Default Matrix sizes in case of SVS
sizeX=1
sizeY=1
sizeZ=1

#Search for VectorSize
search_VectorSize = "sSpecPara.lVectorSize"
index_VectorSize = file.find(search_VectorSize)

#print search_VectorSize, "found at index", index_VectorSize

#Split the string into lines, 100 chars should be enough for one line, anyway the first line is important here
temp_VectorSize = file[index_VectorSize:index_VectorSize+100].splitlines()
split_temp_VectorSize=temp_VectorSize[0].split()
str_VectorSize = split_temp_VectorSize[2]
VectorSize = int(str_VectorSize)
print 'Vector size: ', VectorSize

#Search for MatrixSize Z (Slice)
search_sizeZ = "sSpecPara.lFinalMatrixSizeSlice"
index_sizeZ = file.find(search_sizeZ)

#print search_sizeZ, "found at index", index_sizeZ

#Split the string into lines, 100 chars should be enough for one line, anyway the first line is important here [0]
temp_sizeZ = file[index_sizeZ:index_sizeZ+100].splitlines()
split_temp_sizeZ=temp_sizeZ[0].split()
str_sizeZ = split_temp_sizeZ[2]
sizeZ = int(str_sizeZ)
print 'X size: ', sizeZ

#Filesize
fileinfo = os.stat(DICOMfile)
Filesize = fileinfo.st_size
print 'File size:', Filesize, 'bytes'

# Headersize 
Datasize=VectorSize*sizeX*sizeY*sizeZ*8 #8 is dat_siz
Headersize=Filesize-Datasize #Datasize - at the bottom/lower part of DICOM file!
print 'Header size', Headersize

# Read the file again and find the part with the data
file_in = DICOMfile
fd = open(file_in,'rb')
position = Headersize # File pointer here
no_of_doubles = VectorSize
fd.seek(position) # Move to position in file

# Straight to numpy data (no buffering) 
numpy_data = np.fromfile(fd, dtype = np.dtype('complex64'), count = no_of_doubles)
#print numpy_data[0].real
#Write data to file
f = open("datafile.txt", "w")
for i in range(VectorSize):
    f.write(str(numpy_data[i].real)+'\n')
f.close()
fileHandle.close() #close binary file

# Plot real FID data
Xaxis = np.arange(0, 1024, 1)
Yaxis = numpy_data.real
pylab.subplot(211)
pylab.plot(Xaxis, Yaxis)
pylab.xlabel('Datapoints')
pylab.ylabel('Signal amplitude')
pylab.title('FID real & FFT real')
pylab.grid(True)
pylab.savefig('simple_plot')

# Plot real FID data
Xaxis = np.arange(0, 1024, 1)
Yaxis = scipy.fftpack.fftshift(scipy.fft(numpy_data)).real
pylab.subplot(212)
pylab.plot(Xaxis, Yaxis)
pylab.xlabel('Frequency')
pylab.ylabel('Signal amplitude')
pylab.grid(True)
pylab.savefig('simple_plot')
pylab.show()
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

import matplotlib as matplt
import numpy.ma as ma
import sys

from astropy.io.votable.tree import VOTableFile, Resource, Table, Field


# reading the data from 2mrs catalogue
ID = []
ra = []
dec = []
mag = []
color = []
z = []

pts = 0
zmax = 0

# cmap ranges:
cmap_start = [0, 2206, 3935, 6028, 7748, 12131, 15146]
cmap_end = [2206, 1729, 6028, 7748, 12131, 15146, 52164]

file = open('2mrs_1175_done.dat', 'r')
for line in file:
	data = line.split()
	if line.startswith("#"):
		continue
	#print data[1], data[2], data[24]
	ID.append(data[0])
	ra.append(data[1])
	dec.append(data[2])
	mag.append(data[5])  #  Ks isophotal magnitude, extinction corrected [XSC: k_m_k20fe]
	
	velocity = int(data[24]) + 300	
	z.append((float(velocity))/10000)

	# giving a color index. Lookup for redshift.cmap for colors
	for color_index in range(0,6):       
		if ( (velocity >= cmap_start[color_index]) and (velocity < cmap_end[color_index])): 
			color.append(color_index)
			continue
		color.append(7) 
	pts+=1

print pts

#creating and populating a VOTable

# Create a new VOTable file...
votable = VOTableFile()

resource = Resource()
votable.resources.append(resource)

table = Table(votable)
resource.tables.append(table)

# Define fields:
table.fields.extend([
        Field(votable, name="ID", datatype="char", arraysize="*"),
        Field(votable, name="ra", datatype="double"),
        Field(votable, name="dec", datatype="double"),
        Field(votable, name="mag", datatype="float", unit="mag"),
        Field(votable, name="color", datatype="int"),
        Field(votable, name="dist", datatype="float")])

# Now, use those field definitions to create the numpy record arrays, with
# the given number of rows
table.create_arrays(pts)

# Now table.array can be filled with data
for i in range(0,pts):
	table.array[i] = (ID[i], ra[i], dec[i], mag[i], color[i], z[i])


# Now write the whole thing to a file.
# Note, we have to use the top-level votable file object
votable.to_xml("new_votable.vot")


#colors = [	(0   	   ,  [1  , 1  , 0.5]),
#			((1582/52164.),  [1  , 0.9  , 0.2]),
#			((2830/52164.),  [1  , 0.75  , 0]),
#			((5040/52164.),  [0.75  , 1  , 0]),
#			((7016/52164.),  [0  , 1  , 0]),
#			((14318/52164.), [0.25  , 1  , 0]),
#			((15970/52164.), [1  , 0.5  , 0]),
#			((30000/52164.), [1  , 0.25  , 0]),
#			(1          ,    [1  , 0  , 0])]	

#[1582, 2830, 5040, 7016, 8480, 14318, 15973]

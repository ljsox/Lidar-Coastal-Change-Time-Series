# GRASS GIS 7.0.0 Windows
# Name: interpolate_RST_method_tuned.py
# Description: A Python script for launch in GRASS 7.0.0 to create vector file and interpolate all files to rasters using RST method
# Author: LESLIE JOHN SOX
# Unity id: ljsox
# NCSU GIS582 Spring 2015
# Date: April 16, 2015
# Import point clouds and interpolate using the rst method.
# tension manually set 
# Reference: E. Hardin et al., GIS-based Analysis of Coastal Lidar Time-Series, Springer Briefs in Computer Science, DOI 10.1007/978-1-4939-1835-5__3

import os, sys, subprocess
from grass.script import core as grass
from grass.script import vector as grass
from grass.script import raster as grass
import grass.script as gscript

# take directory from command line input and change path
path = sys.argv[1]
if len(sys.argv) <1:
    print "You should provide the directory path as a parameter"
    sys.exit(1)
os.chdir( path )
dirs = os.listdir( path )

#make sure MASK is removed before running
# remove mask with r.mask -r 

# print message
gscript.message('Hello GRASS GIS user!')
gscript.message('Creating Mask')
grass.run_command('g.region', raster='DEM20m', res='5')

# Mask to smallest area of Atlantic Beach - Fort Macon horizontal section 2010_USACE_SE_raw
grass.run_command('r.in.xyz', input='2010_USACE_SE_raw.txt', output='2010_USACE_SE_raw_n_5m', separator=',', skip=1, method='n', overwrite=True)
grass.run_command('r.mapcalc', expression='2010_USACE_SE_raw_mask=if(2010_USACE_SE_raw_n_5m == 0, null(), 1 )', overwrite=True)

# Limit raster operations with the mask just created, 2m resolution
grass.run_command('g.region', res='0.5')
grass.run_command('r.mask', raster='2010_USACE_SE_raw_mask', overwrite=True)  

# print message
gscript.message('MASK is now set')

# print message
gscript.message('Now importing points. This will take some time.')

# Find and set region from specified point cloud 
# 2010_USACE_SE_raw.txt has the smallest map area
# Flags: -z Create 3D vector map, -t Do not create table in points mode
grass.run_command('v.in.ascii', flags='t', input='2010_USACE_SE_raw.txt', output='temp', separator=',', skip=1, z=3, overwrite=True) 
	
# Region set from points and resolution set to 1m
grass.run_command('g.region', flags='pa', vect='temp', res='1') 

for f in range(len(dirs)):
	#remove .txt from file name and create new raster name
	import re
	raster = re.sub('.txt', '', dirs[f]) 
	vect = 'R_'+ raster 
	rast = 'r_'+str(raster)+'_1mrst_t800'
	
	# print message
	gscript.message('Now interpolating raster map.')
	print str(raster)
	
	# Import Lidar files 
	# Flags: -z Create 3D vector map, -t Do not create table in points mode
	grass.run_command( 'v.in.ascii', flags='tr', input=dirs[f], output=vect, separator=',', skip=1, z=3, overwrite=True)
	
	# Interpolate using RST with tension fixed at 800
	# tension=1500 smooth 1.0 
	# Flags: -t Use scale dependent tension
	grass.run_command( 'v.surf.rst', flags='t', input=vect, elev='elev_'+ rast, tension=800, smooth=1.0, npmin=150, segmax=25, dmin=2, overwrite=True)
	# create maps (slope and aspect)
	grass.run_command( 'r.slope.aspect', elev='elev_'+ rast, slope='slope_'+ rast, aspect='aspect_'+ rast, overwrite=True)

# print message
gscript.message('All ASCII lidar text files in the given directory have now been interpolated.')

 



# GRASS GIS 7.0.0 Windows
# Name: create_survey_mask.py
# Description: A Python script for launch in GRASS 7.0.0 to create and apply survey mask file
# Author: LESLIE JOHN SOX
# Unity id: ljsox
# NCSU GIS582 Spring 2015
# Date: April 11, 2015
# Reference: E. Hardin et al., GIS-based Analysis of Coastal Lidar Time-Series, Springer Briefs in Computer Science, DOI 10.1007/978-1-4939-1835-5__3

#Create a masked survey area
import os, sys
from grass.script import core as grass
import grass.script as gscript

#import path to lidar text files 
path = sys.argv[1]

if len(sys.argv) <1:
    print "You should provide the directory path as a parameter"
    sys.exit(1)

#now change directory
os.chdir( path )

# print message
gscript.message('Creating Mask Area')

# Mask to smallest area of Atlantic Beach - Fort Macon horizontal section 2010_USACE_SE_raw
grass.run_command('r.in.xyz', input='2010_USACE_SE_raw.txt', output='2010_USACE_SE_raw_n_5m', separator=',', skip=1, method='n', overwrite=True)
grass.run_command('r.mapcalc', expression='2010_USACE_SE_raw_mask=if(2010_USACE_SE_raw_n_5m == 0, null(), 1 )', overwrite=True)

# Limit raster operations with the mask just created
grass.run_command('g.region', raster='2010_USACE_SE_raw_mask', res='5')
grass.run_command('r.colors', map='2010_USACE_SE_raw_mask', color='blues')    
grass.run_command('r.mask', raster='2010_USACE_SE_raw_mask', overwrite=True)  

#remove mask with r.mask -r 
# print message
gscript.message('MASK is now set')
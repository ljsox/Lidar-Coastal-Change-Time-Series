# GRASS GIS 7.0.0 Windows
# Name: eliminate_water_surface_features.py
# Description: A Python script for launch in GRASS 7.0.0 to eliminate water features less than 0.36
# Iterates through a folder location passed via sys.argv based on given keywords
# Unity id: ljsox
# NCSU GIS582 Spring 2015
# Date: April 15, 2015
# Reference: E. Hardin et al., GIS-based Analysis of Coastal Lidar Time-Series, Springer Briefs in Computer Science, DOI 10.1007/978-1-4939-1835-5__3

import os, sys, subprocess
from grass.script import list_strings, mapcalc
from grass.script.core import run_command
import grass.script as gscript
from grass.script import vector as grass

# take directory from command line input and change path
path = sys.argv[1]
if len(sys.argv) <1:
    print "You should provide the directory path as a parameter"
    sys.exit(1)
# now change the path
os.chdir( path )

# print message
gscript.message('Hello GRASS user!')

# *** use GRASS list_strings to find specified rasters using a regular expression, change as file names change
rasters = list_strings(type='raster', pattern='^elev_r_.*_2mrst_t1500$', flag='r')

for raster in rasters:
	short = raster.split('@')[0]
	
	# print message
	gscript.message('We are now using map calculator to eliminate water features.')
	
	#expression using mapcalc to save only elevations above .36 and rename with '_higher_036'
	mapcalc("{short}_higher_036 = if({rast} > 0.36, 1, null())".format(rast=raster, short=short), overwrite=True)
	newmap = short + '_higher_036'
	
	# create a vector for a report
	run_command('r.to.vect', input=newmap, output=newmap, type='area', overwrite=True) 
	
	# Find the unique category of the largest area
	# run_command('v.report', map=newmap, option='area') #< remove comment to see on screen report
	mask = short + '_mask'
	masked = short + '_masked'
	# Extract the features and covert back to a raster then use mapcalc to multiply by float and create new map name
	run_command('v.extract', input=newmap, output=mask, cats='1', overwrite=True)
	run_command('v.to.rast', input=mask, output=mask, use='val', value='1' , overwrite=True)
	
	# use the mask to finally eliminate the cells below .36, create a new map named map_masked
	# the new file name has _masked added to the end
	mapcalc("{short}_masked = ({short} * float({rast}))".format(rast=mask, short=short), overwrite=True)
	
	# print message and file names
	gscript.message('The new files created are:')
	newmap=newmap.split('@')[0]
	mask=mask.split('@')[0]
		
	print newmap
	print mask
	print masked
		
	# print message
	gscript.message('All processing is now completed. The new maps have _masked added to the file names.')



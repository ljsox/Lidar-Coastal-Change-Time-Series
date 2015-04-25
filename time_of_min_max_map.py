# GRASS GIS 7.0.0 Windows
# Name: eliminate_water_surface_features.py
# Unity id: ljsox
# NCSU GIS582 Spring 2015
# Date: April 17, 2015
# Purpose: Compute time-of-minimum and time-of-maximum maps, and apply categories.
# Reference: E. Hardin et al., GIS-based Analysis of Coastal Lidar Time-Series, Springer Briefs in Computer Science, DOI 10.1007/978-1-4939-1835-5__3

import tempfile
import os
import sys
from grass.script.core import run_command
from grass.script import core as grass
import grass.script as gscript


# take directory from command line input and change path
path = sys.argv[1]
if len(sys.argv) <1:
    print "You should provide the directory path as a parameter"
    sys.exit(1)
# now change the path
os.chdir( path )

# print message
gscript.message('Hello GRASS user!')
gscript.message('Now running r.series and r.category to compute time-of-minimum and time-of-maximum maps.')

# Region set from points and resolution set to 2
grass.run_command('g.region', rast='2010_USACE_SE_raw_mask', res='2')

fname = tempfile.mkstemp()[1]
f = open( fname, 'w' )
rules = '''0:2001
1:2004
2:2010
3:2011'''
f.write( rules )
f.close()
mlist = 'elev_r_2001_NC_PhaseI_raw_05mrst_t800_masked,elev_r_2004_PreIvan_raw_05mrst_t800_masked,elev_r_2010_USACE_SE_raw_05mrst_t800_masked,elev_r_2011_post_irene_NC_raw_05mrst_t800_masked'
run_command( 'r.series', flags='nz', input=mlist, output='FM_min_time', method='min_raster', overwrite=True)
run_command( 'r.series', flags='nz', input=mlist, output='FM_max_time', method='max_raster', overwrite=True)
run_command( 'r.category', map='FM_min_time', separator=':', rules=fname)
run_command( 'r.category', map='FM_max_time', separator=':', rules=fname)
gscript.message('Computations Completed!')
#os.remove( fname )



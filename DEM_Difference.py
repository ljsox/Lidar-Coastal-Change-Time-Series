# GRASS GIS 7.0.0 Windows
# Name: DEM_Difference.py
# Unity id: ljsox
# NCSU GIS582 Spring 2015
# Date: April 17, 2015
# Purpose: DEMs of Difference (DoD) map
# Reference: E. Hardin et al., GIS-based Analysis of Coastal Lidar Time-Series, Springer Briefs in Computer Science, DOI 10.1007/978-1-4939-1835-5__3
# Purpose: Compute a DEM of Difference (DoD).
import os, sys, subprocess
from grass.script.core import run_command
from grass.script import core as grass
from grass.script import mapcalc
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
gscript.message('Now computing a DEMs of Difference maps.')
grass.run_command('r.mapcalc', expression='FM_total_change=elev_r_2011_post_irene_NC_raw_05mrst_t800-elev_r_2001_NC_PhaseI_raw_05mrst_t800', overwrite=True)
# Set color ramp
grass.run_command( 'r.colors', map='FM_total_change', rules='color_elevation_diff.txt' )
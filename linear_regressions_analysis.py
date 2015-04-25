# GRASS GIS 7.0.0 Windows
# Name: eliminate_water_surface_features.py
# Description: compute Null maps for use when elevation snapshots are not evenly spaced in time
# Unity id: ljsox
# NCSU GIS582 Spring 2015
# Date: April 16, 2015
# Reference: E. Hardin et al., GIS-based Analysis of Coastal Lidar Time-Series, Springer Briefs in Computer Science, DOI 10.1007/978-1-4939-1835-5__3

import os, sys
from grass.script.core import run_command
from grass.script import core as grass
import grass.script as gscript
from grass.script import mapcalc,list_strings

# take directory from command line input and change path
path = sys.argv[1]
if len(sys.argv) <1:
    print "You should provide the directory path as a parameter"
    sys.exit(1)
# now change the path
os.chdir( path )

# print message
gscript.message('Hello GRASS user!')
gscript.message('Now running r.series.')
gscript.message('The following methods are being computed:')
gscript.message('slope: linear regression slope')
gscript.message('offset: linear regression offset')
gscript.message('detcoeff: linear regression coefficient of determination')
gscript.message('minimum: lowest value')
gscript.message('maximum: highest value')

# Region set from points and resolution set to 2
grass.run_command('g.region', rast='2010_USACE_SE_raw_mask', res='2') 

#expression using mapcalc to create Null maps
mapcalc("Null=null()", overwrite=True)
#Create manual file name list for r.series and insert Null maps from previous because r.series assumes input maps are at even time intervals 
mlist = 'elev_r_2001_NC_PhaseI_raw_1mrst_t1500_masked,Null,Null,elev_r_2004_PreIvan_raw_1mrst_t1500_masked,Null,Null,Null,Null,Null,elev_r_2010_USACE_SE_raw_1mrst_t1500_masked,elev_r_2011_post_irene_NC_raw_1mrst_t1500_masked'
print 'Processing files done.'
run_command('r.series', input=mlist, output='FM_r_slope,FM_core,FM_envel,FM_r_offset,FM_r_coeff', method='slope,minimum,maximum,offset,detcoeff', overwrite=True )
grass.run_command( 'r.colors', map='FM_r_slope',
rules='C:\Users\LESLIEJOHN\Documents\GitHub\coastal-erosion-from-lidar-time-series\Color_Tables\color_regrslope.txt' )
grass.run_command( 'r.colors', map='FM_r_coeff',
rules='C:\Users\LESLIEJOHN\Documents\GitHub\coastal-erosion-from-lidar-time-series\Color_Tables\color_regrcoefdet.txt' )









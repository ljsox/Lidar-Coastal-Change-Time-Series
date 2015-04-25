# GRASS GIS 7.0.0
# Name: GetMeanCellStats.py
# Description: A Python script for launch in GRASS 7.0.0 to get mean cell stats at 1,2,5,10m resolution and generate a report for ASCII LiDAR text files
# Author: LESLIE JOHN SOX
# Unity id: ljsox
# NCSU GIS582 Spring 2015
# Date: April 8, 2015
# Reference: E. Hardin et al., GIS-based Analysis of Coastal Lidar Time-Series, Springer Briefs in Computer Science, DOI 10.1007/978-1-4939-1835-5__3

#Get mean cell statistics
import os, sys
from grass.script import core as grass
import grass.script as gscript

# take directory from command line input and change path
path = sys.argv[1]
if len(sys.argv) <1:
    print "You should provide the directory path as a parameter"
    sys.exit(1)
# now change the path
os.chdir( path )
grass.run_command('g.region', rast='DEM20m')
files = ['2001_NC_PhaseI_raw.txt', '2004_PreIvan_raw.txt', '2010_USACE_SE_raw.txt', '2011_post_irene_NC_raw.txt'] 
resolutions=[1, 2, 5, 10]
#resolution .5 was too large for memory
report='date\tres\tn\trange\n'
for f in files:
	report += f + '\n'
	for res in resolutions:
		report += '\t' + str(res) + '\t'
		#set the resolution
		grass.run_command('g.region', res=res)
		#Get the per cell count
		grass.run_command('r.in.xyz', input=f, output='FM_stats_n', separator=',', skip=1, method='n', overwrite=True)
		grass.run_command('r.null', map='FM_stats_n', setnull=0)
		#Get the mean per cell count
		stats = grass.parse_command('r.univar', flags='eg', map='FM_stats_n')
		report += str(stats['mean']) + '\t'
		#Get the per cell range
		grass.run_command('r.in.xyz', input=f, output='FM_stats_range', separator=',', skip=1, method='range', overwrite=True)
		grass.run_command('r.mapcalc', expression='FM_stats_range_c=if(isnull(FM_stats_n), null(), FM_stats_range)', overwrite=True)
		#Get the mean per cell range
		stats = grass.parse_command('r.univar', flags='eg', map='FM_stats_range_c')
		report += str(stats['mean']) + '\n'
print(report)
# GRASS GIS 7.0.0
# Name: limit_with_survey_mask.py
# Description: A Python script for launch in GRASS 7.0.0 to set a survey mask by a defined raster file
# Author: LESLIE JOHN SOX
# Unity id: ljsox
# NCSU GIS582 Spring 2015
# Date: April 8, 2015
# Reference: E. Hardin et al., GIS-based Analysis of Coastal Lidar Time-Series, Springer Briefs in Computer Science, DOI 10.1007/978-1-4939-1835-5__3

# Limit raster operations with a mask to 1m resolution
from grass.script import core as grass
grass.run_command('g.region', res='2')
grass.run_command('r.mask', raster='Lidar_DEM20') 
#!Raster operation will continue to be limited to the mask area until the mask is removed by running r.mask with the -r flag
#r.mask -r Lidar_DEM20

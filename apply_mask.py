# GRASS GIS 7.0.0 Windows
# Name: create_survey_mask.py
# Description: A Python script for launch in GRASS 7.0.0 to apply mask raster 2010_USACE_SE_raw_mask
# Author: LESLIE JOHN SOX
# Unity id: ljsox
# NCSU GIS582 Spring 2015
# Date: April 12, 2015

#Create a masked survey area
# Limit raster operations with a mask
grass.run_command('g.region', res='.5')
grass.run_command('r.mask', raster='2010_USACE_SE_raw_mask', overwrite=True)  
#! /opt/rocks/bin/python
#
# Start one instance of Google Earth on each display
#
# @Copyright@
# @Copyright@
#
# $Log: start-google-earth.py,v $
# Revision 1.1  2010/10/07 19:47:12  mjk
# - added support for Google's Liquid Galaxy
# - remove sage and some of the deps
#


import os
import string

displays = []

for file in os.listdir('/opt/google-earth'):
	tokens = file.split(':')
	if len(tokens) == 2:
		if tokens[0] == 'drivers.ini':
			displays.append(tokens[1])

for display in displays:
	dir = 'google-earth:%s' % display
	
	os.system('rm -rf %s' % dir)
	os.system('mkdir %s' % dir)
	os.system('cp -r /opt/google-earth/* %s' % dir)
	os.system('rm %s/drivers.ini' % dir)
	os.system('cp %s/drivers.ini:%s %s/drivers.ini' % (dir, display, dir))

	os.chdir(dir)
	os.system('DISPLAY=:%s ./googleearth --fullscreen &' % display)
	os.chdir('..')



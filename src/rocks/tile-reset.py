#!/opt/rocks/bin/python
#
# @Copyright@
# @Copyright@
#
# $Log: tile-reset.py,v $
# Revision 1.3  2009/06/03 01:23:23  mjk
# - Now using the idea of modes for the wall (e.g. simple, sage, cglx)
# - Simple (chromium) and Sage modes work
# - Requires root to do a "rocks sync viz mode=??" to switch
# - "rocks enable/disable hidebezels" is chromium specific
#   The command line needs to change to reflect this fact
# - Tile-banner tell you the resolution and mode node
# - Sage works (surprised)
# - Removed autoselect of video mode on first boot, started to crash nodes
#
# Revision 1.2  2009/05/12 18:36:29  mjk
# *** empty log message ***
#
# Revision 1.1  2009/05/12 00:26:54  mjk
# *** empty log message ***
#

import sys
import os
import getopt
import tempfile


def NVidiaXConfig(flags):
	os.system('/opt/viz/bin/nvidia-xconfig %s > /dev/null' % flags)


def SetResolutions(resolutions):
	xconf = '/etc/X11/xorg.conf'

	os.system('cp %s %s.bak' % (xconf, xconf))

	fin  = open(xconf, 'r')
	fout = open('%s.bak' % xconf, 'w')

	# Set the video resolution for single display systems (Mode) and
	# TwinView systems (MetaModes).  To do this we cound Screen sections
	# and make sure we use the resolution of the correct tile.  Even
	# in TwinView mode we can have two screen sections for the case
	# of 4 monitors per node (Xinerama + TwinView)

	meta = False
	display = -1
	for line in fin.readlines():
		if line.find('"DPMS"') != -1:
			line = '\tOption\t"DPMS"\t"False"\n'
		elif line.find('Section "Screen"') != -1:
			display += 1
		elif line.find('Option         "MetaModes"') != -1:
			line = '    Option         "MetaModes" "%s,%s"\n' % \
				(resolutions[display*2], 
				resolutions[display*2+1])
			meta = True
		elif not meta and line.find('SubSection     "Display"') != -1:
			try:
				line += '\tModes       "%s"\n' % \
					resolutions[display]
			except:
				pass

		fout.write(line)

	fin.close()
	fout.close()

	os.system('mv %s.bak %s' % (xconf, xconf))



mode = None
orientation = None

try:
	opts, args = getopt.getopt(sys.argv[1:], 'm:o:')
except getopt.GetoptError, msg:
	sys.stderr.write("error - %s\n" % msg)
	sys.exit(1)
for c in opts:
	if c[0] == '-m':
		mode = c[1]
	if c[0] == '-o':
		orientation = c[1]

if mode == 'twinview':
	NVidiaXConfig('--twinview --twinview-orientation=%s -a' % orientation)
else:
	NVidiaXConfig('--separate-x-screens --no-twinview -a ')

SetResolutions(args)



#!/opt/rocks/bin/python
#
# @Copyright@
# @Copyright@
#
# $Log: tile-reset.py,v $
# Revision 1.4  2009/06/10 02:56:02  mjk
# - can enable/disable tile banner per display
# - nuke sample xml files
# - added rocks/tile.py for tile oriented commands
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



xconf = '/etc/X11/xorg.conf'
mode = 'simple'
orientation = None

try:
	opts, args = getopt.getopt(sys.argv[1:], 'mo:')
except getopt.GetoptError, msg:
	sys.stderr.write("error - %s\n" % msg)
	sys.exit(1)
for c in opts:
	if c[0] == '-m':
		mode = 'meta'
	if c[0] == '-o':
		orientation = c[1]


# Modes
#
#   simple - one xserver per tile
#   *      - twinview in pairs, then xinerama twinview tiles
#
# Use the nvidia-xconfig tool to create the xorg.conf file.  This
# will get almost everything correct.  See next section

flags = '-a '

# Turn on Xinerama for grouping two (or more) Twinview Screens

if len(args) <= 2 or mode == 'simple':
	flags += '--no-xinerama '
else:
	flags += '--xinerama '

# Simple mode is one server per tile, anything else means TwinView

if mode == 'simple':
	flags += '--separate-x-screens --no-twinview'
else:
	flags += '--twinview --twinview-orientation=%s' % orientation

os.unlink(xconf)
os.system('/opt/viz/bin/nvidia-xconfig %s > /dev/null' % flags)


# The xorg.conf is almost correct but we need to cleanup the following
#
# Disable DPMS
#
# Single Tile
#	Set the Modes to the correct resolution
#
# Twinview Tiles
#	Set the MetaModes to the correct resolution
#	Do not generate a Modes line in the Display section
#
# Xinerama
#	By default Xinerama has a "RightOf" layout replace this with
#	the same orientation used in Twinview (cannot do squares)


resolutions = args

os.system('cp %s %s.bak' % (xconf, xconf))

fin  = open(xconf, 'r')
fout = open('%s.bak' % xconf, 'w')
display = -1
meta = False
for line in fin.readlines():
	if line.find('"DPMS"') != -1:
		line = '    Option        "DPMS"\t"False"\n'
	elif orientation and line.find('RightOf') != -1:
		line = line.replace('RightOf', orientation)
	elif line.find('Section "Screen"') != -1:
		display += 1
	elif line.find('Option         "MetaModes"') != -1:
		meta = True
		line = '    Option         "MetaModes" "%s,%s"\n' % \
			(resolutions[display*2],
			resolutions[display*2+1])
	elif not meta and line.find('SubSection     "Display"') != -1:
		line += '        Modes       "%s"\n' % resolutions[display]
	elif line.find('Section "Device"') != -1:
		line += '    Option         "UseDisplayDevice" "DFP, CRT"\n'
	fout.write(line)
fin.close()
fout.close()

os.system('mv %s.bak %s' % (xconf, xconf))



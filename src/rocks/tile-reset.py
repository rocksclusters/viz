#!/opt/rocks/bin/python
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.6 (Emerald Boa)
# 		         version 6.1 (Emerald Boa)
# 
# Copyright (c) 2000 - 2013 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#
# $Log: tile-reset.py,v $
# Revision 1.8  2012/11/27 00:49:33  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.7  2012/05/06 05:49:44  phil
# Copyright Storm for Mamba
#
# Revision 1.6  2011/07/23 02:31:38  phil
# Viper Copyright
#
# Revision 1.5  2010/09/07 23:53:28  bruno
# star power for gb
#
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



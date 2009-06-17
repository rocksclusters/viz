# $Id: plugin_simple.py,v 1.2 2009/06/17 18:07:04 mjk Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 5.2 (Chimichanga)
# 
# Copyright (c) 2000 - 2009 The Regents of the University of California.
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
# $Log: plugin_simple.py,v $
# Revision 1.2  2009/06/17 18:07:04  mjk
# - viz commands gone
# - tile commands now
#
# Revision 1.1  2009/06/09 23:51:46  mjk
# *** empty log message ***
#
# Revision 1.1  2009/06/06 00:56:30  mjk
# *** empty log message ***
#


import os
import rocks.commands.sync.tile


class Plugin(rocks.commands.sync.tile.Plugin):

	def provides(self):
		return 'simple'

	def configureHost(self, owner, host):
		tiles = self.getHostTiles(host)

		flags =  '--force-generate'
		flags += ' --no-xinerama --separate-x-screens --no-twinview'
		if len(tiles) > 1:
			flags += ' -a'
		else:
			flags += ' --only-one-x-screen '

		xconf = '%s-simple-%s' % (self.getXConfPath(), host)
		os.system('ssh -x %s "/opt/viz/bin/nvidia-xconfig %s"' %
		      	(host, flags))
		self.getFileFromHost(host, self.getXConfPath(), xconf)

		list = []
		fin  = open(xconf, 'r')
		display = -1
		for line in fin.readlines():
			if line.find('Option         "DPMS"') != -1:
				line = '\tOption\t"DPMS"\t"False"\n'
			elif line.find('Section "Screen"') != -1:
				display += 1
			elif line.find('SubSection     "Display"') != -1:
				line += '\tModes\t"%sx%s"\n' % \
					(tiles[display]['xres'],
					 tiles[display]['yres'])
			elif line.find('Section "Device"') != -1:
				line += '\tOption\t"UseDisplayDevice" "DFP, CRT"\n'
			list.append(line)
		fin.close()
		fout = open(xconf, 'w')
		for line in list:
			fout.write(line)
		fout.close()

		self.sendXConf(host, 'simple')

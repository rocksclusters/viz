# $Id: __init__.py,v 1.13 2009/05/01 19:07:31 mjk Exp $
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
# $Log: __init__.py,v $
# Revision 1.13  2009/05/01 19:07:31  mjk
# chimi con queso
#
# Revision 1.12  2008/10/18 00:56:20  mjk
# copyright 5.1
#
# Revision 1.11  2008/05/31 02:57:37  mjk
# - SAGE is back and works (mostly)
# - DMX building from source (in progress)
# - Updated nvidia driver
#
# Revision 1.10  2008/03/06 23:42:02  mjk
# copyright storm on
#
# Revision 1.9  2007/12/19 22:00:12  mjk
# fix bug of mode not being in the config file
# default to 800x600 and then fix according to the database.
#
# Revision 1.8  2007/11/01 17:01:59  mjk
# full path for nvidia-xconfig
#
# Revision 1.7  2007/09/19 13:28:58  mjk
# Swiss Viss
#
# Revision 1.6  2007/09/19 11:35:08  mjk
# more swiss changes
#
# Revision 1.5  2007/08/14 22:51:18  mjk
# SDSU wall is alive
#
# Revision 1.4  2007/07/24 02:11:35  mjk
# - sage2 starting to work
#
# Revision 1.3  2007/07/06 18:38:10  mjk
# 4.3 Command Line cleanup
#
# Revision 1.2  2007/06/23 04:04:05  mjk
# mars hill copyright
#
# Revision 1.1  2007/05/10 20:37:02  mjk
# - massive rocks-command changes
# -- list host is standardized
# -- usage simpler
# -- help is the docstring
# -- host groups and select statements
# - added viz commands
#

import os
import sys
import string
import re
import tempfile
import rocks.commands

class Command(rocks.commands.list.host.command):
	"""
	Lists the X11 Xorg configuration for the given list of hosts.  If no
	host list is provided the configuration for the current machine is
	listed.
	
	<arg name='host' type='string' repeat='1'>
	Zero or more host names.
	</arg>

	<example cmd='list host xconfig'>
	Lists the X11 configuration for the local host.
	</example>
	
	<example cmd='list host xconfig tile-0-0 tile-0-1'>
	Lists the X11 configuration for tile-0-0 and tile-0-1.
	</example>
	"""

	def outputXConfig(self, host):
	
		self.db.execute("""select v.hcoord, v.vcoord, 
			v.lhborder, v.rhborder, v.tvborder, v.bvborder, 
			v.hres, v.vres 
			from nodes n, videowall v 
			where n.name='%s' and n.id=v.node and v.cardid=1 
			order by v.vcoord asc, v.hcoord asc"""
			% host)

		vals = self.db.fetchall()
		
		if not vals:
		
			# We could not fine any tile information in the
			# database.  This means the command was run for
			# the frontend (common case), an unconfigured tile
			# node, or some other appliance type.  For all
			# these cases we just run the xorg.conf on the
			# local disk through nvidia-xconfig.

			tmp = tempfile.mktemp()
			os.system('/opt/viz/bin/nvidia-xconfig '
				'-o %s > /dev/null' % tmp)
			file = open(tmp, 'r')
			for line in file.readlines():
				self.addOutput(host, line[:-1])
			file.close()
			os.unlink(tmp)
		else:

			# Found the host in the tile layout database, so we
			# rewrite the xorg.conf using the current one on the
			# local host as a template.  If multiple entries are
			# found for a given tile we know we are in 
			# TwinView mode.
		
			try:
				hres = int(vals[0][6])
				vres = int(vals[0][7])
			except IndexError:
				pass

			tmp = tempfile.mktemp()
		
			twinview = ''	
			if len(vals) == 2:
				twinview = '--twinview'
				if vals[0][0] != vals[1][0]:	# RightOf
					hoffset = hres
					hbezels = int(vals[0][3] + vals[0][2])
					voffset = 0
					vbezels = 0
				else:				# Below
					hoffset = 0
					hbezels = 0
					voffset = vres
					vbezels = int(vals[0][5] + vals[1][4])

				modes = '"%dx%d+0+0,%dx%d+%d+%d' % \
					(hres, vres, hres, vres, 
					hoffset, voffset)

				modes += '; %dx%d+0+0,%dx%d+%d+%d"' % \
					(hres, vres, hres, vres, 
					hoffset + hbezels, 
					voffset + vbezels)


			os.system('/opt/viz/bin/nvidia-xconfig '
				'--mode=800x600 '	
				'%s -c /dev/null -o %s'
				'>/dev/null 2>&1' % (twinview, tmp))

			file = open(tmp, 'r')
			lines = file.readlines()
			file.close()
			os.unlink(tmp)

			re1 = '(^[ \t]+option[ \t]+"metamodes"[ \t]+)'
			re3 = '(^[ \t]+modes[ \t]+)'
			
			for line in lines:

				m1 = re.search(re1, line.lower())
				m3 = re.search(re3, line.lower())

				if m1 and m1.groups():
					self.addOutput(host, '%s%s' %
						(line[0:len(m1.groups()[0])],
						modes))
					continue

				if m3 and m3.groups():
					self.addOutput(host,
						'\tModes\t"%dx%d"' %
						(hres, vres))
					continue

				self.addOutput(host, line[:-1])
				
	def run(self, params, args):
		if not len(args):
			hosts = [ self.db.getHostname() ]
		else:
			hosts = self.getHostnames(args)


		self.beginOutput()
		for host in hosts:
			try:
				self.outputXConfig(host)
			except TypeError:
				pass
		self.endOutput(padChar='')
	

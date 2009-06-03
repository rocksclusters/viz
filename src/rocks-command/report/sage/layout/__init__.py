# $Id: __init__.py,v 1.5 2009/06/03 01:23:23 mjk Exp $
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
# Revision 1.5  2009/06/03 01:23:23  mjk
# - Now using the idea of modes for the wall (e.g. simple, sage, cglx)
# - Simple (chromium) and Sage modes work
# - Requires root to do a "rocks sync viz mode=??" to switch
# - "rocks enable/disable hidebezels" is chromium specific
#   The command line needs to change to reflect this fact
# - Tile-banner tell you the resolution and mode node
# - Sage works (surprised)
# - Removed autoselect of video mode on first boot, started to crash nodes
#
# Revision 1.4  2009/05/01 19:07:31  mjk
# chimi con queso
#
# Revision 1.3  2008/10/18 00:56:21  mjk
# copyright 5.1
#
# Revision 1.2  2008/07/03 01:14:13  mjk
# - fix path to xrandr
# - call xrandr twice (current mode, desired mode)
#   otherwise it fails to set the desired mode
# - sage respects the hidebezels mode
#
# Revision 1.1  2008/05/31 02:57:37  mjk
# - SAGE is back and works (mostly)
# - DMX building from source (in progress)
# - Updated nvidia driver
#

import rocks.util
import rocks.commands

class Command(rocks.commands.report.command):
	"""
	Reports the SAGE tile layout configuration file.
	
	<example cmd='report sage layout'>
	</example>
	"""

	def run(self, params, args):

		layout = eval(self.command('report.viz.wall'))

		# Sage computes Mullions in inches not pixels

		hosts = {}
		ppi = 100
		maxX = 0
		maxY = 0
		for tile in layout:

			if tile['name'] not in hosts:
				hosts[tile['name']] = []
			hosts[tile['name']].append(tile)

			if tile['x'] > maxX:
				maxX = tile['x']
			if tile['y'] > maxY:
				maxY = tile['y']

		# Use the values from the last tile we saw for the
		# SAGE global settings.  Future versions of SAGE will
		# allow these to be display dependent.
		
		self.addText('TileDisplay\n')
		self.addText('\tDimensions %d %d\n' % (maxX+1, maxY+1))
		self.addText('\tMullions %.3f %.3f %.3f %.3f\n' %
			(float(tile['topborder'])   / ppi,
			float(tile['bottomborder']) / ppi, 
			float(tile['leftborder'])   / ppi,
			float(tile['rightborder']   / ppi)))
		self.addText('\tResolution %d %d\n' % 
			(tile['xres'], tile['yres']))
		self.addText('\tPPI %d\n' % ppi)
		self.addText('\tMachines %d\n' % len(hosts))
		
		list = hosts.keys()
		list.sort()
		for host in list:
			self.addText('\nDisplayNode\n')
			self.addText('\tName %s\n' % host)
			
			self.db.execute("""select net.ip from 
				nodes n,networks net where
				n.name="%s" and net.node=n.id and
				net.device="eth0" """ % host)
				
			for ip, in self.db.fetchall():
				if ip:
					self.addText('\tIP %s\n' % ip)
			self.addText('\tMonitors %d ' % len(hosts[host]))
			for tile in hosts[host]:
				self.addText('(%d,%d) ' %
					(tile['x'], tile['y']))
			self.addText('\n')

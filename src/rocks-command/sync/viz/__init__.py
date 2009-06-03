# $Id: __init__.py,v 1.13 2009/06/03 01:23:23 mjk Exp $
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
# Revision 1.13  2009/06/03 01:23:23  mjk
# - Now using the idea of modes for the wall (e.g. simple, sage, cglx)
# - Simple (chromium) and Sage modes work
# - Requires root to do a "rocks sync viz mode=??" to switch
# - "rocks enable/disable hidebezels" is chromium specific
#   The command line needs to change to reflect this fact
# - Tile-banner tell you the resolution and mode node
# - Sage works (surprised)
# - Removed autoselect of video mode on first boot, started to crash nodes
#
# Revision 1.12  2009/05/29 19:35:41  mjk
# *** empty log message ***
#
# Revision 1.11  2009/05/17 13:41:53  mjk
# checkpoint before zurich
#
# Revision 1.10  2009/05/09 23:04:08  mjk
# - tile-banner use rand seed to sync the logo on multi-head nodes
# - Xclients is python, and disables screensaver (again)
# - xorg.conf on tiles turns off DPMS
# - tiles come up in a completely probed mode (resolution not set)
# - all else is just broken and this is a check point
#
# Revision 1.9  2009/05/01 19:07:32  mjk
# chimi con queso
#
# Revision 1.8  2008/10/18 00:56:21  mjk
# copyright 5.1
#
# Revision 1.7  2008/03/06 23:42:02  mjk
# copyright storm on
#
# Revision 1.6  2008/01/14 22:03:47  bruno
# tweaks for V
#
# Revision 1.5  2007/09/19 11:35:08  mjk
# more swiss changes
#
# Revision 1.4  2007/08/10 23:38:56  mjk
# *** empty log message ***
#
# Revision 1.3  2007/07/06 18:38:10  mjk
# 4.3 Command Line cleanup
#
# Revision 1.2  2007/06/23 04:04:06  mjk
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
import string
import rocks.commands

class Command(rocks.commands.Command):
	"""
	Generates a new X11 configuration for each tile node on the frontend
	and then copies the files to the nodes.  After the copy all tile
	nodes are reset (not re-installed) to restart X11.  This should be
	used push out changes when the layout of the wall changes.
	
	<example cmd="sync viz">
	</example>
	"""

	def syncUserMode(self):
		"""
		Manual mode applies to all Tile appliances, not just the
		Tiles defined in the database.  Look for any 
		/etc/X11/xorg.conf.HOSTNAME files and use these rather than the
		computed configuration.  This allows the user to override the 
		Rocks defaults.
		"""
		self.db.execute("""select n.name from nodes n, memberships m 
			where n.membership=m.id and m.name='Tile'""")
		for (host, ) in self.db.fetchall():
			xconf = os.path.join(os.sep, 'etc', 'X11', 
				'xorg.conf.%s' % host)
			if os.path.isfile(xconf):
				self.addText('sync %s (%s)\n' % (host, xconf))
				os.system('scp %s %s:%s' % (xconf, host,
					os.path.join(os.sep, 
					'etc', 'X11', 'xorg.conf')))

	def syncSageMode(self, host, tiles):
		if len(tiles) == 1:
			return self.syncSimpleMode(host, tiles)

		displays = []
		x = []
		y = []
		for tile in tiles:
			displays.append((tile['display'], 
				tile['xres'], tile['yres']))
			x.append(tile['x'])
			y.append(tile['y'])
		displays.sort()

		if x[0] > x[1]:
			orientation = 'LeftOf'
		elif x[0] < x[1]:
			orientation  = 'RightOf'
		elif y[0] > y[1]:
			orientation = 'Above'
		elif y[0] < y[1]:
			orientation = 'Below'
		else:
			return # error - do not configure the node

		resolutions = ''
		for e in displays:
			resolutions += '%dx%d ' % (e[1], e[2])
		resolutions = resolutions.strip()

		self.addText('sync %s (%s %s)\n' % 
			(host, orientation, resolutions))
		self.command('run.host', [ host, 'x11=false',
			'/opt/viz/sbin/tile-reset -mtwinview -o%s %s' % 
			(orientation, resolutions) ])


	def syncSimpleMode(self, host, tiles):
		displays = []
		for tile in tiles:
			displays.append((tile['display'], 
				tile['xres'], tile['yres']))
		displays.sort()
		resolutions = ''
		for e in displays:
			resolutions += '%dx%d ' % (e[1], e[2])
		resolutions = resolutions.strip()
		self.addText('sync %s (%s)\n' % (host, resolutions))
		self.command('run.host', [ host, 'x11=false',
			'/opt/viz/sbin/tile-reset -mstandard %s' % resolutions
			])


	def run(self, params, args):

		(mode, ) = self.fillParams([('mode', 'simple')])

		if mode not in [ 'user', 'simple', 'sage', 'cglx' ]:
			self.abort('invalid mode "%s"' % mode)

		if mode == 'user':
			self.syncUserMode()
		else:

			# Build a dictionary of hostnames with the value
			# a list of tiles attached to the host

			layout = eval(self.command('report.viz.wall', []))
			hosts = {}
			for tile in layout:
				if tile['name'] not in hosts:
					hosts[tile['name']] = []
				hosts[tile['name']].append(tile)

			for host in hosts.keys():
				tiles = hosts[host]
				if mode == 'simple':
					self.syncSimpleMode(host, tiles)
				elif mode == 'sage':
					self.syncSageMode(host, tiles)
				elif mode == 'cglx':
					self.syncCGLXMode(host, tiles)

		self.command('run.host',
			[ 'tile', 'x11=false', 'killall /usr/sbin/gdm-binary' ])
		self.command('run.host', 
		 	[ 'tile', 'x11=false',
				'echo %s > /opt/viz/etc/mode' % mode ])







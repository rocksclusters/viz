# $Id: __init__.py,v 1.7 2012/11/27 00:49:36 phil Exp $
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
# $Log: __init__.py,v $
# Revision 1.7  2012/11/27 00:49:36  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.6  2012/05/06 05:49:47  phil
# Copyright Storm for Mamba
#
# Revision 1.5  2011/07/23 02:31:40  phil
# Viper Copyright
#
# Revision 1.4  2010/10/07 19:41:47  mjk
# - use dpi instead of pixels to measure offsets
# - added horizontal|vertical shift attrs to deal with uneven walls (ours)
# - removed sage
# - added support for Google's liquid galaxy
#
# Revision 1.3  2010/09/07 23:53:30  bruno
# star power for gb
#
# Revision 1.2  2010/02/24 00:49:11  mjk
# - nvidia driver auto updates, but still works fine if the cluster is
#   not on the network.  Each node polls/pulls from nvidia.com the latest
#   driver.  User can disable and control the driver manually.
#   No more Roll updates to refresh the nvidia driver
# - X11 modules controlled by viz_x11_modules attribute
# - DPMS added back in
# - rocks start|stop tile to turn wall on|off
# - usersguide fixes (still needs work)
# - add nvidia driver version to tile-banner
# - bump version to 5.3.1
#
# Revision 1.1  2009/06/09 23:51:46  mjk
# *** empty log message ***
#
# Revision 1.15  2009/06/06 00:55:32  mjk
# checkpoint
#
# Revision 1.14  2009/06/03 20:15:31  mjk
# - kill gdm-binary to reset X server
# - bezel commands are chromium specific
#
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
import rocks.tile
import rocks.commands

class command(rocks.tile.TileCommand,
	rocks.tile.TileArgumentProcessor,
	rocks.commands.sync.command):
	pass

class Plugin(rocks.commands.Plugin):

	def getXConfPath(self):
		return os.path.join(os.sep, 'etc', 'X11', 'xorg.conf')


	def sendFileToHost(self, src, host, dst=None):
		if not os.path.isfile(src):
			self.owner.addText('warning - file %s does not exist\n' % src)
			return

		if dst == None:
			dst = src
		os.system('scp -q %s %s:%s' % (src, host, dst))


	def getFileFromHost(self, host, src, dst=None):
		if dst == None:
			dst = src
		os.system('scp -q %s:%s %s' % (host, src, dst))



	def getHosts(self):
		"""Returns a list of host that currently have tiles
		connected to them."""
		list = []
		for tile in self.layout:
			if tile['name'] not in list:
				list.append(tile['name'])
		list.sort()
		return list

	def sendXConf(self, host, mode):
		"""Send the host specific xorg.conf file to the host and
		record the mode we are in."""
		xconf = '%s-%s-%s' % (self.getXConfPath(), mode, host)
		self.owner.addText('sync %s (%s)\n' % (host, xconf))
		self.sendFileToHost(xconf, host, self.getXConfPath())
		self.owner.command('run.host', [ host, 'x11=false',
			'echo %s > /opt/viz/etc/mode' % mode ])


	def getHostTiles(self, host):
		"""Return a list of tiles that are connected to the given
		host sortd by the display number"""
		dict = {}
		list = []
		for tile in self.layout:
			if tile['name'] == host:
				dict[tile['display']] = tile
		displays = dict.keys()
		displays.sort()
		for display in displays:
			list.append(dict[display])
		return list

	def configureWall(self, owner):
		"""Calls the configureHost method for all Tile machines
		define in the viz layout."""

		for host in self.getHosts():
			self.configureHost(owner, host)

	def run(self, args):
		self.owner   = args[0]
		self.layout  = args[1]
		self.methods = args[2]
		self.methods[self.provides()] = self



class Command(command):
	"""
	Generates a new X11 configuration for each tile node on the frontend
	and then copies the files to the nodes.  After the copy all tile
	nodes are reset (not re-installed) to restart X11.  This should be
	used push out changes when the layout of the wall changes.
	
	<example cmd="sync viz">
	</example>
	"""

	def run(self, params, args):

		(mode, ) = self.fillParams([
			('mode', 'simple'),
		        ])

		# Build a list of hostnames that are connected to the
		# specified tiles, and a list of fully qualified display
		# names.

		hosts = []
		self.tiles = []
		for (server, display) in self.getTileNames(args):
			if server not in hosts:
				hosts.append(server)
			self.tiles.append('%s:%s' % (server, display))

		layout  = eval(self.command('report.tile', self.tiles))
		methods = {}

		self.runPlugins([self, layout, methods])
		if mode not in methods:
			self.abort('invalid mode "%s"' % mode)

		methods[mode].configureWall(self)

		args = hosts
		args.append('x11=false')
		args.append('killall gdm-binary')
		self.command('run.host', args)



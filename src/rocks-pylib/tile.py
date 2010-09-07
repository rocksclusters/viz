# $Id: tile.py,v 1.2 2010/09/07 23:53:30 bruno Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4 (Maverick)
# 
# Copyright (c) 2000 - 2010 The Regents of the University of California.
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
# $Log: tile.py,v $
# Revision 1.2  2010/09/07 23:53:30  bruno
# star power for gb
#
# Revision 1.1  2009/06/10 02:56:02  mjk
# - can enable/disable tile banner per display
# - nuke sample xml files
# - added rocks/tile.py for tile oriented commands
#

import string
import rocks.commands

class TileCommand:
	"""
	An Interface class to add Tile database methods to the Rocks
	command line.
	"""

	def getTileAttrs(self, tile, showsource=False):

		(server, display) = tile.split(':')
		attrs = self.db.getHostAttrs(server, showsource)

		self.db.execute("""select a.attr, a.value from 
			tile_attributes a, tiles t, nodes n where
			t.node=n.id and n.name='%s' and t.name='%s'""" %
			(server, display))
		for (a, v) in self.db.fetchall():
			if showsource:
				attrs[a] = (v, 'T')
			else:
				attrs[a] = (v)

		return attrs

	def getTileAttr(self, tile, key):
		return self.getTileAttrs(tile).get(key)


class TileArgumentProcessor(rocks.commands.HostArgumentProcessor):
	"""
	An Interface class to add the ability to process tile arguments.

	host(s)	- All Display attached to the host(s)
	:i	- All display of the ith server for all Tile hosts
	:i.j	- Display j of server i on all Tile hosts
	"""

	def getTileNames(self, names=None):
		"""Return a list of tiles from the database.  If NAMES is
		provided verify all the names tiles exists, otherwise
		return all the defined tiles"""

		# Terminology
		#
		# DISPLAY - X11 DISPLAY environment variable (w/o hostname)
		#	    Stored in the database w/o the leading ':'
		#
		# SERVER  - X11 server number on a host
		#
		# DISPNUM - X11 server's display number
		#
		# Example: 
		#
		# 	tile:0.1
		#		DISPLAY = :0.1
		#		SERVER  = 0
		#		DISPNUM = 1





		tiles = []	# (hostname, server, dispnum)
		tilehosts = []	# list of tile appliances

		self.db.execute("""select n.name,t.name from 
			nodes n, tiles t where t.node=n.id""")
		for host, display in self.db.fetchall():
			try:
				(server, dispnum) = display.split('.')
			except:
				server  = display
				dispnum = None
			tiles.append((host, server, dispnum))
			tilehosts.append(host)


		# If called w/o any names return a list of (hostname, display)
		# tuples.  

		if not names:
			list = []
			for (host, server, dispnum) in tiles:
				if dispnum:
					display = '%s.%s' % (server, dispnum)
				else:
					display = '%s' % server
				list.append((host, display))
			return list


		list = []
		for name in names:

			# If the name starts with ':' find all the matching
			# displays in the database (TILES array).  A null
			# dispnum means match all display for the given server

			if name[0] == ':':
				if len(name) <= 1:
					self.abort('unknown display %s' % name)
				if name.find('.') != -1:
					(s, dn) = name.split('.')
				else:
					s  = name
					dn = None
				s = s[1:]	# remove leading ':'
				for tile in tiles:
					(host, server, dispnum) = tile
					if s == server and not dn:
						list.append(tile)
					if s == server and dn == dispnum:
						list.append(tile)

			
			elif name.find(':') > 0:
				try:
					(host, display)   = name.split(':')
					(server, dispnum) = display.split('.')
				except:
					self.abort('not a tile %s' % name)
				for tile in tiles:
					if (host, server, dispnum) == tile:
						list.append(tile)


			# For anything else we match as a host argument and
			# then verify it is a tile appliance

			else:
				for hostname in self.getHostnames([name]):
					if hostname not in tilehosts:
						self.abort('not a tile %s' %
							hostname)
					for tile in tiles:
						(host, server, dispnum) = tile
						if hostname == host: 
							list.append(tile)

		# Turn the (hostname, server, dispnum) list into a list of
		# (hostname, display).

		tiles = list	# Set to only the requested tiles
		list = []	# Clear and use for retval

		for (host, server, dispnum) in tiles:
			if dispnum:
				display = '%s.%s' % (server, dispnum)
			else:
				display = '%s' % server
			list.append((host, display))
		return list
					

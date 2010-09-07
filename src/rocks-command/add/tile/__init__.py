# $Id: __init__.py,v 1.3 2010/09/07 23:53:28 bruno Exp $
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
# $Log: __init__.py,v $
# Revision 1.3  2010/09/07 23:53:28  bruno
# star power for gb
#
# Revision 1.2  2009/06/16 22:06:14  mjk
# fix checking for existing tile
#
# Revision 1.1  2009/06/10 01:35:18  mjk
# *** empty log message ***
#

import os
import sys
import string
import rocks.tile
import rocks.commands

class command(rocks.tile.TileCommand,
	rocks.tile.TileArgumentProcessor,
        rocks.commands.add.command):
	pass
	
class Command(command):
	"""
	Add Tile

        <arg type='string' name='tile'>
	A single tile name.  If the tilename is not of the standard from of
	host:server.display then a host param is required.
        </arg>

        <param type='string' name='host'>
        A single host name.  This is only required if the hostname is not
	part of the tilename,
        </param>

        <param type='int' name='x'>
	The X-axis position of the Tile.  Tiles are numbered starting at 0 from
	the left side of the wall.
        </param>

	<param type='int' name='y'>
	The Y-axis position of the Tile.  Tiles are numbered starting at 0 from
	the bottom row of the wall.
	</param>

	<example cmd='add host tile tile-2-1'>
	Adds a single tile to host tile-2-1 with coordinates (2,1).
	</example>

	<example cmd='add host tile :0.1 host=tile-0-0 x=0 y=1'>
	Adds a tile on the second display if tile-0-0 at coordinated (0,1).
	</example>

	"""

	def run(self, params, args):
	
		if len(args) != 1:
			self.abort('must supply one tile')
		
		tile = args[0]

		try:
			(host, display) = tile.split(':')
		except:
			self.abort('invalid time name %s' % tile)

		(h, x, y) = self.fillParams(
			[('host', None), 
			('x', None),
			('y', None) ])
		
		# Make sure exactly one host is specified either in
		# the tilename or from the host parameter.  The user
		# can do both but the names need to agree.  Last
		# normalize the hostname so we can use it against the database.

		if not host:
			if h:
				host = h
			else:
				self.abort('no hostname')
		else:
			if h and host != h:
				self.abort('too many hostnames')
		host = self.db.getHostname(host)

		# Make sure the tile doesn't already exist

		if self.getTileNames(['%s:%s' % (host, display)]):
			self.abort('tile %s exists' % tile)

		# Lookup the rack and rank of the host and use these values
		# as the default (x, y) coordinated.  This makes simple
		# non-TwinView wall trivial to configure since the host
		# (rack, rank) and tile (x, y) are identical.

		self.db.execute("""select rack, rank from nodes 
			where name='%s'""" % host)
		(rack, rank) = self.db.fetchone()
		if not x:
			x = rack
		if not y:
			y = rank
		try:
			x = int(x)
		except:
			self.abort('bad x-coordinate %s' % x)
		try:
			y = int(y)
		except:
			self.abort('bad y-coordinate %s' % y)

		self.db.execute("""insert tiles
			(node, name, x, y)
			values ((select id from nodes where name='%s'),
			'%s', %d, %d)""" % (host, display, x, y))

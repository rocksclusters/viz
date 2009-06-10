# $Id: tile.py,v 1.1 2009/06/10 02:56:02 mjk Exp $
#
# @Copyright@
# @Copyright@
#
# $Log: tile.py,v $
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
					

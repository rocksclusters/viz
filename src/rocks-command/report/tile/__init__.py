# $Id: __init__.py,v 1.9 2012/11/27 00:49:36 phil Exp $
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
# Revision 1.9  2012/11/27 00:49:36  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.8  2012/05/06 05:49:46  phil
# Copyright Storm for Mamba
#
# Revision 1.7  2011/07/23 02:31:40  phil
# Viper Copyright
#
# Revision 1.6  2010/12/18 00:27:34  mjk
# *** empty log message ***
#
# Revision 1.5  2010/10/07 19:41:47  mjk
# - use dpi instead of pixels to measure offsets
# - added horizontal|vertical shift attrs to deal with uneven walls (ours)
# - removed sage
# - added support for Google's liquid galaxy
#
# Revision 1.4  2010/09/07 23:53:30  bruno
# star power for gb
#
# Revision 1.3  2009/06/10 02:51:14  mjk
# - Everything is now tile oriented (no more viz keywords)
# - Can control everything on a per tile (host, x11server, display) basis
# - Missing: add host / insert-ethers plugin for default non-twinview layout
#
# Revision 1.2  2009/06/10 02:12:50  mjk
# *** empty log message ***
#
# Revision 1.1  2009/06/10 01:35:19  mjk
# *** empty log message ***
#
# Revision 1.1  2009/06/03 01:23:23  mjk
# - Now using the idea of modes for the wall (e.g. simple, sage, cglx)
# - Simple (chromium) and Sage modes work
# - Requires root to do a "rocks sync viz mode=??" to switch
# - "rocks enable/disable hidebezels" is chromium specific
#   The command line needs to change to reflect this fact
# - Tile-banner tell you the resolution and mode node
# - Sage works (surprised)
# - Removed autoselect of video mode on first boot, started to crash nodes
#

import os
import sys
import string
import rocks.tile
import rocks.commands.report

class command(rocks.tile.TileCommand,
	rocks.tile.TileArgumentProcessor,
	rocks.commands.report.command):

	MustBeRoot = 0


class Command(command):
	"""
	Reports the layout of the Viz Wall as a Python list of tiles.
	"""


	def getXOffset(self, wall, x, y):
		offset = wall[x][y]['leftborder'] + wall[x][y]['leftoffset']
		for i in range(0, x):
			t = wall[i][y]
			offset += t['xres'] + t['leftborder'] + t['rightborder'] + t['leftoffset']
		return offset

	def getYOffset(self, wall, x, y):
		offset = wall[x][y]['bottomborder'] + wall[x][y]['bottomoffset']
		for i in range(0, y):
			t = wall[x][i]
			offset += t['yres'] + t['bottomborder'] + t['topborder'] + t['bottomoffset']
		return offset


	def run(self, params, args):

		tiles = self.getTileNames(args)
		if not tiles:
			self.addText('%s' % [])
			return

		# Removed bezel hiding toggle, just define the bezels to zero to not hide
		# bezels.
		
		hideBezels = True

		self.db.execute('select max(x), max(y) from tiles')
		maxX, maxY = self.db.fetchone()
	
		# Create 2D Array represening the wall

		wall = []
		for i in range(0, maxX+1):
			list = []
			for j in range(0, maxY+1):
				list.append(None)
			wall.append(list)

		self.db.execute("""select n.name, t.name, t.x, t.y from
			nodes n, tiles t where t.node=n.id""")

		for (host, display, x, y) in self.db.fetchall():

			attrs = self.getTileAttrs('%s:%s' % (host, display))
			tile = {}
			tile['name']	= host
			tile['display']	= display
			tile['x']	= int(x)
			tile['y']	= int(y)
			tile['xoffset']	= 0
			tile['yoffset']	= 0

	
			res = attrs['viz_tile_resolution'].split('x')
			tile['xres'] = int(res[0])
			tile['yres'] = int(res[1])

			dpi = tile['xres'] / float(attrs['viz_tile_width'])
			tile['leftborder']  = int(round( float(attrs['viz_tile_left_bezel']) * dpi )) 
			tile['rightborder'] = int(round( float(attrs['viz_tile_right_bezel']) * dpi ))
			tile['leftoffset']  = int(round( float(attrs['viz_tile_horizontal_shift']) * dpi ))

			dpi = tile['yres'] / float(attrs['viz_tile_height'])
			tile['topborder']     = int(round( float(attrs['viz_tile_top_bezel']) * dpi ))
			tile['bottomborder']  = int(round( float(attrs['viz_tile_bottom_bezel']) * dpi ))
			tile['bottomoffset']  = int(round( float(attrs['viz_tile_vertical_shift']) * dpi ))

			if not hideBezels:
				tile['leftborder']   = 0
				tile['rightborder']  = 0
				tile['topborder']    = 0
				tile['bottomborder'] = 0

			wall[tile['x']][tile['y']] = tile

				
		# Traverse the perimeter of the wall and set the outside 
		# bezel sizes to zero.  After the above operations this leaves
		# only the interior bezels in place.
		
		for x in wall:
			x[0]['bottomborder'] = 0 # clear bottom edge
			x[maxY]['topborder'] = 0 # clear top edge

		for y in range(0, maxY+1):
			wall[0][y]['leftborder'] = 0	  # clear left side
			wall[maxX][y]['rightborder'] = 0 # clear right side
			

		# Compute the xoffset and yoffset of each tile

		for x in range(0, maxX+1):
			for y in range(0, maxY+1):
				tile = wall[x][y]
				tile['xoffset'] = self.getXOffset(wall, x, y)
				tile['yoffset'] = self.getYOffset(wall, x, y)


		# Flatten the 2x2 matrix to just a list of tiles

		list = []
		for col in wall:
			for tile in col:
				if (tile['name'], tile['display']) in tiles:
					list.append(tile)

		self.addText('%s' % list)





			
		

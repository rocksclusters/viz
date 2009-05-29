# $Id: __init__.py,v 1.1 2009/05/29 19:35:41 mjk Exp $
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
# Revision 1.1  2009/05/29 19:35:41  mjk
# *** empty log message ***
#

import string
import rocks.util
import rocks.commands

class Command(rocks.commands.report.command):
	"""
	Generates the DMX configuration file for the Wall.  This can
	be used to recreate the user's ~/.dmxrc file based on the Rocks
	defaults.
	
	<example cmd="report dmx layout">
	</example>
	"""

	def splitRes(self, res):
		(x, y) = res.split('x')
		return (int(x), int(y))
		
	def getXOffset(self, wall, x, y):
		offset = wall[x][y].leftborder
		for i in range(0, x):
			tile = wall[i][y]
			(xres, yres) = self.splitRes(tile.resolution)
			offset += xres + tile.leftborder + tile.rightborder
		return offset

	def getYOffset(self, wall, x, y):
		offset = wall[x][y].bottomborder
		for i in range(0, y):
			tile = wall[x][i]
			(xres, yres) = self.splitRes(tile.resolution)
			offset += yres + tile.bottomborder + tile.topborder
		return offset

	
	def dumpDMX(self, hideBezels):
	
		self.db.execute('select max(x), max(y) from videowall')
		maxX, maxY = self.db.fetchone()
	
		# Create 2D Array represening the wall

		wall = []
		for i in range(0, maxX+1):
			list = []
			for j in range(0, maxY+1):
				list.append(None)
			wall.append(list)


		self.db.execute("""select n.name, 
			v.display, v.resolution, v.x, v.y,
			v.leftborder, v.rightborder,
			v.topborder, v.bottomborder
			from nodes n, videowall v where
			v.node=n.id""")
			
		for tokens in self.db.fetchall():

			tile		= rocks.util.Struct()
			tile.name	= tokens[0]
			tile.display	= tokens[1]
			tile.resolution	= tokens[2]
			tile.x		= int(tokens[3])
			tile.y		= maxY - int(tokens[4])
			tile.xoffset	= 0
			tile.yoffset	= 0

			if hideBezels:
				tile.leftborder		= int(tokens[5])
				tile.rightborder	= int(tokens[6])
				tile.topborder		= int(tokens[7])
				tile.bottomborder	= int(tokens[8])
			else:
				tile.leftborder		= 0
				tile.rightborder	= 0
				tile.topborder		= 0
				tile.bottomborder	= 0

			wall[tile.x][tile.y] = tile

				
		# Traverse the perimeter of the wall and set the outside 
		# bezel sizes to zero.  After the above operations this leaves
		# only the interior bezels in place.
		
		for x in wall:
			x[0].bottomborder = 0	# clear bezels on bottom row
			x[maxY].topborder = 0	# clear bezels on top row

		for y in range(0, maxY+1):
			wall[0][y].leftborder = 0	# clear bezels on left
			wall[maxX][y].leftborder = 0	# clear bezels on right
			

		# Compute the xoffset and yoffset of each tile

		for x in range(0, maxX+1):
			for y in range(0, maxY+1):
				tile = wall[x][y]
				tile.xoffset = self.getXOffset(wall, x, y)
				tile.yoffset = self.getYOffset(wall, x, y)
				if x == maxX and y == maxY:
					res = self.splitRes(tile.resolution)
					xres = res[0] + tile.xoffset
					yres = res[1] + tile.yoffset

		if hideBezels:
			name = 'hide_bezels'
		else:
			name = 'show_bezels'

		self.addText('virtual %s %dx%d {\n' % (name, xres, yres))
		self.addText('\toption +xinerama -fontpath unix/:7100;\n')
		for x in range(0, maxX+1):
			for y in range(0, maxY+1):
				tile = wall[x][y]
				display = '%s:%s' % (tile.name, tile.display)
				self.addText('\tdisplay %s %s @%dx%d;\n' % (
					display, tile.resolution,
					tile.xoffset, tile.yoffset))
		self.addText('}\n')

		
	def run(self, params, args):
		self.dumpDMX(0) # Show Bezels (default)
		self.dumpDMX(1) # Hide Bezels (rocks enable hidebezels)





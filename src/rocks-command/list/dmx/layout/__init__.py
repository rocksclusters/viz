# $Id: __init__.py,v 1.7 2009/05/01 19:07:31 mjk Exp $
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
# Revision 1.7  2009/05/01 19:07:31  mjk
# chimi con queso
#
# Revision 1.6  2008/10/18 00:56:20  mjk
# copyright 5.1
#
# Revision 1.5  2008/03/06 23:42:02  mjk
# copyright storm on
#
# Revision 1.4  2007/09/19 11:35:08  mjk
# more swiss changes
#
# Revision 1.3  2007/07/06 18:38:10  mjk
# 4.3 Command Line cleanup
#
# Revision 1.2  2007/06/23 04:04:05  mjk
# mars hill copyright
#
# Revision 1.1  2007/05/11 18:35:52  mjk
# no more lib64
#

import string
import rocks.util
import rocks.commands

class Command(rocks.commands.list.command):
	"""
	Generates the DMX configuration file for the Wall.  This can
	be used to recreate the user's ~/.dmxrc file based on the Rocks
	defaults.
	
	<example cmd="list dmx layout">
	</example>
	"""
		
	def getOffsets(self, tile):

		# Horizontal offset is the sum of resolutions and bezels to 
		# our left.  Start with our left bezel size then add up
		# everything else to our left.
						
		hoffset = tile.lhborder
		for (m, t) in self.wall[tile.vcoord][0:tile.hcoord]:
			hoffset += t.lhborder + t.rhborder + t.hres

		# Vertical offset is the sum of the resolutions and bezels 
		# above us.  Start with our top bezel size  then add up
		# everything else above us.

		voffset = tile.tvborder
		for subwall in self.wall[0:tile.vcoord]:
			(m, t) = subwall[tile.hcoord]
			voffset += t.bvborder + t.tvborder + t.vres
	
		return (hoffset, voffset)
		
		
	
	def dumpDMX(self, hideBezels):
	
		self.db.execute("""select max(hcoord), max(vcoord) 
			from videowall""")
		hmax, vmax = self.db.fetchone()
	
		# Create 2D Array represening the wall

		self.wall = []
		for i in range(0, vmax+1):
			list = []
			for j in range(0, hmax+1):
				list.append(None)
			self.wall.append(list)


		self.db.execute("""select n.name, v.cardid,
			v.hcoord, v.vcoord, v.hres, v.vres,
			v.lhborder, v.rhborder, v.bvborder, v.tvborder
			from nodes n, videowall v where
			v.node=n.id order by v.vcoord asc, v.hcoord asc""")
			
		dict = {}
		for tokens in self.db.fetchall():
			tile		= rocks.util.Struct()
			tile.name	= tokens[0]
			tile.card	= int(tokens[1])
			tile.hcoord	= int(tokens[2])
			tile.vcoord	= int(tokens[3])
			tile.hres	= int(tokens[4])
			tile.vres	= int(tokens[5])
			
			# When running not is hidebezels mode
			# set all the bezel borders to zero.  Otherwise
			# get the border settings from the database.  This
			# way the rest of the code is set to always hide
			# the bezels (0 size or not).
			
			if not hideBezels:
				tile.lhborder = 0
				tile.rhborder = 0
				tile.bvborder = 0
				tile.tvborder = 0
			else:
				tile.lhborder = int(tokens[6])
				tile.rhborder = int(tokens[7])
				tile.bvborder = int(tokens[8])
				tile.tvborder = int(tokens[9])


			# Build the wall matrix of (MASTER, TILE)
			# - MASTER: FALSE iff the tile is a secondary display
			#   for a TwinView host.  Otherwise this is true.
			# - TILE: The above tile structure
			
			key = (tile.name, tile.card)
			if dict.has_key(key):

				# TwinView Vertical (Below)
				# - Compute the total vertical resolution with
				#   the bezels and update the vertical
				#   resolution of the master
				# - Zero the vertical resolution the slave
				# - Zero the top bezel size of the slave
				# - Zero the bottom bezel size of the master
				#
				# Result is the slave tile is set to zero
				# vertical resolution except for the
				# bottom bezel, and the master gets all
				# the pixels from the slave.
				
				if dict[key].hcoord == tile.hcoord:
					dict[key].vres += tile.vres + \
						dict[key].bvborder  + \
						tile.tvborder
					tile.vres          = 0
					tile.tvborder      = 0
					dict[key].bvborder = 0


				# TwinView Vertical (Right)
				# - Compute the total horizontal resolution,
				#   with or without, the bezels and update the
				#   horizontal resolution of the master
				# - Zero the horizontal resolution the slave
				# - Zero the left bezel size of the slave
				# - Zero the right bezel size of the master
				#
				# Result is the slave tile is set to zero
				# horizontal resolution except for the
				# right bezel, and the master gets all
				# the pixels from the slave.
						
				elif dict[key].vcoord == tile.vcoord:
					dict[key].hres += tile.hres + \
						dict[key].rhborder  + \
						tile.lhborder
					tile.hres          = 0
					tile.lhborder      = 0
					dict[key].rhborder = 0
							
				self.wall[tile.vcoord][tile.hcoord] = (0, tile)

			else:
				dict[key] = tile
				self.wall[tile.vcoord][tile.hcoord] = (1, tile)
				

		# Traverse the perimeter of the wall and set the outside 
		# bezel sizes to zero.  After the above operations this leaves
		# only the interior non-TwinView bezels in place.
		
		for row in self.wall:
			(lm, lt) = row[0]
			(rm, rt) = row[hmax]
			lt.lhborder = 0		# zero wall bezel (left)
			rt.rhborder = 0		# zero wall bezel (right)
		for (m, t) in self.wall[0]:
			t.tvborder = 0		# zero wall bezel (top)
		for (m, t) in self.wall[vmax]:
			t.bvborder = 0		# zero wall bezel (bottom)
			

		if hideBezels:
			name = 'hide_bezels'
		else:
			name = 'show_bezels'

		hmax = 0
		vmax = 0
		displays = []
		for row in self.wall:
			for (m, t) in row:
				if not m:
					continue
				(h, v) = self.getOffsets(t)
				if (h + t.hres) > hmax:
					hmax = h + t.hres
				if (v + t.vres) > vmax:
					vmax = v + t.vres
				displays.append('%s:%d %dx%d @%dx%d' %
					(t.name, t.card-1,
					t.hres, t.vres, h, v))

		self.addText('virtual %s %dx%d {\n' % (name, hmax, vmax))
		self.addText('\toption +xinerama -fontpath unix/:7100;\n')
		for display in displays:				
			self.addText('\tdisplay %s;\n' % display)
		self.addText('}\n')
		

		
	def run(self, params, args):
		self.dumpDMX(0) # Show Bezels (default)		
		self.dumpDMX(1) # Hide Bezels (rocks enable hidebezels)





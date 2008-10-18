#!/opt/rocks/bin/python
#
# $RCSfile: xdmx.py,v $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		           version 5.1  (VI)
# 
# Copyright (c) 2000 - 2008 The Regents of the University of California.
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
# $Log: xdmx.py,v $
# Revision 1.25  2008/10/18 00:56:18  mjk
# copyright 5.1
#
# Revision 1.24  2008/03/06 23:42:00  mjk
# copyright storm on
#
# Revision 1.23  2007/06/23 04:04:03  mjk
# mars hill copyright
#
# Revision 1.22  2006/09/11 22:50:31  mjk
# monkey face copyright
#
# Revision 1.21  2006/08/10 00:12:08  mjk
# 4.2 copyright
#
# Revision 1.20  2006/06/27 00:30:02  mjk
# - chromium reads config from DMX not from DB now
# - DMX config fixes for crazy Kim layout
# - Tile background color is a hash of the hostname
#
# Revision 1.19  2006/06/23 22:32:30  mjk
# twinview changes
#
# Revision 1.18  2006/01/16 06:49:15  mjk
# fix python path for source built foundation python
#
# Revision 1.17  2005/10/12 18:11:14  mjk
# final copyright for 4.1
#
# Revision 1.16  2005/09/16 01:04:52  mjk
# updated copyright
#
# Revision 1.15  2005/08/08 21:25:03  mjk
# foundation
#
# Revision 1.14  2005/05/24 21:24:04  mjk
# update copyright, release is not any closer
#
# Revision 1.13  2005/01/14 03:02:32  mjk
# x,y always update -- bezels are mod
#
# Revision 1.12  2005/01/14 02:58:10  mjk
# closer, need to test on sio cluster
#
# Revision 1.11  2005/01/13 21:42:56  mjk
# first pass at bertha support
#
# Revision 1.10  2004/12/06 18:24:28  mjk
# fixes bug 85
#
# Revision 1.9  2004/09/11 05:52:01  mjk
# option goes inside block
#
# Revision 1.8  2004/09/07 22:26:26  mjk
# set options in config file
#
# Revision 1.7  2004/09/03 19:35:14  mjk
# just call them Tiles now
#
# Revision 1.6  2004/08/31 21:21:22  mjk
# window mode works
#
# Revision 1.5  2004/08/31 20:08:11  mjk
# hide pixels
#
# Revision 1.4  2004/07/15 16:54:16  mjk
# looks good
#
# Revision 1.3  2004/07/15 16:48:49  mjk
# phat phingered
#
# Revision 1.2  2004/07/15 16:46:16  mjk
# might even work
#
# Revision 1.1  2004/07/15 15:26:20  mjk
# 1st pass at xdmx report
#

import os
import sys
import socket
import string
import numpy
import rocks.reports.base


class Report(rocks.reports.base.ReportBase):

	def dumpDisplay(self, tile):


#		print 'dumpDisplay', tile.__dict__
#		print 'W', self.wall
	
		# Compute horizonal offset by adding up the pixels to the
		# left of us.  Watch out for empty nodes in the wall, these
		# are ganged displays.
	
		hoffset = 0
#		print 'H', self.wall[tile.vcoord][0:tile.hcoord]
		for e in self.wall[tile.vcoord][0:tile.hcoord]:
			if e:
				hoffset += e.hres
	
		# Compute the vertical offset by adding up the pixels above
		# us.  Also watch for empty entries in the wall for ganged
		# displays.  If the tile above us is vacant get the 
		# resolution from the one to the left (assumed ganged)
		
		voffset = 0
#		print 'V', self.wall[0:tile.vcoord]
		for e in self.wall[0:tile.vcoord]:
			if e[tile.hcoord]:
				voffset += e[tile.hcoord].vres
			elif tile.hcoord > 0 and e[tile.hcoord - 1]:
				voffset += e[tile.hcoord - 1].vres
			
		print '\tdisplay %s:%d %dx%d @%dx%d;' % \
			(tile.name, tile.card - 1,
			tile.hres, tile.vres, hoffset, voffset)
		
	def run(self):
	
		self.execute('select max(hcoord),max(vcoord) from videowall')
		hmax, vmax = self.fetchone()
		
		self.wall = []
		for i in range(0, vmax+1):
			list = []
			for j in range(0, hmax+1):
				list.append(None)
			self.wall.append(list)

		self.execute('select '
			'nodes.name, '
			'videowall.cardid, '
			'videowall.hcoord, videowall.vcoord, '
			'videowall.hres, videowall.vres, '
			'videowall.lhborder, videowall.rhborder, '
			'videowall.bvborder, videowall.tvborder, '
			'videowall.ppi '
			'from nodes, videowall where '
			'videowall.node=nodes.id '
			'order by videowall.vcoord asc, videowall.hcoord asc')
			
		dict = {}
		for tokens in self.fetchall():
			tile		= rocks.util.Struct()
			tile.name	= tokens[0]
			tile.card	= int(tokens[1])
			tile.hcoord	= int(tokens[2])
			tile.vcoord	= int(tokens[3])
			tile.hres	= int(tokens[4])
			tile.vres	= int(tokens[5])
			tile.lhborder	= float(tokens[6])
			tile.rhborder	= float(tokens[7])
			tile.bvborder	= float(tokens[8])
			tile.tvborder	= float(tokens[9])
			tile.ppi	= int(tokens[10])


			# If key exists add the secondary tile's resolution to
			# the known tile's resolution.  Otherwise just 
			# record that we've seen the tile,card tuple already.
			
			key = (tile.name, tile.card)
			if dict.has_key(key):
				if dict[key].hcoord == tile.hcoord:
					dict[key].vres += tile.vres
				elif dict[key].vcoord == tile.vcoord:
					dict[key].hres += tile.hres
			else:
				dict[key] = tile
				self.wall[tile.vcoord][tile.hcoord] = tile

		try:
			configname = string.split(socket.gethostname(), '.')[0]
		except:
			configname = 'rocks'

		# The assumption is the far left column specifies the 
		# vertical resolution and the top row specifies the 
		# horizontal resolation.  This does not imply all tiles 
		# have the same screen resolution but does assume the 
		# display is a rectangle.
	
		hres = 0
		vres = 0
		for e in self.wall[0]:
			if e:
				hres += e.hres
		for row in self.wall:
			for e in row:
				if e and e.hcoord == 0:
					vres += e.vres

		print self.getHeader()
		print 'virtual %s %dx%d {' % (configname, hres, vres)
		print '\toption +xinerama -fontpath unix/:7100;'
		for row in self.wall:
			for tile in row:
				if tile:
					self.dumpDisplay(tile)
		print '}'




#!/opt/rocks/bin/python
#
# $RCSfile: sagetile.py,v $
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
# $Log: sagetile.py,v $
# Revision 1.8  2008/10/18 00:56:18  mjk
# copyright 5.1
#
# Revision 1.7  2008/03/06 23:42:00  mjk
# copyright storm on
#
# Revision 1.6  2007/06/23 04:04:03  mjk
# mars hill copyright
#
# Revision 1.5  2006/09/30 00:57:25  mjk
# Fix bug 90 (trac.rocksclusters.org)
# Only list eth0 network in the tile IP configuration
#
# Revision 1.4  2006/09/11 22:50:31  mjk
# monkey face copyright
#
# Revision 1.3  2006/08/10 00:12:08  mjk
# 4.2 copyright
#
# Revision 1.2  2006/06/23 22:32:30  mjk
# twinview changes
#
# Revision 1.1  2006/02/23 02:01:55  mjk
# sage looks good
#
# Revision 1.1  2006/02/17 20:30:00  mjk
# *** empty log message ***

import os
import sys
import socket
import string
import rocks.reports.base


class Report(rocks.reports.base.ReportBase):

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
			'videowall.tvborder, videowall.bvborder, '
			'videowall.ppi '
			'from nodes, videowall where '
			'videowall.node=nodes.id '
			'order by videowall.vcoord desc, videowall.hcoord asc')
			
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
			tile.tvborder	= float(tokens[8])
			tile.bvborder	= float(tokens[9])
			tile.ppi	= int(tokens[10])


			# If key exists add the secondary tile's resolution to
			# the known tile's resolution.  Otherwise just 
			# record that we've seen the tile,card tuple already.
			
			key = (tile.name, tile.card)
			if dict.has_key(key):
				dict[key].append(tile)
			else:
				dict[key] = [ tile ]
				
		# Use the values from the last tile we saw for the
		# SAGE global settings.  Future versions of SAGE will
		# allow these to be display dependent.
		
		print self.getHeader()
		print 'TileDisplay'
		print '\tDimensions', hmax+1, vmax+1
		print '\tMullions', \
			tile.tvborder, tile.bvborder, \
			tile.lhborder, tile.rhborder
		print '\tResolution', tile.hres, tile.vres
		print '\tPPI', tile.ppi
		print '\tMachines', len(dict)
		
		# key = (node-name, card-number)
		# value = list of tiles for this key (node,card)
		
		for key in dict.keys():
			print
			print 'DisplayNode'
			print '\tName', key[0]
			
			self.execute('select networks.ip '
				'from nodes,networks where '
				'nodes.name="%s" and networks.node=nodes.id '
				'and networks.device="eth0"' %
				key[0])
			for ip, in self.fetchall():
				if ip:
					print '\tIP', ip
			print '\tMonitors %d ' % len(dict[key]),
			for tile in dict[key]:
				print '(%d,%d) ' % \
					(tile.hcoord, vmax - tile.vcoord),
			print

		sys.exit(0)
		







# $Id: __init__.py,v 1.1 2008/05/31 02:57:37 mjk Exp $
#
# @Copyright@
# 
# 				Rocks(tm)
# 		         www.rocksclusters.org
# 		        version 4.3 (Mars Hill)
# 
# Copyright (c) 2000 - 2007 The Regents of the University of California.
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
# 	"This product includes software developed by the Rocks(tm)
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
# Revision 1.1  2008/05/31 02:57:37  mjk
# - SAGE is back and works (mostly)
# - DMX building from source (in progress)
# - Updated nvidia driver
#

import rocks.util
import rocks.commands

class Command(rocks.commands.report.command):
	"""
	Reports the SAGE tile layout configuration file.
	
	<example cmd='report sage layout'>
	</example>
	"""

	def run(self, params, args):

		self.db.execute("""select max(hcoord), max(vcoord)
			from videowall""")
		hmax, vmax = self.db.fetchone()
		
		self.wall = []
		for i in range(0, vmax+1):
			list = []
			for j in range(0, hmax+1):
				list.append(None)
			self.wall.append(list)

		self.db.execute("""select n.name, v.cardid, 
			v.hcoord, v.vcoord, v.hres, v.vres, 
			v.lhborder, v.rhborder, v.tvborder, v.bvborder
			from nodes n, videowall v where 
			v.node=n.id order by v.vcoord desc, v.hcoord asc""")
			
		dict = {}
		for tokens in self.db.fetchall():
			tile		= rocks.util.Struct()
			ppi		= 100
			tile.name	= tokens[0]
			tile.card	= int(tokens[1])
			tile.hcoord	= int(tokens[2])
			tile.vcoord	= int(tokens[3])
			tile.hres	= int(tokens[4])
			tile.vres	= int(tokens[5])
			tile.lhborder	= float(tokens[6]) / ppi
			tile.rhborder	= float(tokens[7]) / ppi
			tile.tvborder	= float(tokens[8]) / ppi
			tile.bvborder	= float(tokens[9]) / ppi


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
		
		self.addText('TileDisplay\n')
		self.addText('\tDimensions %d %d\n' % (hmax+1, vmax+1))
		self.addText('\tMullions %.3f %.3f %.3f %.3f\n' %
			(tile.tvborder, tile.bvborder, 
			tile.lhborder, tile.rhborder))
		self.addText('\tResolution %d %d\n' % (tile.hres, tile.vres))
		self.addText('\tPPI %d\n' % ppi)
		self.addText('\tMachines %d\n' % len(dict))
		
		# key = (node-name, card-number)
		# value = list of tiles for this key (node,card)
		
		list = dict.keys()
		list.sort()
		for key in list:
			self.addText('\nDisplayNode\n')
			self.addText('\tName %s\n' % key[0])
			
			self.db.execute("""select net.ip from 
				nodes n,networks net where
				n.name="%s" and net.node=n.id and
				net.device="eth0" """ % key[0])
				
			for ip, in self.db.fetchall():
				if ip:
					self.addText('\tIP %s\n' % ip)
			self.addText('\tMonitors %d ' % len(dict[key]))
			for tile in dict[key]:
				self.addText('(%d,%d) ' %
					(tile.hcoord, vmax - tile.vcoord))
			self.addText('\n')

#! @PYTHON@
#
# $Id: tilelayout.py,v 1.11 2008/10/18 00:56:18 mjk Exp $
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
# $Log: tilelayout.py,v $
# Revision 1.11  2008/10/18 00:56:18  mjk
# copyright 5.1
#
# Revision 1.10  2008/03/06 23:42:00  mjk
# copyright storm on
#
# Revision 1.9  2007/06/23 04:04:03  mjk
# mars hill copyright
#
# Revision 1.8  2006/09/11 22:50:31  mjk
# monkey face copyright
#
# Revision 1.7  2006/09/09 00:45:18  mjk
# Report generates valid config w/ an empty database table.
# Fixes bug 49 (trac.rocksclusters.org)
#
# Revision 1.6  2006/08/10 00:12:08  mjk
# 4.2 copyright
#
# Revision 1.5  2006/06/23 22:32:30  mjk
# twinview changes
#
# Revision 1.4  2006/06/19 23:12:45  mjk
# *** empty log message ***
#
# Revision 1.3  2006/05/02 01:29:37  mjk
# more host/node confusion
#
# Revision 1.2  2006/05/02 01:24:26  mjk
# node not host
#
# Revision 1.1  2006/05/02 01:15:43  mjk
# tilelayout.py
#

import rocks.reports.base

class Report(rocks.reports.base.ReportBase):

	def defaultLayout(self):
		self.execute('select nodes.name,nodes.rank,nodes.rack '
			'from nodes,memberships where '
			'nodes.membership = memberships.id and '
			'memberships.name = "Tile"'
			'order by rack,rank')
		col = []
		for (name, r, c) in self.fetchall():
			try:
				col[c].append(name)
			except IndexError:
				col.append([name])

		print '<wall>'
		print
		print '\t<!-- edit the following line -->'
		print '\t<defaults card="1" hres="1920" vres="1200" ' \
			'hborder="0.8" vborder="0.8" ppi="100"/>'
		print
		for c in col:
			print '\t<col>'
			for r in c:
				print '\t\t<display host="%s"/>' % r
			print '\t</col>'
		print '</wall>'

	def existingLayout(self):
		self.execute('select max(vcoord),max(hcoord) '
			'from videowall')
		rows,cols =  self.fetchone()
		print '<wall>'
		for c in range(0, cols+1):
			print '\t<col>'
			for r in range(rows, -1, -1):
				self.execute('select nodes.name,'
					'videowall.cardid,'
					'videowall.lhborder,'
					'videowall.rhborder,'
					'videowall.tvborder,'
					'videowall.bvborder,'
					'videowall.hres,'
					'videowall.vres,'
					'videowall.ppi'
					' '
					'from nodes,videowall '
					'where nodes.id=videowall.node '
					'and videowall.hcoord=%d '
					'and videowall.vcoord=%d ' %
					(c, r))
				node, cardid, lhborder, rhborder, \
					tvborder, bvborder, \
					hres, vres, ppi = self.fetchone()
				print '\t\t<display host="%s" card="%d" ' \
					'lhborder="%.3f" rhborder="%.3f" ' \
					'tvborder="%.3f" bvborder="%.3f" ' \
					'hres="%d" vres="%d" ppi="%d"/>' % \
					(node, cardid, 
					lhborder, rhborder,
					tvborder, bvborder,
					hres, vres, ppi)
			print '\t</col>'
		print '</wall>'

	def run(self):
		self.execute('select count(*) from videowall')
		count, = self.fetchone()

		if not count:
			self.defaultLayout()
		else:
			self.existingLayout()

	

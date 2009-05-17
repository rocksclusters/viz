# $Id: __init__.py,v 1.1 2009/05/17 13:41:53 mjk Exp $
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
# Revision 1.1  2009/05/17 13:41:53  mjk
# checkpoint before zurich
#

import rocks.util
import rocks.commands

class Command(rocks.commands.report.viz.command):
	"""
	Report the layout of the video wall.
	
	<example cmd='report viz layout'>
	</example>
	"""

	def run(self, params, args):

		rows = self.db.execute("""select * from videowall""")
		if not rows:
			self.abort('layout does no exist')
					
		self.db.execute('select max(x),max(y) from videowall')
		maxX, maxY =  self.db.fetchone()
		
		self.db.execute("""select n.name, 
			v.display, v.resolution, v.x, v.y, 
			v.leftborder, v.rightborder, v.topborder, v.bottomborder
			from nodes n, videowall v where
			n.id=v.node order by v.x, v.y desc""")

		self.addText('<wall>\n')
		prevX = -1
		for row in self.db.fetchall():
			hostname	= row[0]
			display		= row[1]
			resolution	= row[2]
			x		= row[3]
			y		= row[4]
			border		= rocks.util.Struct()
			border.l	= row[5]
			border.r	= row[6]
			border.t	= row[7]
			border.b	= row[8]
			if x != prevX:
				if x > 0:
					self.addText('\t</col>\n')
				self.addText('\t<col>\n')

			attrs  = 'resolution="%s" '  % resolution
			attrs += 'leftborder="%d" '  % border.l
			attrs += 'rightborder="%d" ' % border.r
			attrs += 'topborder="%d" '   % border.t
			attrs += 'bottomborder="%d"' % border.b
			self.addText('\t\t<display %s>%s:%s</display>\n' %
				(attrs, hostname, display))
			prevX = x	
		
		if prevX != -1:
			self.addText('\t</col>\n')
		self.addText('</wall>\n')
		
			


	


	

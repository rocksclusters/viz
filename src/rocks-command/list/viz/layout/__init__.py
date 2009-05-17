# $Id: __init__.py,v 1.12 2009/05/17 13:41:53 mjk Exp $
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
# Revision 1.12  2009/05/17 13:41:53  mjk
# checkpoint before zurich
#
# Revision 1.11  2009/05/01 19:07:31  mjk
# chimi con queso
#
# Revision 1.10  2008/10/18 00:56:21  mjk
# copyright 5.1
#
# Revision 1.9  2008/03/06 23:42:02  mjk
# copyright storm on
#
# Revision 1.8  2007/10/30 18:28:14  mjk
# - Fix whitespace error (start chromium)
# - Remove PPI stuff from the create/list viz layout commands
#
# Revision 1.7  2007/10/03 22:19:58  mjk
# *** empty log message ***
#
# Revision 1.6  2007/08/10 23:38:56  mjk
# *** empty log message ***
#
# Revision 1.5  2007/08/05 04:20:50  bruno
# doc tweak.
#
# Revision 1.4  2007/07/24 02:11:36  mjk
# - sage2 starting to work
#
# Revision 1.3  2007/07/06 18:38:10  mjk
# 4.3 Command Line cleanup
#
# Revision 1.2  2007/06/23 04:04:06  mjk
# mars hill copyright
#
# Revision 1.1  2007/05/11 18:35:52  mjk
# no more lib64
#

import rocks.util
import rocks.commands

class Command(rocks.commands.list.command):
	"""
	List the layout of the video wall.
	
	<example cmd='list viz layout'>
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
			n.id=v.node order by v.x, v.y""")

		for row in self.db.fetchall():
			self.addOutput(row[0], row[1:])
			
		self.endOutput(header=['host',
			'display', 'resolution', 'x', 'y',
			'leftborder', 'rightborder',
			'topborder', 'bottomborder'])
			


	


	

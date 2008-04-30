# $Id: __init__.py,v 1.7 2008/03/06 23:42:02 mjk Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		            version 5.0 (V)
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
# $Log: __init__.py,v $
# Revision 1.7  2008/03/06 23:42:02  mjk
# copyright storm on
#
# Revision 1.6  2008/01/14 22:03:47  bruno
# tweaks for V
#
# Revision 1.5  2007/09/19 11:35:08  mjk
# more swiss changes
#
# Revision 1.4  2007/08/10 23:38:56  mjk
# *** empty log message ***
#
# Revision 1.3  2007/07/06 18:38:10  mjk
# 4.3 Command Line cleanup
#
# Revision 1.2  2007/06/23 04:04:06  mjk
# mars hill copyright
#
# Revision 1.1  2007/05/10 20:37:02  mjk
# - massive rocks-command changes
# -- list host is standardized
# -- usage simpler
# -- help is the docstring
# -- host groups and select statements
# - added viz commands
#


import os
import tempfile
import rocks.commands

class Command(rocks.commands.Command):
	"""
	Generates a new X11 configuration for each tile node on the frontend
	and then copies the files to the nodes.  After the copy all tile
	nodes are reset (not re-installed) to restart X11.  This should be
	used push out changes when the layout of the wall changes.
	
	<example cmd="sync viz">
	</example>
	"""

	def run(self, params, args):

		hideBezels = self.db.getGlobalVar('Viz', 'HideBezels')

		self.db.execute("""select distinctrow n.name from
			nodes n, videowall v where v.node=n.id""")
			
		for host, in self.db.fetchall():
			temp = tempfile.mktemp()
			fout = open(temp, 'w')
			fout.write(self.command('list.host.xconfig', 
				[host, 'hidebezels=%s' % hideBezels]))
			fout.close()
			os.system('scp -q %s %s:/etc/X11/xorg.conf' % 
				(temp, host))
			os.unlink(temp)
		
		os.system('tentakel -g tile killall Xorg')


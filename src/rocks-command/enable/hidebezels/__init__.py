# $Id: __init__.py,v 1.5 2008/07/03 01:14:13 mjk Exp $
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
# Revision 1.5  2008/07/03 01:14:13  mjk
# - fix path to xrandr
# - call xrandr twice (current mode, desired mode)
#   otherwise it fails to set the desired mode
# - sage respects the hidebezels mode
#
# Revision 1.4  2008/03/06 23:42:02  mjk
# copyright storm on
#
# Revision 1.3  2007/10/03 22:19:58  mjk
# *** empty log message ***
#
# Revision 1.2  2007/09/19 13:28:58  mjk
# Swiss Viss
#
# Revision 1.1  2007/09/19 11:35:08  mjk
# more swiss changes
#

import rocks.commands.enable
import os

class Command(rocks.commands.enable.command):
	"""
	Enable Bezel Hiding mode.
	
	<example cmd="enable hidebezels">
	</example>
	"""
	
	MustBeRoot = 0

	def run(self, params, args):

		os.system('touch ~/.hidebezels')
		
		# If the database videowall layout has two (or more) entries
		# for the same host and card we know we are in twinview
		# mode.  In this case we need to reconfigure and restart
		# X11 for this host.
		
		self.db.execute("""select n.name, v.cardid 
			from nodes n, videowall v where v.node=n.id""")
		dict     = {}
		for key in self.db.fetchall():
			if dict.has_key(key):
				dict[key] = 1	# TwinView host
			else:
				dict[key] = 0	# NonTwinView host (so far)

		for (host, card) in dict.keys():
			if dict[(host, card)]:
				os.system('ssh -f '
					'%s /usr/bin/xrandr -d :0 -s 0'
					% host)
				os.system('ssh -f '
					'%s /usr/bin/xrandr -d :0 -s 1'
					% host)

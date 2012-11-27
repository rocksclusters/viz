# $Id: videowall.py,v 1.10 2012/11/27 00:49:32 phil Exp $
#
# insert-ethers plugin module
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.6 (Emerald Boa)
# 		         version 6.1 (Emerald Boa)
# 
# Copyright (c) 2000 - 2013 The Regents of the University of California.
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
# $Log: videowall.py,v $
# Revision 1.10  2012/11/27 00:49:32  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.9  2012/05/06 05:49:44  phil
# Copyright Storm for Mamba
#
# Revision 1.8  2011/07/23 02:31:38  phil
# Viper Copyright
#
# Revision 1.7  2010/09/07 23:53:27  bruno
# star power for gb
#
# Revision 1.6  2009/06/10 20:09:07  mjk
# - run only for Tile appliances
# - remove uses the command line
# - add create a default :0.0 tile for the host
#
# Revision 1.5  2009/05/01 19:07:29  mjk
# chimi con queso
#
# Revision 1.4  2008/10/18 00:56:19  mjk
# copyright 5.1
#
# Revision 1.3  2008/03/06 23:42:01  mjk
# copyright storm on
#
# Revision 1.2  2007/06/23 04:04:04  mjk
# mars hill copyright
#
# Revision 1.1  2006/09/15 19:52:08  mjk
# added plugin
#
#

import os
import rocks.sql

class Plugin(rocks.sql.InsertEthersPlugin):

	def isTile(self, id):
		self.app.execute("""select m.name from 
			nodes n, memberships m where 
			n.membership=m.id and n.id=%d""" % id)
		membership, = self.app.fetchone()
		if membership == 'Tile':
			return True
		return False

	def added(self, nodename, id):
		if self.isTile(id):
			os.system('rocks add tile %s:0.0' % nodename)

	def removed(self, nodename, id):
		if self.isTile(id):
			os.system('rocks remove tile %s' % nodename)


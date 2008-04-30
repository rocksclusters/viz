#!/opt/rocks/bin/python
#
# $RCSfile: sage.py,v $
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
# $Log: sage.py,v $
# Revision 1.11  2008/03/06 23:42:00  mjk
# copyright storm on
#
# Revision 1.10  2007/06/23 04:04:03  mjk
# mars hill copyright
#
# Revision 1.9  2006/09/11 22:50:31  mjk
# monkey face copyright
#
# Revision 1.8  2006/08/10 00:12:08  mjk
# 4.2 copyright
#
# Revision 1.7  2006/07/27 22:03:03  mjk
# added VNC support
#
# Revision 1.6  2006/07/17 19:19:56  mjk
# play dvds again
#
# Revision 1.5  2006/07/11 17:35:18  mjk
# more SAGE changes
#
# Revision 1.4  2006/06/28 14:19:14  phil
#
# Add a default DVD entry
#
# Revision 1.3  2006/03/05 20:39:40  mjk
# less buffers, less memory leaks
#
# Revision 1.2  2006/02/23 02:01:55  mjk
# sage looks good
#
# Revision 1.1  2006/02/17 20:30:00  mjk
# *** empty log message ***

import os
import socket
import string
import rocks.reports.base


class Report(rocks.reports.base.ReportBase):

	def run(self):

		host     = self.getGlobalVar('Kickstart', 'PrivateAddress')
		hostname = self.getGlobalVar('Kickstart', 'PublicHostname')
		sagedir  = os.environ['SAGE_DIRECTORY']

		print 'displayBinDir', sagedir
		print 'appBinDir', sagedir
		print
		print 'appList'
		print
		print 'atlantis {'
		print 'configName local'
		print 'nodeNum 1'
		print 'Init 100 100 1000 1000'
		print 'exec %s %s/bin/atlantis 0 %s' % (host, sagedir, host)
		print 'nwProtocol %s/lib/tvTcpModule.so' % sagedir
		print '}'
		print
		print 'checker {'
		print 'configName local'
		print 'nodeNum 1'
		print 'Init 100 100 1000 1000'
		print 'exec %s %s/bin/checker 0 %s' % (host, sagedir, host)
		print 'nwProtocol %s/lib/tvTcpModule.so' % sagedir
		print '}'
		print
		print 'render {'
		print 'configName local'
		print 'nodeNum 1'
		print 'Init 100 100 1000 1000'
		print 'exec %s %s/bin/render 0 %s' % (host, sagedir, host)
		print 'nwProtocol %s/lib/tvTcpModule.so' % sagedir
		print '}'
		print
		print 'imageviewer {'
		print 'configName images'
		print 'nodeNum 1'
		print 'Init 100 100 500 500'
		print 'exec %s %s/bin/imageviewer %s' % (host, sagedir, host)
		print 'nwProtocol %s/lib/tvTcpModule.so' % sagedir
		print '}'
		print
		print 'mplayer {'
		print 'configName movies'
		print 'nodeNum 1'
		print 'Init 100 100 640 480'
		print 'exec %s %s/bin/mplayer ' % (host, sagedir)
		print 'nwProtocol %s/lib/tvTcpModule.so' % sagedir
		print '}'
		print 
		print 'dvdplayer {'
		print 'configName %s' % hostname
		print 'nodeNum 1'
		print 'Init 100 100 1600 900'
		print 'exec %s %s/bin/dvdplayer -vo sage -af volume=20 ' \
			'-alang en,de,fr -loop 0 ' \
			'dvd://1' % (host, sagedir)
		print 'nwProtocol %s/lib/tvTcpModule.so' % sagedir
		print '}'
		print
		print 'VNCViewer {'
		print 'configName %s' % hostname
		print 'nodeNum 1'
		print 'Init 100 100 1024 768'
		print 'exec %s %s/bin/VNCViewer' % (host, sagedir)
		print 'nwProtocol %s/lib/tvTcpModule.so' % sagedir
		print '}'
		print
		print 'endList'
		print
		print 'tileConfiguration stdtile.conf'
		print 'receiverBaseSyncPort 12000'
		print 'receiverBufNum 4'
		print 'receiverStreamPort 21000'
		print 'fullScreen 1'
		print 'sailBaseSyncPort 11000'









# $Id: __init__.py,v 1.19 2012/05/06 05:49:47 phil Exp $
#
# This script began life as the autodmx.conf mothersip configuration from 
# the Chromium source code, and inherits the following copyright.
#
# Copyright (c) 2001, Stanford University
# All rights reserved 
#
# All additions to the base code are subject to the following copyright.
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.5 (Mamba)
# 		         version 6.0 (Mamba)
# 
# Copyright (c) 2000 - 2012 The Regents of the University of California.
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
# Revision 1.19  2012/05/06 05:49:47  phil
# Copyright Storm for Mamba
#
# Revision 1.18  2011/07/23 02:31:40  phil
# Viper Copyright
#
# Revision 1.17  2010/09/07 23:53:30  bruno
# star power for gb
#
# Revision 1.16  2009/06/17 18:07:04  mjk
# - viz commands gone
# - tile commands now
#
# Revision 1.15  2009/06/03 01:23:23  mjk
# - Now using the idea of modes for the wall (e.g. simple, sage, cglx)
# - Simple (chromium) and Sage modes work
# - Requires root to do a "rocks sync viz mode=??" to switch
# - "rocks enable/disable hidebezels" is chromium specific
#   The command line needs to change to reflect this fact
# - Tile-banner tell you the resolution and mode node
# - Sage works (surprised)
# - Removed autoselect of video mode on first boot, started to crash nodes
#
# Revision 1.14  2009/05/30 00:12:06  mjk
# remove dmx and fvwm
#
# Revision 1.13  2009/05/30 00:02:26  mjk
# *** empty log message ***
#
# Revision 1.12  2009/05/01 19:07:31  mjk
# chimi con queso
#
# Revision 1.11  2008/10/18 00:56:21  mjk
# copyright 5.1
#
# Revision 1.10  2008/03/06 23:42:02  mjk
# copyright storm on
#
# Revision 1.9  2007/11/16 00:21:13  mjk
# add array SPU for google earth (needs testing)
#
# Revision 1.8  2007/10/30 18:28:14  mjk
# - Fix whitespace error (start chromium)
# - Remove PPI stuff from the create/list viz layout commands
#
# Revision 1.7  2007/10/03 22:19:58  mjk
# *** empty log message ***
#
# Revision 1.6  2007/09/19 13:28:58  mjk
# Swiss Viss
#
# Revision 1.5  2007/09/19 11:35:08  mjk
# more swiss changes
#
# Revision 1.4  2007/09/17 15:23:28  mjk
# Zurich fixes
#
# Revision 1.3  2007/08/21 19:24:13  mjk
# *** empty log message ***
#
# Revision 1.2  2007/08/08 19:18:45  bruno
# fix fix katz's of the excellent documentation by w/ vi editor.
#
# Revision 1.1  2007/08/03 21:48:10  mjk
# *** empty log message ***
#
# Revision 1.2  2007/07/30 23:11:29  mjk
# beta time
#
# Revision 1.1  2007/07/27 23:33:50  mjk
# *** empty log message ***
#

import os
import sys
import string
import random
import rocks.commands.start

sys.path.append(os.path.join(os.sep, 'opt', 'viz', 'share', 'cr', 
	'mothership', 'server'))
from mothership import *


class Command(rocks.commands.start.command):
	"""
	Starts a Chromium application either inside or outside of DMX. This
	command is used internally by the system (by scanning the user's
	~/.crconfig file) and is of limited value when called directly by the
	user.
	
	<arg type='string' name='app'>
	Name of the GL application.
	</arg>
	
	<arg type='int' name='port'>
	Mothership port number.
	</arg>
	
	<param type='int' name='port'>
	Same as port argument.
	</param>
	
	<param type='int' name='mtu'>
	Size in KByte for Chromium MTU (default is 10MB).
	</param>
	
	<example cmd="start crapp glxgears 10075">
	Start glxgears using chromium using mothership on port 10075
	</example>
	"""

	MustBeRoot = 0

	def run(self, params, args):
		
		(args, mothershipPort) = self.fillPositionalArgs(('port',))
		
		if len(args) != 1:
			self.abort('must supply application')

		app = args[0]
	
		(mtu,) = self.fillParams([ ('mtu', 10*1024) ])

		mothershipPort	= int(mothershipPort)
		mtu		= int(mtu)

		layout = eval(self.command('report.tile'))

		localHostname = self.db.getHostname()

		cr = CR()
		cr.MTU(mtu*1024)

		tilesortspu = SPU('tilesort')
		clientnode  = CRApplicationNode()
		clientnode.SetApplication(app)
		clientnode.AddSPU(SPU('array'))
		clientnode.AddSPU(tilesortspu)
		clientnode.Conf('show_cursor', 1)

		serverPort = random.randint(7000, 7099)

		for tile in layout:
			servernode = CRNetworkNode(tile['name'])
			renderspu  = SPU('render')
			renderspu.Conf('display_string', '%s:%s' % 
				(tile['name'], tile['display']))
			renderspu.Conf('show_cursor', 1)
			renderspu.Conf('fullscreen', 1)
			renderspu.Conf('borderless', 1)
			renderspu.Conf('window_geometry', 
				[0, 0, tile['xres'], tile['yres']])
			servernode.AddTile(tile['xoffset'], tile['yoffset'],
				tile['xres'], tile['yres'])
					
			servernode.AddSPU(renderspu)
			cr.AddNode(servernode)

			servernode.AutoStart(["/usr/bin/ssh", '-x',
				tile['name'],
			 	"bash --login -c "
				"'env DISPLAY=:%s %s -mothership %s:%d'" %
				(tile['display'],
				os.path.join(crbindir, 'crserver'),
				localHostname, mothershipPort)])

			tilesortspu.AddServer(servernode, protocol='tcpip',
				port=serverPort + 
					int(float(tile['display']) * 10))

		cr.AddNode(clientnode)
		cr.Go(mothershipPort)


			
		

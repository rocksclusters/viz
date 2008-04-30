# $Id: __init__.py,v 1.10 2008/03/06 23:42:02 mjk Exp $
#
# This script began from the autodmx.conf mothersip configuration from 
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
	
		# Check the return code of dmx_config to see if
		# dmx is running.  In either case we still get the
		# configuration from ~/.dmx_config.
		
		if not os.system(os.path.join(crbindir, 'dmx_config')):
			dmx = 1
		else:
			self.command('start.dmx', [ 'wm=/bin/true' ])
			dmx = 0

		filename = os.path.join(os.environ['HOME'], '.dmx_config')
		file = open(filename, 'r')
		cfg = file.read()
		file.close()
		layout = eval(cfg)
		if not cfg:
			self.abort('cannot read tile layout')

		
		# The origin for DMX is the upper-left, but for Chromium
		# the origin is the lower left.  To fix this we need to
		# know the the height of the wall. 
		# (only required w/o DMX).

		yoriginMax = 0
		for tile in layout:
			if tile['yorigin'] > yoriginMax:
				yoriginMax = tile['yorigin']
				
		wallHeight = 0
		for tile in layout:
			if tile['yorigin'] == yoriginMax:
				height = tile['yorigin'] + tile['height']
				if height > wallHeight:
					wallHeight = height


			
		serverPort = random.randint(7000, 7099)
		localHostname = self.db.getHostname()

		cr = CR()
		cr.MTU(mtu*1024)

		tilesortspu = SPU('tilesort')
		clientnode  = CRApplicationNode()
		clientnode.SetApplication(app)
		clientnode.AddSPU(SPU('array'))
		clientnode.AddSPU(tilesortspu)
		clientnode.Conf('show_cursor', 1)
		if dmx:
			tilesortspu.Conf('use_dmx', 1)
			clientnode.Conf('track_window_size', 1)
			clientnode.Conf('track_window_position', 1)

		for tile in layout:
			host = tile['display'].split(':')[0]

			servernode = CRNetworkNode(host)
			renderspu  = SPU('render')
			renderspu.Conf('display_string', tile['display'])
			renderspu.Conf('show_cursor', 1)
			if dmx:
				renderspu.Conf('render_to_app_window', 1)
				servernode.AddTile(0, 0,
					tile['width'], tile['height'])
				servernode.Conf('use_dmx', 1)
			else:
				renderspu.Conf('fullscreen', 1)
				renderspu.Conf('borderless', 1)
				renderspu.Conf( 'window_geometry', 
					[0, 0, tile['width'], tile['height']])
				servernode.AddTile(tile['xorigin'],
					wallHeight - (tile['yorigin'] + 
						tile['height']),
					tile['width'],
					tile['height'])
					
			servernode.AddSPU(renderspu)
			cr.AddNode(servernode)

			servernode.AutoStart(["/usr/bin/ssh", '-x', host,
			 	"bash --login -c "
				"'env DISPLAY=:0.0 %s -mothership %s:%d'" %
				(os.path.join(crbindir, 'crserver'),
				localHostname, mothershipPort)])

			tilesortspu.AddServer(servernode, protocol='tcpip',
				port=serverPort )

		cr.AddNode(clientnode)
		cr.Go(mothershipPort)


			
		

# $Id: __init__.py,v 1.8 2008/07/12 00:38:13 mjk Exp $
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
# Revision 1.8  2008/07/12 00:38:13  mjk
# *** empty log message ***
#
# Revision 1.7  2008/03/06 23:42:02  mjk
# copyright storm on
#
# Revision 1.6  2007/10/03 22:19:58  mjk
# *** empty log message ***
#
# Revision 1.5  2007/09/20 15:46:30  mjk
# cleanup lock file
#
# Revision 1.4  2007/09/19 13:28:58  mjk
# Swiss Viss
#
# Revision 1.3  2007/09/19 11:35:08  mjk
# more swiss changes
#
# Revision 1.2  2007/09/04 22:47:35  mjk
# move dmxrc generation to rcl
#
# Revision 1.1  2007/08/30 17:24:37  mjk
# *** empty log message ***
#

import rocks.commands.start
import popen2
import os

class Command(rocks.commands.start.command):
	"""
	Starts a DMX session.
	
	<param name="display" type="int">
	X11 display numbers (default is 1).
	</param>
	
	<param name="hidebezels" type="bool">
	Set the TRUE to hide the LCD bezels (default is false).
	</param>
	
	<param name="wm" type="string">
	Name of window manager to use (default is fvwm).
	</param>
	
	<example cmd="start dmx">
	</example>
	"""

	MustBeRoot = 0
	
	def run(self, params, args):
	
		(xdmx, wm, outputDisplay) = self.fillParams([
			('dmx', '/usr/bin/Xdmx'),
			('wm', '/opt/rocks/bin/fvwm'),
			('display', 1)
			])

		if os.path.exists(os.path.join(os.environ['HOME'],
			'.hidebezels')):
			config = 'hide_bezels'
			self.command('enable.hidebezels', [])
		else:
			config = 'show_bezels'
			self.command('disable.hidebezels', [])

		try:
			inputDisplay = os.getenv('DISPLAY')
		except:
			self.Abort('X11 not running')
			
		os.environ['WINDOWMANAGER'] = wm

		dmxlayout = os.path.join(os.environ['HOME'], '.dmxrc')
		
		if not os.path.exists(dmxlayout):
			file = open(dmxlayout, 'w')
			file.write(self.command('list.dmx.layout'))
			file.close()

		cmd = 'startx -- %s :%d -config %s -configfile %s -input %s' % \
			(xdmx, outputDisplay, config, dmxlayout, inputDisplay)
			
		r,w = popen2.popen2(cmd)
			
		for line in r.readlines():
			self.addText(line[:-1])

		if os.path.exists('/tmp/.X%d-lock' % outputDisplay):
			os.unlink('/tmp/.X%d-lock' % outputDisplay)
		

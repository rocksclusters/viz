# $Id: __init__.py,v 1.4 2010/09/07 23:53:30 bruno Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4 (Maverick)
# 
# Copyright (c) 2000 - 2010 The Regents of the University of California.
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
# Revision 1.4  2010/09/07 23:53:30  bruno
# star power for gb
#
# Revision 1.3  2009/05/01 19:07:32  mjk
# chimi con queso
#
# Revision 1.2  2008/10/18 00:56:21  mjk
# copyright 5.1
#
# Revision 1.1  2008/06/03 23:10:17  mjk
# - Added stop host sage
# - Added stop sage
#

import rocks.commands
import os
import string
import popen2

class Command(rocks.commands.stop.host.command):
	"""
	Stops a SAGE session an a given host

        <arg optional='1' type='string' name='host' repeat='1'>
        Zero, one or more host names.
        </arg>
	
	<example cmd="stop sage host tile">
	Kills SAGE processes on the tile nodes
	</example>
	"""

	MustBeRoot = 0
	
	def run(self, params, args):
	
		# Split into two commands to force the backend to kill
		# before the frontend.

		try:
			del os.environ['DISPLAY']
		except:
			pass
		
		for host in self.getHostnames(args):
			self.stopSage(host)
			
	def traverse(self, dict, pid, list):
		if dict.has_key(str(pid)):
			for id in dict[str(pid)]:
				self.traverse(dict, id, list)
		list.append(str(pid))
		
	def stopSage(self, host):

		sageDir  = os.getenv('SAGE_DIRECTORY')
		ptree	 = {}
		children = []
		master	 = -1

		output = self.command('run.host', 
			[ host, 'ps --no-headers -u $USER -fw' ])
		for line in output.split('\n'):

			try:
	                	tokens	= string.split(line[:-1])
        	        	pid	= int(tokens[1])
                		ppid	= tokens[2]
                		cmd	= string.join(tokens[7:])
                	except:
                		continue
                	
                	# Use the sageLauncher to find the fsManager
                	# We leave the master running since it's the GUI
                	
                	if cmd.find('sageLauncher') > 0:
                		master = pid
                	elif cmd.find(sageDir) >= 0:
                		children.append(pid)
                	elif cmd.find('SAGE_DIRECTORY') >= 0:
                		children.append(pid)
                		
                	if ptree.has_key(ppid):
                		ptree[ppid].append(pid)
                	else:
                		ptree[ppid] = [ pid ]

		if master > 0 and ptree.has_key(str(master)):              	
	                children.extend(ptree[str(master)])

		# For any process we flagged as child find all of their
		# children as well the kill them all.
		
		list = []
                for pid in children:
                	self.traverse(ptree, pid, list)
		list.sort()
		
                self.addText('kill %s:%s\n' % (host, string.join(list)))
                self.command('run.host',
                	[ host, 'kill %s' % string.join(list) ])
                self.command('run.host',
                	[ host, 'kill -9 %s' % string.join(list) ])


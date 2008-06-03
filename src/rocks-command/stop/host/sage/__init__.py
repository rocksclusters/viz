# $Id: __init__.py,v 1.1 2008/06/03 23:10:17 mjk Exp $
#
# @Copyright@
# @Copyright@
#
# $Log: __init__.py,v $
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


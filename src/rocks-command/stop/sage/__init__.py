# $Id: __init__.py,v 1.5 2008/06/03 23:10:17 mjk Exp $
#
# @Copyright@
# @Copyright@
#
# $Log: __init__.py,v $
# Revision 1.5  2008/06/03 23:10:17  mjk
# - Added stop host sage
# - Added stop sage
#

import rocks.commands.stop
import os
import string
import popen2

class Command(rocks.commands.stop.command):
	"""
	Stops a SAGE session.
	
	<example cmd="stop sage">
	</example>
	"""

	MustBeRoot = 0
	
	def run(self, params, args):
	
		# Split into two commands to force the backend to kill
		# before the frontend.
		
		self.addText(self.command('stop.host.sage', [ 'tile' ]))
		self.addText(self.command('stop.host.sage', [ 'localhost' ]))
			

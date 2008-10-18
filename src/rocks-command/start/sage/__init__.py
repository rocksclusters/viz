# $Id: __init__.py,v 1.8 2008/10/18 00:56:21 mjk Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		           version 5.1  (VI)
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
# Revision 1.8  2008/10/18 00:56:21  mjk
# copyright 5.1
#
# Revision 1.7  2008/07/03 01:14:13  mjk
# - fix path to xrandr
# - call xrandr twice (current mode, desired mode)
#   otherwise it fails to set the desired mode
# - sage respects the hidebezels mode
#
# Revision 1.6  2008/05/31 02:57:37  mjk
# - SAGE is back and works (mostly)
# - DMX building from source (in progress)
# - Updated nvidia driver
#
# Revision 1.4  2007/08/05 04:18:39  bruno
# whoa! a checkin by bruno!
#
# fix docs.
#
# Revision 1.3  2007/07/30 23:11:29  mjk
# beta time
#
# Revision 1.2  2007/07/27 17:30:22  mjk
# checkpoint
#
# Revision 1.1  2007/07/24 02:11:36  mjk
# - sage2 starting to work
#

import rocks.commands.start
import os

class Command(rocks.commands.start.command):
	"""
	Starts a SAGE session.
	
	<example cmd="start sage">
	</example>
	"""

	MustBeRoot = 0
	
	def run(self, params, args):
	
		sageOpt = '/opt/sage'
		sageDir = os.getenv('SAGE_DIRECTORY')
		if not sageDir:
			self.Abort('SAGE_DIRECTORY not defined')

		fsManagerConf	= os.path.join(sageDir, 'bin',
					       'fsManager.conf')
		stdTileConf	= os.path.join(sageDir, 'bin',
					       'stdtile.conf')
		stdTileHBConf	= os.path.join(sageDir, 'bin',
					       'hide_bezels.conf')
		stdTileSBConf	= os.path.join(sageDir, 'bin',
					       'show_bezels.conf')
		audioConf	= os.path.join(sageDir, 'bin',
					       'audio.conf')
		
		# Create a local copy of SAGE (used to be lndir)
		
		if not os.path.exists(sageDir):
			os.system('cp -a %s %s' % (sageOpt, sageDir))
			os.unlink(fsManagerConf)
			os.unlink(stdTileConf)

		# Determine what bezel mode we are in. Then no matter
		# what reset the system to show bezel mode.  We do
		# this so the hardware (twinview mode) bezel hiding
		# doesn't run under SAGE. We touch the ~/.hidebezels
		# file after disabling to make sure we leave the system
		# in the right state.

		hb = os.path.join(os.environ['HOME'], '.hidebezels')
		if os.path.exists(hb):
			self.command('disable.hidebezels', [])
			os.system('touch %s' % hb)
			os.system('ln -s %s %s' % (stdTileHBConf, stdTileConf))
		else:
			self.command('disable.hidebezels', [])
			os.system('ln -s %s %s' % (stdTileSBConf, stdTileConf))

		
		if not os.path.exists(fsManagerConf):
			file = open(fsManagerConf, 'w')
			file.write(self.command('report.sage.fsmanager'))
			file.close()

		if not os.path.exists(stdTileHBConf):
			file = open(stdTileConf, 'w')
			file.write(self.command('report.sage.layout',
						['hidebezels=1']))
			file.close()

		if not os.path.exists(stdTileSBConf):
			file = open(stdTileConf, 'w')
			file.write(self.command('report.sage.layout',
						['hidebezels=0']))
			file.close()

		if not os.path.exists(audioConf):
			file = open(audioConf, 'w')
			file.write(self.command('report.sage.audio'))
			file.close()
			
		os.chdir(os.path.join(sageDir, 'bin'))
		os.system('./sage &')
			

# $Id: __init__.py,v 1.7 2008/07/03 01:14:13 mjk Exp $
#
# @Copyright@
# @Copyright@
#
# $Log: __init__.py,v $
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
			

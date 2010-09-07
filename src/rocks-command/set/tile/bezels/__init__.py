# $Id: __init__.py,v 1.2 2010/09/07 23:53:30 bruno Exp $
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
# Revision 1.2  2010/09/07 23:53:30  bruno
# star power for gb
#
# Revision 1.1  2009/06/10 01:35:19  mjk
# *** empty log message ***
#

import string
import rocks.commands


class Command(rocks.commands.set.tile.command):
	"""
	Sets the default tile bezel sizes in pixels.
	"""

        def run(self, params, args):
		(args, left, right, top, bottom) = self.fillPositionalArgs(
			('left', 'right', 'top', 'bottom'))

		if not left:
			self.abort('must supply left bezel width')
		if not right:
			self.abort('must supply right bezel width')
		if not top:
			self.abort('must supply top bezel height')
		if not bottom:
			self.abort('must supply bottom bezel height')
		try:
			int(left)
		except:
			self.abort('invalid width %s' % left)
		try:
			int(right)
		except:
			self.abort('invalid width %s' % right)
		try:
			int(top)
		except:
			self.abort('invalid height %s' % top)
		try:
			int(bottom)
		except:
			self.abort('invalid height %s' % bottom)



		# If no tile listed change the default for all tiles
		# Otherwise change the tile-specific attributes

		if not args:
			self.command('set.appliance.attr', [ 'tile',
				'viz_tile_left_bezel', left ])
			self.command('set.appliance.attr', [ 'tile',
				'viz_tile_right_bezel',right ])
			self.command('set.appliance.attr', [ 'tile',
				'viz_tile_top_bezel', top ])
			self.command('set.appliance.attr', [ 'tile',
				'viz_tile_bottom_bezel', bottom ])
		else:
			for (host, display) in self.getTileNames(args):
				tile = '%s:%s' % (host, display)
				self.command('set.appliance.attr', [ tile,
					'viz_tile_left_bezel', left ])
				self.command('set.appliance.attr', [ tile,
					'viz_tile_right_bezel',right ])
				self.command('set.appliance.attr', [ tile,
					'viz_tile_top_bezel', top ])
				self.command('set.appliance.attr', [ tile,
					'viz_tile_bottom_bezel', bottom ])





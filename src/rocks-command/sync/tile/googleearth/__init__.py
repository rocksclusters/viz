# $Id: __init__.py,v 1.4 2011/07/23 02:31:40 phil Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4.3 (Viper)
# 
# Copyright (c) 2000 - 2011 The Regents of the University of California.
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
# 	Development Team at the San Diego Supercomputer Center at the
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
# Revision 1.4  2011/07/23 02:31:40  phil
# Viper Copyright
#
# Revision 1.3  2011/01/14 18:52:45  mjk
# New version on Google Earth (just released
#
# Revision 1.2  2010/12/18 00:27:34  mjk
# *** empty log message ***
#
# Revision 1.1  2010/10/07 19:41:47  mjk
# - use dpi instead of pixels to measure offsets
# - added horizontal|vertical shift attrs to deal with uneven walls (ours)
# - removed sage
# - added support for Google's liquid galaxy
#

import os
import shutil
import string
import rocks.commands.sync.tile

class Command(rocks.commands.sync.tile.command):
        """
        Updates the drivers.ini file to setup syncronization between all the
        google earth instances running on the tile displays with the frontend
        as the master.

        <example cmd="sync tile googleearth">
        </example>
        """

	def configureMaster(self):
		"""Patch the drivers.ini file that came with Google Earth to add the
		required ViewSync directives.  A backup of this file remains in /etc/X11,
		and the original is updated.
		"""
		
		fin  = open('/opt/google/earth/free/drivers.ini', 'r')
		fout = open('/etc/X11/ge-drivers.ini',      'w')
		
		for line in fin.readlines():
			fout.write(line)
			if line.find('SETTINGS {') != 0:
				continue
			fout.write('\tViewSync/send = true\n')
			fout.write('\tViewSync/receive = false\n')

			fout.write('\tViewSync/hostname = %s\n' %
				   self.db.getHostAttr('localhost',
						       'Kickstart_PrivateBroadcast'))
                        fout.write('\tViewSync/port = 21567\n')
			fout.write('\n')
			fout.write('\tViewSync/horizFov    = 60\n')
                        fout.write('\tViewSync/rollOffset  = 0\n')
                        fout.write('\tViewSync/yawOffset   = 0\n')
			fout.write('\tViewSync/pitchOffset = 0\n')
			fout.write('\n')


		fin.close()
		fout.close()

		shutil.copy('/etc/X11/ge-drivers.ini', '/opt/google/earth/free/drivers.ini')

		
	def configureTile(self, tile, yawOffset, pitchOffset):
		(host, display) = tile.split(':')
		
		attrs = self.getTileAttrs(tile)

		if not os.path.exists('/etc/X11/ge-drivers.ini'):
			self.configureMaster()
			
		fin = open('/etc/X11/ge-drivers.ini', 'r')
		list = []
		for line in fin.readlines():

			if line.find('ViewSync/') == -1:
				list.append(line)
		
			elif line.find('ViewSync/send') != -1:
				list.append('\tViewSync/send = false\n')

			elif line.find('ViewSync/receive') != -1:
				list.append('\tViewSync/receive = true\n')

                        elif line.find('ViewSync/hostname') != -1:
				attr = attrs.get('Kickstart_PrivateBroadcast')
                                list.append('\tViewSync/hostname = %s\n' % attr)

                        elif line.find('ViewSync/port') != -1:
                                list.append('\tViewSync/port = 21567\n')

                        elif line.find('ViewSync/horizFov') != -1:
				hfov = attrs.get('viz_googe_earth_horiz_fov')
				if not hfov:
					hfov = 16
                                list.append('\tViewSync/horizFov = %f\n' % hfov)

                        elif line.find('ViewSync/rollOffset') != -1:
                                list.append('\tViewSync/rollOffset = 0\n')

                        elif line.find('ViewSync/yawOffset') != -1:
                                list.append('\tViewSync/yawOffset = %f\n' % yawOffset)

                        elif line.find('ViewSync/pitchOffset') != -1:
                                list.append('\tViewSync/pitchOffset = %f\n' % pitchOffset)

			else:
				list.append(line)

		fin.close()
			
		filename = '/etc/X11/ge-drivers.ini-%s' % tile
		fout = open(filename, 'w')
		for line in list:
			fout.write(line)
		fout.close()

                os.system('scp -q %s %s:/opt/google/earth/free/drivers.ini:%s' % (filename, host, display))


        def run(self, params, args):

                tiles = []
                for (server, display) in self.getTileNames(args):
                        tiles.append('%s:%s' % (server, display))

                list = eval(self.command('report.tile'))
		layout = {}
		for i in range(0, len(list)):
			name = '%s:%s' % (list[i]['name'], list[i]['display'])
			layout[name] = list[i]

		# The Horizontal Field Of View is the only setting.  Using
		# the video resolution determine the Vertical FOV.
		# All displays are assumed to be the same resolution so 
		# just grab data from the first tile.

                hfov = self.db.getHostAttr('localhost', 'viz_googe_earth_horiz_fov')
   	        if not hfov:
        	        hfov = 16
                res   = self.getTileAttr(tiles[0], 'viz_tile_resolution').split('x')
                ratio = float(res[0]) / int(res[1]) # X:Y
		vfov  = float(hfov) / ratio

		for tile in tiles:
			xoffset = layout[tile]['xoffset']
			yoffset = layout[tile]['yoffset']
			xres    = layout[tile]['xres']
			yres    = layout[tile]['yres']

			ppd = float(xres) / hfov		# pixels per degree
			yawOffset = -float(xoffset) / ppd	# convert pixels into -degrees

			ppd = float(yres) / vfov		# pixels per degree
			bp = layout[tile]['y'] * 16		# pixels lost on menu bars (cannot disable)
			pitchOffset = (float(yoffset) + bp) / ppd	# convert pixels into degrees

#			pr = float(yres) / vfov			# pixels per degree (vert)
#			pm = layout[tile]['y'] * 16		# pixels consumed by menu bar (cannot disable)
#			p1 = (int(yoffset) / yres) * vfov	# pitch not including bezels
#			p2 = float(yoffset) / yres		# pitch of bezels only
#			pitchOffset = float(pm)/yres + p1 + p2


			self.configureTile(tile, yawOffset, pitchOffset)
			





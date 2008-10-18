#!/opt/rocks/bin/python
#
# $Id: tile-banner.py,v 1.14 2008/10/18 00:56:20 mjk Exp $
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
# $Log: tile-banner.py,v $
# Revision 1.14  2008/10/18 00:56:20  mjk
# copyright 5.1
#
# Revision 1.13  2008/03/06 23:42:01  mjk
# copyright storm on
#
# Revision 1.12  2007/10/01 20:36:30  mjk
# remove all traces of sage (for now)
#
# Revision 1.11  2007/08/31 21:54:23  mjk
# *** empty log message ***
#
# Revision 1.10  2007/08/30 00:55:32  mjk
# new banner, less burn in, better logo
#
# Revision 1.9  2007/06/23 04:04:05  mjk
# mars hill copyright
#
# Revision 1.8  2006/09/11 22:50:39  mjk
# monkey face copyright
#
# Revision 1.7  2006/08/10 00:12:14  mjk
# 4.2 copyright
#
# Revision 1.6  2006/01/16 06:49:16  mjk
# fix python path for source built foundation python
#
# Revision 1.5  2005/10/12 18:11:18  mjk
# final copyright for 4.1
#
# Revision 1.4  2005/09/16 01:04:56  mjk
# updated copyright
#
# Revision 1.3  2005/08/08 21:25:04  mjk
# foundation
#
# Revision 1.2  2005/05/24 21:24:08  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2004/10/07 22:53:24  mjk
# Added tile-banner to label nodes by hostname
# Viz user profile calls tile-banner
#


import os
import sys
import time
import string
import socket
import pygtk
import gtk
import gobject
import random
import rocks.app

class App(rocks.app.Application):

		
	def __init__(self, argv):
		rocks.app.Application.__init__(self, argv)
		imagepath = os.path.join(os.sep, 'opt', 'viz', 'lib', 'images')
			
		logo = [ ]
		for i in range(0, 6):
			logo.append(gtk.Image())
		logo[0].set_from_file(os.path.join(imagepath, 
			'rocks-logo-red.png'))
		logo[1].set_from_file(os.path.join(imagepath,
			'rocks-logo-yellow.png'))
		logo[2].set_from_file(os.path.join(imagepath,
			'rocks-logo-green.png'))
		logo[3].set_from_file(os.path.join(imagepath, 
			'rocks-logo-cyan.png'))
		logo[4].set_from_file(os.path.join(imagepath,
			'rocks-logo-blue.png'))
		logo[5].set_from_file(os.path.join(imagepath,
			'rocks-logo-magenta.png'))

		self.color = [
			( 0xff, 0x00, 0x00 ),	# R
			( 0xff, 0xff, 0x00 ),	# Y
			( 0x00, 0xff, 0x00 ),	# G
			( 0x00, 0xff, 0xff ),	# C
			( 0x00, 0x00, 0xff ),	# B
			( 0xff, 0x00, 0xff )	# M
			]
		
		self.label = [ ]
		self.box = []
		
		for i in range(0, 6):
			self.label.append(gtk.Label())

		for i in range(0, 6):
			self.box.append(gtk.VBox())
			self.box[i].pack_start(logo[(i+3)%6])
			self.box[i].pack_start(self.label[i])


	def loop(self):
		"""Run once a second after processing outstanding GTK
		events."""
		
		if random.randint(0, 100) < 80:
			self.moveLogo()
		else:
			self.index = (self.index + 1) % 6
			self.changeColor(random.randint(0,5))


	def moveLogo(self):
		(winWidth, winHeight) = self.window.get_size()
		screenWidth  = gtk.gdk.screen_width()
		screenHeight = gtk.gdk.screen_height()
		
		maxX = (screenWidth - winWidth)
		maxY = (screenHeight - winHeight)
		
		newX = random.randint(0, maxX)
		newY = random.randint(0, maxY)
		
		self.window.move(newX, newY)

	
	def changeColor(self, index):
		currBox = self.box[index]
		prevBox = self.window.get_child()
		if prevBox:
			self.window.remove(prevBox)
			prevBox.unparent()

		self.window.add(currBox)

		(r, g, b) = self.color[index]
		if not r:
			r = 0x3f
		if not g:
			g = 0x3f
		if not b:
			b = 0x3f
		rgb = ((r<<16) + (g<<8) + b) & 0x7f7f7f
		(r, g, b) = self.color[index]
		r = ~r & 0xff
		g = ~g & 0xff
		b = ~b & 0xff
		if not r:
			r = 0x3f
		if not g:
			g = 0x3f
		if not b:
			b = 0x3f
		notrgb = ((r<<16) + (g<<8) + b) & 0x7f7f7f
		
		
		self.window.modify_bg(gtk.STATE_NORMAL, 
			gtk.gdk.color_parse('#%06x' % rgb))
		self.label[index].modify_fg(gtk.STATE_NORMAL, 
			gtk.gdk.color_parse('#%06x' % notrgb))

		self.window.show_all()
		os.system('xsetroot -solid "#%06x"' % rgb)

	def run(self):
	
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_position(gtk.WIN_POS_CENTER)

		self.index = random.randint(0,5)
		self.changeColor(self.index)
		
		display = self.window.get_screen().get_display().get_name()
		hostname = socket.gethostname().split('.')[0]
		
		for i in range(0, 6):
			self.label[i].set_markup(
				'<span weight="bold" face="sans" size="64000">'\
				'%s%s</span>' % (hostname, display))

		gobject.timeout_add(10000, callback, self)
		gtk.main()



def callback(o):
	o.loop()
	return True


app = App(sys.argv)
app.parseArgs()
app.run()

# $Id: __init__.py,v 1.4 2012/05/06 05:49:45 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.5 (Mamba)
# 		         version 6.0 (Mamba)
# 
# Copyright (c) 2000 - 2012 The Regents of the University of California.
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
# Revision 1.4  2012/05/06 05:49:45  phil
# Copyright Storm for Mamba
#
# Revision 1.3  2011/07/23 02:31:39  phil
# Viper Copyright
#
# Revision 1.2  2010/09/07 23:53:28  bruno
# star power for gb
#
# Revision 1.1  2009/06/10 01:35:19  mjk
# *** empty log message ***
#
# Revision 1.10  2009/06/06 00:55:31  mjk
# checkpoint
#
# Revision 1.9  2009/05/29 19:35:41  mjk
# *** empty log message ***
#
# Revision 1.8  2009/05/17 13:41:53  mjk
# checkpoint before zurich
#
# Revision 1.7  2009/05/09 23:04:08  mjk
# - tile-banner use rand seed to sync the logo on multi-head nodes
# - Xclients is python, and disables screensaver (again)
# - xorg.conf on tiles turns off DPMS
# - tiles come up in a completely probed mode (resolution not set)
# - all else is just broken and this is a check point
#
# Revision 1.6  2009/05/01 19:07:31  mjk
# chimi con queso
#
# Revision 1.5  2008/10/18 00:56:20  mjk
# copyright 5.1
#
# Revision 1.4  2008/07/08 19:40:03  mjk
# - build dmx again
# - added dump viz layout (saxutils.escape quoted for restore roll)
#
# Revision 1.3  2008/03/06 23:42:02  mjk
# copyright storm on
#
# Revision 1.2  2007/10/30 18:28:14  mjk
# - Fix whitespace error (start chromium)
# - Remove PPI stuff from the create/list viz layout commands
#
# Revision 1.1  2007/08/31 20:53:06  mjk
# move to rcl
#
# Revision 1.10  2007/08/10 23:38:56  mjk
# *** empty log message ***
#
# Revision 1.9  2007/06/23 04:04:05  mjk
# mars hill copyright
#
# Revision 1.8  2006/09/11 22:50:39  mjk
# monkey face copyright
#
# Revision 1.7  2006/08/10 17:58:09  mjk
# fix default hres, vres
#
# Revision 1.6  2006/08/10 00:12:14  mjk
# 4.2 copyright
#
# Revision 1.5  2006/06/29 19:56:45  mjk
# added viz-reconfig
#
# Revision 1.4  2006/06/23 22:32:18  mjk
# twinview changes
#
# Revision 1.3  2006/06/19 23:13:21  mjk
# *** empty log message ***
#
# Revision 1.2  2006/05/02 01:52:22  mjk
# fix tabs
#
# Revision 1.1  2006/05/02 01:45:42  mjk
# added tilelayout
#

import os
import sys
import string
import xml
import popen2
import socket
import rocks.util
import rocks.graph
import rocks.commands
from xml.sax import saxutils
from xml.sax import handler
from xml.sax import make_parser

class Command(rocks.commands.add.tile.command):
	"""
	Creates the Tile Layout table in the cluster database.  If an XML
	file is provided the layout is taken from this file, otherwise a default 
	layout is computed from the rack and cabinet number of all the tiles.
	
	<arg type='string' name='file' required='no'>
	XML description of the wall.
	</arg>
	
	<example cmd='create tile layout layout.xml'>
	Creates the layout from the layout.xml file.
	</example>

	"""

	def insertDisplay(self, display, x, y):
		self.db.execute("""insert tiles (node, name, x, y) values 
			((select id from nodes where name="%s"), %s, %d, %d)"""
			% (self.db.getHostname(display.hostname),
			   display.display, x, y))

	def run(self, params, args):

		if len(args):
			filename = args[0]
			try:
				file = open(filename, 'r')
			except:
				self.abort('cannot open file', filename)
			xml = string.join(file.readlines())
		else:
			self.abort('no input')

		parser  = make_parser()
		handler = LayoutHandler()
		parser.setContentHandler(handler)
		parser.feed(xml)
		displays = handler.getDisplays()
		(maxY, maxX) = handler.getGeometry()

		if self.db.execute('select * from tiles') > 0:
			self.abort('tiles already defined')

		for x in range(0, maxX):
			for y in range(maxY -1, -1, -1):
				i = (x*maxY)+y
				self.insertDisplay(displays[i], x, maxY-y-1)




class LayoutHandler(handler.ContentHandler,
	handler.DTDHandler,
	handler.EntityResolver,
	handler.ErrorHandler):

	def __init__(self):
		handler.ContentHandler.__init__(self)
		self.cols	= 0
		self.rows	= 0
		self.displays	= []		

	def getGeometry(self):
		return (self.rows, self.cols)
		
	def getDisplays(self):
		return self.displays

	# <col>
	def startElement_col(self, name, attrs):
		self.cols += 1
		self.rows  = 0

	# <display>
	
	def startElement_display(self, name, attrs):
		self.rows += 1
		self.current = rocks.util.Struct()


	def endElement_display(self, name):
		(name, display) = self.text.strip().split(':')

		self.current.hostname = name
		self.current.display = display
		self.displays.append(self.current)

	def startElement(self, name, attrs):
		self.text = ''
		try:
			eval('self.startElement_%s' % name)
		except AttributeError:
			return
		eval('self.startElement_%s(name, attrs)' % name)	

	def endElement(self, name):
		try:
			eval('self.endElement_%s' % name)
		except AttributeError:
			return	
		eval('self.endElement_%s(name)' % name)

	def characters(self, s):
		self.text += s
		



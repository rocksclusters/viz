# $Id: __init__.py,v 1.7 2009/05/09 23:04:08 mjk Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 5.2 (Chimichanga)
# 
# Copyright (c) 2000 - 2009 The Regents of the University of California.
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

class Command(rocks.commands.create.command):
	"""
	Creates the Tile Layout table in the cluster database.  If an XML
	file is provided the layout is taken from this file, otherwise a default 
	layout is computed from the rack and cabinet number of all the tiles.
	
	<arg type='string' name='file' required='no'>
	XML description of the wall.
	</arg>
	
	<example cmd='create viz layout layout.xml'>
	Creates the layout from the layout.xml file.
	</example>
	"""

	def run(self, params, args):

		# If a filename is provided read the XML layout from
		# the files.  Othewise if we are not a tty read the XML
		# layout from the pipe we are connected to (restore roll
		# uses this).  Final case (no data) use the default layout.
		
		if len(args):
			filename = args[0]
			try:
				file = open(filename, 'r')
			except:
				self.abort('cannot open file', filename)
			xml = string.join(file.readlines())
		else:
			if not sys.stdin.isatty:
				xml = ''
				for line in sys.stdin.readlines():
					xml += list
			else:
				xml = self.command('list.viz.layout', [])

		#
		# First Pass: learn row,col geometry of the wall
		#

		parser  = make_parser()
		handler = LayoutHandlerPassOne()
		parser.setContentHandler(handler)
		parser.feed(xml)

		#
		# Second Pass: find diplay and populate database
		#

		geometry = handler.geometry()
		parser  = make_parser()
		handler = LayoutHandlerPassTwo(LayoutDefaults(self), geometry)
		parser.setContentHandler(handler)
		parser.feed(xml)

		self.db.execute('delete from videowall')
		for display in handler.wall():
			self.db.execute("""insert videowall 
				(Node, HCoord, VCoord)
				values ((select id from nodes where name="%s"), 
				%d, %d)""" % 
				(display.host, display.hcoord, display.vcoord))

			# Update for any settings non-default settings.  This
			# keeps all the default settings under the control
			# of mysql.  No defaults are provided from this
			# python code.

			attrs = []
			if display.cardid  != None:
				attrs.append('CardId=%d' % display.cardid)
			if display.lhborder != None:
				attrs.append('LHBorder=%f' % display.lhborder)
			if display.rhborder != None:
				attrs.append('RHBorder=%f' % display.rhborder)
			if display.tvborder != None:
				attrs.append('TVBorder=%f' % display.tvborder)
			if display.bvborder != None:
				attrs.append('BVBorder=%f' % display.bvborder)
			if display.hres    != None:
				attrs.append('HRes=%d' % display.hres)
			if display.vres    != None:
				attrs.append('VRes=%d' % display.vres)
			self.db.execute("""update videowall set %s where
				node=(select id from nodes where name="%s") and
				hcoord=%d and vcoord=%d""" %
				(string.join(attrs, ','),
				display.host,
				display.hcoord, display.vcoord))


class LayoutBase:
	def __init__(self):
		self.lhborder	= None
		self.rhborder	= None
		self.tvborder	= None
		self.bvborder	= None
		self.hres	= None
		self.vres	= None
		self.cardid	= None

class LayoutDisplay(LayoutBase):
	def __init__(self, defaults):
		LayoutBase.__init__(self)
		self.lhborder	= defaults.lhborder
		self.rhborder	= defaults.rhborder
		self.tvborder	= defaults.tvborder
		self.bvborder	= defaults.bvborder
		self.hres	= defaults.hres
		self.vres	= defaults.vres
		self.cardid	= defaults.cardid
		self.hcoord	= 0
		self.vcoord	= 0
		self.host	= None

class LayoutDefaults(LayoutBase):
	def __init__(self, sql):
		LayoutBase.__init__(self)
		self.hres = 800
		self.vres = 600

		

class LayoutHandlerPassOne(handler.ContentHandler,
	handler.DTDHandler,
	handler.EntityResolver,
	handler.ErrorHandler):
	"""
	First Pass parsing of the layout XML file.  All we do here is
	count the number of columns and rows in the file.  This gives
	us the knowledge of the geometry of the wall before we start to
	parse the <display> tags, and lets us assign the row,col to the
	displays.
	"""
	def __init__(self):
		handler.ContentHandler.__init__(self)
		self.cols = 0
		self.rows = 0

	def geometry(self):
		return (self.rows, self.cols)

	# <col>
	def startElement_col(self, name, attrs):
		self.cols += 1
		self.rows  = 0

	# <display>
	def startElement_display(self, name, attrs):
		self.rows += 1


	def startElement(self, name, attrs):
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



class LayoutHandlerPassTwo(handler.ContentHandler,
	handler.DTDHandler,
	handler.EntityResolver,
	handler.ErrorHandler):
	"""
	Sample format:

	<wall>
	        <col>
	                <display host="tile-0-0" card="1"/>
	                <display host="tile-0-0" card="1"/>
	        </col>
	        <col>
	                <display host="tile-0-1" card="1"/>
	                <display host="tile-0-1" card="1"/>
	        </col>
	</wall>
	"""

	def __init__(self, defaults, geometry):
		handler.ContentHandler.__init__(self)
		self.vtiles = geometry[0]	# number of rows (tall)
		self.htiles = geometry[1]	# number of cols (wide)
		self.vcoord = 0			# counting up from bottom
		self.hcoord = 0			# conting up from left
		self.displays = []
		self.defaults = defaults

	def wall(self):
		return self.displays

	# <defaults>

	def startElement_defaults(self, name, attrs):
		if attrs.get('hres'):
			self.defaults.hres = int(attrs.get('hres'))
		if attrs.get('vres'):
			self.defaults.vres = int(attrs.get('vres'))
		if attrs.get('hborder'):
			self.defaults.lhborder = float(attrs.get('hborder'))
			self.defaults.rhborder = self.defaults.lhborder
		if attrs.get('lhborder'):
			self.defaults.lhborder = float(attrs.get('lhborder'))
		if attrs.get('rhborder'):
			self.defaults.rhborder = float(attrs.get('rhborder'))
		if attrs.get('vborder'):
			self.defaults.tvborder = float(attrs.get('vborder'))
			self.defaults.bvborder = self.defaults.tvborder
		if attrs.get('tvborder'):
			self.defaults.tvborder = float(attrs.get('tvborder'))
		if attrs.get('bvborder'):
			self.defaults.bvborder = float(attrs.get('bvborder'))
		if attrs.get('card'):
			self.defaults.cardid = int(attrs.get('card'))

	# <col>

	def startElement_col(self, name, attrs):
		self.vcoord = 0

	def endElement_col(self, name):
		self.hcoord += 1
	
	# <display>
	
	def startElement_display(self, name, attrs):
		display = LayoutDisplay(self.defaults)
		display.host = attrs.get('host')
		display.vcoord = self.vcoord
		display.hcoord = self.hcoord
		if attrs.get('hres'):
			display.hres = int(attrs.get('hres'))
		if attrs.get('vres'):
			display.vres = int(attrs.get('vres'))
		if attrs.get('hborder'):
			display.lhborder = float(attrs.get('lhborder'))
			display.rhborder = display.lhborder
		if attrs.get('lhborder'):
			display.lhborder = float(attrs.get('lhborder'))
		if attrs.get('rhborder'):
			display.rhborder = float(attrs.get('rhborder'))
		if attrs.get('vborder'):
			display.tvborder = float(attrs.get('vborder'))
			display.bvborder = display.tvborder
		if attrs.get('tvborder'):
			display.tvborder = float(attrs.get('tvborder'))
		if attrs.get('bvborder'):
			display.bvborder = float(attrs.get('bvborder'))
		if attrs.get('card'):
			display.cardid = int(attrs.get('card'))

		self.displays.append(display)
		self.vcoord += 1


	def startElement(self, name, attrs):
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



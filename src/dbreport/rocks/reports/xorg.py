#! @PYTHON@
#
# $Id: xorg.py,v 1.9 2008/10/18 00:56:18 mjk Exp $
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
# $Log: xorg.py,v $
# Revision 1.9  2008/10/18 00:56:18  mjk
# copyright 5.1
#
# Revision 1.8  2008/03/06 23:42:00  mjk
# copyright storm on
#
# Revision 1.7  2007/06/23 04:04:03  mjk
# mars hill copyright
#
# Revision 1.6  2007/04/06 22:16:31  mjk
# hack for new nvidia driver
#
# Revision 1.5  2006/09/11 22:50:31  mjk
# monkey face copyright
#
# Revision 1.4  2006/08/10 00:12:08  mjk
# 4.2 copyright
#
# Revision 1.3  2006/06/27 00:30:02  mjk
# - chromium reads config from DMX not from DB now
# - DMX config fixes for crazy Kim layout
# - Tile background color is a hash of the hostname
#
# Revision 1.2  2006/06/23 22:32:30  mjk
# twinview changes
#
# Revision 1.1  2006/06/21 23:16:49  mjk
# *** empty log message ***
#

import os
import sys
import string
import re
import tempfile
import rocks.reports.base

class Report(rocks.reports.base.ReportBase):

	def run(self):

		if len(self.args):
			host = self.args[0]
		else:
			host = None

		# If called without an argument configure the xorg.conf
		# file for the frontend.

		if not host:
			tmp = tempfile.mktemp()
			os.system('nvidia-xconfig -o %s > /dev/null' % tmp)
			file = open(tmp, 'r')
			for line in file.readlines():
				print line[:-1]
			file.close()
			os.unlink(tmp)
			return

		# Called with a hostname argument to generate the config
		# for that node.  If multiple entries are found for 
		# a given tile we know we are in TwinView mode.

		self.execute('select videowall.hcoord,videowall.vcoord,'
			'videowall.lhborder,videowall.rhborder,'
			'videowall.tvborder,videowall.bvborder,'
			'videowall.hres,videowall.vres,videowall.ppi '
			'from nodes,videowall where nodes.name="%s" and '
			'nodes.id=videowall.node and videowall.cardid=1'
			% host)
		vals = self.fetchall()
		
		try:
			hres = int(vals[0][6])
			vres = int(vals[0][7])
		except IndexError:
			pass
			
		if len(vals) == 2:
			coords = ((vals[0][0], vals[0][1]), \
					(vals[1][0], vals[1][1]))
			if vals[0][0] != vals[1][0]:
				twinview = 'RightOf'
				hborder = 0
				vborder = hres #+ \
#					int(vals[0][8])*float(vals[0][5]) + \
#					int(vals[1][8])*float(vals[1][4])
			else:
				twinview = 'Below'
				hborder = vres #+ \
#					int(vals[0][8])*float(vals[0][2]) + \
#					int(vals[1][8])*float(vals[1][3])
				vborder = 0
		else:
			twinview = None

		tmp = tempfile.mktemp()
		if twinview:
			os.system('nvidia-xconfig --twinview -twinvieworientation=clone -o %s > /dev/null'
				% tmp)
		else:
			os.system('nvidia-xconfig -o %s > /dev/null' % tmp)
		file = open(tmp, 'r')
		lines = file.readlines()
		file.close()
		os.unlink(tmp)

		for line in lines:

			m1 = re.search(
			'(^[ \t]+option[ \t]+"metamodes"[ \t]+)',
			line.lower())

			m2 = re.search(
			'(^[ \t]+option[ \t]+"twinvieworientation"[ \t]+)',
			line.lower())

			m3 = re.search(
			'(^[ \t]+modes[ \t]+)',
			line.lower())

			if m1 and m1.groups():
#				print '%s"%dx%d +%d+%d , %dx%d +0+0"' % \
#					(line[0:len(m1.groups()[0])],
#					hres, vres, 
#					vborder, hborder,
#					hres, vres)
				print '%s"%dx%d,%dx%d"' % \
					(line[0:len(m1.groups()[0])],
					hres, vres, 
					hres, vres)
				continue

			if m2 and m2.groups():
				print '%s"%s"' % \
					(line[0:len(m2.groups()[0])],
					twinview)
				continue
		
			if m3 and m3.groups():
				print '\tModes\t"%dx%d"' % (hres, vres)
				continue

			print line[:-1]
	

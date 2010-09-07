# --------------------------------------------------- -*- Makefile -*- --
# $Id: Makefile,v 1.10 2010/09/07 23:53:28 bruno Exp $
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
# $Log: Makefile,v $
# Revision 1.10  2010/09/07 23:53:28  bruno
# star power for gb
#
# Revision 1.9  2009/05/01 19:07:30  mjk
# chimi con queso
#
# Revision 1.8  2008/10/18 00:56:19  mjk
# copyright 5.1
#
# Revision 1.7  2008/07/01 23:07:35  mjk
# roll almost v ready
#
# Revision 1.6  2008/03/06 23:42:01  mjk
# copyright storm on
#
# Revision 1.5  2007/10/03 21:26:16  mjk
# *** empty log message ***
#
# Revision 1.4  2007/10/01 21:12:41  mjk
# chromium movies (no sage)
#
# Revision 1.3  2007/08/31 21:48:58  mjk
# non-evl mplayer with ldd fixed in building
#
# Revision 1.6  2007/08/18 19:46:40  mjk
# thinking about dropping sage and magiccarpet (code too messy)
#
# Revision 1.5  2007/08/13 21:50:05  mjk
# new name, new version
#
# Revision 1.4  2007/06/23 04:04:06  mjk
# mars hill copyright
#
# Revision 1.3  2006/09/11 22:50:42  mjk
# monkey face copyright
#
# Revision 1.2  2006/08/10 00:12:17  mjk
# 4.2 copyright
#
# Revision 1.1  2006/07/24 17:55:16  mjk
# move evl into viz, they've become too interdependent
#
# Revision 1.4  2006/07/17 19:19:14  mjk
# play dvds again
#
# Revision 1.3  2006/07/13 18:08:41  mjk
# trying to get mplayer and vnc to work
#
# Revision 1.2  2006/02/16 03:30:58  mjk
# mplayer builds
#
# Revision 1.1  2006/02/16 00:59:51  mjk
# *** empty log message ***
#
# Revision 1.1  2006/01/12 00:35:32  mjk
# *** empty log message ***
#
# Revision 1.1  2006/01/11 18:13:29  mjk
# add mpeg and fw stuff
#

SCRIPTS		= mplayergl

PKGROOT		= /opt/viz
REDHAT.ROOT	= $(PWD)/../../
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

build:: $(SCRIPTS)
	tar -xzf MPlayer-1.0rc1.tar.gz
	(							\
		cd MPlayer-1.0rc1;				\
		./configure 					\
			--with-sdl-config=/opt/rocks/bin/sdl-config \
			--disable-rpath				\
			--prefix=$(PKGROOT);			\
		make FREETYPE_LIB="-lfreetype -lz";		\
	)


install::
	mkdir -p $(ROOT)/$(PKGROOT)/bin
	(							\
		cd MPlayer-1.0rc1;				\
		make DESTDIR=$(ROOT) install;			\
	)
	install -m 755 $(SCRIPTS) $(ROOT)/$(PKGROOT)/bin/


clean::
	rm -rf MPlayer-1.0rc1 
	rm -f $(SCRIPTS)

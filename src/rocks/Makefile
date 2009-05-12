# --------------------------------------------------- -*- Makefile -*- --
# $Id: Makefile,v 1.41 2009/05/12 00:26:54 mjk Exp $
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
# $Log: Makefile,v $
# Revision 1.41  2009/05/12 00:26:54  mjk
# *** empty log message ***
#
# Revision 1.40  2009/05/01 19:07:30  mjk
# chimi con queso
#
# Revision 1.39  2008/10/18 00:56:20  mjk
# copyright 5.1
#
# Revision 1.38  2008/07/01 23:07:35  mjk
# roll almost v ready
#
# Revision 1.37  2008/03/06 23:42:01  mjk
# copyright storm on
#
# Revision 1.36  2007/09/19 12:48:47  mjk
# *** empty log message ***
#
# Revision 1.35  2007/08/30 00:55:32  mjk
# new banner, less burn in, better logo
#
# Revision 1.34  2007/08/21 19:24:13  mjk
# *** empty log message ***
#
# Revision 1.33  2007/07/30 23:11:29  mjk
# beta time
#
# Revision 1.32  2007/07/27 17:30:22  mjk
# checkpoint
#
# Revision 1.31  2007/06/23 04:04:05  mjk
# mars hill copyright
#
# Revision 1.30  2006/12/20 22:12:44  bruno
# this is not the cursor you are looking for.
#
# on tile nodes, make the mouse pointer cursor invisible.
#
# Revision 1.29  2006/09/11 22:50:39  mjk
# monkey face copyright
#
# Revision 1.28  2006/09/07 19:19:19  mjk
# added tile-refresh to fix screen blanking
#
# Revision 1.27  2006/08/10 00:12:14  mjk
# 4.2 copyright
#
# Revision 1.26  2006/07/11 17:35:18  mjk
# more SAGE changes
#
# Revision 1.25  2006/06/29 19:56:45  mjk
# added viz-reconfig
#
# Revision 1.24  2006/06/28 05:46:42  phil
# fix permissions on tile-banner
# actually install tilelayout so that it is in the RPM.
#
# Revision 1.23  2006/06/26 19:53:13  mjk
# zurich.xml
#
# Revision 1.22  2006/05/02 01:45:42  mjk
# added tilelayout
#
# Revision 1.21  2006/02/17 21:02:42  mjk
# *** empty log message ***
#
# Revision 1.20  2006/02/17 20:22:11  mjk
# *** empty log message ***
#
# Revision 1.19  2006/02/17 20:21:16  mjk
# added sage start/kill
#
# Revision 1.18  2006/02/14 01:04:05  mjk
# switch to fvwm
#
# Revision 1.17  2006/01/11 21:02:38  phil
# Add building of viz-xconfig-nvidia
#
# Revision 1.16  2006/01/11 19:49:51  phil
# Build and install viz-autolayout
#
# Revision 1.15  2006/01/11 18:21:36  mjk
# *** empty log message ***
#
# Revision 1.14  2006/01/11 18:20:25  mjk
# kill spec file, add ldconfig
#
# Revision 1.13  2006/01/11 00:26:40  phil
# install viztile in /opt/rocks/sbin. Remove explicit rocks version number on version.mk
#
# Revision 1.12  2005/10/12 18:11:18  mjk
# final copyright for 4.1
#
# Revision 1.11  2005/09/16 01:04:56  mjk
# updated copyright
#
# Revision 1.10  2005/05/24 21:24:08  mjk
# update copyright, release is not any closer
#
# Revision 1.9  2004/10/08 07:12:54  mjk
# fix perms
#
# Revision 1.8  2004/10/07 22:53:24  mjk
# Added tile-banner to label nodes by hostname
# Viz user profile calls tile-banner
#
# Revision 1.7  2004/10/06 22:53:18  mjk
# add crconfig for chromium
#
# Revision 1.6  2004/09/15 02:10:09  mjk
# kill gnome
#
# Revision 1.5  2004/09/15 00:55:04  mjk
# fixed path
#
# Revision 1.4  2004/09/11 04:19:16  mjk
# viz should be in PKGROOT like other makefiles
#
# Revision 1.3  2004/09/11 04:08:47  mjk
# typo
#
# Revision 1.2  2004/09/11 04:07:44  mjk
# *** empty log message ***
#
# Revision 1.1  2004/09/08 20:09:32  mjk
# added rocks-viz, moved stuff from common to master node
#
# Revision 1.1  2004/07/15 15:26:20  mjk
# 1st pass at xdmx report
#


PKGROOT = /opt/viz
SCRIPTS = tile-banner tile-reset
REDHAT.ROOT = $(PWD)/../../

-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

install::
	mkdir -p $(ROOT)/etc/skel
	mkdir -p $(ROOT)/etc/skel/.fvwm
	mkdir -p $(ROOT)/etc/sysconfig
	mkdir -p $(ROOT)/$(PKGROOT)/etc/.ssh
	mkdir -p $(ROOT)/$(PKGROOT)/etc/.gnome2
	mkdir -p $(ROOT)/$(PKGROOT)/etc/.fvwm
	mkdir -p $(ROOT)/$(PKGROOT)/sbin
	mkdir -p $(ROOT)/$(PKGROOT)/lib/images
	mkdir -p $(ROOT)/$(PKGROOT)/lib/tilelayout/examples
	mkdir -p $(ROOT)/etc/ld.so.conf.d
	echo $(PKGROOT)/lib >> $(ROOT)/etc/ld.so.conf.d/viz.conf
	install -m744 etc/skel/Xclients		$(ROOT)/etc/skel/.Xclients
	install -m544 etc/skel/fvwm2rc		$(ROOT)/etc/skel/.fvwm/.fvwm2rc
	install -m744 viz/etc/Xclients		\
		$(ROOT)/$(PKGROOT)/etc/.Xclients
	install -m744 viz/etc/invisible-cursor.xbm	\
		$(ROOT)/$(PKGROOT)/etc/
	install -m544 viz/etc/gnome2/gdm	\
		$(ROOT)/$(PKGROOT)/etc/.gnome2/gdm
	touch	$(ROOT)/$(PKGROOT)/etc/.ssh/id_rsa.pub
	install -m755 tile-banner		$(ROOT)/$(PKGROOT)/sbin
	install -m755 tile-reset		$(ROOT)/$(PKGROOT)/sbin
	install -m444 rocks-logo-*.png		$(ROOT)/$(PKGROOT)/lib/images
	install -m644 *.xml	$(ROOT)/$(PKGROOT)/lib/tilelayout/examples

build: $(SCRIPTS)

clean::
	-rm -f $(SCRIPTS)


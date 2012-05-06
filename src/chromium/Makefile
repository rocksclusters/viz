# --------------------------------------------------- -*- Makefile -*- --
# $Id: Makefile,v 1.37 2012/05/06 05:49:44 phil Exp $
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
# $Log: Makefile,v $
# Revision 1.37  2012/05/06 05:49:44  phil
# Copyright Storm for Mamba
#
# Revision 1.36  2011/07/23 02:31:38  phil
# Viper Copyright
#
# Revision 1.35  2010/09/07 23:53:26  bruno
# star power for gb
#
# Revision 1.34  2009/06/11 22:57:52  mjk
# - Build chromium 64bit and 32bit libs
# - Google Earth now runs on a 64bit wall
# - 32bit Viz Roll is now dead
#
# Revision 1.33  2009/05/01 19:07:24  mjk
# chimi con queso
#
# Revision 1.32  2008/10/18 00:56:18  mjk
# copyright 5.1
#
# Revision 1.31  2008/07/01 23:07:31  mjk
# roll almost v ready
#
# Revision 1.30  2008/03/06 23:42:00  mjk
# copyright storm on
#
# Revision 1.29  2007/08/21 19:24:13  mjk
# *** empty log message ***
#
# Revision 1.28  2007/07/30 23:11:29  mjk
# beta time
#
# Revision 1.27  2007/07/30 21:31:14  mjk
# *** empty log message ***
#
# Revision 1.26  2007/07/27 17:30:21  mjk
# checkpoint
#
# Revision 1.25  2007/06/23 04:04:03  mjk
# mars hill copyright
#
# Revision 1.24  2007/05/01 00:16:05  mjk
# - Remove SDL RPMS
# - Put SDL into the foundation in /opt/viz (not /opt/rocks)
# - Build chromium from head of tree not the released version
#
# Revision 1.23  2007/04/30 18:48:23  mjk
# *** empty log message ***
#
# Revision 1.22  2007/04/30 18:26:23  mjk
# *** empty log message ***
#
# Revision 1.21  2007/04/28 01:37:24  mjk
# grab version from CVS
#
# Revision 1.20  2007/04/28 01:35:18  mjk
# *** empty log message ***
#
# Revision 1.19  2007/04/26 20:35:41  mjk
# *** empty log message ***
#
# Revision 1.18  2006/09/11 22:50:27  mjk
# monkey face copyright
#
# Revision 1.17  2006/08/10 00:12:06  mjk
# 4.2 copyright
#
# Revision 1.16  2006/02/14 22:25:29  mjk
# *** empty log message ***
#
# Revision 1.15  2005/12/30 18:39:45  mjk
# remove spec files
#
# Revision 1.14  2005/10/12 18:11:11  mjk
# final copyright for 4.1
#
# Revision 1.13  2005/09/16 01:04:51  mjk
# updated copyright
#
# Revision 1.12  2005/05/24 21:24:02  mjk
# update copyright, release is not any closer
#
# Revision 1.11  2004/10/16 00:13:37  mjk
# works
#
# Revision 1.10  2004/10/15 23:28:57  mjk
# aaaaarrrrrggggg
#
# Revision 1.9  2004/10/07 20:52:14  mjk
# more cr stuff
#
# Revision 1.8  2004/07/14 23:29:37  mjk
# slam uid to fix bad tarball
#
# Revision 1.7  2004/01/15 18:09:49  mjk
# install fix
#
# Revision 1.6  2004/01/15 18:04:56  mjk
# create profile.d dir
#
# Revision 1.5  2004/01/15 17:46:26  mjk
# Chromium does not 'install' and want all the files including source
#
# Revision 1.4  2004/01/15 17:15:08  mjk
# added option.mk patch (no changes yet)
#
# Revision 1.3  2004/01/15 16:42:07  mjk
# first pass at rpm
#
# Revision 1.2  2004/01/15 01:37:43  mjk
# builds and installs (needs spec file)
#
# Revision 1.1  2004/01/15 01:17:30  mjk
# *** empty log message ***
#

PKGROOT		= /opt/viz
REDHAT.ROOT	= $(PWD)/../../
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

CRCONFIG = $(PKGROOT)/share/cr/mothership/server/crconfig.py

refresh: clean
	$(CVS) -d:pserver:anonymous@chromium.cvs.sourceforge.net:/cvsroot/chromium login
	$(CVS) -d:pserver:anonymous@chromium.cvs.sourceforge.net:/cvsroot/chromium co cr
	tar -czf cr.tar.gz cr
	rm -rf cr

install::
	mkdir -p $(ROOT)/$(PKGROOT)/bin
	mkdir -p $(ROOT)/$(PKGROOT)/lib32/cr
	mkdir -p $(ROOT)/$(PKGROOT)/lib/cr
	mkdir -p $(ROOT)/$(PKGROOT)/include/cr/state
	mkdir -p $(ROOT)/$(PKGROOT)/share/cr
	mkdir -p $(ROOT)/$(PKGROOT)/share/cr/mothership/configs
	mkdir -p $(ROOT)/$(PKGROOT)/share/cr/mothership/prshd
	mkdir -p $(ROOT)/$(PKGROOT)/share/cr/mothership/server
	mkdir -p $(ROOT)/$(PKGROOT)/share/cr/mothership/tools
	mkdir -p $(ROOT)/etc/ld.so.conf.d
	mkdir -p $(ROOT)/etc/profile.d
	echo $(PKGROOT)/lib    > $(ROOT)/etc/ld.so.conf.d/$(NAME)-$(ARCH).conf
	echo $(PKGROOT)/lib32 >> $(ROOT)/etc/ld.so.conf.d/$(NAME)-$(ARCH).conf
	$(INSTALL) -m644 chromium.sh  $(ROOT)/etc/profile.d
	$(INSTALL) -m644 chromium.csh $(ROOT)/etc/profile.d
	$(INSTALL) cr/bin/Linux/* $(ROOT)/$(PKGROOT)/bin/
	$(INSTALL) cr/lib/Linux/*.a $(ROOT)/$(PKGROOT)/lib/
	$(INSTALL) cr/lib/Linux/*.so $(ROOT)/$(PKGROOT)/lib/
	$(INSTALL) cr/lib32/Linux/*.a $(ROOT)/$(PKGROOT)/lib32/
	$(INSTALL) cr/lib32/Linux/*.so $(ROOT)/$(PKGROOT)/lib32/
	$(INSTALL) -m644 cr/include/*.h $(ROOT)/$(PKGROOT)/include/cr/
	$(INSTALL) -m644 cr/include/state/*.h \
		$(ROOT)/$(PKGROOT)/include/cr/state/
	$(INSTALL) -m644 cr/mothership/configs/*.conf \
		$(ROOT)/$(PKGROOT)/share/cr/mothership/configs/
	$(INSTALL) -m644 cr/mothership/prshd/*.py \
		$(ROOT)/$(PKGROOT)/share/cr/mothership/prshd/
	$(INSTALL) -m644 cr/mothership/server/*.py \
		$(ROOT)/$(PKGROOT)/share/cr/mothership/server/
	$(INSTALL) -m644 cr/mothership/tools/*.py \
		$(ROOT)/$(PKGROOT)/share/cr/mothership/tools/
	echo "import os"				>  $(ROOT)/$(CRCONFIG)
	echo "arch = 'Linux'"				>> $(ROOT)/$(CRCONFIG)
	echo "crdir = '/opt/viz/'"			>> $(ROOT)/$(CRCONFIG)
	echo "crbindir = os.path.join(crdir, 'bin')"	>> $(ROOT)/$(CRCONFIG)
	echo "crlibdir = os.path.join(crdir, 'lib')"	>> $(ROOT)/$(CRCONFIG)

build: 
	gunzip -c cr.tar.gz | tar -x
	cd patch-files && find . -type f | grep -v CVS | cpio -pduv ../
	(							\
		cd cr;						\
		cp options-32.mk options.mk;			\
		make;						\
		mv lib lib32;					\
		cp options-64.mk options.mk;			\
		make clean;					\
		make;						\
	)

clean::
	rm -rf cr

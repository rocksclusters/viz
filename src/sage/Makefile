# --------------------------------------------------- -*- Makefile -*- --
# $Id: Makefile,v 1.20 2008/10/18 00:56:21 mjk Exp $
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
# $Log: Makefile,v $
# Revision 1.20  2008/10/18 00:56:21  mjk
# copyright 5.1
#
# Revision 1.19  2008/07/01 23:07:36  mjk
# roll almost v ready
#
# Revision 1.18  2008/05/31 02:57:37  mjk
# - SAGE is back and works (mostly)
# - DMX building from source (in progress)
# - Updated nvidia driver
#
# Revision 1.17  2008/05/29 20:45:01  mjk
# rocks specific fork of sage (no idea why)
#
# Revision 1.16  2008/05/27 17:42:52  mjk
# luc has landed
#
# Revision 1.14  2007/07/30 23:11:29  mjk
# beta time
#
# Revision 1.13  2007/07/27 17:30:22  mjk
# checkpoint
#
# Revision 1.12  2007/07/25 19:18:38  mjk
# *** empty log message ***
#
# Revision 1.11  2007/07/25 19:13:38  mjk
# *** empty log message ***
#
# Revision 1.10  2007/07/25 18:52:38  mjk
# *** empty log message ***
#
# Revision 1.4  2007/07/24 02:11:03  mjk
# atlantis works
#
# Revision 1.3  2007/06/23 04:04:06  mjk
# mars hill copyright
#
# Revision 1.2  2007/04/28 01:26:11  mjk
# *** empty log message ***
#
# Revision 1.1  2007/04/27 19:19:56  mjk
# *** empty log message ***
#

PKGROOT		= /opt/sage
REDHAT.ROOT	= $(PWD)/../../
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

refresh: clean
	svn checkout svn://cube.evl.uic.edu/dev/$(SVNNAME)
	-find $(SVNNAME) -name .svn -exec rm -rf {} \;
	tar -czf $(SVNNAME).tar.gz $(SVNNAME)
	rm -rf $(SVNNAME)
	
build:
	gunzip -c $(SVNNAME).tar.gz | tar -x
	cd patch-files && find . -type f | grep -v CVS | cpio -pduv ../
	(							\
		export SAGE_DIRECTORY=`pwd`/$(SVNNAME);		\
		cd $(SVNNAME);					\
		make clean;					\
		make;						\
		cd app/mplayer;					\
		./configure --prefix=build --disable-x264;	\
		make;						\
		make install;					\
		cp build/bin/mplayer ../../bin;			\
	)

install::
	mkdir -p $(ROOT)/$(PKGROOT)
	mkdir -p $(ROOT)/etc/profile.d
	mkdir -p $(ROOT)/etc/ld.so.conf.d
	(							\
		cd $(SVNNAME);					\
		make ROOT=$(ROOT) install;			\
	)
	install -m644 $(NAME).sh  $(ROOT)/etc/profile.d/
	install -m644 $(NAME).csh $(ROOT)/etc/profile.d/
	echo $(PKGROOT)/lib > $(ROOT)/etc/ld.so.conf.d/$(NAME).conf


clean::
	rm -rf $(SVNNAME)

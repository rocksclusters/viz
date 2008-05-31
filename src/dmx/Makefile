#
# $Id: Makefile,v 1.18 2008/05/31 02:57:18 mjk Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		            version 5.0 (V)
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
# Revision 1.18  2008/05/31 02:57:18  mjk
# - SAGE is back and works (mostly)
# - DMX building from source (in progress)
# - Updated nvidia driver
#
# Revision 1.17  2008/03/06 23:42:00  mjk
# copyright storm on
#
# Revision 1.16  2008/01/14 22:03:32  bruno
# tweaks for V
#
# Revision 1.15  2007/06/23 04:04:03  mjk
# mars hill copyright
#
# Revision 1.14  2007/04/28 01:09:34  mjk
# need to use code from sf, not xorg
#
# Revision 1.13  2007/04/26 23:07:57  mjk
# using all the bits
#
# Revision 1.12  2006/09/11 22:50:32  mjk
# monkey face copyright
#
# Revision 1.11  2006/08/10 00:12:08  mjk
# 4.2 copyright
#
# Revision 1.10  2006/06/01 03:44:03  bruno
# needed a new DMX to run on wall with more than 16 machines
#
# Revision 1.9  2006/06/01 01:51:11  mjk
# *** empty log message ***
#
# Revision 1.7  2005/12/30 18:39:46  mjk
# remove spec files
#
# Revision 1.6  2005/10/12 18:11:15  mjk
# final copyright for 4.1
#
# Revision 1.5  2005/09/16 01:04:53  mjk
# updated copyright
#
# Revision 1.4  2005/05/24 21:24:05  mjk
# update copyright, release is not any closer
#
# Revision 1.3  2005/02/17 00:58:20  mjk
# nuke devel manpages (were missing from old RPM also)
#
# Revision 1.2  2005/02/17 00:30:51  mjk
# more makefile fixes
#
# Revision 1.1  2005/02/16 23:49:36  mjk
# build from dmx cvs source
#

PKGROOT		= /opt/viz
REDHAT.ROOT	= $(PWD)/../../
ROCKSROOT	= ../../../../..
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk


install::
	mkdir -p $(ROOT)/$(PKGROOT)/bin
	mkdir -p $(ROOT)/$(PKGROOT)/lib
	mkdir -p $(ROOT)/$(PKGROOT)/man/man1
	mkdir -p $(ROOT)/$(PKGROOT)/man/man3
	mkdir -p $(ROOT)/$(PKGROOT)/include/X11/extensions
	(								\
		cd $(NAME)/xc;						\
		install -m 555 programs/Xserver/Xdmx			\
			$(ROOT)/$(PKGROOT)/bin/; 			\
		install -m 644 exports/lib/libdmx.a 			\
			$(ROOT)/$(PKGROOT)/lib/;			\
		install -m 644 exports/lib/libdmx.so			\
			$(ROOT)/$(PKGROOT)/lib/;			\
		install -m 644 exports/include/X11/extensions/dmxext.h	\
			exports/include/X11/extensions/dmxproto.h	\
			$(ROOT)/$(PKGROOT)/include/X11/extensions/;	\
		install -m 644 programs/Xserver/hw/dmx/Xdmx._man	\
			$(ROOT)/$(PKGROOT)/man/man1/Xdmx.1;		\
	)

build:
	gunzip -c xorg-server-$(VERSION).tar.gz | tar -x
	(								\
		cd xorg-server-$(VERSION);				\
		aclocal ; automake ; autoconf;				\
		./configure;						\
	)
	#cd patch-files && find . -type f | grep -v CVS | cpio -pduv ../
	#cp host.def xorg-server-$(VERSION)/xc/config/cf/
	#( cd $(NAME)/xc; make World )
	#echo '.so man3/DMXAddInput.3' > \
	#	$(NAME)/xc/doc/man/DMX/DMXAddBackendInput._man
	#echo '.so man3/DMXAddInput.3' > \
	#	$(NAME)/xc/doc/man/DMX/DMXAddConsoleInput._man

clean::
	rm -rf $(NAME)

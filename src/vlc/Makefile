# --------------------------------------------------- -*- Makefile -*- --
# $Id: Makefile,v 1.6 2008/10/18 00:56:22 mjk Exp $
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
# Revision 1.6  2008/10/18 00:56:22  mjk
# copyright 5.1
#
# Revision 1.5  2008/07/01 23:07:59  mjk
# roll almost v ready
#
# Revision 1.4  2008/03/06 23:42:03  mjk
# copyright storm on
#
# Revision 1.3  2007/12/19 21:43:20  mjk
# vlc plays dvds now
#
# Revision 1.2  2007/12/18 22:59:11  mjk
# more vlc deps
#
# Revision 1.1  2007/12/18 20:42:00  mjk
# vlc runs
#

PKGROOT		= /opt/rocks
REDHAT.ROOT	= $(PWD)/../../
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

build::
	gunzip -c $(NAME)-$(VERSION).tar.gz | tar -x
	(							\
		cd $(NAME)-$(VERSION);				\
		export CPPFLAGS="-I/opt/rocks/include -I/opt/viz/include"; \
		export LDFLAGS="-L/opt/rocks/lib -L/opt/viz/lib"; \
		export PKG_CONFIG_PATH=/opt/rocks/lib/pkgconfig; \
		./configure --prefix=$(PKGROOT)			\
			--enable-faad					\
			--with-ffmpeg-faac				\
			--enable-dvdread				\
			--with-sdl-config-path=/opt/rocks/bin/sdl-config \
			--with-wx-config-path=/opt/rocks/bin/wx-config; \
		make;						\
	)


install::
	mkdir -p $(ROOT)/$(PKGROOT)
	(							\
		cd $(NAME)-$(VERSION);				\
		make prefix=$(ROOT)/$(PKGROOT) install;		\
	)

clean::
	rm -rf $(NAME)-$(VERSION)

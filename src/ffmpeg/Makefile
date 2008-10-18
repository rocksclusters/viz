# --------------------------------------------------- -*- Makefile -*- --
# $Id: Makefile,v 1.11 2008/10/18 00:56:19 mjk Exp $
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
# Revision 1.11  2008/10/18 00:56:19  mjk
# copyright 5.1
#
# Revision 1.10  2008/07/01 23:07:31  mjk
# roll almost v ready
#
# Revision 1.9  2008/03/06 23:42:00  mjk
# copyright storm on
#
# Revision 1.8  2007/12/19 21:43:19  mjk
# vlc plays dvds now
#
# Revision 1.7  2007/12/18 22:59:11  mjk
# more vlc deps
#
# Revision 1.6  2007/07/11 00:13:05  mjk
# - update boostrapping
# - /opt/rocks for non-viz stuff
# - /opt/viz for viz only stuff
# - support for doom
#
# Revision 1.5  2007/06/23 04:04:03  mjk
# mars hill copyright
#
# Revision 1.4  2006/09/11 22:50:33  mjk
# monkey face copyright
#
# Revision 1.3  2006/08/10 00:12:10  mjk
# 4.2 copyright
#
# Revision 1.2  2006/07/25 23:43:05  mjk
# working on vlc
#
# Revision 1.1  2006/07/25 01:02:34  mjk
# *** empty log message ***
#

PKGROOT		= /opt/rocks
REDHAT.ROOT	= $(PWD)/../../
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

ffmpeg:
	tar -xzf $(NAME).tar.gz

refresh: clean
	$(SVN) checkout svn://svn.mplayerhq.hu/ffmpeg/trunk ffmpeg
	tar -czf $(NAME).tar.gz $(NAME)
	rm -rf $(NAME)
	
build:: ffmpeg 
	cd patch-files && find . -type f | grep -v CVS | cpio -pduv ../
	(							\
		cd $(NAME);					\
		./configure --prefix=$(PKGROOT)			\
			--extra-cflags=-I/opt/rocks/include	\
			--extra-ldflags=-L/opt/rocks/lib	\
			--enable-faad				\
			--enable-faac				\
			--enable-gpl				\
			--enable-pp;				\
		make;						\
	)

install::
	mkdir -p $(ROOT)/$(PKGROOT)
	(							\
		cd $(NAME);					\
		make DESTDIR=$(ROOT) install;			\
	)

clean::
	rm -rf $(NAME)

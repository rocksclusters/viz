# --------------------------------------------------- -*- Makefile -*- --
# $Id: Makefile,v 1.14 2008/05/30 19:28:13 mjk Exp $
#
# @Copyright@
# 
# 				Rocks(tm)
# 		         www.rocksclusters.org
# 		        version 4.3 (Mars Hill)
# 
# Copyright (c) 2000 - 2007 The Regents of the University of California.
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
# 	"This product includes software developed by the Rocks(tm)
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
# Revision 1.14  2008/05/30 19:28:13  mjk
# *** empty log message ***
#
# Revision 1.12  2007/06/23 04:04:04  mjk
# mars hill copyright
#
# Revision 1.11  2007/05/11 18:35:52  mjk
# no more lib64
#
# Revision 1.10  2007/04/26 23:08:13  mjk
# using all the bits
#
# Revision 1.9  2006/09/11 22:50:39  mjk
# monkey face copyright
#
# Revision 1.8  2006/08/10 00:12:14  mjk
# 4.2 copyright
#
# Revision 1.7  2006/07/24 17:55:14  mjk
# move evl into viz, they've become too interdependent
#
# Revision 1.6  2006/07/10 23:13:13  mjk
# use latests version
#
# Revision 1.5  2006/06/27 01:17:23  mjk
# - use tarball not svn
#
# Revision 1.4  2006/04/13 23:43:10  mjk
# Get latest from SVN
#
# Revision 1.3  2006/03/02 04:54:25  mjk
# more vizn
#
# Revision 1.2  2006/03/01 23:56:55  mjk
# stop using SVN
#
# Revision 1.1  2006/01/11 16:57:51  mjk
# *** empty log message ***
#
# Revision 1.2  2006/01/11 02:28:54  mjk
# sage works
#
# Revision 1.1  2006/01/10 15:37:51  mjk
# *** empty log message ***
#

PKGROOT		= /opt/viz
REDHAT.ROOT	= $(PWD)/../../
ROCKSROOT	= ../../../../..
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

build:
	tar -xzf $(NAME)-$(VERSION).tar.gz
	cd patch-files && find . -type f | grep -v CVS | cpio -pduv ../
	(							\
		cd $(NAME)-$(VERSION);					\
		./bootstrap;					\
		./configure --prefix=$(PKGROOT);		\
		echo 'override libdir=$$(prefix)/lib' >> src/Makefile;	\
		make;						\
	)

install::
	mkdir -p $(ROOT)/$(PKGROOT)
	mkdir -p $(ROOT)/etc/ld.so.conf.d
	echo $(PKGROOT)/lib > \
		$(ROOT)/etc/ld.so.conf.d/$(NAME).conf
	(							\
		cd $(NAME)-$(VERSION);				\
		make prefix=$(ROOT)/$(PKGROOT) install;		\
	)

clean::
	rm -rf $(NAME)-$(VERSION)

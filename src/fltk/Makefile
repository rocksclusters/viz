# --------------------------------------------------- -*- Makefile -*- --
# $Id: Makefile,v 1.12 2010/09/07 23:53:27 bruno Exp $
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
# Revision 1.12  2010/09/07 23:53:27  bruno
# star power for gb
#
# Revision 1.11  2009/05/01 19:07:25  mjk
# chimi con queso
#
# Revision 1.10  2008/10/18 00:56:19  mjk
# copyright 5.1
#
# Revision 1.9  2008/07/01 23:07:32  mjk
# roll almost v ready
#
# Revision 1.8  2008/03/06 23:42:00  mjk
# copyright storm on
#
# Revision 1.7  2007/06/23 04:04:03  mjk
# mars hill copyright
#
# Revision 1.6  2006/09/11 22:50:34  mjk
# monkey face copyright
#
# Revision 1.5  2006/08/10 00:12:10  mjk
# 4.2 copyright
#
# Revision 1.4  2006/02/07 22:00:48  mjk
# add bootstrapping
#
# Revision 1.3  2005/10/12 18:11:16  mjk
# final copyright for 4.1
#
# Revision 1.2  2005/09/16 01:04:54  mjk
# updated copyright
#
# Revision 1.1  2005/06/29 23:24:04  mjk
# *** empty log message ***
#
# Revision 1.1  2005/06/28 22:34:48  mjk
# add quanta from evl
#

PKGROOT		= /opt/$(NAME)
REDHAT.ROOT	= $(PWD)/../../
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk


install::

build: 
	gunzip -c $(NAME)-$(VERSION)-source.tar.gz | tar -x
	if [ -d patch-file ]; then					\
		cd patch-files;						\
		find . -type f | grep -v CVS | cpio -pduv ../;		\
	fi
	if [ ! -e $(PKGROOT) ]; then mkdir -p $(PKGROOT); fi
	mount -t tmpfs tmpfs $(PKGROOT)
	(								\
		cd $(NAME)-$(VERSION); 					\
		./configure --prefix=$(PKGROOT);	 		\
		make; 							\
		make install;						\
		mkdir -p $(ROOT)/$(PKGROOT);				\
		find . | cpio -pdu $(ROOT)/$(PKGROOT);			\
		umount $(PKGROOT);					\
	)
		

clean::
	rm -rf $(NAME)-$(VERSION)
	rm -f $(NAME).spec.in

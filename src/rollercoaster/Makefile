# $Id: Makefile,v 1.18 2012/05/06 05:49:48 phil Exp $
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
# Revision 1.18  2012/05/06 05:49:48  phil
# Copyright Storm for Mamba
#
# Revision 1.17  2011/07/23 02:31:41  phil
# Viper Copyright
#
# Revision 1.16  2010/09/07 23:53:31  bruno
# star power for gb
#
# Revision 1.15  2010/06/22 21:43:58  mjk
# remove ROCKSROOT
#
# Revision 1.14  2009/05/01 19:07:32  mjk
# chimi con queso
#
# Revision 1.13  2008/10/18 00:56:21  mjk
# copyright 5.1
#
# Revision 1.12  2008/03/06 23:42:03  mjk
# copyright storm on
#
# Revision 1.11  2007/06/23 04:04:06  mjk
# mars hill copyright
#
# Revision 1.10  2006/09/11 22:50:41  mjk
# monkey face copyright
#
# Revision 1.9  2006/08/10 00:12:16  mjk
# 4.2 copyright
#
# Revision 1.8  2005/12/30 18:39:48  mjk
# remove spec files
#
# Revision 1.7  2005/10/12 18:11:20  mjk
# final copyright for 4.1
#
# Revision 1.6  2005/09/16 01:04:58  mjk
# updated copyright
#
# Revision 1.5  2005/05/24 21:24:10  mjk
# update copyright, release is not any closer
#
# Revision 1.4  2005/02/23 23:09:57  mjk
# opteron patches
#
# Revision 1.3  2004/09/08 21:21:19  mjk
# moved to viz/demos
#
# Revision 1.2  2004/07/15 20:05:57  bruno
# tweak
#
# Revision 1.1  2004/07/15 19:55:00  bruno
# new fun demo
#
# Revision 1.2  2004/07/07 05:09:43  bruno
#
# testing multiple file updates
#
# Revision 1.1  2004/06/26 18:00:28  bruno
# first rev of the IB driver and mpich over IB
#

PKGROOT		= /opt/viz/demos
REDHAT.ROOT     = $(PWD)/../../
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

install::
	mkdir -p $(ROOT)/$(PKGROOT)/$(NAME)
	install -m444 $(NAME)-$(VERSION)-src/bin/*.{trk,tga} \
		 $(ROOT)/$(PKGROOT)/$(NAME)/
	install -m555 $(NAME)-$(VERSION)-src/bin/roller \
		$(ROOT)/$(PKGROOT)/$(NAME)/
	install -m444 tracks/*.trk $(ROOT)/$(PKGROOT)/$(NAME)

build:
	gunzip -c $(NAME)-$(VERSION)-src.tar.gz | tar -x
	cd patch-files && find . -type f | grep -v CVS | cpio -pduv ../
	( cd $(NAME)-$(VERSION)-src; make; )

clean::
	rm -rf $(NAME)-$(VERSION)-src
	rm -f $(NAME).spec.in

# --------------------------------------------------- -*- Makefile -*- --
# $Id: Makefile,v 1.26 2012/05/06 05:49:44 phil Exp $
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
# Revision 1.26  2012/05/06 05:49:44  phil
# Copyright Storm for Mamba
#
# Revision 1.25  2011/07/23 02:31:38  phil
# Viper Copyright
#
# Revision 1.24  2010/09/07 23:53:28  bruno
# star power for gb
#
# Revision 1.23  2010/02/24 00:49:11  mjk
# - nvidia driver auto updates, but still works fine if the cluster is
#   not on the network.  Each node polls/pulls from nvidia.com the latest
#   driver.  User can disable and control the driver manually.
#   No more Roll updates to refresh the nvidia driver
# - X11 modules controlled by viz_x11_modules attribute
# - DPMS added back in
# - rocks start|stop tile to turn wall on|off
# - usersguide fixes (still needs work)
# - add nvidia driver version to tile-banner
# - bump version to 5.3.1
#
# Revision 1.22  2009/11/13 20:19:36  mjk
# new drivers
#
# Revision 1.21  2009/06/17 21:11:16  mjk
# - no more 32 bit
# - install nvidia and cuda driver
# - attrs used for driver name (user selectable version)
#
# Revision 1.20  2009/06/17 20:17:10  mjk
# *** empty log message ***
#
# Revision 1.19  2009/05/01 19:07:30  mjk
# chimi con queso
#
# Revision 1.18  2008/10/18 00:56:19  mjk
# copyright 5.1
#
# Revision 1.17  2008/07/01 23:07:35  mjk
# roll almost v ready
#
# Revision 1.16  2008/05/31 02:57:37  mjk
# - SAGE is back and works (mostly)
# - DMX building from source (in progress)
# - Updated nvidia driver
#
# Revision 1.15  2008/03/06 23:42:01  mjk
# copyright storm on
#
# Revision 1.14  2007/10/09 21:37:45  mjk
# *** empty log message ***
#
# Revision 1.13  2007/06/23 04:04:04  mjk
# mars hill copyright
#
# Revision 1.12  2006/09/11 22:50:36  mjk
# monkey face copyright
#
# Revision 1.11  2006/08/10 00:12:13  mjk
# 4.2 copyright
#
# Revision 1.10  2006/01/11 02:28:54  mjk
# sage works
#
# Revision 1.9  2005/12/30 18:39:47  mjk
# remove spec files
#
# Revision 1.8  2005/10/12 18:11:17  mjk
# final copyright for 4.1
#
# Revision 1.7  2005/09/16 01:04:55  mjk
# updated copyright
#
# Revision 1.6  2005/05/24 21:24:08  mjk
# update copyright, release is not any closer
#
# Revision 1.5  2005/04/21 01:27:09  bruno
# new nvidia driver need path /usr/src/linux
#
# Revision 1.4  2004/09/03 20:25:06  mjk
# added init script
#
# Revision 1.3  2004/07/16 17:10:36  mjk
# builds
#
# Revision 1.2  2004/07/16 17:02:35  mjk
# *** empty log message ***
#
# Revision 1.1  2004/07/16 16:54:59  mjk
# *** empty log message ***
#

PKGROOT		= /opt/viz
REDHAT.ROOT	= $(PWD)/../../
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

build:
	tar -xzf nvidia-xconfig-1.0.tar.gz
	(							\
		cd nvidia-xconfig-1.0;				\
		make;						\
	)

install:: 
	mkdir -p $(ROOT)/$(PKGROOT)/bin
	mkdir -p $(ROOT)/$(PKGROOT)/drivers
	mkdir -p $(ROOT)/etc/rc.d/init.d
	install -m755 $(NVIDIA_DRIVER)	$(ROOT)/$(PKGROOT)/drivers/nvidia.run
	install -m755 nvidia-update.run	$(ROOT)/$(PKGROOT)/drivers/
	install nvidia			$(ROOT)/etc/rc.d/init.d/
	(							\
		cd nvidia-xconfig-1.0;				\
		make prefix=$(ROOT)/$(PKGROOT) install;		\
	)
	
	
clean::
	rm -rf nvidia-xconfig-1.0

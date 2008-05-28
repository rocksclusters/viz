# --------------------------------------------------- -*- Makefile -*- --
# $Id: Makefile,v 1.18 2008/05/28 01:08:07 mjk Exp $
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
# Revision 1.18  2008/05/28 01:08:07  mjk
# python code now included in rpm
#
# Revision 1.17  2008/03/06 23:42:03  mjk
# copyright storm on
#
# Revision 1.16  2008/01/14 22:03:47  bruno
# tweaks for V
#
# Revision 1.15  2007/12/18 20:37:32  mjk
# new version
#
# Revision 1.14  2007/07/10 18:43:40  mjk
# build w/o tmpfs
#
# Revision 1.13  2007/06/23 04:04:06  mjk
# mars hill copyright
#
# Revision 1.12  2006/10/02 21:46:44  mjk
# place in /opt/viz tree
#
# Revision 1.11  2006/09/11 22:50:43  mjk
# monkey face copyright
#
# Revision 1.10  2006/08/10 00:12:19  mjk
# 4.2 copyright
#
# Revision 1.9  2006/02/07 22:00:49  mjk
# add bootstrapping
#
# Revision 1.8  2006/01/11 02:28:57  mjk
# sage works
#

PKGROOT		= /opt/rocks
REDHAT.ROOT	= $(PWD)/../../
ROCKSROOT	= ../../../../..
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

build:
	bunzip2 -c wxPython-src-$(VERSION).tar.bz2 | tar -x
	mkdir wxPython-src-$(VERSION)/bld
	(							\
		cd wxPython-src-$(VERSION)/bld;			\
		../configure --prefix=$(PKGROOT)		\
			--enable-rpath=/opt/rocks/lib		\
			--enable-unicode			\
			--with-gtk				\
			--with-opengl				\
			--enable-geometry			\
			--enable-sound				\
			--with-sdl				\
			--enable-display			\
			--disable-debugreport			\
			--enable-monolithic			\
			--with-libjpeg=builtin 			\
			--with-libpng=builtin			\
			--with-libtiff=builtin			\
			--with-zlib=builtin;			\
		make;						\
		make -C contrib/src/gizmos;			\
		make -C contrib/src/stc;			\
		cd ../wxPython;					\
		$(PY.PATH) setup.py				\
			WX_CONFIG=../bld/wx-config		\
			build_ext --inplace;			\
	)


install::
	mkdir -p $(ROOT)/$(PKGROOT)
	mkdir -p $(ROOT)/etc/ld.so.conf.d
	echo /lib           >> $(ROOT)/etc/ld.so.conf.d/$(NAME)-$(ARCH).conf
	echo /lib64         >> $(ROOT)/etc/ld.so.conf.d/$(NAME)-$(ARCH).conf
	echo /usr/lib       >> $(ROOT)/etc/ld.so.conf.d/$(NAME)-$(ARCH).conf
	echo /usr/lib64     >> $(ROOT)/etc/ld.so.conf.d/$(NAME)-$(ARCH).conf
	echo $(PKGROOT)/lib >> $(ROOT)/etc/ld.so.conf.d/$(NAME)-$(ARCH).conf
	(							\
		cd wxPython-src-$(VERSION)/bld;			\
		make prefix=$(ROOT)/$(PKGROOT) install;		\
		make prefix=$(ROOT)/$(PKGROOT) -C contrib/src/gizmos  install;\
		make prefix=$(ROOT)/$(PKGROOT) -C contrib/src/stc     install;\
	)
	# fix the wx-config symlink to point into the /opt not
	# the build area config
	(							\
		cd $(ROOT)/$(PKGROOT)/bin;			\
		rm wx-config;					\
		ln -s ../lib/wx/config/* wx-config;		\
	)
	# install the python hooks
	(							\
		cd wxPython-src-$(VERSION)/wxPython;		\
		$(PY.PATH) setup.py				\
		WX_CONFIG="$(ROOT)/$(PKGROOT)/bin/wx-config --prefix=$(ROOT)/$(PKGROOT)"\
		install --root=$(ROOT);				\
	)

clean::
	rm -rf wxPython-src-$(VERSION)

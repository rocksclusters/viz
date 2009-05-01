# --------------------------------------------------- -*- Makefile -*- --
# $Id: Makefile,v 1.26 2009/05/01 19:07:32 mjk Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 5.2 (Chimichanga)
# 
# Copyright (c) 2000 - 2009 The Regents of the University of California.
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
# Revision 1.26  2009/05/01 19:07:32  mjk
# chimi con queso
#
# Revision 1.25  2008/10/18 00:56:22  mjk
# copyright 5.1
#
# Revision 1.24  2008/07/01 23:07:59  mjk
# roll almost v ready
#
# Revision 1.23  2008/03/06 23:42:03  mjk
# copyright storm on
#
# Revision 1.22  2007/07/11 00:13:06  mjk
# - update boostrapping
# - /opt/rocks for non-viz stuff
# - /opt/viz for viz only stuff
# - support for doom
#
# Revision 1.21  2007/06/23 04:04:06  mjk
# mars hill copyright
#
# Revision 1.20  2007/04/26 23:08:14  mjk
# using all the bits
#
# Revision 1.19  2006/12/07 06:58:08  phil
# Add profiles to search for vtk shared object libararies
#
# Revision 1.18  2006/12/06 19:11:06  phil
# Add building of shared object files
#
# Revision 1.17  2006/12/02 05:27:27  phil
# Install in /opt/vtk
#
# Revision 1.16  2006/12/01 21:25:02  phil
# Captial VTK.
#
# Revision 1.15  2006/12/01 20:17:58  phil
#
# This should build
#
# Revision 1.14  2006/11/16 15:32:21  mjk
# *** empty log message ***
#
# Revision 1.13  2006/09/11 22:50:43  mjk
# monkey face copyright
#
# Revision 1.12  2006/08/10 00:12:18  mjk
# 4.2 copyright
#
# Revision 1.11  2005/12/30 18:39:48  mjk
# remove spec files
#
# Revision 1.10  2005/10/12 18:11:20  mjk
# final copyright for 4.1
#
# Revision 1.9  2005/09/16 01:04:59  mjk
# updated copyright
#
# Revision 1.8  2005/05/24 21:24:10  mjk
# update copyright, release is not any closer
#
# Revision 1.7  2004/09/01 01:28:13  mjk
# nuke uids so it builds
#
# Revision 1.6  2004/01/16 05:41:39  mjk
# cmake.in built on the fly -- need variables
#
# Revision 1.5  2004/01/16 05:05:19  mjk
# first pass at rpm
#
# Revision 1.4  2004/01/16 03:32:22  mjk
# turn off java support for now
#
# Revision 1.3  2004/01/15 22:53:36  mjk
# *** empty log message ***
#
# Revision 1.2  2004/01/15 22:47:05  mjk
# patching another great piece of software
#
# Revision 1.1  2004/01/15 21:28:57  mjk
# *** empty log message ***
#


PKGROOT		= /opt/$(NAME)
REDHAT.ROOT	= $(PWD)/../../
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

install::
	mkdir -p $(ROOT)/$(PKGROOT)/lib
	mkdir -p $(ROOT)/etc/profile.d
	install -m 755 profile.d/*sh $(ROOT)/etc/profile.d
	cp -a html $(ROOT)/$(PKGROOT)/
	cp -a VTKData $(ROOT)/$(PKGROOT)/
	chown -R root.root $(ROOT)/$(PKGROOT)
	(								\
		cd vtkmpeg2encode;					\
		$(INSTALL) -m644 					\
			libvtkMPEG2Encode.so				\
			$(ROOT)/$(PKGROOT)/lib/;			\
	)
	(								\
		cd VTK;							\
		chown -R root.root .;					\
		make install;						\
	)

build: 
	gunzip -c $(NAME)-$(VERSION).tar.gz | tar -x
	gunzip -c $(NAME)data-$(VERSION).tar.gz | tar -x
	gunzip -c $(NAME)DocHtml-$(VERSION).tar.gz | tar -x
	gunzip -c vtkmpeg2encode.tar.gz | tar -x
	(								\
		cd vtkmpeg2encode;					\
		/opt/rocks/bin/cmake 					\
			-DBUILD_SHARED_LIBS=BOOL:YES			\
			.;						\
		make;							\
	)
	(								\
		cd VTK;							\
		/opt/rocks/bin/cmake					\
			-DCMAKE_INSTALL_PREFIX:PATH=$(ROOT)$(PKGROOT)	\
			-DBUILD_EXAMPLES:BOOL=ON			\
			-DBUILD_SHARED_LIBS:BOOL=ON			\
			-DVTK_WRAP_PYTHON:BOOL=ON			\
			-DVTK_USE_MPEG2_ENCODER:BOOL=ON			\
			-DvtkMPEG2Encode_INCLUDE_PATH:PATH=$(PWD)/vtkmpeg2encode \
			-DvtkMPEG2Encode_LIBRARIES:STRING=$(PWD)/vtkmpeg2encode/libvtkMPEG2Encode.so \
			. ;						\
		make;							\
	)

clean::
	rm -rf VTK VTKData html vtkmpeg2encode
	rm -f $(NAME).spec.in

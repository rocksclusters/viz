#!/bin/sh
#
# This file should remain OS independent
#
# $Id: bootstrap.sh,v 1.15 2008/10/15 20:13:05 mjk Exp $
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
# $Log: bootstrap.sh,v $
# Revision 1.15  2008/10/15 20:13:05  mjk
# - more changes to build outside of the tree
# - removed some old fds-only targets
#
# Revision 1.14  2008/07/15 22:41:46  mjk
# added portaudio
#
# Revision 1.13  2008/03/12 17:32:31  bruno
# better bootstrap
#
# Revision 1.12  2008/03/06 23:41:59  mjk
# copyright storm on
#
# Revision 1.11  2008/03/03 20:15:54  bruno
# no more sage2
#
# Revision 1.10  2007/12/17 22:26:17  bruno
# updated SDL and SDL_ttf for V
#
# Revision 1.9  2007/07/11 00:13:05  mjk
# - update boostrapping
# - /opt/rocks for non-viz stuff
# - /opt/viz for viz only stuff
# - support for doom
#
# Revision 1.8  2007/06/23 04:04:02  mjk
# mars hill copyright
#
# Revision 1.7  2006/09/11 22:50:20  mjk
# monkey face copyright
#
# Revision 1.6  2006/08/10 00:12:03  mjk
# 4.2 copyright
#
# Revision 1.5  2006/07/25 23:44:55  mjk
# add evl bootstrap
#
# Revision 1.4  2006/02/14 21:47:09  mjk
# use dmx from centos
#
# Revision 1.3  2006/02/14 20:52:14  mjk
# FlightGear bootstrapping
#
# Revision 1.2  2006/02/07 22:01:31  mjk
# add bootstrapping
#
# Revision 1.1  2006/02/07 22:00:47  mjk
# add bootstrapping
#

. $ROLLSROOT/etc/bootstrap-functions.sh

install_os_packages viz-server

install libdmx
install libdmx-devel

compile SRPMS
install glut
install glut-devel
install joy2key
install joystick

compute_and_install cmake

compile_and_install foundation-sdl
compile_and_install foundation-sdl-image
compile_and_install foundation-sdl-mixer
compile_and_install foundation-sdl-net
compile_and_install foundation-sdl-ttf

compile_and_install chromium
compile_and_install libraw1394
compile_and_install openal
compile_and_install freealut
compile_and_install plib
compile_and_install SimGear

compile_and_install libmad
compile_and_install libdvdread
compile_and_install faac
compile_and_install faad2
compile_and_install ffmpeg
compile_and_install mpeg2dec
compile_and_install wx
compile_and_install portaudio

compile quanta
install QUANTA


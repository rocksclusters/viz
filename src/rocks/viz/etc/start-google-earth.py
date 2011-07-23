#! /opt/rocks/bin/python
#
# Start Google Earth on the specified display using a unique HOME directory for the
# cache and configuration files.  The lock file is still shared between instances which
# is wrong but not a real problem.  Google Earth is like Firefox in that it trys hard to
# have only one instance per user.  By lying about the HOME directory we can get away
# with this.
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4.3 (Viper)
# 
# Copyright (c) 2000 - 2011 The Regents of the University of California.
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
# 	Development Team at the San Diego Supercomputer Center at the
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
# $Log: start-google-earth.py,v $
# Revision 1.4  2011/07/23 02:31:38  phil
# Viper Copyright
#
# Revision 1.3  2011/01/14 18:52:44  mjk
# New version on Google Earth (just released
#
# Revision 1.2  2010/12/18 00:27:34  mjk
# *** empty log message ***
#
# Revision 1.1  2010/10/07 19:47:12  mjk
# - added support for Google's Liquid Galaxy
# - remove sage and some of the deps
#


import os
import sys
import pwd
import shutil
import socket
import string


display = sys.argv[1]

dir = os.path.join(os.sep, 'tmp',
		   'ge-%s-%s:%s' % (pwd.getpwuid(os.getuid()).pw_name,
				    socket.gethostname(), display))

# Clone the google-earth directory so we can have a unique drivers.ini file,
# just doing lndir will not work.
	
if not os.path.exists(dir):
	shutil.copytree('/opt/google/earth/free', dir)

# Copy config files from the viz user account to turn off layer that we want
# turned on for the frontend.
	
if not os.path.exists(os.path.join(dir, '.config')):
	shutil.copytree(os.path.join(os.sep, 'opt', 'viz', 'etc', '.config'),
			os.path.join(dir, '.config'))

# Copy tile specific drivers.ini file.  This is where the offsets for the
# display are specified.  Original files created by rocks sync tile googleearth

os.unlink(os.path.join(dir, 'drivers.ini')) 
shutil.copyfile(os.path.join('/opt/google/earth/free', 'drivers.ini:%s' % display),
		os.path.join(dir, 'drivers.ini'))


os.system('DISPLAY=:%s HOME=%s %s/googleearth --fullscreen &' % (display, dir, dir))



#! /opt/rocks/bin/python
#
# Start Google Earth on the specified display using a unique HOME directory for the
# cache and configuration files.  The lock file is still shared between instances which
# is wrong but not a real problem.  Google Earth is like Firefox in that it trys hard to
# have only one instance per user.  By lying about the HOME directory we can get away
# with this.
#
# @Copyright@
# @Copyright@
#
# $Log: start-google-earth.py,v $
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
	shutil.copytree('/opt/google-earth', dir)

# Copy config files from the viz user account to turn off layer that we want
# turned on for the frontend.
	
if not os.path.exists(os.path.join(dir, '.config')):
	shutil.copytree(os.path.join(os.sep, 'opt', 'viz', 'etc', '.config'),
			os.path.join(dir, '.config'))

# Copy tile specific drivers.ini file.  This is where the offsets for the
# display are specified.  Original files created by rocks sync tile googleearth
	
shutil.copyfile(os.path.join('/opt/google-earth', 'drivers.ini:%s' % display),
		os.path.join(dir, 'drivers.ini'))


os.system('DISPLAY=:%s HOME=%s %s/googleearth --fullscreen &' % (display, dir, dir))



# $Id: Makefile,v 1.1 2010/03/11 03:08:34 mjk Exp $
#
# Build and pick out only the RPMs from this Roll that will be served as 
# updates.  You should always tag the CVS Tree (including this file) and then
# run the command.
#
# This file is pretty verbose by design.  It forces us to be explicit about
# updates, dangerous stuff.
#
# Type 'make' and you can then copy the resulting RPMs into the updates
# directory.  For example:
# 	ftp.rocksclusters.org:/var/ftp/pub/rocks/rocks-5.3/linux/updates
#
# @Copyright@
# @Copyright@
#
# $Log: Makefile,v $
# Revision 1.1  2010/03/11 03:08:34  mjk
# let's see if we can update this roll
#


rpm: \
	roll-viz-kickstart-5.3-1.noarch.rpm	\
	rocks-viz-5.3-1.noarch.rpm		\
	rocks-command-viz-5.3-1.x86_64.rpm	\
	nvidia-driver-5.3-2.x86_64.rpm

# graph/nodes
#  - new attributes
#  - new conds

roll-viz-kickstart-5.3-1.noarch.rpm:
	(cd ..; make profile)
	cp ../RPMS/noarch/$@ $@

# screensaver updated to show driver version

rocks-viz-5.3-1.noarch.rpm:
	make -C ../src/rocks rpm
	cp ../RPMS/noarch/$@ $@

# heavily updated

rocks-command-viz-5.3-1.x86_64.rpm:
	make -C ../src/rocks-command rpm
	cp ../RPMS/x86_64/$@ $@

# new driver
# - automatically updates to latest driver (if online)

nvidia-driver-5.3-2.x86_64.rpm:
	make -C ../src/nvidia rpm
	cp ../RPMS/x86_64/$@ $@

clean:
	-rm *.rpm

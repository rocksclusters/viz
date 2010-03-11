#!/bin/bash
#
# This script is called by the 'rocks update' command to complete the
# update processes for the Frontend.  THIS FILE MUST BE RE-ENTRANT, since it
# is called every time 'rocks update' is run.
#
# Normally this file will be empty, but if the XML profile of the Frontend has
# changed since the release you must replicate the changes here.  If this file 
# becomes long you should be re-releasing the Roll and not supporting updates.
#
# We do not try to use 'rocks run roll' because the Graph is not re-entrant.
# Specifically, in this Roll the XML drops tables to create the schema.
#
# @Copyright@
# @Copyright@
#
# $Log: update-viz.sh,v $
# Revision 1.1  2010/03/11 03:08:34  mjk
# let's see if we can update this roll
#


# If the viz_use_cuda attribute is present the Frontend is already current
# and we return success.  Otherwise update the attributes and multicast
# route for GCLX.

if rocks list appliance attr tile | fgrep viz_use_cuda; then
	exit 0
fi


# From viz-server.xml

/opt/rocks/bin/rocks set appliance attr tile viz_use_cuda    true
/opt/rocks/bin/rocks set appliance attr tile viz_use_nvidia  true
/opt/rocks/bin/rocks set appliance attr tile viz_x11_modules "dbe extmod type1 freetype glx"

/opt/rocks/bin/rocks add route 225.0.0.0 eth0 netmask=255.255.255.0


# Special cleanup - remove old attributes (not strictly required)

/opt/rocks/bin/rocks remove appliance attr tile cuda
/opt/rocks/bin/rocks remove appliance attr tile viz_nvidia_driver
/opt/rocks/bin/rocks remove appliance attr tile viz_nvidia_driver_options



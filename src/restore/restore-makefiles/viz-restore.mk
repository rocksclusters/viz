#
# $Id: viz-restore.mk,v 1.2 2008/01/16 17:30:58 bruno Exp $
#
# $Log: viz-restore.mk,v $
# Revision 1.2  2008/01/16 17:30:58  bruno
# update for rocks command line
#
# Revision 1.1  2006/07/27 19:46:54  bruno
# first pass at the viz extensions to the restore roll
#
#
TILELAYOUTFILE		= /tmp/tilelayout.xml
FILES			+= $(TILELAYOUTFILE)

TILELAYOUTSCRIPT	= viz-restore-post.sh
SCRIPTS			+= $(TILELAYOUTSCRIPT)


viz_files:
	/opt/rocks/bin/rocks list viz layout > $(TILELAYOUTFILE)

viz_post:
	echo "/opt/rocks/bin/rocks create viz layout $(TILELAYOUTFILE)" > \
		$(TILELAYOUTSCRIPT)	

pretar::	viz_files viz_post

clean::
	rm -f $(TILELAYOUTSCRIPT)


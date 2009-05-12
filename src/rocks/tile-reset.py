#!/opt/rocks/bin/python
#
# @Copyright@
# @Copyright@
#
# $Log: tile-reset.py,v $
# Revision 1.2  2009/05/12 18:36:29  mjk
# *** empty log message ***
#
# Revision 1.1  2009/05/12 00:26:54  mjk
# *** empty log message ***
#

import sys
import os
import tempfile

resolutions = sys.argv[1:]

tmp = tempfile.mktemp()

os.system('/opt/viz/bin/nvidia-xconfig \
	--separate-x-screens --no-twinview -a -o %s> /dev/null' % tmp)

display = -1
fin = open(tmp, 'r')
try:
	fout = open('/etc/X11/xorg.conf', 'w')
except:
	fout = None

for line in fin.readlines():
	if line.find('"DPMS"') != -1:
		line = '\tOption\t"DPMS"\t"False"\n'
	elif line.find('Section "Screen"') != -1:
		display += 1
	elif line.find('SubSection     "Display"') != -1:
		try:
			line += '\tModes\t"%s"\n' % resolutions[display]
		except:
			pass
	if fout:
		fout.write(line)
	else:
		print line[:-1]

fin.close()
if fout:
	fout.close()
os.unlink(tmp)



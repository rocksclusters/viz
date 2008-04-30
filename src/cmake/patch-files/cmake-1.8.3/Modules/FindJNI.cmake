# $Id: FindJNI.cmake,v 1.2 2004/01/15 22:40:37 mjk Exp $
#
# This module finds if Java is installed and determines where the
# include files and libraries are. It also determines what the name of
# the library is. This code sets the following variables:
#
#  JAVA_AWT_LIB_PATH     = the path to where the jawt library is
#  JAVA_INCLUDE_PATH     = the path to where jni.h can be found
#  JAVA_AWT_INCLUDE_PATH = the path to where jni.h can be found
# 
# $Log: FindJNI.cmake,v $
# Revision 1.2  2004/01/15 22:40:37  mjk
# fix awt library path
#
# Revision 1.1  2004/01/15 22:13:16  mjk
# fix java paths (cmake sucks)
#

# Rocks - Throw away everything else and set this up for the Java Roll

SET(JAVA_AWT_LIBRARY_DIRECTORIES
  /usr/java/j2sdk1.4.2_02/jre/lib/i386
  /usr/java/j2sdk1.4.2_02/jre/lib/ia64
  )

SET(JAVA_AWT_INCLUDE_DIRECTORIES
  /usr/java/j2sdk1.4.2_02/include
  )

# add in the include path    
FIND_PATH(JAVA_INCLUDE_PATH jni.h 
  ${JAVA_AWT_INCLUDE_DIRECTORIES}
)

FIND_PATH(JAVA_INCLUDE_PATH2 jni_md.h 
  ${JAVA_AWT_INCLUDE_DIRECTORIES}
  ${JAVA_INCLUDE_PATH}/win32
  ${JAVA_INCLUDE_PATH}/linux
)

FIND_PATH(JAVA_AWT_INCLUDE_PATH jawt.h 
          ${JAVA_AWT_INCLUDE_DIRECTORIES} ${JAVA_INCLUDE_PATH} )

MARK_AS_ADVANCED(
  JAVA_AWT_LIBRARY
  JAVA_AWT_INCLUDE_PATH
  JAVA_INCLUDE_PATH
  JAVA_INCLUDE_PATH2
)

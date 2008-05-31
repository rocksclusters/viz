# $Id: config.mk,v 1.1 2008/05/31 02:57:57 mjk Exp $
#
# Rocks configuration for SAGE
#
# $Log: config.mk,v $
# Revision 1.1  2008/05/31 02:57:57  mjk
# - SAGE is back and works (mostly)
# - DMX building from source (in progress)
# - Updated nvidia driver
#

IS_ROCKS=1
AUDIO=1
GLSL_YUV=1

COMPILER=g++

QUANTA_DIR=/opt/viz
QUANTA_CFLAGS=-I${QUANTA_DIR}/include -DQUANTA_USE_PTHREADS -DQUANTA_THREAD_SAFE
QUANTA_LIB=-L${QUANTA_DIR}/lib

SDL_CFLAGS=`/opt/rocks/bin/sdl-config --cflags`
SDL_LIBS=`/opt/rocks/bin/sdl-config --libs`

READLINE_CFLAGS=
READLINE_LIB=-lreadline -lncurses

PORTAUDIO_DIR=/opt/rocks
PORTAUDIO_CFLAGS=-I${PORTAUDIO_DIR}/include -DSAGE_AUDIO
PAUDIO_LIB= -L${PORTAUDIO_DIR}/lib -lportaudio -lasound


SAIL_LIB=libsail.so
SHLD_FLAGS=-shared

# GPU programming setting
ifeq ($(GLSL_YUV), 1)
  GLEW_LIB= -lGLEW
  GLEW_CFLAGS=
  GLSL_YUV_DEFINE=-DGLSL_YUV
else
  GLEW_LIB=
  GLEW_CFLAGS=
  GLSL_YUV_DEFINE=
endif

MACHINE=$(shell uname -s)
ARCHITECTURE=$(shell uname -p)

ifeq ($(ARCHITECTURE), x86_64)
  QUANTA_LIB=-L${QUANTA_DIR}/lib -lquanta_64
  XLIBS=-L/usr/X11R6/lib64 -lGLU -lGL -lXmu -lXi -lXext -lX11
else
  # anything else is 32bit 
  QUANTA_LIB=-L${QUANTA_DIR}/lib -lquanta_32
  XLIBS=-L/usr/X11R6/lib -lGLU -lGL -lXmu -lXi -lXext -lX11
endif





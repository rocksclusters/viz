#!/bin/bash

/opt/rocks/bin/mplayer -vo gl:yuv=2 -framedrop $@ 

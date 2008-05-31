PREFIX=$(ROOT)/opt/sage

preprojects = 
subprojects = app app/atlantis app/vnc app/FileViewer app/bitplay app/mplayer


default:
	@for i in `echo $(preprojects)`; do pushd $$i; $(MAKE) install; popd ; done
	@pushd src; $(MAKE) install; popd
	@for i in `echo $(subprojects)`; do pushd $$i; $(MAKE) install; popd ; done

install: default
	/bin/mkdir -p ${PREFIX}
	/bin/cp -rf bin ${PREFIX}
	/bin/cp -rf lib ${PREFIX}
	/bin/cp -rf include ${PREFIX}
	/bin/cp -rf ui dim ${PREFIX}

clean:
	@for i in `echo $(preprojects)`; do pushd $$i; $(MAKE) $@; popd ; done
	@for i in `echo src $(subprojects)`; do pushd $$i; $(MAKE) $@; popd ; done


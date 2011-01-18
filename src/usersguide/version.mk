NAME    = roll-$(ROLL)-usersguide
RELEASE = 1
RPM.ARCH = noarch

SUMMARY_COMPATIBLE      = $(VERSION)
SUMMARY_MAINTAINER      = Rocks Group
SUMMARY_ARCHITECTURE    = x86_64

ROLL_REQUIRES           = base hpc kernel os1 os2 $(ROLL)
ROLL_CONFLICTS          = xen


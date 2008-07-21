NAME    = roll-$(ROLL)-usersguide
RELEASE = 0

SUMMARY_COMPATIBLE      = $(VERSION)
SUMMARY_MAINTAINER      = Rocks Group
SUMMARY_ARCHITECTURE    = i386, x86_64

ROLL_REQUIRES           = base hpc kernel java os1 os2 os3 os4 os5 service-pack $(ROLL)
ROLL_CONFLICTS          = xen


NAME    = roll-$(ROLL)-usersguide
RELEASE = 2
RPM.ARCH = noarch

SUMMARY_COMPATIBLE      = $(VERSION)
SUMMARY_MAINTAINER      = Rocks Group
SUMMARY_ARCHITECTURE    = x86_64

ROLL_REQUIRES           = base kernel service-pack os
ROLL_REQUIRES_FULL_OS	= 1
ROLL_CONFLICTS          = xen


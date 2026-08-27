#!/bin/sed -f
# sed -i -r -f sddm.conf.sed /etc/sddm.conf
/RememberLastUser/s/^# *//
s/RememberLastUser=true/RememberLastUser=false/

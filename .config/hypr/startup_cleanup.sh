#!/env/bin/bash
sleep 10
hyperctl keyword windowrule "workspace unset,WebCord"
hyperctl keyword windowrule "workspace unset,title:^(Steam)(.*)$"

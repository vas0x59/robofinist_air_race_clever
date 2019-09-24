#!/bin/sh

# echo ""


# Mavlink SDK
# echo $$


GREEN='\033[0;32m'
LGREEN='\033[1;32m'

ORANGE='\033[0;33m'

RED='\033[0;31m'
LRED='\033[1;31m'

BLUE='\033[0;34m'
LBLUE='\033[1;34m'

PURPLE='\033[0;35m'
LPURPLE='\033[1;35m'

CYAN='\033[0;36m'
LCYAN='\033[1;36m'

NC='\033[0m'


ar=$(arch)
# ar="x86"
program="$1"
ip_port="127.0.0.1:14540"

ar_postfix=""

if [ "$ar" = "x86_64" ]
then
    LCOLOR=$LBLUE
else 
    if [ "$ar" = "armv7l" ]
    then
        LCOLOR=$LGREEN
        ar_postfix=" : ${LGREEN}Raspberry${LRED} PI${NC}"
        export LD_LIBRARY_PATH=/home/pi/lib 
    else
        if [ "$ar" = "armv6l" ]
        then
            LCOLOR=$LPURPLE
            ar_postfix=" : ${LPURPLE}Raspberry${LRED} PI Zero${NC}"
            export LD_LIBRARY_PATH=/home/pi/lib 
        else
        LCOLOR=$ORANGE
        fi
    fi
fi

logo=" 

 on $LCOLOR$ar$NC$ar_postfix
 Version $(./get_version.sh)
                                                                                     by Vasily Yuryev
                                                                                                 2019
"
echo "$logo"

echo "$(uname -a)"
echo ""
# ./log.sh INFO runner START
# ./log.sh INFO runner Starting mavlink-router

# echo ""




# echo "mavlink-routerd_pid: $mrouter_pid"

if [ -f "/home/pi/src/$program" ]
then
    ./log.sh INFO runner "Starting $program"
    echo ""
    python /home/pi/src/$program
else
    ./log.sh ERROR runner "File: $program - not found"
fi
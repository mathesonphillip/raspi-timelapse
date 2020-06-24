#!/usr/bin/env bash
#
# Python script for timelapse photography with the RaspberryPi
# Based upon: https://www.raspberrypi.org/documentation/usage/camera/raspicam/timelapse.md
#
# Intended to be used with grep on the RaspberryPi
#
#

##########################
#? This section handles input parameters
#?  Allows you to set the delay between images
#?  Sets defaults
##########################
Script="run_timelapse.sh"            # Used to print out the help
Delay=5                              # Delay (seconds) between photos
Length=1440                          # Length (minutes) of timelapse session
Timestamp=$(date +%Y-%m-%dT%H-%M-%S) # Used to create the filename
Filename=$Timestamp_d$Delay_l$Length # Used to create the filename

function example() {
    echo -e "EXAMPLES:"
    echo -e "   $Script -d <SECONDS> -l <MINUTES>"
    echo -e "   $Script"
    echo -e "   $Script -d 3 -l 60"
    echo -e "   $Script -d 10 -l 120"
    echo -e ""
}

function usage() {
    echo -e "Usage: $0 [-d seconds] [-l minutes]"
    echo -e ""
}

function help() {
    usage
    echo -e "OPTION:"
    echo -e "  -d, Delay (seconds) between photos. Default=5"
    echo -e "  -l, Length (minutes) of timelapse session. Default=1440 (24hrs)"
    echo -e ""
    example
    exit 1
}

while getopts 'al' arg; do
    case "$arg" in
    d)
        Delay="$OPTARG"
        ;;
    l)
        Length="$OPTARG"
        ;;
    [?])
        help
        ;;
    esac
done
shift $((OPTIND - 1))

# ##########################
# Convert default inputs to actual values
#   raspistill command expects inputs in ms
#   need to convert seconds into milliseconds
# ##########################

Delay=$Delay * 1000
Length=$Length * 1000

echo $Delay
echo $Length
echo $Filename

# ################

# raspistill --timelapse $Delay -t $Length -o /home/pi/timelapse/"$FILENAME".jpg

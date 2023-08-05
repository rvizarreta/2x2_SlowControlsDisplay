#!/bin/bash

# set environment variables
echo "Exporting environment variables"

# path to working directory for the tests
export TESTDIR="/home/acd/acdemo/gizmo-control"
echo "TESTDIR=$TESTDIR"

# path to DAQ executable
export DAQEXECPATH="/home/acd/acdemo/gizmo-control/gizmo"
echo "DAQEXECPATH=$DAQEXECPATH"

# activate venv
source $TESTDIR/py3/bin/activate

NC=$'\e[0m'
RED=$'\e[0;31m'
CY=$'\e[0;36m' 

cd $DAQEXECPATH

STARTDATE=$(date '+%Y-%m-%d %H:%M:%S')
echo "${CY}Start Date and Time is: ${STARTDATE}${NC}"

echo "${RED}Executing $DAQEXECPATH/gizmo_write.py -d False${NC}"

python3 $DAQEXECPATH/gizmo_write.py -d False
 
ENDDATE=$(date '+%Y-%m-%d %H:%M:%S')
echo "${CY}End Date and Time is: ${ENDDATE}${NC}"

cd $TESTDIR



#!/bin/bash

# path to working directory for the tests
export TESTDIR="/home/acd/acdemo/gizmo-control"

# path to DAQ executable
export DAQEXECPATH="/home/acd/acdemo/gizmo-control/gizmo"

# activate venv
source $TESTDIR/py3/bin/activate

cd $DAQEXECPATH

# execute python script
python3 $DAQEXECPATH/save_plot.py

deactivate


## Impedance monitor control
Set of tools to control the Ground Impedance Monitor (GIZMO) at LArTF.

* Read values from the impedance monitor (GIZMO) and store them in InfluxDB.


**Use screen to run the test in detached mode**
- Create a new screen
~~bash
$ screen -S <session_name>
~~
To go on detached mode, press ```Ctrl+a``` ``` Ctrl+d```

- To reattach to a screen session, find the session ID with:
~~bash
$ screen -ls
~~
and then 
~~bash
$ screen -rd <ID>
~~

**Start acquiring GIZMO data**
~~bash
$ cd /home/acd/acdemo/gizmo-control
$ . launch.sh
~~

**Set a cron-job to save plots**

~~bash
$ crontab -e

59 23 * * * . /home/acd/acdemo/gizmo-control/gizmo/plot.sh
~~

This executes `plot.sh` every 24 hours (i.e. each day at 11:59 PM).

**Stop acquisition**

To stop data acquisition reattach to screen session
~~bash
$ screen -rd <ID>
~~
and then press ``` Ctrl+c```.

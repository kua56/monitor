# monitoring

Monitor a linux system, especailly CentOS, then post those information to a slack channel.

1. monitor
It collects cpu temparature, ram usage, disk usage and store them into sqlite3 tables.

2. prep
It creates tables needed by other scripts.

3. report
It posts monitored information aquired from sqlite3 tables.

# requirement

Python 3.x and venv

check requirements.txt for python libraries.

# installation

1.create sqlite3 tables.
$ python prep.py

2.change config.ini

result_file: adjust path to where you want to place temporary working file.

slack_post: set to your slack webhool url.

# usage

1.collect your system information.

$ python monitor.py

2.post collected system information.

$ python report.py

It is recomended to add those script to your crontab.

ex:

2 * * * * /home/dev/monitor/monitor.sh 2>&1 | logger -t monitor.sh -p local0.info

3 10-18/2 * * * /home/dev/monitor/report.sh 2>&1 | logger -t report.sh -p local0.info

# license
See LICENSE.


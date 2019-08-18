import datetime
import subprocess
from sqlalchemy import create_engine

engine = create_engine('sqlite:///monitor.sqlite')

def get_temp():
    """get cpu temparature"""
 
    now = datetime.datetime.now()

    try:
        args = ['cat', '/sys/devices/platform/coretemp.0/hwmon/hwmon1/temp1_input']
        res = subprocess.check_output(args)
        values = res.decode('utf8').split()
        values.insert(0, '{0:%Y-%m-%d}'.format(now))
        values.insert(1, '{0:%H:%M:%S}'.format(now))
        values.append(0)

        keys = ['check_date', 'check_time', 'cpu_temp', 'cpu_num']
        insert_data = dict(zip(keys, values))

        with engine.connect() as con:
            con.execute("insert into os_temp(" \
            "check_date, check_time, cpu_temp, cpu_num) " \
            "values(:check_date, :check_time, :cpu_temp, :cpu_num)", 
            **insert_data)

    except subprocess.CalledProcessError as e:
        print(e.cmd)
        print(e.output)

def get_ram_usage():
    """get ram usage"""

    now = datetime.datetime.now()

    try:
        args = ['free']
        res = subprocess.check_output(args)
        res = res.decode('utf8').split('\n')
        values = res[1].split()[1:]
        values.insert(0, '{0:%Y-%m-%d}'.format(now))
        values.insert(1, '{0:%H:%M:%S}'.format(now))

        keys = ['check_date', 'check_time', 'total_amount', 'usage_amount', 
                'free_amount', 'shared_amount', 'buff_cache_amount', 
                'available_amount']
        insert_data = dict(zip(keys, values))

        with engine.connect() as con:
            con.execute("insert into ram_usage(" \
                "check_date, check_time, total_amount, usage_amount, " \
                "free_amount, shared_amount, buff_cache_amount, " \
                "available_amount) " \
            "values(:check_date, :check_time, :total_amount, " \
                ":usage_amount, :free_amount, :shared_amount, " \
                ":buff_cache_amount, :available_amount)",
            **insert_data)
        
    except subprocess.CalledProcessError as e:
        print(e.cmd)
        print(e.output)

def get_disk_usage():
    """get disk usage"""

    now = datetime.datetime.now()

    try:
        args = ['df']
        res = subprocess.check_output(args)
        res = res.decode('utf8').split('\n')

        keys = ['check_date', 'check_time', 'filesystem', \
               'disk_size', 'disk_used', 'disk_available', 'mount']

        for r in res[1:-1]:
            r = r.split()
            r.insert(0, '{0:%Y-%m-%d}'.format(now))
            r.insert(1, '{0:%H:%M:%S}'.format(now))
            insert_data = dict(zip(keys, r))

            with engine.connect() as con:
                con.execute("insert into disk_usage(" \
                    "check_date, check_time, filesystem, " \
                    "disk_size, disk_used, disk_available, mount) " \
                "values(" \
                    ":check_date, :check_time, :filesystem, " \
                    ":disk_size, :disk_used, :disk_available, :mount)", 
                **insert_data)

    except subprocess.CalledProcessError as e:
        print(e.cmd)
        print(e.output)

def main():

    get_temp()
    get_ram_usage()
    get_disk_usage()

if __name__ == '__main__':
    main()

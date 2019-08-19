import datetime
import subprocess
from sqlalchemy import *
import configparser
import slackweb

config = configparser.ConfigParser()
config.read('config.ini')
db_string = config['DB']['db_string']
result_file = config['RESULT']['result_file']
slack_post = config['URL']['slack_post']

engine = create_engine(db_string)

now = datetime.datetime.now()
today = '{0:%Y-%m-%d}'.format(now)


def get_temp():
    """get cpu temparature"""

    q = (
        select([
            literal_column('cpu_temp'),
        ])
        .select_from(table('os_temp'))
        .where(literal_column('check_date') == today)
        .order_by(text('check_date desc LIMIT 1'))
    )
 
    try:
        rows = engine.execute(q)
        #print(rows.fetchone())
        with open(result_file, 'w', encoding='utf-8') as f:
            for row in rows:
                #print(row)
                f.write("CPU temp: \n")
                f.write("  {:.2f}".format(row[0] / 1000) + "C\n")

    except subprocess.CalledProcessError as e:
        print(e.cmd)
        print(e.output)

def get_ram_usage():
    """get ram usage"""

    q = (
        select([
            literal_column('total_amount'),
            literal_column('usage_amount'),
            literal_column('free_amount'),
            literal_column('shared_amount'),
            literal_column('buff_cache_amount'),
            literal_column('available_amount'),
        ])
        .select_from(table('ram_usage'))
        .where(literal_column('check_date') == today)
        .order_by(text('check_date desc LIMIT 1'))
    )

    try:
       rows = engine.execute(q)
       with open(result_file, 'a', encoding='utf-8') as f:
           f.write("\nMempory usage:\n")
           for row in rows:
               #print(row)
               f.write('  total: ' + "{:.2f}".format(row[0]/1000) + 'MB\n')
               f.write('  used: ' + "{:.2f}".format(row[1]/1000) + 'MB\n')
               f.write('  free: ' + "{:.2f}".format(row[2]/1000) + 'MB\n')
               f.write('  shared: ' + "{:.2f}".format(row[3]/1000) + 'MB\n')
               f.write('  buff/cache: ' + "{:.2f}".format(row[4]/1000) + 'MB\n')
               f.write('  avail: ' + "{:.2f}".format(row[5]/1000) + 'MB\n')
 
    except subprocess.CalledProcessError as e:
        print(e.cmd)
        print(e.output)

def get_disk_usage():
    """get disk usage"""

    q = (
        select([
            literal_column('check_date'),
            literal_column('check_time'),
            literal_column('filesystem'),
            literal_column('disk_size'),
            literal_column('disk_used'),
            literal_column('disk_available'),
            literal_column('mount'),
        ])
        .select_from(table('disk_usage'))
        .where(
            and_(
                literal_column('check_date') == today,
                text('check_time = (select max(check_time) as t from disk_usage group by check_date order by t limit 1)')
            )
        )
    )

    try:
        rows = engine.execute(q)
        with open(result_file, 'a', encoding='utf-8') as f:
            f.write("\nDisk usage:\n")
            for row in rows:
                f.write("  " + str(row) + '\n')

    except subprocess.CalledProcessError as e:
        print(e.cmd)
        print(e.output)

def main():

    get_temp()
    get_ram_usage()
    get_disk_usage()

    post = ""
    with open(result_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            post += line

    print(post) 
    slack = slackweb.Slack(url=slack_post)
    slack.notify(text=post)

if __name__ == '__main__':
    main()

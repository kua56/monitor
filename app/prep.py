from sqlalchemy import create_engine

def main():
    """create tables for monotoring tool"""
    engine = create_engine('sqlite:///monitor.sqlite')
    with engine.connect() as con:

        con.execute("drop table if exists os_temp")
        con.execute("create table os_temp(id integer primary key, check_date text, check_time text, cpu_temp real, cpu_num integer)")

        con.execute("drop table if exists ram_usage")
        con.execute("create table ram_usage(id integer primary key, check_date text, check_time text, total_amount integer, usage_amount integer, free_amount integer, shared_amount integer, buff_cache_amount integer, available_amount integer)")

        con.execute("drop table if exists disk_usage")
        con.execute("create table disk_usage(id integer primary key, check_date text, check_time text, filesystem text, disk_size integer, disk_used integer, disk_available integer, mount text)")

if __name__ == "__main__":
    main()


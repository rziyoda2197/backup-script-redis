import os
import shutil
import redis
import sqlite3
import datetime

# Redis backup script
def redis_backup(host, port, password, filename):
    r = redis.Redis(host=host, port=port, password=password)
    with open(filename, 'w') as f:
        for key in r.keys():
            value = r.get(key)
            f.write(f"{key}:{value}\n")

# Database backup script
def database_backup(db_name, filename):
    conn = sqlite3.connect(db_name)
    with open(filename, 'w') as f:
        for row in conn.execute("SELECT * FROM sqlite_master"):
            f.write(f"CREATE TABLE {row[1]} ({', '.join([f'{col[1]} {col[2]}' for col in conn.execute(f"PRAGMA table_info({row[1]})")])})\n")
        for table in conn.execute("SELECT name FROM sqlite_master WHERE type='table'"):
            f.write(f"\nINSERT INTO {table[0]} VALUES\n")
            for row in conn.execute(f"SELECT * FROM {table[0]}"):
                f.write(f"({', '.join([str(value) for value in row])}),\n")
    conn.close()

# Main function
def main():
    redis_host = 'localhost'
    redis_port = 6379
    redis_password = 'password'
    redis_filename = 'redis_backup.txt'
    db_name = 'database.db'
    db_filename = 'database_backup.sql'

    redis_backup(redis_host, redis_port, redis_password, redis_filename)
    database_backup(db_name, db_filename)

    # Backup files to a specific directory
    backup_dir = 'backup'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    shutil.move(redis_filename, backup_dir)
    shutil.move(db_filename, backup_dir)

    # Log the backup process
    with open('backup_log.txt', 'a') as f:
        f.write(f"Backup created at {datetime.datetime.now()}\n")

if __name__ == "__main__":
    main()


import pandas as pd, csv, sqlite3, os, shapely, fiona

conn = sqlite3.connect('/var/www/django_app/db.sqlite3')

# Get tables
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(c.fetchall())

# Get data from sql
biodiversityrecords = pd.read_sql_query("SELECT * from django_app_biodiversityrecords", conn)

finalDumpFile = '/var/www/django_app/dumpSQL/django_app_biodiversityrecords.csv'
biodiversityrecords = biodiversityrecords.replace([';'],',')
biodiversityrecords.to_csv(finalDumpFile, sep=';', header=True, index=False)

speciesrecords = pd.read_sql_query("SELECT * from django_app_speciesrecords", conn)

finalDumpFile = '/var/www/django_app/dumpSQL/django_app_speciesrecords.csv'
speciesrecords = speciesrecords.replace([';'],',')
speciesrecords.to_csv(finalDumpFile, sep=';', header=True, index=False)

conn.close()
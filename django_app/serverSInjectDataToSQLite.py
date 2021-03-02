
# ssh jorge@10.4.1.33 # jorge?123
# python3

for element in dir():
    if element[0:2] != "__":
        del globals()[element]

del element

import pandas as pd, csv, sqlite3, os, shapely, fiona

# ---------------------------------------------
# ---------------------------------------------
# Read External file

datafile = '/var/www/django_app/inputData/BiodiversityDwcCleanWormsLand2.csv'
data = pd.read_csv(datafile, sep=';', header=0,low_memory=False)
list(data.columns)
data.head()
data.rename(columns = {'family':'Family', 'class':'Class', 'order':'Order', 'genus':'Genus', 'kingdom':'Kingdom','phylum':'Phylum' }, inplace = True)

# ---------------------------------------------
# ---------------------------------------------
# Open sqlite3

os.getcwd()
conn = sqlite3.connect('/var/www/django_app/db.sqlite3')

# Get tables
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(c.fetchall())

# Get data from sql
results = pd.read_sql_query("SELECT * from django_app_biodiversityrecords", conn)

# Count number of records
results.shape[0]

# Get structure
names = list(results.columns)
print(names)

# ---------------------------------------------
# ---------------------------------------------
# Remove surplus columns from new data

columnsInList = [i for i in range(len(data.columns)) if data.columns[i] in names]
data = data[data.columns[columnsInList]]
data.shape

# ---------------------------------------------
# ---------------------------------------------
# Remove already present data

notInList = []

for x in range(0, data.shape[0]):
    if data['occurrenceID'][x] not in list(results['occurrenceID']):
        notInList.append(x)

data = data.loc[notInList]
data.shape

# ---------------------------------------------
# ---------------------------------------------
# Inject data to sql

# Delete all records
# c.execute("DELETE FROM django_app_biodiversityrecords WHERE modified != 0")
# conn.commit()

data.to_sql('django_app_biodiversityrecords', conn, if_exists='append', index=False)
conn.close()

# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------

# Inject Species data

datafile = '/var/www/django_app/inputData/speciesListSimple.csv'
data = pd.read_csv(datafile, sep=';', header=0,low_memory=False)
list(data.columns)
data.head()

# ---------------------------------------------
# ---------------------------------------------
# Open sqlite3

os.getcwd()
conn = sqlite3.connect('/var/www/django_app/db.sqlite3')

# Get tables
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(c.fetchall())

# ---------------------------------------------

# Delete all species
# c.execute("DELETE FROM django_app_speciesrecords WHERE ScientificName != 0")
# conn.commit()

data.to_sql('django_app_speciesrecords', conn, if_exists='append', index=False)
conn.close()
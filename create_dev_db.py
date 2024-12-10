"""
  Create a development psql database for local development
  
  'NAME': 'crm_db',
  'USER': 'crm_user',
  'PASSWORD': 'crm_password',
  'HOST': 'localhost',
  'PORT': '5432',
  
"""

import psycopg2

# create user

conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='postgres',
    host='localhost',
    port='5432'
)

conn.autocommit = True

cur = conn.cursor()

cur.execute('CREATE DATABASE crm_db;')

cur.execute('CREATE USER crm_user WITH PASSWORD \'crm_password\';')

cur.execute('ALTER ROLE crm_user SET client_encoding TO \'utf8\';')

cur.execute('ALTER ROLE crm_user SET default_transaction_isolation TO \'read committed\';')

cur.execute('ALTER ROLE crm_user SET timezone TO \'UTC\';')

cur.execute('GRANT ALL PRIVILEGES ON DATABASE crm_db TO crm_user;')

cur.close()

conn.close()

print('Database crm_db created successfully')

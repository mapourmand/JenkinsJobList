import sqlite3
conn = sqlite3.connect('sql.sqlite')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS "logservices" ("servicename" TEXT, "logtime" TEXT, "status" TEXT)')
conn.commit()

import jenkinsapi
from jenkinsapi.jenkins import Jenkins
import datetime

J = Jenkins('http://localhost:8080', 'root', '123456')

jobs = J.keys()

for job in J.keys():
    if not J[job].is_enabled():
        status = 'disable'
    elif J[job].is_running():
        status = 'running'
    else:
        status = 'enable'
    try:
        c.execute("INSERT INTO logservices ({cs}, {cstatus}, {ct}) VALUES (?, ?, ?)".\
            format( cs='servicename', cstatus='status', ct='logtime'),(job, status, datetime.datetime.now().strftime("%B %d, %Y"), ))
    except sqlite3.IntegrityError:
        print('ERROR: Insert fail ')

conn.commit()

conn.close()

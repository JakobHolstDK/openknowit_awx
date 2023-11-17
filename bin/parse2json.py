#!/usr/bin/env python
import json
import xmltodict
import pprint
import time
import psycopg2


def read_xml():
  with open('data/quatareport.xml') as fd:
    doc = xmltodict.parse(fd.read())
    return doc
  


def connectdb():
    conn = psycopg2.connect("dbname=dash user=dash password=dash113 host=localhost")
    cur = conn.cursor()

    # check if table exists
    try:
        cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)", ('quotadata',))
        exists = cur.fetchone()[0]
    except:
        print("Error checking for table quotadata")

    if not exists:
        try:
            cur.execute("CREATE TABLE quota_reports (reportdate TIMESTAMP, type TEXT, snaps INTEGER, lin TEXT, physical BIGINT, logical BIGINT, inodes BIGINT, applogical BIGINT, shadow_refs BIGINT, physical_data BIGINT, physical_protection BIGINT, reduction TEXT, efficiency TEXT, container TEXT, enforcements TEXT, notifications TEXT, path TEXT, PRIMARY KEY (reportdate, path))")
            conn.commit()
        except:
            print("Error creating table quota_reports")
#CREATE TABLE fileservers ( id SERIAL PRIMARY KEY, name TEXT, description TEXT, url TEXT);
    try:
        cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)", ('fileservers',))
        exists = cur.fetchone()[0]
    except:
        print("Error checking for table fileservers")
    
    if not exists:
        try:
            cur.execute("CREATE TABLE fileservers ( id SERIAL PRIMARY KEY, name TEXT, description TEXT, url TEXT)")
            conn.commit()
        except:
            print("Error creating table fileservers")
#CREATE TABLE path ( path TEXT PRIMARY KEY, created TIMESTAMP, updated TIMESTAMP, fileserver_id INTEGER, FOREIGN KEY (fileserver_id) REFERENCES fileservers(id)
    try:
        cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)", ('path',))
        exists = cur.fetchone()[0]
    except:
        print("Error checking for table path")
    if not exists:
        try:
            cur.execute("CREATE TABLE path ( path TEXT PRIMARY KEY, created TIMESTAMP, updated TIMESTAMP, fileserver_id INTEGER, FOREIGN KEY (fileserver_id) REFERENCES fileservers(id))")
            conn.commit()
        except:
            print("Error creating table path")
#CREATE TABLE allocation ( path TEXT, fileserver_id INTEGER, PRIMARY KEY (path, fileserver_id), FOREIGN KEY (path) REFERENCES path(path), FOREIGN KEY (fileserver_id) REFERENCES fileservers(id));
    try:
        cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)", ('allocation',))
        exists = cur.fetchone()[0]
    except:
        print("Error checking for table allocation")
    if not exists:
        try:    
            cur.execute("CREATE TABLE allocation ( path TEXT, fileserver_id INTEGER, PRIMARY KEY (path, fileserver_id), FOREIGN KEY (path) REFERENCES path(path), FOREIGN KEY (fileserver_id) REFERENCES fileservers(id))")
            conn.commit()
        except:
            print("Error creating table allocation")
    return cur, conn

# create table quota_reports if it does not exist
#print(json_formatted_doc)
## print keys in dict doc
def insertdata(data):
    conn = psycopg2.connect(
    database="dash",
    user="dash",
    password="dash113",
    host="127.0.0.1",
    port="5432"
)
    cur = conn.cursor()
    cur.execute("select * from quotadata_table;")
    print("-----------------------------------------------------------")
    pprint.pprint(data)
    print("-----------------------------------------------------------")
    #sqlstatement = "INSERT INTO quotadata_table ( reportdate, data_type, snaps, lin, physical, logical, inodes, applogical, shadow_refs, physical_data, physical_protection, reduction, efficiency, container, path) VALUES ( \"%s\", \"%s\", %s, \"%s\", %s, %s, %s, %s, %s, %s, %s, \"%s\", \"%s\", \"%s\", \"%s\")" %  ( data['reportdate'], data['type'], data['snaps'], data['lin'], data['physical'], data['logical'], data['inodes'], data['applogical'], data['shadow_refs'], data['physical_data'], data['physical_protection'], data['reduction'], data['efficiency'], data['container'], str(data['enforcements']), str(data['notifications']), data['path'])
    sqlstatement = """
    INSERT INTO quotadata_table (
        reportdate, 
        data_type, 
        snaps, 
        lin, 
        physical, 
        logical, 
        inodes,
        applogical, 
        shadow_refs, 
        physical_data, 
        physical_protection,
        reduction, 
        efficiency, 
        container, 
        path
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
"""

    # Data to be inserted
    data_values = (
        data['reportdate'], 
        data['type'], 
        data['snaps'], 
        data['lin'], 
        data['physical'],
        data['logical'], 
        data['inodes'],
        data['applogical'], 
        data['shadow_refs'],
        data['physical_data'], 
        data['physical_protection'], 
        data['reduction'],
        data['efficiency'], 
        data['container'], 
        data['path']
    )

    print("Inserting data into table quotadata_table - precommit")
    cur.execute(sqlstatement, data_values)
    print("Inserted data into table quotadata_table - precommit")
    conn.commit()



    return True



def main():
    doc = read_xml()
    conn = psycopg2.connect(
    database="dash",
    user="dash",
    password="dash113",
    host="127.0.0.1",
    port="5432"
)
    cur = conn.cursor()
    cur.execute("select * from quotadata_table;")
    cur.close()
    conn.close()

    print("Connected to database")
    mykeys = doc['quota-report'].keys()
    reportdate = doc['quota-report']['@time']
    reportdate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(reportdate)))
    mydomains = []
    allmydata = {}
    datalist = []
    for domain in doc['quota-report']['domains']['domain']:
        mytype = (domain['@type'])
        mysnaps = (domain['@snaps'])
        mylin = (domain['@lin'])
        myusages = (domain['usage'])
        mypathdata = {}
        for myusage in myusages:
            myresource = (myusage['@resource'])
            myvalue = (myusage['#text'])
            try:
                mypathdata[myresource] = int(myvalue)
            except:
                mypathdata[myresource] = myvalue
        myreduction = (domain['reduction'])
        myefficiency = (domain['efficiency'])
        try:
            mycontainer = (domain['container'])
        except:
            mycontainer = "None"
        myenforcements = (domain['enforcements'])
        mynotifications = (domain['notifications'])
        mypath = (domain['path'])
        myidentifier = reportdate + ";" + mypath
        mydata = {}
        mydata['reportdate'] = reportdate
        mydata['type'] = mytype
        mydata['snaps'] = mysnaps
        mydata['lin'] = mylin
        for key in mypathdata.keys():
            mydata[key] = mypathdata[key]
        mydata['reduction'] = myreduction
        mydata['efficiency'] = myefficiency
        mydata['container'] = mycontainer
        mydata['enforcements'] = myenforcements
        mydata['notifications'] = mynotifications
        mydata['path'] = mypath
        allmydata[myidentifier] = mydata
        datalist.append(mydata)
    #pprint.pprint(allmydata)
    for data in datalist:
        print(data['reportdate'], data['path'])
        insertdata(data)
        #upload to database
        #print(data)
            
                
              
if __name__ == '__main__':
    main()












    



















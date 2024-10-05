# format invoice

import sqlite3
import time
from datetime import datetime
import calendar

DB1 = "comp_data.sqlite"
DB2 = "invoice_data.sqlite"

companiesdata = []
addressdata = []
invoicedata = []

epochtime = time.time() # gives epoch time
time1 = time.strftime('%Y%m%d', time.localtime(epochtime))
time2 = time.strftime('%d/%m/%Y', time.localtime(epochtime))
starttime = time.strftime('01/%m/%Y', time.localtime(epochtime))
endtime = time.strftime('/%m/%Y', time.localtime(epochtime))

dt1 = datetime.today()
dt2 = calendar.monthrange(dt1.year, dt1.month)
endmonth = dt2[1]


def readSqlTable(dbName, clientID):
    sqliteConnection = sqlite3.connect(dbName)
    cursor = sqliteConnection.cursor()

    select_query = """SELECT * FROM Company WHERE rowid = 1"""
    cursor.execute(select_query)
    records = cursor.fetchall()
    for row in records:
        companiesdata.append(list(row))
 
    cursor.execute("""SELECT * FROM Company WHERE ID = (?)""", (clientID,))
    records = cursor.fetchall()
    for row in records:
        companiesdata.append(list(row))
    cursor.close()

    sqliteConnection.close()
    return

def addAddress(dbName):
    sqliteConnection = sqlite3.connect(dbName)
    cursor = sqliteConnection.cursor()

    select_query = """SELECT * FROM Address"""
    cursor.execute(select_query)
    records = cursor.fetchall()
    for row in records:
        addressdata.append(list(row))
    cursor.close()

    sqliteConnection.close()
    return

def checkHistory(dbName):
    sqliteConnection = sqlite3.connect(dbName)
    cursor = sqliteConnection.cursor()

    cursor.execute("""SELECT * FROM History WHERE IssueDate = (?)""", (time1,))
    records = cursor.fetchall()
    length = len(records)
    cursor.close()

    sqliteConnection.close()

    return(length)

def sortdata(list1, list2, hours, rate):
    list1[0].pop(3)
    list1[1].pop(3)
    bankdetails = list1[0][-1].split()
    for companies in list1:
        for addresses in list2:
            if addresses[0] == companies[2]:
                companies.pop(2)
                for item in addresses[1::]: # so that the ID isn't inserted
                    companies.insert(2, item)

    for row in list1:
        for item in row[1:7:]:
            invoicedata.append(item)

    invoicedata.append('{}0{}'.format(time1, checkHistory(DB2) + 1)) # Invoice No
    invoicedata.append(list1[1][0]) # Client ID
    invoicedata.append(time2) # Invoice date
    invoicedata.append('{}'.format(starttime)) # Period of Invoice start
    invoicedata.append('{}{}'.format(endmonth, endtime))

    invoicedata.append('{}'.format(hours)) # hours
    invoicedata.append('{}'.format(rate)) # rate
    invoicedata.append('{:.2f}'.format(round(hours * rate, 2))) # amount
    invoicedata.append('£{:.2f}'.format(round(hours * rate, 2))) # amount

    invoicedata.append(bankdetails[0]) # My bank
    invoicedata.append(bankdetails[1])
    invoicedata.append(bankdetails[2])
    invoicedata.append(bankdetails[3])

    invoicedata.append('{}, registered in England and Wales, registered no. {}.'.format(list1[0][0], list1[0][7]))
    invoicedata.append('Registered office: {}, {}, {}, {}.'.format(list1[0][2], list1[0][3], list1[0][4], list1[0][6]))

    return


def writepage(template, htmlpage):
    with open(template, 'r') as file1:
        with open(htmlpage, 'w') as file2:
            counter1 = 0
            for line in file1:
                if '%' in line:
                    file2.write('{}\n'.format(invoicedata[counter1]))
                    counter1 += 1
                else:
                    file2.write(line)
    return

def savetohistory(dbName, issuer, invoiceno, recipient, rate, hours, issuedate):
    with sqlite3.connect(dbName) as db:
        cursor = db.cursor()

        newdata = [invoiceno, issuer, recipient, rate, hours, issuedate]

        cursor.execute("""INSERT INTO History VALUES (?,?,?,?,?,?)""", newdata)
    
        db.commit()
    return


def mainInvoice(clientname, hours, rate):
    readSqlTable(DB1, clientname)
    addAddress(DB1)
    sortdata(companiesdata, addressdata, hours, rate)
    print('\nData sorted.\n') # Marker for myself
    writepage('html/invoicetemplate.html', 'html/invoice.html')
    return


def SaveHistory(client, rate, hours):
    invoiceno = ('{}0{}'.format(time1, checkHistory(DB2) + 1))
    savetohistory(DB2, companiesdata[0][0], invoiceno, client, rate, hours, time1)
    return




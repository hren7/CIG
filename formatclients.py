# Format clients

import sqlite3

DB1 = "comp_data.sqlite"

clientdata = []
addressdata = []


def readSqlTable(dbName):
    sqliteConnection = sqlite3.connect(dbName)
    cursor = sqliteConnection.cursor()

    select_query = """SELECT * FROM Company"""
    cursor.execute(select_query)
    records = cursor.fetchall()
    for row in records[1:]:
        clientdata.append(list(row))
    cursor.close()

    sqliteConnection.close()
    return

def addAddress(dbName):
    sqliteConnection = sqlite3.connect(dbName)
    cursor = sqliteConnection.cursor()

    select_query = """SELECT * FROM Address"""
    cursor.execute(select_query)
    records = cursor.fetchall()
    for row in records[1:]:
        addressdata.append(list(row))
    cursor.close()

    sqliteConnection.close()
    return

def writepage(template, htmlpage):
    with open(template, 'r') as file1:
        with open(htmlpage, 'w') as file2:
            for line in file1:
                if '%' in line:
                    for row in clientdata:
                        file2.write('<tr class="table1">\n')
                        for item in row:
                            if type(item) == int:
                                for address in addressdata:
                                    if address[0] == item:
                                        file2.write('<td>')
                                        for values in address[:0:-1]:
                                            file2.write('{}<br>\n    '.format(values))
                                        file2.write('</td>\n')
                            else:
                                file2.write('<td>{}</td>\n'.format(item))
                else:
                    file2.write(line)
    return


readSqlTable(DB1)
addAddress(DB1)
writepage('html/clientstemplate.html', 'html/clients.html')
    

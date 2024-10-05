# Format clients

import sqlite3
from datetime import datetime

DB1 = "invoice_data.sqlite"

historydata = []


def readSqlTable(dbName):
    sqliteConnection = sqlite3.connect(dbName)
    cursor = sqliteConnection.cursor()

    select_query = """SELECT * FROM History"""
    cursor.execute(select_query)
    records = cursor.fetchall()
    for row in records:
        historydata.append(list(row))
    cursor.close()

    sqliteConnection.close()
    return

def writepage(template, htmlpage):
    with open(template, 'r') as file1:
        with open(htmlpage, 'w') as file2:
            for line in file1:
                if '%' in line:
                    for row in historydata:
                        file2.write('<tr class="table1">\n')
                        for item in row:
                            if row.index(item) == (len(row) - 1):
                                time1 = datetime.strptime(str(item), '%Y%m%d').strftime('%d/%m/%Y')
                                file2.write('<td>{}</td>\n'.format(time1))
                            else:
                                file2.write('<td>{}</td>\n'.format(item))
                else:
                    file2.write(line)
    return


readSqlTable(DB1)
writepage('html/historytemplate.html', 'html/history.html')
    

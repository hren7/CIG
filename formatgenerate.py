# format generate page

import sqlite3

DB1 = "comp_data.sqlite"

clientdata = []


def readSqlTable(dbName):
    sqliteConnection = sqlite3.connect(dbName)
    cursor = sqliteConnection.cursor()

    select_query = """SELECT ID FROM Company
    ORDER BY rowid
    LIMIT -1 OFFSET 1"""
    cursor.execute(select_query)
    records = cursor.fetchall()
    for row in records:
        clientdata.append(list(row))
    cursor.close()

    sqliteConnection.close()
    return

def writepage(template, htmlpage):
    with open(template, 'r') as file1:
        with open(htmlpage, 'w') as file2:
            for line in file1:
                if '%' in line:
                    for row in clientdata:
                        file2.write('<input type="radio" id="{0}" name="client" value="{0}" required>\n'.format(row[0]))
                        file2.write('<label for="{0}">{0}</label><br>\n'.format(row[0]))
                else:
                    file2.write(line)
    return


readSqlTable(DB1)
writepage('html/generatetemplate.html', 'html/generate.html')

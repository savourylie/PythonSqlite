import sqlite3
import re

conn = sqlite3.connect('week2.sqlite')
cur = conn.cursor()

cur.execute('''
DROP TABLE IF EXISTS Counts''')

cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

emails = []

fname = raw_input('Enter file name: ')
if ( len(fname) < 1 ) : fname = 'mbox.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From: ') : continue
    # pieces = line.split()
    # email = pieces[1]
    # email = re.findall("\S+@\S+", line)[0]
    org = re.findall("\S+@(\S+)", line)[0]

    # print(org, email)

    cur.execute('SELECT * FROM Counts WHERE org = ? ', (org, ))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count) 
                VALUES ( ?, 1 )''', (org, ) )
    else : 
        cur.execute('UPDATE Counts SET count=count+1 WHERE org = ?', 
            (org, ))
    # This statement commits outstanding changes to disk each 
    # time through the loop - the program can be made faster 
    # by moving the commit so it runs only after the loop completes
    conn.commit()

# # https://www.sqlite.org/lang_select.html
# sqlstr = 'SELECT email, count FROM Counts ORDER BY count DESC LIMIT 10'

# print
# print "Counts:"
# for row in cur.execute(sqlstr) :
#     print str(row[0]), row[1]

cur.close()


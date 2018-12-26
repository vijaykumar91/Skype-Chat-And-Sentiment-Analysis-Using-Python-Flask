import csv
import  pymysql
import MySQLdb

conn = MySQLdb.connect (host = "67.222.23.104",
                        user = "loginwor_walmart",
                        passwd = "1#password",
                        db = "loginwor_walmart",
                        port=3306)
cursor = conn.cursor ()
cursor.execute ("SELECT VERSION()")
with open('walmartdataset.csv', newline='',encoding="utf8", errors='ignore') as File:
    reader = csv.reader(File)
    t=0;
    for row in reader:
        print(row[0])
        sql = "INSERT INTO product (imagelink, category,description,rating,pageimage) VALUES (%s, %s,%s, %s,%s)"
        val = (row[0], row[1],row[2],row[3],row[4])
        cursor.execute(sql, val)
row = cursor.fetchone ()





# with open('walmartdataset.csv', newline='',encoding="utf8", errors='ignore') as File:
#     reader = csv.reader(File)
#     t=0;
#     for row in reader:
#         print(row[0])
#         sql = "INSERT INTO product (imagelink, category,description,rating,pageimage) VALUES (%s, %s,%s, %s,%s)"
#         val = (row[0], row[1],row[2],row[3],row[4])
#         mycursor.execute(sql, val)

mydb.commit()


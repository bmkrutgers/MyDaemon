import mysql.connector

mydb = mysql.connector.connect(
  host="cloudnine.c87lmy1ftwtu.us-east-2.rds.amazonaws.com",
  user="modi1234",
  passwd="Was160497",
  database="CloudNine"
)

mycursor = mydb.cursor()

#create tables--the first time program runs

#created table user
#mycursor.execute("CREATE TABLE user (username VARCHAR(255) not null primary key, passwd not null VARCHAR(255))")

#created table fileinfo
#mycursor.execute("CREATE TABLE fileinfo (filename VARCHAR(255) not null, fileid VARCHAR(255) not null, cloud_provider VARCHAR(50) not null, encryption_key int, decryption_key int, primary key(fileid,cloud_provider))")








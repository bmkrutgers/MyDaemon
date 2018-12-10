#!/usr/bin/env python3

import time
import  os
import sys
import array
import string
import Joining_files
import os.path
import shutil
from shutil import copyfile
from filesystem import EventHandler
import Split 
import cloud_storage_api.google_drive as gdrive
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

TOKEN = '8d2zpj3IYCAAAAAAAAAAyfYnUtShU194fH2pHW-s1xOuHLBa6Vw9UEqqwMRhxmQk'

mydb = mysql.connector.connect(
  host="cloudnine.c87lmy1ftwtu.us-east-2.rds.amazonaws.com",
  user="modi1234",
  passwd="Was160497",
  database="CloudNine"
)


mycursor = mydb.cursor()

#create backup folder
def setupSnapshot():
    
	#get curr dir
	dirpath = os.listdir()
    parentdir = os.path.abspath(os.path.join(dirpath, os.pardir))
	#change dir
    os.chdir(parentdir)
    if not os.path.exists(".backup"):
        os.makedirs(".backup")
    

def createSnapshot(events):
    
    files =  getListofSnapshotFiles()
    
    src = os.listdir()
    parentdir = os.path.abspath(os.path.join(src, os.pardir))
    
    dest = parentdir + "/" + ".backup"
    
    size = len(files)
    for x in range(0, size):
        filename = files[x]
        copyfile(src, dest)
    
    return

def deleteSnapshot():
    
	#get curr dir
    src = os.listdir()
	#get parent dir
    parentdir = os.path.abspath(os.path.join(src, os.pardir))
    
	#backup folder path
    dest = parentdir + "/" + ".backup"
    
    for the_file in os.listdir(dest):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print("snapshot file cannot be deleted")
    return

def getListofSnapshotFiles(events):

    f = []
	for key in events.keys():
		f.append(key)
	
    return f

def dropbox_upload(filename):
	filepath = "/" + filename
	
	with open(filename, 'rb') as f:
		# We use WriteMode=overwrite to make sure that the settings in the file
		# are changed on upload
		#print("Uploading " + LOCALFILE + " to Dropbox as " + BACKUPPATH + "...")
		try:
			dbx.files_upload(f.read(), filepath)
		except ApiError as err:
			# This checks for the specific error where a user doesn't have
			# enough Dropbox space quota to upload this file
			if (err.error.is_path() and
					err.error.get_path().reason.is_insufficient_space()):
				sys.exit("ERROR: Cannot back up; insufficient space.")
			elif err.user_message_text:
				print(err.user_message_text)
				sys.exit()
			else:
				print(err)
				sys.exit()

def addFile(filename):
	
	src = os.listdir()
    parentdir = os.path.abspath(os.path.join(src, os.pardir))
    
    dest = parentdir + "/" + ".backup"
	
	os.chdir(dest)
	
	Split.split_files(filename,2)
	
	filepath = dest + "/" + filename
	
	gdrive.upload_file(filename)
	
	dropbox_upload(filename)
	
	sql = "UPDATE fileinfo SET fileid = %s WHERE filename = %s AND cloud_provider = %s"
    val = (filename, filename, "dropbox")
	mycursor.execute(sql, val)
	mydb.commit()
	
	
    print("Add/Modify Files")
    return

def renameFile(oldpFileName,newpFileName):

	deleteFile(oldpFileName)
	addFile(newpFileName)
    print("rename File")
    print(oldpFileName)
    print(newpFileName)
    return

def deleteFile(filename):
    
	fileid = getGDriveFileIdFromDbase(filename)
	
	gdrive.delete_file(fileid)
	
	dropbox.files_delete(filename)
	
	sql = "DELETE FROM fileinfo WHERE filename = %s"
    val = (filename )

    mycursor.execute(sql, val)

    mydb.commit()
	
    return

def executeCloud9():
    file = open('fileResult.txt', 'r')
    content = file.read().splitlines()
    num_lines = sum(1 for line in open('fileResult.txt'))
    for fileVariable in range(0,num_lines):
        binaryArray = []
        arrayFile = content[fileVariable].split()
        oldpFileName = arrayFile[0]
        newpFileName = arrayFile[1]
        binaryArray.append(arrayFile[2])
        binaryArray.append(arrayFile[3])
        binaryArray.append(arrayFile[4])
        binaryArray.append(arrayFile[5])
        binarystr = ''.join(binaryArray)
        pFinalresult = int(binarystr, 2)
        if(pFinalresult == 1):
            renameFile(oldpFileName,newpFileName)
        elif(pFinalresult == 2):
            deleteFile(newpFileName)
        else:
            addFile(newpFileName)
    return

def listFilesinDirectory();
    cwd = os.getcwd()
    os.listdir()
    f = []
    for (dirpath, dirnames, filenames) in os.walk(cwd):
        f.extend(filenames)
        break
    return f

def getDatabselist():    
    
    dblist = []
    
    sql = "SELECT filename FROM fileinfo"
    mycursor.execute(sql)

    myresult = mycursor.fetchall()

    for x in myresult:
       dblist.append(x)

    return dblist

def getDecryptKeyfromDbase(filename):
    
    sql = "SELECT encryption_key FROM fileinfo WHERE cloud_provider = %s AND filename = %s"
    mycursor.execute(sql, "google", filename)

    myresult = mycursor.fetchall()

    for x in myresult:
        passkey = x
        
    return passkey

def getDropBoxFileIdFromDbase(filename):
    
    sql = "SELECT fileid FROM fileinfo WHERE cloud_provider = %s AND fileid = %s"
    mycursor.execute(sql, "dropbox", filename)

    myresult = mycursor.fetchall()

    for x in myresult:
        pDropBoxId = x
        
    return pDropBoxId


def getGDriveFileIdFromDbase(filename):
    
    sql = "SELECT fileid FROM fileinfo WHERE cloud_provider = %s AND filename = %s"
    mycursor.execute(sql, "google", filename)

    myresult = mycursor.fetchall()

    for x in myresult:
        pGdriveId = x
    
    return pGdriveId
    

def downLoad_DropBox(fileId_dropBox):
	
	src = os.listdir()

    dbx.files_download_to_file(fileId_dropBox, src)
	
	return
    
def getGdriveName(fileId_gDrive):
    
    sql = "SELECT filename FROM fileinfo WHERE cloud_provider = %s AND fileid = %s"
    mycursor.execute(sql, "google", fileId_gDrive)

    myresult = mycursor.fetchall()

    for x in myresult:
        pGdrivefilename = x
    
    return pGdrivefilename
	
def downLoad_Gdrive(fileId_gDrive):
    
	src = os.listdir()
	
	gdrive.download_file(fileId_gDrive,src)
	
    return 

def options():
    fileList = listFilesinDirectory()
    dbList = getDatabselist()
    if(!fileList && dbList)
        for fileName in dbList:
            fileId_dropBox = getDropBoxFileIdFromDbase(fileName)
            fileId_gDrive = getGDriveFileIdFromDbase(fileName)
            fileDropBoxName = getDropBoxFileNameFromDbase(fileName)
            fileGdriveName = getGdriveFileNameFromDbase(fileName)
            pDecryptKey = getDecryptKeyfromDbase(fileName)
            pDropBoxfilename = downLoad_DropBox(fileId_dropBox)
            pGdrivefilename = downLoad_Gdrive(fileId_gDrive)
            listFiles = []
            listFilesLines[]
            listFilesLines.append(fileGdriveName)
            listFilesLines.append(pGdrivefilename)
            listFilesLines.append(fileDropBoxName)
            listFilesLines.append(pDropBoxfilename)
            listFiles.append(LisFilesLines[0])
            listFiles.append(ListFileNames[1])
            Joining_files.joining_files(listFiles,filePass,textOriginal)

    while True:
        print("Hi")
        createSnapshot()
        executeCloud9()
        deleteSnapshot()
        time.sleep(300)
        return

	with EventHandler(path='/some/path/to/folder', recursive=False) as event_handler:
		#list = event_handler.get_snapshot()
		
		try:
			while True:
				time.sleep(5)
				events = event_handler.get_new_batch()
				setupSnapshot()
				createSnapshot(events)
				executeCloud9()
				deleteSnapshot()
				
					# process events of current batch
		finally:
				# post processing
			pass
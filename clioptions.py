#!/usr/bin/env python3

import time
import os
import sys
import array
import string
import Joining_files
import os.path
import shutil
from shutil import copyfile
import filesystem
import Split
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
from cloud_storage_api.google_drive import GoogleDrive
import mysql.connector
import ntpath
from typing import Any

TOKEN = 'ketP6PVRRsAAAAAAAAAACvTqOPrJ6jv6ntnJbeGXx3FLt0PzAKk5GVzOuirMOYlP'

dirpath = "/home/bmk/Documents/git/Cl9"

mydb = mysql.connector.connect(
	host="cloudnine.c87lmy1ftwtu.us-east-2.rds.amazonaws.com",
	user="modi1234",
	passwd="Was160497",
	database="CloudNine"
)

dbx = dropbox.Dropbox(TOKEN)

gdrive = GoogleDrive()

mycursor = mydb.cursor()

def path_leaf(path):
	head, tail = ntpath.split(path)
	return tail or ntpath.basename(head)


# create backup folder
def setupSnapshot():
	cwd = os.path.dirname(os.path.realpath(__file__))
	parentdir = os.path.abspath(os.path.join(dirpath, os.pardir))
	# print("parent directory of folder sent: " + parentdir)
	os.chdir(parentdir)


	if not os.path.exists(".backup"):
		os.makedirs(".backup")
	os.chdir(cwd)
	return


def createSnapshot(events):

	pSet = isinstance(events, dict)

	if pSet:
		files = getListofSnapshotFiles(events)
	else:
		files = events

	src = dirpath

	# print( "src directory in createSnapshot: " + src)

	parentdir = os.path.abspath(os.path.join(dirpath, os.pardir))

	dest = parentdir + "/" + ".backup"

	# print( "dest directory in createSnapshot: " + dest)

	size = len(files)

	for x in range(0, size):
		filename = path_leaf(files[x])
		srctemp = src + "/" + filename
		desttemp = dest + "/" + filename
		copyfile(srctemp, desttemp)
		srctemp = ""
		desttemp = ""
	return



def deleteSnapshot():
	parentdir = os.path.abspath(os.path.join(dirpath, os.pardir))

	dest = parentdir + "/" + ".backup"

	for the_file in os.listdir(dest):
		file_path = os.path.join(dest, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception as e:
			print("snapshot file cannot be deleted")
	return


def getListofSnapshotFiles(events):
	f = []
	for key in events.keys():
		if os.path.isfile(key):
			f.append(key)

	return f


def dropbox_upload(filename):
	filename = path_leaf(filename)
	filepath = "/" + filename

	print(filepath)

	with open(filename, 'rb') as f:
		# We use WriteMode=overwrite to make sure that the settings in the file
		# are changed on upload
		# print("Uploading " + LOCALFILE + " to Dropbox as " + BACKUPPATH + "...")
		try:
			dbx.files_upload(f.read(), filepath, mode=dropbox.files.WriteMode.overwrite)
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

	return


def addFile(filename):

	filename = path_leaf(filename)

	cwd = os.path.dirname(os.path.realpath(__file__))

	src = dirpath

	parentdir = os.path.abspath(os.path.join(src, os.pardir))

	dest = parentdir + "/" + ".backup"

	os.chdir(dest)

	(filegoogle, filedropbox, passwordkey) = Split.split_files(filename)

	sql = "INSERT INTO fileinfo (filename, gcloud_provider, encryption_key) VALUES (%s,%s,%s)"
	val = (filename,filegoogle, passwordkey)
	mycursor.execute(sql, val)
	mydb.commit()

	sql = "UPDATE  fileinfo  SET dcloud_provider = %s WHERE filename = %s"
	val = (filedropbox, filename)
	mycursor.execute(sql, val)
	mydb.commit()

	gdrivefileId = gdrive.upload_file(filegoogle)

	sql = "UPDATE fileinfo SET googlefileid = %s WHERE filename = %s"
	val = (gdrivefileId, filename)
	mycursor.execute(sql, val)
	mydb.commit()

	dropbox_upload(filedropbox)

	sql = "UPDATE fileinfo SET dropboxfileid = %s WHERE filename = %s"
	val = (filedropbox, filename)
	mycursor.execute(sql, val)
	mydb.commit()


	os.chdir(cwd)


	print("Add/Modify Files")


	return


def renameFile(oldpFileName, newpFileName):

	deleteFile(oldpFileName)
	addFile(newpFileName)


	print("rename File")
	print(oldpFileName)
	print(newpFileName)
	return


def deleteFile(filename):
	
	filename = path_leaf(filename)

	#filegoogle =  filename + "google" + ".aes"
	#filedropboxdb = filename + "dropbox" + ".aes"
	filedropbox = "/" + filename + "dropbox" + ".aes"

	fileid = getGDriveFileIdFromDbase(filename)

	gdrive.delete_file(fileid)

	dbx.files_delete(filedropbox)

	
	sql = "DELETE FROM fileinfo WHERE filename = %s"
	
	val = (filename,)
	mycursor.execute(sql, val)
	mydb.commit()

	
	#sql = "DELETE FROM fileinfo WHERE filename = AND cloud_provider = %s"
	
	#val = (filegoogle, "google")
	#mycursor.execute(sql, val)
	#mydb.commit()
	
	
	return

def executeCloud9(events):
	for key, val in events.items():
		pFinalvalue = int(val,2)
		if (pFinalvalue == 4):
			print("adding Files")
			pValcheck = checkifexists(key)
			if not pValcheck:
				addFile(key)
		elif (pFinalvalue == 2):
			print("deletingfiles")
			pValcheck = checkifexists(key)
			if pValcheck:
				deleteFile(key)
		elif (pFinalvalue == 1):
			print("modifying files")
			deleteFile(key)
			addFile(key)
		elif(pFinalvalue == 0):
			print("system is idle")
		else:
			continue

	return


def listFilesinDirectory(fileDirectory):

	f = []

	for (dirpath, dirnames, filenames) in os.walk(fileDirectory):

		f.extend(filenames)
		break

	return f


def checkifexists(filename):

	filename = path_leaf(filename)

	sql = "SELECT COUNT(1) FROM fileinfo WHERE filename = %s"
	val = (filename,)
	mycursor.execute(sql, val)

	myresult = mycursor.fetchall()

	for y in myresult:
		x = y

	if (x[0] == 0 ):
		return 0

	return 1


def getDatabselist():

	dblist = []

	sql = "SELECT filename FROM fileinfo"

	mycursor.execute(sql)

	myresult = mycursor.fetchall()

	for x in myresult:
		x = ''.join(x)
		dblist.append(x)

	#print (dblist)

	return dblist


def getDecryptKeyfromDbase(filename):

	filename = path_leaf(filename)

	#print ("filename is ",filename)
	sql = "SELECT encryption_key FROM fileinfo WHERE filename = %s"
	val = (filename,)
	mycursor.execute(sql, val)

	myresult = mycursor.fetchall()
	
	passkey = ""

	#print ("passkey is ", passkey)

	for x in myresult:
		x =''.join(x)
		passkey = x

	return passkey


def getDropBoxFileIdFromDbase(filename):

	filename = path_leaf(filename)
	sql = "SELECT dropboxfileid FROM fileinfo WHERE filename = %s"
	val = (filename,)
	mycursor.execute(sql, val)

	myresult = mycursor.fetchall()
	
	pDropBoxId = "" 

	for x in myresult:
		pDropBoxId = x

	return pDropBoxId


def getGDriveFileIdFromDbase(filename):

	filename = path_leaf(filename)

	sql = "SELECT googlefileid FROM fileinfo WHERE filename = %s"

	val = (filename,)

	mycursor.execute(sql, val)
	
	pGdriveId = ""

	myresult = mycursor.fetchall()

	for x in myresult:
		x = ''.join(x)
		pGdriveId = x

	return pGdriveId


def downLoad_DropBox(fileId_dropBox):

	cwd = os.path.dirname(os.path.realpath(__file__))

	os.chdir(dirpath)

	#print(fileId_dropBox)

	backup = "/" + fileId_dropBox

	dbx.files_download_to_file(fileId_dropBox, backup, None)

	os.chdir(cwd)

	return


def downLoad_Gdrive(fileId_gDrive, src):

	gdrive.download_file(fileId_gDrive, src)
	return


def getDropBoxFileNameFromDbase(filename):

	filename = path_leaf(filename)

	sql = "SELECT dcloud_provider FROM fileinfo WHERE filename = %s"
	val = (filename,)
	mycursor.execute(sql, val)

	myresult = mycursor.fetchall()
	
	pDrobBoxfilename = ""

	for x in myresult:
		x = ''.join(x)
		pDrobBoxfilename = x

	return pDrobBoxfilename

def getGdriveFileNameFromDbase (filename):

	filename = path_leaf(filename)

	sql = "SELECT gcloud_provider FROM fileinfo WHERE filename = %s"
	val = (filename,)
	mycursor.execute(sql, val)

	myresult = mycursor.fetchall()
	
	pGdrivefilename = "" 

	for x in myresult:
		x = ''.join(x)
		pGdrivefilename = x


	return pGdrivefilename


def deleteEntries(filename):
	sql = "SELECT googlefileid FROM fileinfo WHERE googlefileid IS NULL AND filename = %s;"
	val = (filename,)
	mycursor.execute(sql, val)

	myresult = mycursor.fetchall()
	myresult = myresult[0]

	sql = "SELECT dropboxfileid FROM fileinfo WHERE googlefileid IS NULL AND filename = %s;"
	val = (filename,)
	mycursor.execute(sql, val)
	myresult2 = mycursor.fetchall()
	myresult2 = myresult2[0]

	if ((not myresult[0]) or (not myresult2[0])):
		sql = "delete FROM fileinfo WHERE filename = %s;"
		val = (filename,)
		mycursor.execute(sql, val)

		mydb.commit()

	return

def options():
	bool = "true"
	dir = dirpath
	filelist = listFilesinDirectory(dir)
	dblist = getDatabselist()
	for staleentries in dblist:
		deleteEntries(staleentries)
	dblist = getDatabselist()
	setA = set(filelist)
	setB = set(dblist)

	fileTobeAdded = list(setA.difference(setB))

	fileTobeDownloaded = list(setB.difference(setA))

	print (fileTobeAdded)

	print (fileTobeDownloaded)

	if (fileTobeDownloaded):
		for fileName in fileTobeDownloaded:
			#print(fileName)
			pDropBoxId = " "
			pGdriveId = " "
			pDropBoxfilename = " "
			pGdrivefilename = " "
			passkey = " "
			fileName = os.path.join(dirpath, fileName)
			pDropBoxId = getDropBoxFileIdFromDbase(fileName)
			pGdriveId = getGDriveFileIdFromDbase(fileName)
			pDropBoxfilename = getDropBoxFileNameFromDbase(fileName)
			pGdrivefilename = getGdriveFileNameFromDbase(fileName)
			pDecryptKey = getDecryptKeyfromDbase(fileName)
			#print(pGdriveId)
			#print (pDropBoxId)
			#print (pDropBoxfilename)
			#print (pGdrivefilename)
			downLoad_DropBox(pDropBoxfilename)
			restoregdriveFile = os.path.join(dirpath,pGdrivefilename)
			downLoad_Gdrive(pGdriveId, restoregdriveFile)
			listFilesLines = []
			plainGdriveFileName = os.path.splitext(pGdrivefilename)[0]
			plainDropboxFileName = os.path.splitext(pDropBoxfilename)[0]
			#print ("Unencrypted Google Drive", plainGdriveFileName)
			#print ("Unencrypted DropBox", plainDropboxFileName)
			plainGdriveFileName = os.path.join(dirpath,plainGdriveFileName)
			plainDropboxFileName = os.path.join(dirpath, plainDropboxFileName)
			pGdrivefilename = os.path.join(dirpath, pGdrivefilename)
			pDropBoxfilename = os.path.join(dirpath, pDropBoxfilename)
			listFilesLines.append(plainGdriveFileName)
			listFilesLines.append(pGdrivefilename)
			listFilesLines.append(plainDropboxFileName)
			listFilesLines.append(pDropBoxfilename)
			restoreFile = os.path.join(dirpath, fileName)
			Joining_files.joining_files(listFilesLines, pDecryptKey, restoreFile)

	if(fileTobeAdded):
			setupSnapshot()
			createSnapshot(fileTobeAdded)
			backupfile = ""
			for fileName in fileTobeAdded:
				backupfile = os.path.join(dirpath, fileName)
				addFile(backupfile)
			deleteSnapshot()

	with filesystem.EventHandler(path= dirpath, recursive=False) as event_handler:
		# list = event_handler.get_snapshot()

		try:
			while True:
				events = event_handler.get_new_batch()
				if events:
					setupSnapshot()
					createSnapshot(events)
					executeCloud9(events)
					deleteSnapshot()
				print("checking time stamp")
				time.sleep(50)

		finally:
			# post processing
			pass
	return

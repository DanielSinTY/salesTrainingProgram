from pydrive.auth import GoogleAuth

gauth = GoogleAuth()
gauth.LocalWebserverAuth() 
from pydrive.drive import GoogleDrive
from joblib import dump, load
from sklearn.model_selection import train_test_split
import numpy as np
import re
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
from empath import Empath
from numpy import record
import spacy
import os

lexicon = Empath()

drive = GoogleDrive(gauth)
folder_id=None
def upload(upload_file):
    global folder_id
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for i in file_list:
        if i['title']=='model':
            folder_id=i['id']
    gfile=None
    file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(folder_id)}).GetList()
    for i, file in enumerate(sorted(file_list, key = lambda x: x['title']), start=1):
        
        if file['title']==upload_file:
            id=file['id']
            gfile = drive.CreateFile({'id':id,'parents': [{'id': folder_id}]})
    if not gfile:
        gfile = drive.CreateFile({'parents': [{'id': folder_id}]})
	# Read file and set it as the content of this instance.
    gfile.SetContentFile(upload_file)
    gfile.Upload() # Upload the file.
def download(download_file):
    global folder_id
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for i in file_list:
        if i['title']=='model':
            folder_id=i['id']
    file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(folder_id)}).GetList()
    for i, file in enumerate(sorted(file_list, key = lambda x: x['title']), start=1):
        
        if file['title']==download_file:
            file.GetContentFile(file['title'],mimetype="application/octet-stream")
            model=load(file['title'])

def delete(delete_file):
    global folder_id
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for i in file_list:
        if i['title']=='model':
            folder_id=i['id']
    file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(folder_id)}).GetList()
    for i, file in enumerate(sorted(file_list, key = lambda x: x['title']), start=1):
        
        if file['title']==delete_file:
            
            file.Delete()

       

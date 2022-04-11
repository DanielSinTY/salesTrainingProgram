from pydrive.auth import GoogleAuth


from pydrive.drive import GoogleDrive
from joblib import dump, load
import os
import sys

def resource_path(relative_path):
    
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = resource_path('client_secrets.json')
gauth = GoogleAuth()
gauth.LocalWebserverAuth() 

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
        gfile = drive.CreateFile({'title':'model.joblib','parents': [{'id': folder_id}]})
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
            file.GetContentFile(resource_path(file['title']),mimetype="application/octet-stream")
            

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

       

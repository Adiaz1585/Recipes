from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload

scopes = 'https://www.googleapis.com/auth/drive'

def getAuthorization():
    store = file.Storage('token.json')
    creds = store.get()

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', scopes)
        creds = tools.run_flow(flow, store)
    
    service = build('drive', 'v3', http=creds.authorize(Http()))

    return service

def uploadFile(ingrediantFileName,stepsFileName,recipeName):
    drive = getAuthorization()
    folder_id = '1G5VdY0IyyevSlZMtH8GYRx4FOmN279-B'
    metadata = {'name': '{}'.format(recipeName),'mimeType': 'application/vnd.google-apps.folder','parents': [folder_id]}
    file = drive.files().create(body=metadata,fields='id').execute()

    folder_id = file.get('id')
    metadata = {'name': '{}.txt'.format(ingrediantFileName), 'parents' : [folder_id]}
    media = MediaFileUpload('{}.txt'.format(ingrediantFileName),mimetype='text/plain')
    file = drive.files().create(body=metadata, media_body=media,fields='id').execute()

    metadata = {'name': '{}.txt'.format(stepsFileName), 'parents' : [folder_id]}
    media = MediaFileUpload('{}.txt'.format(stepsFileName),mimetype='text/plain')
    file = drive.files().create(body=metadata, media_body=media,fields='id').execute()

    print ('File ID: %s' % file.get('id'))

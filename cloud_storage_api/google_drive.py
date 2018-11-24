import os
import io
import httplib2

from oauth2client import (client, tools)
from oauth2client.file import Storage

from apiclient import discovery
from apiclient.http import (MediaFileUpload, MediaIoBaseDownload)

import logging
logger = logging.getLogger(__name__)

class GoogleDrive:
    """Google Drive API for uploading and deleting files.
        Sets credentials upon instance initialization
    
    Raises:
        exception: http errors from uploading files
        exception: http errors from deleting files
    
    Returns:
        None
    """

    SCOPES              = 'https://www.googleapis.com/auth/drive'
    CLIENT_SECRET_FILE  = 'client_secret.json'
    APPLICATION_NAME    = 'Cloud Nine'

    def __init__(self):

        logger.info('Initializing Google Drive Api')

        self.credentials    = self._get_credentials()
        self.http           = self.credentials.authorize(httplib2.Http())
        self.drive_service  = discovery.build('drive', 'v3', http=self.http)

    def upload_file(self, filepath, mimetype='text/plain', save_as=''):
        """Uploads file to google drive
        
        Args:
            filepath (path): full path to file that is to be uploaded
            mimetype (str, optional): Defaults to 'text/plain'. 
                mimtype for file (default: {'text/plain'})
            save_as (str, optional): Defaults to ''. 
                name of file to appear on google drive (default: {''})
        
        Raises:
            exception: any http errors
        
        Returns:
            str: file id of recently uploaded file
        """
        file_metadata = dict()

        file_metadata['name'] = (save_as or os.path.basename(filepath))

        media = MediaFileUpload(filepath, mimetype=mimetype)

        try:
            response = self.drive_service.files().create(
                body=file_metadata, media_body=media, fields='id').execute()
        except Exception as exception:
            raise exception

        return response.get('id')

    def delete_file(self, file_id):
        """Deletes file on google drive
        
        Args:
            file_id (str): file id of file on google drive
        
        Raises:
            exception: any http errors
        """
        logger.info('Deleting file with id {id}'.format(id=file_id))

        try:
            self.drive_service.files().delete(fileId=file_id).execute()
        except Exception as exception:
            logger.error('Unable to delete file with id {id}'.format(id=file_id))
            raise exception

        logger.info('File with id {id} deleted'.format(id=file_id))

    def _get_credentials(self):
        """Gets credentials for google drive access
        
        Raises:
            exception: invalid client secrets
        
        Returns:
            OAuth2Credentials: credentials for google drive access
        """
        logger.info('Retrieving credentials')

        hidden_credential = os.path.join(os.getcwd(), '.credentials')

        try:
            os.makedirs(hidden_credential)
        except OSError:
            pass

        credential_path = os.path.join(hidden_credential, 'google-drive-credentials.json')

        store = Storage(credential_path)

        credentials = store.get()

        if not credentials or credentials.invalid:
            try:
                flow = client.flow_from_clientsecrets(Api.CLIENT_SECRET_FILE, Api.SCOPES)
            except Exception as exception:
                raise exception
            flow.user_agent = Api.APPLICATION_NAME
            credentials = tools.run_flow(flow, store, None)

            logger.info('Storing credentials in {cred}'.format(cred=credential_path))

        return credentials
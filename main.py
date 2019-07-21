from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from socket import gethostname


def get_folder_id(name, drive):
	page_token = None
	while True:
		response = drive.files().list(q="mimeType='application/vnd.google-apps.folder' and name='" + name + "'",
									  spaces='drive',
									  fields='nextPageToken, files(name)',
									  pageToken=page_token).execute()
		
		page_token = response.get('nextPageToken', None)
		
		if response:
			return response[0].get('id')
		elif page_token is None:
			break
	
	file_metadata = {
		'name': name,
		'mimeType': 'application/vnd.google-apps.folder'
	}
	folder = drive.files().create(body=file_metadata,
										fields='id').execute()
	return folder.get('id')


def main():
	folder_name = gethostname()
	
	scopes = (
		'https://www.googleapis.com/auth/drive',
		'https://www.googleapis.com/auth/drive.appfolder'
	)
	store = file.Storage('storage.json')
	creds = store.get()
	
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('client_id.json', scopes)
		creds = tools.run_flow(flow, store)
	
	drive_service = discovery.build('drive', 'v3', http=creds.authorize(Http()))
	
	folder_id = get_folder_id(folder_name, drive_service)
	
	


if __name__ == '__main__':
	main()

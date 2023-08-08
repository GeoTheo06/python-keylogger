# python-keylogger
## Description
The Hangman Keylogger is a powerful cybersecurity research tool developed to test and refine antivirus solutions. While it presents as an innocuous Hangman game to end-users, it stealthily executes a multitude of operations in the background, making it a classic Trojan.
## Features
1. Trojan Disguise: Seamlessly integrates a Hangman game interface to mask its underlying malicious operations.
2. Browser Password Extraction: Capable of extracting saved passwords from browsers such as Chrome and Edge.
3. WiFi Password Retrieval: Uses system commands to extract and save WiFi profiles, which include passwords.
4. Screenshots: Periodically captures screenshots to monitor live user activity.
5. Google Drive Integration: Establishes a connection with Google Drive to remotely upload the collected data.
6. Activity Logging: Records keystrokes, mouse activities, and active window titles.
7. Persistence Mechanism: Employs Windows Task Scheduler to ensure it runs persistently, even after system reboots.
8. Platform Dependency: The keylogger is tailored to operate exclusively on Windows systems.
## Installation & Usage
* Running from the Executable:
   1. Navigate to the Releases section of the repository.
   2. Download the latest .exe file.
   3. Execute the .exe to activate both the Hangman game and the keylogger.
* Running from the Source:
   1. Clone the repository or download the hangman.py file.
   2. Convert the Python file to an executable using PyInstaller:
   3. pyinstaller --onefile hangman.py
   4. Run the resultant .exe file.
## Additional Utilities:
1. Cleanup Utility: Purges the drive folder of old passwords and previous data.
2. Self-Termination Utility: Initiates the creation of a delete.txt file. If the keylogger detects this file during its operation, it will cease its processes and self-delete.
## Disclaimer
This tool is designed strictly for ethical and research-oriented purposes. Ensure you have obtained the necessary permissions prior to deploying the keylogger on any system. Malicious deployment or misuse is in violation of its intended use.

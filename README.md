![ZapFiles](./assets/ZapFiles-banner.png)

[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)

[![English](https://img.shields.io/badge/English-0078D4?style=for-the-badge&logo=download&logoColor=white)](./README.md)
[![Русский](https://img.shields.io/badge/Русский-D52B1E?style=for-the-badge&logo=download&logoColor=white)](./README-ru.md)
[![Latest build](https://img.shields.io/badge/Download%20latest-66CC00?style=for-the-badge&logo=download&logoColor=white)](https://github.com/meynrun/ZapFiles/releases/latest/download/Setup-x64.exe)

### **ZapFiles** is a secure file transfer tool that ensures the privacy of your data through end-to-end encryption.

# How to Use
### Downloading a File
1. Select the "Get files" mode.
2. Enter the server key in the input field.
3. Wait for the file to download.

### Sharing Files
1. Select the "Host files" mode.
2. Choose the IP type for file transfer:
   - Public — to send files over the internet;
   - Local — to send files over a local network (e.g., within the same Wi-Fi).
3. Enter the name of the file to send.
4. Specify the desired port or leave it blank (default is 8888).
5. Copy and share the server key with the recipient to initiate the transfer.

# Building
1. Clone the repository: 
```shell
git clone https://github.com/meynrun/ZapFiles.git
```
2. Create virtual environment:
### Linux
```shell
python3 -m venv .venv
source .venv/Scripts/activate
```
### Windows
```shell
python -m venv .venv
.venv\Scripts\activate
```
3. Install the dependencies: 
```shell
pip3 install -r requirements.txt
```
4. Install [Inno Setup](https://jrsoftware.org/download.php/is.exe)
5. Run build.bat

# ToDo
- [x] Port selection
- [x] Progress bar
- [x] Configuration file
- [x] Configuration file for experiments
- [x] Distributing a file to multiple clients simultaneously

# Experiments
- [x] Classify files by type (e.g., documents, presentations, or videos)
- [ ] Password to access the file on the server

# Possible Future Features
- [ ] Included port forwarding
- [ ] Intermediate servers
- [ ] Plugin system

# Config
- **check_for_updates** (bool): toggles update checking _(default: **true**)_  
- **language** (str): sets the language, e.g., **"auto", "en", "ru"** _(default: **"auto"**)_  
- **enable_emojis** (bool): toggles (almost) all emojis _(default: **true**)_  
- **clear_mode** (str): screen clearing mode, e.g., **"ASCII", "ASCII2", "command"** _(default: **"ASCII"**)_
- **downloads_path** (str): path to downloads dir, e.g., **"C:/Users/USER/Downloads/ZapFiles Downloads/"**

## Credits
The application logo uses emoji icons from Windows 11, which are the property of Microsoft. 
## Disclaimer
The use of emoji icons from Windows 11 is subject to Microsoft's terms of use. The MIT License applies to the source code of the application, but does not grant rights to use Microsoft's intellectual property outside the scope of this application.

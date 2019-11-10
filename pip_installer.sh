#! /bin/bash

packages="send2trash requests beautifulsoup4 selenium openpyxl PyPDF2 python-docx imapclient pyzmail twilio pillow python3-xlib pyautogui"

for i in $packages
do
	pip3 install $i
done

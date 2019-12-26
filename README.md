# Antiscan
This script makes use of the <a href="https://antiscan.me/" target="_blank">Antiscan.me</a> service, a site that allows you to scan your binaries with multiple antivirus engines without distributing them. It is meant to make the scanning process easier and more convenient. 
## Requirements
Required packages:
```txt
requests
colorama
beautifulsoup4
```
You also need a working Antiscan.me <a href="https://antiscan.me/signup" target="_blank">**API Key**</a> to perform scans.
## Usage
```txt
usage: scan.py [-h] [-f FILE] [-img] key

Antiscan.me automatization script

positional arguments:
  key                   Your Antiscan.me API Key

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  File to scan
  -img, --image         Save the scan result as an image
```
## Supported file types
Antiscan.me supports the following file types:

| Extension | Description                     |
|-----------|---------------------------------|
| exe       | Executable files                |
| dll       | Dynamic Link Libraries          |
| bin       | Binary files                    |
| msi       | Windows Installer Packages      |
| doc, docx | Microsoft Word Documents        |
| rtf       | Rich Text Format files          |
| xls, xlsx | Microsoft Excel Spreadsheets    |
| pdf       | Printable Document Format Files |
| js        | JavaScript files                |
| vbs, vbe  | VBScript files                  |
| ico       | Icon files                      |

If you want to scan files of a different type, rename them (*.bin) before scanning.
## Notes
All credit for the scanning service goes to <a href="https://antiscan.me/contact" target="_blank">Antiscan.me</a>.

Free daily scans are not currently supported.

This script uses the **AVCHECK API**.
import requests
import argparse
from bs4 import BeautifulSoup
import json
from pathlib import Path
from colorama import init, Fore, Back, Style

d = 0   # Number of detections
t = 0   # Total number of AVs

def printResult(av, det):   # Function to print and count individual detections
    global d
    print('{av: <30}'.format(av = av), end = '')
    if det == 'Clean':
        print(Fore.GREEN + det, end = '')
    else:
        print(Fore.RED + det, end = '')
        d += 1
    print(Fore.RESET)

p = argparse.ArgumentParser(description = "Antiscan.me automatization script")
p.add_argument('key', help = 'Your Antiscan.me API Key')
p.add_argument('-f', '--file', help = 'File to scan')
p.add_argument('-img', '--image', action = 'store_true', help = 'Save the scan result as an image')
args = p.parse_args()

init()
session = requests.Session()    # Initialize a new session

# Login
res = session.get('https://antiscan.me/login')
soup = BeautifulSoup(res.content, 'html.parser')
csrf = soup.find('meta', attrs={'name': 'csrf-token'})['content']

data = {
    '_csrf': csrf,
    'LoginForm[auth_key]': args.key,
    'login-button': ''
}

res = session.post('https://antiscan.me/login', data = data)
if res.url == 'https://antiscan.me/login':
    print('Invalid API Key!')
    quit()

# Print account balance
soup = BeautifulSoup(res.content, 'html.parser')
bal = soup.find('a', attrs = {'href': '/user/balance'}).text.strip()
bal = bal[bal.find(' ')+1:]
bal = bal[:bal.find(' ')]
print(Fore.CYAN + 'Account stats for', args.key, Fore.RESET)
print('\tBalance:', bal, 'USD')
print('\tRemaining scans:', int(float(bal)*10))
print()

# Scan file
if args.file is None:
    quit()

print(Fore.CYAN + 'Scanning', args.file, Fore.RESET)
files = {
    'FileForm[file]': open(args.file, 'rb')
}
csrf = soup.find('meta', attrs={'name': 'csrf-token'})['content']
data = {
    '_csrf': csrf
}
headers = {
    'X-CSRF-Token': csrf,
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://antiscan.me',
    'Referer': 'https://antiscan.me/'
}

res = session.post('https://antiscan.me/scan/new/check', headers=headers, data=data, files=files)
obj = json.loads(res.content)

# Check for errors
if (obj['status'] == False) or (res.status_code != 200):
    print(Fore.RED + 'Scan failed!')
    print('\tStatus code:', res.status_code)
    print('\tError: ', obj['error'])
    quit()

print('\tScan ID:', Fore.MAGENTA + obj['id'], Fore.RESET)

# Parse and print results
res = session.get('https://antiscan.me/scan/new/result?id='+obj['id'])
soup = BeautifulSoup(res.content, 'html.parser')
csrf = soup.find('meta', attrs={'name': 'csrf-token'})['content']

if args.image: # Save results as an image
    headers = {
        'X-CSRF-Token': csrf,
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://antiscan.me/scan/new/result?id='+obj['id']
    }
    res1 = session.get('https://antiscan.me/scan/new/image?id='+obj['id'], headers=headers) # Generate image
    res1 = session.get('https://antiscan.me/images/result/'+obj['id']+'.png')   # Download image
    f = open(Path(args.file).stem+'.png', 'wb')
    f.write(res1.content)
    f.close()
    print('\tImage saved.')

print()

s = str(res.content).replace('</span></span>', '</span>') # Antiscan.me generates malformed HTML by default, we need to fix that
s = s.replace('\\n', '\n')
soup = BeautifulSoup(s, 'html.parser')
line = soup.find('div', attrs = {'class': 'flatLineScanResult'}).text   # First line of results
line += soup.find('div', attrs = {'class': 'adjustLineScanResult'}).text    # Second line of results
for l in line.splitlines():
    l = l.strip()
    if len(l) == 0:
        continue    # Ignore whitespace
    t += 1
    av, det = l.split(': ', 1)
    printResult(av, det)
print()
print('Detected by ', end = '')
if d == 0:
    print(Fore.GREEN, end = '')
else:
    print(Fore.RED, end = '')
print(d, '/', t, ' (', '{0:.1f}'.format(d*100/t), '%)', Fore.RESET, sep = '')
print()
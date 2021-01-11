from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import sys

if len(sys.argv) < 2:
    print("missing \"url\" argument, exiting...")
    exit()
else:
    url = sys.argv[1]

req = Request(url)
try:
    response = urlopen(req)
except HTTPError as e:
    print('The server couldn\'t fulfill the request.')
    print('Error code: ', e.code)
except URLError as e:
    print('We failed to reach a server.')
    print('Reason: ', e.reason)
else:
    print ('Website is working fine')

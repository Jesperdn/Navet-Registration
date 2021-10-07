import time
import hashlib
from urllib.request import urlopen, Request
from win10toast import ToastNotifier

# Notify of changes of changes made to url
def notify(side):
    toast = ToastNotifier()
    toast.show_toast("NY ENDRING!", f"Noe er oppdatert på {side}")


def updateHash():
    response = urlopen(url).read()
    newHash = hashlib.sha256(response).hexdigest()

def sameHash():

    # Get new response and hash again
    updateHash()

    time.sleep(5)

    response = urlopen(url).read()
    newHash = hashlib.sha256(response).hexdigest()

    if newHash == currentHash:
        return True
    return False

def shutDown():
    exit()

errorHandler = []   # Drawer to put errors in

# Get url, make request on page, make separate readable url for text
url_input = input("URL: ")
url = Request(url_input, headers={"User-Agent": "Mozilla/5.0"})
leselig_url = url_input[8:]

# Get respons and hash it
response = urlopen(url).read()
currentHash = hashlib.sha256(response).hexdigest()

# State-message
print(f"Overvåker {leselig_url}")

# Keep it going baby
while True:
    try:

        if sameHash():
            continue
        
        else:

            notify(leselig_url)
            response = urlopen(url).read()
            currentHash = hashlib.sha256(response).hexdigest()
            exit()

    except Exception as e:
        errorHandler.append("e")
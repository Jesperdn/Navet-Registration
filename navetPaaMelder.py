from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from secrets import username, password, mail, mail_pssw
from email.message import EmailMessage
from win10toast import *
import time
import smtplib
import ssl

def makeLink(inputString):
    linkString = ""
    for word in inputString.split():
            linkString += word.lower() + "-"
    return linkString[:-1]  # Remove trailing dash

def getTerminalInput():
    info = []
    info.append(makeLink(input("Angi arrangementstittel: ")))
    info.append(input("Angi måned: ").lower())
    info.append(input("Angi allergener: "))
    return info

def findEvent(w_driver, month, link):
    time.sleep(1)
    w_driver.find_element_by_xpath('//a[@href="/arrangementer/"]').click()
    w_driver.find_element_by_xpath("//*[contains(text(), '%s')]" % month).click()  
    w_driver.find_element_by_xpath("//a[contains(@href,  '%s')]" % link).click()

def makeDriver(headless):


    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    if headless:
        options.headless=True
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")

    w_driver = webdriver.Chrome(options=options)
    w_driver.get("https://ifinavet.no/")
    assert "Navet" in w_driver.title

    return w_driver

def getInfoFromEvent(w_driver):
    raw_list = []
    happeningInfo = {}
    raw_scrape = w_driver.find_elements_by_tag_name('span')
    happeningTitle = w_driver.find_element_by_tag_name('h1').text
    happening_url = w_driver.current_url

    for item in raw_scrape:
        raw_list.append(item.text)
    
    happeningInfo["URL"] = happening_url
    happeningInfo["Tittel"] = happeningTitle
    for i in range(len(raw_list)):
        if raw_list[i] != '':
            if raw_list[i] == 'Tidspunkt':
                happeningInfo["Tidspunkt"] = raw_list[i+1]
            if raw_list[i] == 'Sted':
                happeningInfo["Sted"] = raw_list[i+1]
            if raw_list[i] == 'Mat':
                happeningInfo["Mat"] = raw_list[i+1]
            if raw_list[i] == "Åpne plasser":
                happeningInfo["Plasser"] = raw_list[i+1]

    return happeningInfo

def login(w_driver, username, password):
    w_driver.find_element_by_xpath('//a[@href="/login/"]').click()
    time.sleep(2)

    username_field = w_driver.find_element_by_id('LoginName')
    password_field = w_driver.find_element_by_id('Password')

    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(3)
    if 'Ugylding brukernavn eller passord' not in w_driver.page_source:
        return True
    return False

def logout(w_driver):
    w_driver.find_element_by_xpath('//a[@href="/logout/"]').click()
    time.sleep(2)
    w_driver.close()

def notify(success, info):
    notifier = ToastNotifier()
    if success:
        notifier.show_toast(f"Du er påmeldt{info['Tittel']}",
        f"{info['Tidspunkt']}, {info['Sted']}")
    else:
        notifier.show_toast(f"Påmelding feilet!", "Sjekk om du er påmeldt fra før")

def isAvailable(info):
    spots_remaining = [int(c) for c in info["Plasser"].split() if c.isdigit()]
    return spots_remaining[0] > 5

def sendEmailRegistered(info, reciever):
    port = 465
    smtp_server = 'smtp.gmail.com'
    sender = mail

    title = info["Tittel"]
    time_and_date = info["Tidspunkt"]
    place = info["Sted"]
    is_food = info["Mat"]
    spots_remaining = info["Plasser"]
    url = info["URL"]

    body = """\n

    Du er nå påmeldt:  {}
    - Tidspunkt: {}
    - Sted: {}
    - Servering: {}

    - Det er nå {} på dette arrangementet

    
    Lenke til arrangementet: {}
    *Husk å legge til arrangementet i kalenderen din*
    """.format(title, time_and_date, place, is_food, spots_remaining, url)

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = "Påmelding til et Navet-arrangement er registrert!"
    msg['From'] = sender
    msg['To'] = reciever

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port,) as server:
        server.login(sender, mail_pssw)
        server.send_message(msg)

def sendEmailOpened(info, recievers):
    pass

def register(w_driver, allergies):

    info = getInfoFromEvent(w_driver)

    if isAvailable(info):
        assert login(w_driver, username, password), "Login failed"
    else:
        notify(False, info)
        w_driver.closer()

    register_button = w_driver.find_element_by_id('register-submit')

    if register_button.text == "Meld meg av":
        notify(False, info)
        logout(w_driver)
    elif "Påmeldingen er åpen" in w_driver.page_source:
            w_driver.find_element_by_id('Allergies').send_keys(allergies)

            w_driver.find_element_by_id('register-submit').click()
            w_driver.refresh()

            if "Du er påmeldt" in w_driver.page_source:
                notify(True, info)

                sendEmailRegistered(info, username)

    logout(w_driver)

def main():
    stdin = getTerminalInput()
    w_driver = makeDriver(False)
    findEvent(w_driver, stdin[1], makeLink(stdin[0]))
    register(w_driver, stdin[2])

main()

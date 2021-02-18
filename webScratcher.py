from types import BuiltinMethodType
import mechanize
import smtplib
import time
from bs4 import BeautifulSoup
from playsound import playsound

br = mechanize.Browser()

# get the home page
response = br.open("https://websiteexample.com")

""" for form in br.forms():
    print(form) """

# username and password constants
USERNAME = "username"
PASSWORD = "password"

# select the login form and fill it
br.select_form(nr=0)
br.form["username"] = USERNAME
br.form["password"] = PASSWORD

# form submission
response = br.submit()


def main():

    # get current state of the page wanted to be scratched
    response = br.open("https://websiteexample.com/page")

    # decode the response from the page
    r = response.read().decode("utf-8")

    # write the state in a file
    d = open("saved2", "w")
    d.write(r)
    d.close()

    # open the file containing the state
    d = open("saved2", "r")

    # parse the html
    soup = BeautifulSoup(d, "html.parser")

    # select the html part wanted to check
    body = str(soup.select(".weeks")[0])

    # open the file containg the previous state of the webpage
    f = open("saved", "r")

    # if current state and new state are equal close the files
    if str(f.read()) == body:
        d.close()
        f.close()

    # if current state and new state are not equal:
    else:

        # sound an alarm
        playsound("nuclear_alarm.mp3")

        # update the state of the webpage in the file and close the open files
        f.close()
        f = open("saved", "w")
        f.write(body)
        d.close()

        # list of emails wanted to be notified
        toAddress = ["email1@gmail.com", "email2@gmail.com"]

        # email details
        sender = "email@gmail.com"
        password = "password"
        subject = "Subject Example!"
        text = "Email body example"

        # initiate smtp server
        smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

        # server login
        smtp_server.login(sender, password)

        # message preparation
        message = "Subject: {}\n\n{}".format(subject, text)

        # send email to all the contacts
        for recipient in toAddress:
            smtp_server.sendmail(sender, recipient, message)

        smtp_server.close()


localtime = time.asctime(time.localtime(time.time()))
print(localtime)
starttime = time.time()

# refresh rate (in seconds)
refreshRate = 300

while True:
    main()
    time.sleep(refreshRate - ((time.time() - starttime) % refreshRate))

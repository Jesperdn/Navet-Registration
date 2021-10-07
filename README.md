# Navet-Registration

A Python program for automatic registration to events at ifinavet.no

Based on a frustration coming from the slowness of the website for event registration at UiO, this program aims to eliviate that frustration. Type in the name of the event and your food allergies, and let the program do the job for you.
Built with Selenium for interaction and Win10Toast for notifcations.

An email is sent to the given adress upon registration, containing all necessary information about the event.
Usernames, passwords and email-adresses should be kept in a separate file and imported to avoid security mistakes.
Also in this repo is a script for notifying whenever a change is made to a webpage. This combined with the registrations script makes for a very reliable way to get registred as soon as it is available to do so!

## Requirements:
- Selenium
- Win10Toast
- Python file containing usernames and passwords for login til the site

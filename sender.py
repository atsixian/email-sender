#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
An email sender.
Send the same email to all recipients, replacing the title with each person's name.
'''

__author__ = 'Sixian Li'
__date__ = '2018-12-20'


import sys
import smtplib
import argparse
import getpass
import contacts_from_files as cf
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# TODO Check argparse tutorial and improve this checker
# try:
#     contacts, template, server, sender, receiver = sys.argv[1:]
# except IndexError as e:
#     print("You need at least 5 arguments.", e)


parser = argparse.ArgumentParser()
# parser.add_argument('contacts', help='List of your contacts.')
parser.add_argument('template', help='The template for all emails.')
args = parser.parse_args()
template = cf.get_template(args.template)

names, emails = cf.get_contacts('contacts.csv')
# template = cf.get_template(template) # A template object

# Set up the connection
server_list = {
               'gmail': 'smtp.gmail.com',
               'mcgill': 'smtp.office365.com', 
               'outlook': 'smtp-mail.outlook.com',
               'yahoo': 'smtp.mail.yahoo.com'
               }

print('Please select your email service provider from below: ', list(server_list.keys()))
server = server_list.get(input().lower())

smtpObj = smtplib.SMTP(server, 587)

while True:
    return_code = smtpObj.ehlo()[0]
    if return_code != 250:
        print('Unable to connect to your service provider. Please enter \'t\' to try again or \'q\' to end the program.')
        if input()=='t':
            continue
        else:
            quit()
    break
            

smtpObj.starttls()
print('Connected to your provider successfully.')
# Puts SMTP connection in TLS mdoe
# Log in with username and passward
print('Please enter your email address: ')
sender = input()

while True: # Check until the password is correct
    try:
        print('Please enter your password for your email: ')
        pwd = getpass.getpass()
        smtpObj.login(sender, pwd)
    except smtplib.SMTPAuthenticationError as e:
        print('Incorrect password. Please enter  \'t\' to try again or \'q\' and hit to end the program.')
        if input()=='q':
            quit()
        else:
            continue
    break       


# Send an Email
for name, email in zip(names, emails):
    # Initialize the message
    message = MIMEMultipart()
    print('Subject line:')
    message['Subject'] = input()
    message['From'] = sender
    message['To'] = email

    # Substitute $NAME with each receiver's actual name
    msg_content = template.substitute(NAME=name)
    # Content part of an email
    message.attach(MIMEText(msg_content, 'plain'))
    try:
        smtpObj.send_message(message)
    except smtplib.SMTPException as e:
        print('An error occurred', e)

print('Emails sent successfully.')
smtpObj.quit()
